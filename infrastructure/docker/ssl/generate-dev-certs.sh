#!/usr/bin/env sh
# Generate a self-signed TLS certificate for LOCAL / STAGING use only.
# For production, supply real certificates (e.g. Let's Encrypt) instead.
set -e

DIR="$(cd "$(dirname "$0")" && pwd)"
CN="${1:-localhost}"

openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout "$DIR/key.pem" \
  -out "$DIR/cert.pem" \
  -subj "/CN=$CN"

echo "Generated self-signed cert.pem and key.pem in $DIR (CN=$CN)."
echo "WARNING: self-signed certificates are for local/staging testing only."
