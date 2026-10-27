#!/usr/bin/env bash
# Pasang https://logikaduit.com di VPS (nginx + SSL Let's Encrypt). Aman dijalankan ulang.
# Jalankan sebagai root:
#   git clone -b <cabang> https://github.com/fourtisf/logikaduit.git /opt/logikaduit
#   bash /opt/logikaduit/deploy/setup-vps.sh
# Situs lain di server (misalnya ruangpikir.id) tidak disentuh. Kalau tes nginx gagal,
# konfigurasi logikaduit.com dikembalikan seperti semula dan nginx tidak di-reload.
set -euo pipefail

DOMAIN=logikaduit.com
SRC=/opt/logikaduit
WEB=/var/www/$DOMAIN
CERT=/etc/letsencrypt/live/$DOMAIN
MARK="# Dibuat oleh deploy/setup-vps.sh (repo logikaduit). Jalankan ulang skrip itu untuk menulis ulang."

say() { printf '\n== %s\n' "$*"; }
die() { printf '\nBERHENTI: %s\n' "$*" >&2; exit 1; }

# Pasang konfigurasi nginx dari stdin; kalau "nginx -t" gagal, kembalikan yang lama.
apply_conf() {
  local tmp backup=""; tmp=$(mktemp)
  cat > "$tmp"
  if [ -f "$CONF" ]; then backup=$(mktemp); cp "$CONF" "$backup"
    grep -qF "$MARK" "$CONF" || cp "$CONF" "$CONF.bak-$(date +%Y%m%d%H%M%S)"; fi
  install -m 644 "$tmp" "$CONF"; rm -f "$tmp"
  [ -z "$LINK" ] || ln -sfn "$CONF" "$LINK"
  if ! nginx -t 2>&1; then
    if [ -n "$backup" ]; then cp "$backup" "$CONF"; else rm -f "$CONF"; [ -z "$LINK" ] || rm -f "$LINK"; fi
    die "tes konfigurasi nginx gagal, konfigurasi logikaduit.com dikembalikan. Situs lain aman. Kirim screenshot ke Claude."
  fi
  [ -z "$backup" ] || rm -f "$backup"
  systemctl reload nginx
}

main() {   # seluruh skrip dibaca dulu sebelum jalan, jadi aman walau repo ter-update di tengah jalan
[ "$(id -u)" = 0 ] || die "jalankan sebagai root."
[ -d "$SRC/.git" ] || die "repo belum ada di $SRC. Jalankan dulu perintah git clone di atas."

say "Cek web server"
if ! command -v nginx >/dev/null || ! systemctl is-active --quiet nginx; then
  ss -ltnp | grep -E ':(80|443)\s' || true
  die "nginx tidak aktif di server ini. Belum ada yang diubah. Kirim screenshot layar ini ke Claude."
fi
if ss -ltnp | grep -E ':(80|443)\s' | grep -vq nginx; then
  ss -ltnp | grep -E ':(80|443)\s'
  die "port 80/443 dipakai program selain nginx. Belum ada yang diubah. Kirim screenshot layar ini ke Claude."
fi
echo "nginx aktif: $(nginx -v 2>&1)"
nginx -t 2>/dev/null || { nginx -t || true; die "konfigurasi nginx yang sudah ada sedang bermasalah (bukan dari logikaduit). Belum ada yang diubah. Kirim screenshot ke Claude."; }

if [ -d /etc/nginx/sites-available ]; then CONF=/etc/nginx/sites-available/$DOMAIN; LINK=/etc/nginx/sites-enabled/$DOMAIN
else CONF=/etc/nginx/conf.d/$DOMAIN.conf; LINK=""; fi
others=$(grep -RlE "server_name[^;]*[[:space:]](www\.)?${DOMAIN}[[:space:];]" /etc/nginx/sites-enabled /etc/nginx/conf.d 2>/dev/null \
  | while read -r f; do [ "$(readlink -f "$f")" = "$(readlink -f "$CONF")" ] || echo "$f"; done || true)
[ -z "$others" ] || die "logikaduit.com sudah dipakai di konfigurasi nginx lain: $others. Belum ada yang diubah. Kirim screenshot ke Claude."

say "Pasang perintah logikaduit-deploy dan salin file website"
branch=$(git -C "$SRC" symbolic-ref --quiet --short HEAD || true)
if [ -n "$branch" ]; then echo "$branch" > /etc/logikaduit-branch
elif [ ! -s /etc/logikaduit-branch ]; then echo main > /etc/logikaduit-branch; fi
echo "Cabang yang di-deploy: $(cat /etc/logikaduit-branch)"
install -m 755 "$SRC/deploy/logikaduit-deploy" /usr/local/bin/logikaduit-deploy
mkdir -p "$(dirname "$WEB")"
LD_NO_CHECK=1 logikaduit-deploy

if [ ! -f "$CERT/fullchain.pem" ]; then
  say "Siapkan http sementara untuk verifikasi SSL"
  apply_conf <<EOF
$MARK
# Sementara, sebelum sertifikat SSL ada.
server {
    listen 80;
    server_name $DOMAIN www.$DOMAIN;
    root $WEB;
    index index.html;
}
EOF
  say "Minta sertifikat SSL Let's Encrypt"
  if ! command -v certbot >/dev/null; then apt-get update -qq; apt-get install -y -qq certbot; fi
  certbot certonly --webroot -w "$WEB" --cert-name "$DOMAIN" -d "$DOMAIN" -d "www.$DOMAIN" \
    --non-interactive --agree-tos --register-unsafely-without-email --keep-until-expiring \
    --deploy-hook "systemctl reload nginx" \
    || die "sertifikat SSL gagal dibuat. Situs sudah bisa dibuka lewat http://$DOMAIN. Kirim screenshot ke Claude."
fi

say "Pasang konfigurasi akhir: https, www dan http diarahkan ke https://$DOMAIN"
SSL="ssl_certificate $CERT/fullchain.pem;
    ssl_certificate_key $CERT/privkey.pem;"
[ ! -f /etc/letsencrypt/options-ssl-nginx.conf ] || SSL="$SSL
    include /etc/letsencrypt/options-ssl-nginx.conf;"
[ ! -f /etc/letsencrypt/ssl-dhparams.pem ] || SSL="$SSL
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;"
apply_conf <<EOF
$MARK
server {
    listen 80;
    server_name $DOMAIN www.$DOMAIN;
    location /.well-known/acme-challenge/ { root $WEB; }
    location / { return 301 https://$DOMAIN\$request_uri; }
}

server {
    listen 443 ssl;
    server_name www.$DOMAIN;
    $SSL
    return 301 https://$DOMAIN\$request_uri;
}

server {
    listen 443 ssl;
    server_name $DOMAIN;
    $SSL
    root $WEB;
    index index.html;

    gzip on;
    gzip_types text/css application/javascript image/svg+xml;

    location / { try_files \$uri \$uri/ =404; expires 10m; }
    location ~* \.(png|svg|ico)$ { expires 30d; }
}
EOF

say "Cek hasil"
LD_NO_CHECK=0 logikaduit-deploy
echo
echo "Selesai. Untuk update berikutnya cukup jalankan: logikaduit-deploy"
}

main "$@"
