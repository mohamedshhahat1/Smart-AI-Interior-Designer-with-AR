# Nginx TLS certificates

The production reverse proxy (`docker-compose.prod.yml` -> `nginx`) mounts this
directory at `/etc/nginx/ssl` (read-only). `nginx.conf` expects:

- `cert.pem` — the TLS certificate (full chain)
- `key.pem` — the matching private key

These files are intentionally **not** committed (see `.gitignore`). Nginx will
fail to start until they exist, so create them before deploying.

## Production

Use a real certificate, for example from Let's Encrypt:

```sh
# After obtaining certs with certbot:
cp /etc/letsencrypt/live/yourdomain.com/fullchain.pem cert.pem
cp /etc/letsencrypt/live/yourdomain.com/privkey.pem   key.pem
```

## Local / staging (self-signed)

For non-production testing only:

```sh
./generate-dev-certs.sh
```

Browsers will warn about the self-signed certificate; that is expected for local
testing and must not be used in production.
