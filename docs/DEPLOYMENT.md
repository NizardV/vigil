# Vigil — Deployment Guide

This guide covers deploying Vigil on any Linux VPS from scratch. Vigil runs entirely as a self-contained Docker Compose stack; the only host-level dependencies are Nginx (for SSL termination and routing) and Certbot (for Let's Encrypt certificates).

---

## Table of Contents

1. [VPS Prerequisites](#1-vps-prerequisites)
2. [DNS Configuration](#2-dns-configuration)
3. [Clone the Repository and Configure .env](#3-clone-the-repository-and-configure-env)
4. [Docker Compose](#4-docker-compose)
5. [Host Nginx Configuration](#5-host-nginx-configuration)
6. [SSL Certificate with Certbot](#6-ssl-certificate-with-certbot)
7. [Discord Bot Setup](#7-discord-bot-setup)
8. [Verifying the Deployment](#8-verifying-the-deployment)
9. [Troubleshooting](#9-troubleshooting)

---

## 1. VPS Prerequisites

| Requirement      | Minimum          | Notes                                       |
|------------------|------------------|---------------------------------------------|
| OS               | Ubuntu 22.04 LTS | Tested on 22.04; 24.04 should also work     |
| RAM              | 2 GB             | 4 GB recommended for running multiple stacks|
| Disk             | 10 GB free       | For PostgreSQL data and Docker images       |
| Docker Engine    | ≥ 24             | Compose v2 plugin required                  |
| Nginx (host)     | ≥ 1.18           | Installed directly on the VPS, not Docker   |
| Certbot          | any              | `python3-certbot-nginx` package             |
| Open ports       | 22, 80, 443      | 8000 and 8501 stay internal (not exposed)   |

Install Nginx and Certbot on the host if not already present:

```bash
sudo apt update
sudo apt install -y nginx certbot python3-certbot-nginx
```

---

## 2. DNS Configuration

Create an A record pointing `vigil.yourdomain.com` to the VPS IP address:

```
vigil.yourdomain.com.  IN  A  <VPS_IP>
```

Verify propagation before requesting the SSL certificate:

```bash
dig +short vigil.yourdomain.com
# Should return the VPS IP
```

---

## 3. Clone the Repository and Configure .env

```bash
# Choose an appropriate directory — /opt is used here
cd /opt
sudo git clone https://github.com/NizardV/vigil.git
sudo chown -R $USER:$USER /opt/vigil
cd /opt/vigil

# Copy the example env file
cp .env.example .env
```

Edit `.env` and fill in every required value:

```dotenv
# ── PostgreSQL ────────────────────────────────────────────────────────────────
POSTGRES_DB=vigil
POSTGRES_USER=vigil_user
POSTGRES_PASSWORD=<strong-random-password>
DATABASE_URL=postgresql://vigil_user:<strong-random-password>@postgres:5432/vigil

# ── Redis / Celery ────────────────────────────────────────────────────────────
REDIS_URL=redis://redis:6379/0
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/1

# ── Google Gemini ─────────────────────────────────────────────────────────────
GEMINI_API_KEY=<your-gemini-api-key>
GEMINI_MODEL=gemini-2.5-flash

# ── FastAPI ───────────────────────────────────────────────────────────────────
SECRET_KEY=<output-of-openssl-rand-hex-32>
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=false

# ── Discord ───────────────────────────────────────────────────────────────────
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/...
DISCORD_PUBLIC_KEY=<discord-app-public-key>
DISCORD_BOT_TOKEN=<discord-bot-token>

# ── Streamlit internal URL ────────────────────────────────────────────────────
API_URL=http://backend:8000/api

# ── Digest schedule (UTC) ─────────────────────────────────────────────────────
DIGEST_HOUR=7
DIGEST_MINUTE=0
```

Generate a strong `SECRET_KEY`:

```bash
openssl rand -hex 32
```

---

## 4. Docker Compose

Start all Vigil services:

```bash
cd /opt/vigil
docker compose up -d
```

Verify all containers are running:

```bash
docker compose ps
```

Expected output:

```
NAME                SERVICE         STATUS
vigil_postgres      postgres        running (healthy)
vigil_redis         redis           running (healthy)
vigil_backend       backend         running
vigil_celery        celery_worker   running
vigil_beat          celery_beat     running
vigil_streamlit     streamlit       running
vigil_n8n           n8n             running
vigil_nginx         nginx           running
```

> The compose file includes an internal `vigil_nginx` service (ports 8080/8443) used for local development. In production, **the host Nginx on 80/443 proxies directly to port 8000 (FastAPI) and 8501 (Streamlit)**, so `vigil_nginx` is not in the public traffic path. You can leave it running or add `--scale nginx=0` to the `up` command to skip it.

The backend creates the `pgvector` extension and all database tables automatically on first startup. Check the logs:

```bash
docker compose logs backend --tail=50
```

---

## 5. Host Nginx Configuration

Vigil's FastAPI backend (port 8000) and Streamlit dashboard (port 8501) are exposed exclusively through host Nginx. They are **not** published directly on the host network.

Create `/etc/nginx/sites-available/vigil` with the following configuration:

```nginx
# ── vigil.yourdomain.com — HTTP → HTTPS redirect ────────────────────────────
server {
    listen 80;
    server_name vigil.yourdomain.com;
    return 301 https://$host$request_uri;
}

# ── vigil.yourdomain.com — HTTPS ─────────────────────────────────────────────
server {
    listen 443 ssl;
    server_name vigil.yourdomain.com;

    ssl_certificate     /etc/letsencrypt/live/vigil.yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/vigil.yourdomain.com/privkey.pem;

    ssl_protocols       TLSv1.2 TLSv1.3;
    ssl_ciphers         HIGH:!aNULL:!MD5;

    # FastAPI REST API + Discord interactions endpoint
    location /api/ {
        proxy_pass         http://127.0.0.1:8000/api/;
        proxy_http_version 1.1;
        proxy_set_header   Host              $host;
        proxy_set_header   X-Forwarded-For   $proxy_add_x_forwarded_for;
        proxy_set_header   X-Forwarded-Proto $scheme;
        # Required for Discord signature verification (raw body must be preserved)
        proxy_request_buffering off;
    }

    # FastAPI docs (Swagger / ReDoc)
    location ~ ^/(docs|redoc|openapi\.json)$ {
        proxy_pass         http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header   Host              $host;
        proxy_set_header   X-Forwarded-For   $proxy_add_x_forwarded_for;
        proxy_set_header   X-Forwarded-Proto $scheme;
    }

    # Streamlit dashboard (root)
    location / {
        proxy_pass         http://127.0.0.1:8501;
        proxy_http_version 1.1;
        proxy_set_header   Upgrade    $http_upgrade;
        proxy_set_header   Connection "upgrade";
        proxy_set_header   Host       $host;
        proxy_read_timeout 86400;
    }
}
```

> **Note on `proxy_request_buffering off`:** Discord sends a raw body that must reach FastAPI intact for Ed25519 signature verification to succeed. Without this directive, Nginx may buffer and alter the byte stream, causing verification failures.

Enable the configuration and reload Nginx:

```bash
sudo ln -s /etc/nginx/sites-available/vigil /etc/nginx/sites-enabled/vigil
sudo nginx -t          # Test config syntax
sudo nginx -s reload   # Reload without downtime
```

---

## 6. SSL Certificate with Certbot

Stop Nginx briefly (Certbot needs port 80 for the standalone challenge) or use the Nginx plugin:

```bash
# Using the Nginx plugin (no downtime)
sudo certbot --nginx -d vigil.yourdomain.com \
  --email votre@email.com \
  --agree-tos \
  --non-interactive
```

Certbot writes the certificate to `/etc/letsencrypt/live/vigil.yourdomain.com/` and can automatically update the Nginx config. If you prefer to keep full control of the Nginx config, use `certonly`:

```bash
sudo certbot certonly --nginx -d vigil.yourdomain.com \
  --email votre@email.com \
  --agree-tos \
  --non-interactive
```

Then reload Nginx manually after certificate generation:

```bash
sudo nginx -s reload
```

### Automatic renewal

Certbot installs a systemd timer by default. Verify it:

```bash
sudo systemctl status certbot.timer
sudo certbot renew --dry-run
```

Add a post-renewal hook to reload Nginx automatically:

```bash
sudo tee /etc/letsencrypt/renewal-hooks/post/reload-nginx.sh > /dev/null <<'EOF'
#!/bin/bash
nginx -s reload
EOF
sudo chmod +x /etc/letsencrypt/renewal-hooks/post/reload-nginx.sh
```

---

## 7. Discord Bot Setup

### Step 1 — Create the application

1. Go to [https://discord.com/developers/applications](https://discord.com/developers/applications) → **New Application**.
2. Name it `Vigil` (or any name visible to your team).

### Step 2 — Create the bot

1. Navigate to **Bot** → **Add Bot**.
2. Under **Token**, click **Reset Token** and copy it → set `DISCORD_BOT_TOKEN` in `.env`.
3. Disable **Public Bot** to prevent unauthorized servers from adding it.

### Step 3 — Get the public key

1. Navigate to **General Information**.
2. Copy **Application ID** (for reference) and **Public Key** → set `DISCORD_PUBLIC_KEY` in `.env`.

### Step 4 — Register the interactions endpoint

1. Still in **General Information**, set **Interactions Endpoint URL** to:
   ```
   https://vigil.yourdomain.com/api/discord/interactions
   ```
2. Click **Save Changes**. Discord sends a PING to verify the endpoint. The backend must be running and reachable. If the verification fails, check:
   - Nginx is reloaded with the new config
   - `docker compose ps` shows the backend as `running`
   - `DISCORD_PUBLIC_KEY` in `.env` matches exactly what the portal shows

### Step 5 — Invite the bot to your server

Generate an invite URL in **OAuth2 → URL Generator**:
- Scopes: `bot`, `applications.commands`
- Bot permissions: `Send Messages`, `Embed Links` (minimum)

Open the generated URL and add the bot to your Discord server.

### Step 6 — Create a webhook for digest delivery

In each Discord channel that should receive digests:

1. **Channel Settings → Integrations → Webhooks → New Webhook**
2. Copy the webhook URL.
3. In the Vigil dashboard (**Webhooks** page), add it and associate it with a theme.

---

## 8. Verifying the Deployment

```bash
# Health check
curl https://vigil.yourdomain.com/health
# Expected: {"status":"ok"}

# List themes (should return empty array on first deploy)
curl https://vigil.yourdomain.com/api/themes
# Expected: []

# Check the Streamlit dashboard
curl -I https://vigil.yourdomain.com
# Expected: HTTP/2 200

# Confirm Discord endpoint is reachable (Discord will PING it)
curl -X POST https://vigil.yourdomain.com/api/discord/interactions \
  -H "Content-Type: application/json" \
  -d '{"type":1}'
# Expected: 401 Unauthorized (missing valid signature — endpoint is reachable)
```

Check all container logs for errors:

```bash
cd /opt/vigil
docker compose logs backend --tail=100
docker compose logs celery_worker --tail=100
docker compose logs celery_beat --tail=100
```

Trigger a manual digest for a theme to validate the end-to-end flow:

```bash
# Replace {theme_id} with an actual theme ID
curl -X POST https://vigil.yourdomain.com/api/digests/trigger/{theme_id}
```

---

## 9. Troubleshooting

### Backend container exits immediately

```bash
docker compose logs backend
```

Common causes:
- `DATABASE_URL` is wrong or the `postgres` container is not healthy yet. The backend retries, but if it exits check the URL format.
- Missing environment variable. All required variables must be set in `.env`.

### Discord interactions return 401

- Confirm `DISCORD_PUBLIC_KEY` in `.env` matches the **Public Key** in the Discord Developer Portal exactly.
- Confirm the interactions endpoint URL saved in the portal ends with `/api/discord/interactions` (no trailing slash).
- Confirm `proxy_request_buffering off` is set in the Nginx location block — without it, Nginx may alter the raw body and break the Ed25519 signature.

### Streamlit shows "Cannot connect to backend"

- Check `API_URL=http://backend:8000/api` in `.env` (internal Docker network, not the public URL).
- Verify the `backend` container is running: `docker compose ps`.

### Celery tasks are not executing

```bash
docker compose logs celery_worker
docker compose logs celery_beat
```

- Beat and worker both need `CELERY_BROKER_URL` pointing to Redis.
- Verify Redis is running: `docker compose ps redis`.

### SSL certificate not renewed automatically

```bash
sudo certbot renew --dry-run
sudo systemctl status certbot.timer
```

If the timer is inactive, enable it:

```bash
sudo systemctl enable --now certbot.timer
```

### Nginx reload after Certbot renewal does not apply

Ensure the post-renewal hook exists and is executable:

```bash
ls -la /etc/letsencrypt/renewal-hooks/post/
sudo nginx -t && sudo nginx -s reload
```
