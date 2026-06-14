# WatchLLM 🔍

Système de veille technologique automatisé avec scoring LLM, feedback loop et déploiement Docker.

## Stack technique

| Couche | Technologie |
|---|---|
| Collecte | n8n + feedparser |
| Backend | FastAPI (Python 3.12) |
| File d''attente | Celery + Redis |
| LLM | Gemini Flash (Google) |
| Embeddings | sentence-transformers (MiniLM) |
| Base de données | PostgreSQL + pgvector |
| Frontend | Streamlit |
| Déploiement | Docker Compose (VPS OVH) |
| Notifications | Discord Webhooks |

## Architecture

```
Sources RSS → n8n (cron) → FastAPI → Celery Worker
                                          ├── Gemini Flash (scoring 1-10)
                                          ├── pgvector (embeddings)
                                          └── PostgreSQL
                                               ↓
                                         Digest quotidien
                                               ↓
                                      Discord Webhook
                                               +
                                      Streamlit Dashboard
                                      (config + feedback 👍👎)
```

## Démarrage

```bash
# 1. Cloner le projet
git clone https://github.com/NizardV/watchllm.git
cd watchllm

# 2. Configurer les variables d''environnement
cp .env.example .env
# Remplir .env avec vos clés (Gemini API key, Discord webhook, etc.)

# 3. Lancer tous les services
docker compose up -d

# 4. Accéder aux interfaces
# API docs :     http://localhost:8000/docs
# Dashboard :    http://localhost:8501
# n8n :          http://localhost:5678
```

## Fonctionnalités

- **Collecte automatique** : sources RSS configurables par thème, toutes les 2h
- **Scoring LLM** : chaque article reçoit un score de pertinence 1-10 + résumé en français
- **Embeddings pgvector** : recherche sémantique entre articles similaires
- **Feedback loop** : les 👍/👎 influencent le prompt LLM pour affiner le scoring
- **Digest quotidien** : synthèse des meilleurs articles envoyée sur Discord chaque matin
- **Dashboard Streamlit** : visualisation des scores, gestion des sources, webhooks

## Variables d''environnement

| Variable | Description |
|---|---|
| `GEMINI_API_KEY` | Clé API Google Gemini |
| `DISCORD_WEBHOOK_URL` | Webhook Discord par défaut |
| `POSTGRES_PASSWORD` | Mot de passe PostgreSQL |
| `DIGEST_HOUR` | Heure d''envoi du digest (UTC) |

