# Vigil

Automated tech watch platform: collects RSS feeds, scores articles with Gemini LLM, sends daily digests to Discord with an interactive feedback loop, and exposes a Streamlit dashboard for configuration.

---

## Architecture

```
                        ┌────────────────────────────────────────────────────────┐
  INTERNET              │  VPS                                                   │
                        │                                                        │
  vigil.yourdomain.com  │  ┌──────────────────────────────────────────────────┐ │
  ─────────────────────►│  │  Host Nginx  (/etc/nginx/sites-available/vigil)  │ │
                        │  │                                                  │ │
                        │  │  /api/*  →  FastAPI  :8000                      │ │
                        │  │  /*      →  Streamlit :8501                     │ │
                        │  └──────────────────┬─────────────────┬────────────┘ │
                        │                     │                 │              │
                        │         ┌───────────▼───────┐  ┌──────▼────────────┐ │
                        │         │  Streamlit :8501  │  │  FastAPI  :8000   │ │
                        │         │  Dashboard UI     │  │  REST API         │ │
                        │         └───────────────────┘  │  Discord handler  │ │
                        │                                 └──────┬────────────┘ │
                        │                      ┌────────────────┼──────────┐   │
                        │                      │                │          │   │
                        │            ┌─────────▼──────┐  ┌──────▼───┐  ┌──▼──┐ │
                        │            │  PostgreSQL    │  │  Redis   │  │Celery│ │
                        │            │  + pgvector   │  │  :6379   │  │Worker│ │
                        │            │  :5433        │  └──────────┘  └─────┘ │
                        │            └───────────────┘                         │
                        └────────────────────────────────────────────────────────┘

  Google Gemini  ◄──►  LLM scoring + digest generation (gemini-2.5-flash)
  Discord        ◄──►  Webhook notifications + interactive buttons (👍 / 👎)
  RSS Feeds      ──►   Celery fetch tasks (configurable interval per source)
```

### Services and ports

| Service       | Container          | Host port        | Description                                |
|---------------|--------------------|------------------|--------------------------------------------|
| FastAPI       | `vigil_backend`    | 8000             | REST API + Discord interactions            |
| Streamlit     | `vigil_streamlit`  | 8501             | Configuration dashboard                    |
| PostgreSQL    | `vigil_postgres`   | 127.0.0.1:5433   | Main database + pgvector (localhost only)  |
| Redis         | `vigil_redis`      | —                | Celery broker / result backend             |
| Celery Worker | `vigil_celery`     | —                | Article fetching and LLM analysis          |
| Celery Beat   | `vigil_beat`       | —                | Hourly scheduler                           |
| n8n           | `vigil_n8n`        | 5678             | Workflow automation (optional)             |

---

## Features

- **Multi-theme tech watch** — define independent themes, each with its own RSS sources, keywords, digest schedule, and Discord channel.
- **RSS feed collection** — configurable fetch interval per source (1 h, 2 h, 6 h, 12 h, 24 h); automatic deduplication by URL.
- **LLM scoring** — each article is scored 1–10 by relevance to its theme using Google Gemini 2.5 Flash; a short summary is generated in French.
- **pgvector embeddings** — 384-dimensional vectors (paraphrase-multilingual-MiniLM-L12-v2) stored alongside each analysis for future semantic similarity queries.
- **Daily Discord digest** — top articles (score ≥ 5) delivered as Discord embeds at a configurable UTC hour per theme.
- **Interactive feedback loop** — each article card in Discord has 👍 / 👎 buttons; ratings are stored and injected into future LLM prompts to continuously tune scoring.
- **Streamlit dashboard** — manage themes, sources, and webhooks; browse articles and statistics from the browser.
- **Ed25519 interaction verification** — all Discord button callbacks are cryptographically verified before processing.

---

## Prerequisites

- **Docker** ≥ 24 and **Docker Compose** v2 (`docker compose` plugin, not `docker-compose`)
- **Google Gemini API key** — [Google AI Studio](https://aistudio.google.com/)
- **Discord application** with a bot token and a public key (see [Discord Setup](#discord-setup))

---

## Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/NizardV/vigil.git
cd vigil

# 2. Copy and fill in the environment file
cp .env.example .env
# Edit .env — at minimum set POSTGRES_PASSWORD, GEMINI_API_KEY,
# SECRET_KEY, DISCORD_PUBLIC_KEY, DISCORD_BOT_TOKEN

# 3. Start all services
docker compose up -d

# 4. Open the dashboard
open http://localhost:8501

# 5. Browse the interactive API docs
open http://localhost:8000/docs
```

The backend creates the `pgvector` extension and all tables automatically on first startup. No manual migration step is needed.

---

## Environment Variables

| Variable                | Required | Default                    | Description                                          |
|-------------------------|----------|----------------------------|------------------------------------------------------|
| `POSTGRES_DB`           | Yes      | `vigil`                    | PostgreSQL database name                             |
| `POSTGRES_USER`         | Yes      | `vigil_user`               | PostgreSQL username                                  |
| `POSTGRES_PASSWORD`     | Yes      | —                          | PostgreSQL password                                  |
| `DATABASE_URL`          | Yes      | —                          | Full SQLAlchemy URL (`postgresql://user:pass@host/db`) |
| `REDIS_URL`             | Yes      | `redis://redis:6379/0`     | Redis connection URL                                 |
| `CELERY_BROKER_URL`     | Yes      | `redis://redis:6379/0`     | Celery broker (same as Redis)                        |
| `CELERY_RESULT_BACKEND` | Yes      | `redis://redis:6379/1`     | Celery result backend                                |
| `GEMINI_API_KEY`        | Yes      | —                          | Google Gemini API key                                |
| `GEMINI_MODEL`          | No       | `gemini-2.5-flash`         | Gemini model identifier                              |
| `SECRET_KEY`            | Yes      | —                          | FastAPI secret key — generate with `openssl rand -hex 32` |
| `DISCORD_WEBHOOK_URL`   | No       | —                          | Default Discord webhook URL for digests              |
| `DISCORD_PUBLIC_KEY`    | Yes*     | —                          | Discord app public key for interaction verification  |
| `DISCORD_BOT_TOKEN`     | Yes*     | —                          | Discord bot token (required for button support)      |
| `DIGEST_HOUR`           | No       | `7`                        | Default global digest hour (UTC)                     |
| `DIGEST_MINUTE`         | No       | `0`                        | Default global digest minute (UTC)                   |
| `API_URL`               | No       | `http://backend:8000/api`  | Internal URL used by Streamlit to reach FastAPI      |
| `DEBUG`                 | No       | `false`                    | FastAPI debug mode                                   |

\* Required for the Discord feedback loop (bot token + public key).

---

## Discord Setup

### 1. Create a Discord Application

1. Open the [Discord Developer Portal](https://discord.com/developers/applications) and click **New Application**.
2. Navigate to **Bot** → click **Add Bot** → copy the **Bot Token** → set `DISCORD_BOT_TOKEN`.
3. Navigate to **General Information** → copy **Public Key** → set `DISCORD_PUBLIC_KEY`.

### 2. Configure the Interactions Endpoint

In **General Information**, set **Interactions Endpoint URL** to:

```
https://vigil.yourdomain.com/api/discord/interactions
```

Discord will send a PING to verify the endpoint. The FastAPI server must be reachable before saving. See [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md) for the Nginx configuration that routes `/api/` to FastAPI.

### 3. Set Up a Webhook for Digest Delivery

1. In your Discord server, open a channel's **Settings → Integrations → Webhooks**.
2. Create a new webhook, copy the URL, and either set it as `DISCORD_WEBHOOK_URL` (global default) or configure it per-theme in the Streamlit dashboard.

### 4. Invite the Bot (for button support)

The bot requires only `bot` and `applications.commands` scopes. It does not need message reading permissions — it only sends messages and receives interaction callbacks via the interactions endpoint.

---

## How the Feedback Loop Works

```
Celery Beat (every hour, minute=0)
    │
    ▼
fetch_all_sources()
    └─► fetch_source(source_id) for each active source
            │  Pulls RSS feed (max 20 entries)
            │  Deduplicates by URL
            │  Inserts new Article records (processed=False)
            └─► process_article(article_id) for each new article
                    │
                    │  1. Load Article + Source + Theme
                    │  2. Build LLM prompt:
                    │       - Theme name + keywords
                    │       - Last 10 user ratings for this theme
                    │         ("Users liked: [titles]" / "Users disliked: [titles]")
                    │  3. Call Gemini → {summary, relevance_score, theme_match}
                    │  4. Generate 384-D embedding → store in pgvector
                    └─► Analysis saved, article marked processed=True

Celery Beat (every hour, minute=0) — also runs send_all_digests()
    └─► send_digest(theme_id) for themes whose digest_hour == current UTC hour
            │  1. Query top 10 articles with score ≥ 5
            │  2. Generate Markdown digest with Gemini
            │  3. Save Digest record to database
            │  4. Send digest embed to all active webhooks
            └─► Send each article as an individual Discord embed:
                    [👍 Relevant]  [👎 Not relevant]  [Read article ↗]

User clicks 👍 or 👎 in Discord
    │
    ▼
POST /api/discord/interactions
    │  Ed25519 signature verified against DISCORD_PUBLIC_KEY
    │  Feedback(article_id, rating=+1 or -1) inserted into PostgreSQL
    └─► Ephemeral reply sent to user ("Thanks for your feedback!")

Next process_article() for the same theme includes this feedback as LLM context
```

---

## Adding a New Theme or Source

### Via the Streamlit dashboard (recommended)

1. Open **https://vigil.yourdomain.com** (or `http://localhost:8501` locally).
2. **Themes** page → **Add theme**: fill in name, description, keywords, and digest hour (UTC).
3. **Sources** page → **Add source**: select the theme, paste an RSS feed URL, choose a fetch interval.
4. **Webhooks** page → **Add webhook**: select the theme, paste the Discord webhook URL.

The next Celery Beat tick (top of the hour) will start collecting articles from the new source.

### Via the API

```bash
# Create a theme
curl -X POST http://localhost:8000/api/themes \
  -H "Content-Type: application/json" \
  -d '{"name":"DevSecOps","keywords":["devsecops","sast","sca","supply chain"],"digest_hour":8}'

# Add an RSS source to the theme (replace theme_id with the returned id)
curl -X POST http://localhost:8000/api/sources \
  -H "Content-Type: application/json" \
  -d '{"theme_id":1,"name":"Krebs on Security","url":"https://krebsonsecurity.com/feed/","fetch_interval_hours":6}'

# Add a Discord webhook for that theme
curl -X POST http://localhost:8000/api/webhooks \
  -H "Content-Type: application/json" \
  -d '{"theme_id":1,"url":"https://discord.com/api/webhooks/...","type":"discord"}'
```

---

## API Overview

The FastAPI backend exposes a REST API at `/api/`. Interactive documentation is available at:

- **Swagger UI** — `https://vigil.yourdomain.com/api/docs`
- **ReDoc** — `https://vigil.yourdomain.com/api/redoc`

| Resource | Base path           | Operations                                              |
|----------|---------------------|---------------------------------------------------------|
| Themes   | `/api/themes`       | List, create, get, update (PATCH), delete               |
| Sources  | `/api/sources`      | List (filter by theme), create, get, update, delete, toggle active |
| Articles | `/api/articles`     | List (filter by theme/score), get, trigger LLM processing |
| Feedback | `/api/feedback`     | Create rating, list by article                          |
| Digests  | `/api/digests`      | List (filter by theme), trigger manually                |
| Webhooks | `/api/webhooks`     | List, create, delete                                    |
| Discord  | `/api/discord`      | Interaction endpoint (Ed25519-verified POST)            |
| Health   | `/health`           | Liveness probe                                          |

See [docs/API.md](docs/API.md) for the complete endpoint reference with request/response schemas.

---

## Deployment

For production deployment on a VPS with host Nginx, Certbot SSL, and Discord interactions endpoint configuration, see [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md).
