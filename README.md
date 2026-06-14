# Vigil

Automated tech watch system with LLM scoring, feedback loop and configurable webhook notifications.

> Systeme de veille technologique automatise avec scoring LLM, boucle de feedback et notifications configurables.

## Stack

| Layer | Technology |
|---|---|
| Collector | n8n + feedparser |
| Backend | FastAPI (Python 3.12) |
| Queue | Celery + Redis |
| LLM | Gemini Flash (Google) |
| Embeddings | sentence-transformers (MiniLM-L12) |
| Database | PostgreSQL + pgvector |
| Dashboard | Streamlit |
| Deployment | Docker Compose (OVH VPS) |
| Notifications | Configurable webhooks (Discord, Slack...) |

## Architecture

```
RSS Sources -> n8n (cron) -> FastAPI -> Celery Worker
                                            |-- Gemini Flash (score 1-10)
                                            |-- pgvector (embeddings)
                                            └-- PostgreSQL
                                                 |
                                           Daily digest
                                                 |
                                        Webhook notifications
                                                 +
                                        Streamlit Dashboard
                                        (sources config + feedback)
```

## Getting started

```bash
# 1. Clone
git clone https://github.com/NizardV/vigil.git
cd vigil

# 2. Configure environment
cp .env.example .env
# Fill in your keys (Gemini API key, webhook URLs, etc.)

# 3. Start all services
docker compose up -d

# 4. Access
# API docs  : http://localhost:8000/docs
# Dashboard : http://localhost:8501
# n8n       : http://localhost:5678
```

## Features

- **Automatic collection** — configurable RSS sources per theme, every 2 hours
- **LLM scoring** — each article gets a relevance score (1-10) + summary in French
- **Vector search** — pgvector embeddings for semantic similarity between articles
- **Feedback loop** — thumbs up/down influence the LLM prompt to refine future scoring
- **Daily digest** — top articles sent every morning via webhook
- **Streamlit dashboard** — score visualization, source management, webhook config

## Environment variables

| Variable | Description |
|---|---|
| `GEMINI_API_KEY` | Google Gemini API key |
| `DISCORD_WEBHOOK_URL` | Default webhook URL |
| `POSTGRES_PASSWORD` | PostgreSQL password |
| `DIGEST_HOUR` | Digest send time (UTC hour) |
| `N8N_PASSWORD` | n8n admin password |