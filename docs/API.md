# Vigil API Reference

## Base URL

| Environment | Base URL                             |
|-------------|--------------------------------------|
| Production  | `https://vigil.yourdomain.com/api`  |
| Local dev   | `http://localhost:8000/api`          |

## Interactive Documentation

- **Swagger UI** — `{base_url}/../docs`
- **ReDoc** — `{base_url}/../redoc`

## Authentication

The API has no authentication layer — it is designed for internal use behind Nginx. Expose it only on trusted networks or via a reverse proxy that enforces access controls.

## Common Response Codes

| Code | Meaning                                         |
|------|-------------------------------------------------|
| 200  | Success                                         |
| 201  | Resource created                                |
| 204  | Success — no content (DELETE)                   |
| 400  | Bad request — invalid payload                   |
| 401  | Unauthorized — used by `/discord/interactions` for invalid signatures |
| 404  | Resource not found                              |
| 422  | Validation error — request body does not match schema |
| 500  | Internal server error                           |

---

## Resources

- [Themes](#themes)
- [Sources](#sources)
- [Articles](#articles)
- [Feedback](#feedback)
- [Digests](#digests)
- [Webhooks](#webhooks)
- [Discord Interactions](#discord-interactions)
- [Health](#health)

---

## Themes

Themes are the top-level organizational unit. Each theme defines a topic of interest, a set of keywords used to guide LLM scoring, a list of RSS sources, and a digest schedule.

### `GET /themes`

List all themes.

**Response** `200 OK`

```json
[
  {
    "id": 1,
    "name": "Cloud Native",
    "description": "Kubernetes, containers, service mesh",
    "keywords": ["kubernetes", "docker", "istio", "eBPF"],
    "digest_hour": 7,
    "digest_enabled": true,
    "created_at": "2024-01-15T10:30:00Z"
  }
]
```

---

### `POST /themes`

Create a new theme.

**Request body**

```json
{
  "name": "DevSecOps",
  "description": "Security in the CI/CD pipeline",
  "keywords": ["devsecops", "sast", "sca", "supply chain"],
  "digest_hour": 8,
  "digest_enabled": true
}
```

| Field            | Type           | Required | Default | Description                          |
|------------------|----------------|----------|---------|--------------------------------------|
| `name`           | string         | Yes      | —       | Theme display name                   |
| `description`    | string \| null | No       | null    | Free-text description                |
| `keywords`       | string[]       | No       | null    | Keywords injected into the LLM prompt |
| `digest_hour`    | integer        | No       | 7       | UTC hour at which the digest is sent |
| `digest_enabled` | boolean        | No       | true    | Whether to send automatic digests    |

**Response** `201 Created`

```json
{
  "id": 2,
  "name": "DevSecOps",
  "description": "Security in the CI/CD pipeline",
  "keywords": ["devsecops", "sast", "sca", "supply chain"],
  "digest_hour": 8,
  "digest_enabled": true,
  "created_at": "2024-06-14T09:00:00Z"
}
```

---

### `GET /themes/{theme_id}`

Get a single theme by ID.

**Path parameters**

| Parameter  | Type    | Description  |
|------------|---------|--------------|
| `theme_id` | integer | Theme ID     |

**Response** `200 OK` — same shape as a single element from `GET /themes`.

**Response** `404 Not Found` if the theme does not exist.

---

### `PATCH /themes/{theme_id}`

Update a theme. All fields are optional; only the fields provided are updated.

**Path parameters**

| Parameter  | Type    | Description  |
|------------|---------|--------------|
| `theme_id` | integer | Theme ID     |

**Request body** — same schema as `POST /themes` (all fields optional in PATCH).

**Response** `200 OK` — updated theme object.

---

### `DELETE /themes/{theme_id}`

Delete a theme and all associated resources (sources, articles, digests, webhooks).

**Path parameters**

| Parameter  | Type    | Description  |
|------------|---------|--------------|
| `theme_id` | integer | Theme ID     |

**Response** `204 No Content`

---

## Sources

Sources are RSS feed URLs associated with a theme. Celery fetches each active source at the configured interval.

### `GET /sources`

List sources, optionally filtered by theme.

**Query parameters**

| Parameter  | Type    | Required | Description              |
|------------|---------|----------|--------------------------|
| `theme_id` | integer | No       | Filter by theme          |

**Response** `200 OK`

```json
[
  {
    "id": 1,
    "theme_id": 1,
    "name": "The Register — DevOps",
    "url": "https://www.theregister.com/devops/headlines.atom",
    "type": "rss",
    "active": true,
    "fetch_interval_hours": 6,
    "created_at": "2024-01-15T10:30:00Z"
  }
]
```

---

### `POST /sources`

Add an RSS source to a theme.

**Request body**

```json
{
  "theme_id": 1,
  "name": "The Register — DevOps",
  "url": "https://www.theregister.com/devops/headlines.atom",
  "type": "rss",
  "active": true,
  "fetch_interval_hours": 6
}
```

| Field                  | Type           | Required | Default | Description                                          |
|------------------------|----------------|----------|---------|------------------------------------------------------|
| `theme_id`             | integer        | Yes      | —       | ID of the parent theme                               |
| `name`                 | string \| null | No       | null    | Human-readable label for the source                  |
| `url`                  | string         | Yes      | —       | RSS/Atom feed URL                                    |
| `type`                 | string         | No       | `"rss"` | Feed type (currently only `"rss"` is processed)      |
| `active`               | boolean        | No       | true    | Whether Celery should fetch this source              |
| `fetch_interval_hours` | integer        | No       | 2       | How often to fetch, in hours (1, 2, 6, 12, or 24)   |

**Response** `201 Created` — created source object.

---

### `GET /sources/{source_id}`

Get a single source by ID.

**Response** `200 OK` — source object.

---

### `PATCH /sources/{source_id}`

Update a source.

**Response** `200 OK` — updated source object.

---

### `DELETE /sources/{source_id}`

Delete a source.

**Response** `204 No Content`

---

### `POST /sources/{source_id}/toggle`

Toggle the `active` field of a source (active → inactive or vice versa).

**Path parameters**

| Parameter   | Type    | Description |
|-------------|---------|-------------|
| `source_id` | integer | Source ID   |

**Response** `200 OK` — updated source object with the new `active` value.

---

## Articles

Articles are individual items fetched from RSS sources. Each article is processed once by the LLM (scored and embedded) and stored with its analysis.

### `GET /articles`

List articles with optional filters.

**Query parameters**

| Parameter   | Type    | Required | Default | Description                              |
|-------------|---------|----------|---------|------------------------------------------|
| `theme_id`  | integer | No       | —       | Filter articles belonging to this theme  |
| `min_score` | float   | No       | —       | Only return articles with score ≥ this   |
| `limit`     | integer | No       | 50      | Maximum number of articles to return     |

**Response** `200 OK`

```json
[
  {
    "id": 42,
    "title": "How eBPF is reshaping observability",
    "url": "https://example.com/articles/ebpf-observability",
    "published_at": "2024-06-13T14:00:00Z",
    "fetched_at": "2024-06-13T16:02:00Z",
    "processed": true,
    "analysis": {
      "summary": "Cet article présente comment eBPF permet une observabilité profonde sans instrumentation du code applicatif.",
      "relevance_score": 8.5,
      "theme_match": "Cloud Native",
      "created_at": "2024-06-13T16:03:00Z"
    }
  }
]
```

Articles that have not yet been processed by the LLM have `"processed": false` and `"analysis": null`.

---

### `GET /articles/{article_id}`

Get a single article by ID, including its analysis if available.

**Response** `200 OK` — article object (same shape as an element from `GET /articles`).

**Response** `404 Not Found`

---

### `POST /articles/{article_id}/process`

Manually trigger LLM processing (scoring + embedding) for a single article. Useful for reprocessing or for articles that were not picked up automatically.

**Path parameters**

| Parameter    | Type    | Description  |
|--------------|---------|--------------|
| `article_id` | integer | Article ID   |

**Response** `200 OK`

```json
{
  "message": "Article queued for processing"
}
```

The task is dispatched asynchronously to Celery. Poll `GET /articles/{article_id}` to check when `processed` becomes `true`.

---

## Feedback

Feedback records store user ratings (👍 = +1, 👎 = −1) associated with articles. Ratings are created automatically when users click buttons in Discord, but can also be submitted via the API.

### `POST /feedback`

Submit a rating for an article.

**Request body**

```json
{
  "article_id": 42,
  "rating": 1,
  "comment": "Very relevant to our ongoing migration"
}
```

| Field        | Type           | Required | Description                                 |
|--------------|----------------|----------|---------------------------------------------|
| `article_id` | integer        | Yes      | ID of the article being rated               |
| `rating`     | integer        | Yes      | `1` for 👍 (relevant), `-1` for 👎 (not relevant) |
| `comment`    | string \| null | No       | Optional free-text comment                  |

**Response** `201 Created`

```json
{
  "id": 7,
  "article_id": 42,
  "rating": 1,
  "comment": "Very relevant to our ongoing migration",
  "created_at": "2024-06-14T08:15:00Z"
}
```

---

### `GET /feedback/article/{article_id}`

List all feedback records for a specific article.

**Path parameters**

| Parameter    | Type    | Description |
|--------------|---------|-------------|
| `article_id` | integer | Article ID  |

**Response** `200 OK`

```json
[
  {
    "id": 7,
    "article_id": 42,
    "rating": 1,
    "comment": null,
    "created_at": "2024-06-14T08:15:00Z"
  }
]
```

---

## Digests

A digest is a Gemini-generated Markdown summary of the top articles for a theme, delivered to Discord at the configured hour.

### `GET /digests`

List past digests, optionally filtered by theme.

**Query parameters**

| Parameter  | Type    | Required | Description              |
|------------|---------|----------|--------------------------|
| `theme_id` | integer | No       | Filter by theme          |

**Response** `200 OK`

```json
[
  {
    "id": 3,
    "theme_id": 1,
    "content": "## Cloud Native — 14 juin 2024\n\n**Tendances du jour :** ...",
    "sent_at": "2024-06-14T07:00:05Z",
    "channel": "discord"
  }
]
```

---

### `POST /digests/trigger/{theme_id}`

Manually trigger digest generation and delivery for a theme. Does not wait for the configured `digest_hour`. Useful for testing.

**Path parameters**

| Parameter  | Type    | Description |
|------------|---------|-------------|
| `theme_id` | integer | Theme ID    |

**Response** `200 OK`

```json
{
  "message": "Digest triggered for theme 1"
}
```

The task is dispatched asynchronously to Celery. The digest will appear in `GET /digests` once the Celery task completes and will be sent to all active webhooks for the theme.

---

## Webhooks

Webhooks define where digests and article notifications are delivered. Currently only Discord webhooks are supported.

### `GET /webhooks`

List all configured webhooks.

**Response** `200 OK`

```json
[
  {
    "id": 1,
    "theme_id": 1,
    "url": "https://discord.com/api/webhooks/1234567890/abc...",
    "type": "discord",
    "active": true
  }
]
```

---

### `POST /webhooks`

Add a webhook for a theme.

**Request body**

```json
{
  "theme_id": 1,
  "url": "https://discord.com/api/webhooks/1234567890/abc...",
  "type": "discord",
  "active": true
}
```

| Field      | Type    | Required | Default     | Description                              |
|------------|---------|----------|-------------|------------------------------------------|
| `theme_id` | integer | Yes      | —           | ID of the associated theme               |
| `url`      | string  | Yes      | —           | Discord webhook URL                      |
| `type`     | string  | No       | `"discord"` | Webhook type (only `"discord"` supported)|
| `active`   | boolean | No       | true        | Whether to send to this webhook          |

**Response** `201 Created` — created webhook object.

---

### `DELETE /webhooks/{webhook_id}`

Delete a webhook.

**Path parameters**

| Parameter    | Type    | Description  |
|--------------|---------|--------------|
| `webhook_id` | integer | Webhook ID   |

**Response** `204 No Content`

---

## Discord Interactions

This endpoint receives button interaction callbacks from Discord. It is not meant to be called directly — Discord calls it automatically when a user clicks a 👍 or 👎 button.

### `POST /discord/interactions`

Handle a Discord interaction (PING verification or button click).

**Required headers**

| Header                   | Description                                      |
|--------------------------|--------------------------------------------------|
| `X-Signature-Ed25519`    | Ed25519 hex signature of the raw request body    |
| `X-Signature-Timestamp`  | Unix timestamp included in the signed payload    |

The signature is verified against `DISCORD_PUBLIC_KEY`. Requests with an invalid or missing signature return `401 Unauthorized`.

**Request body — PING (type 1)**

Discord sends this to verify the endpoint during bot setup:

```json
{
  "type": 1
}
```

**Response** `200 OK`

```json
{
  "type": 1
}
```

---

**Request body — Button interaction (type 3)**

Sent when a user clicks a 👍 or 👎 button on an article embed:

```json
{
  "type": 3,
  "data": {
    "custom_id": "feedback_like_42"
  },
  "member": {
    "user": { "id": "123456789", "username": "alice" }
  }
}
```

The `custom_id` format is:
- `feedback_like_{article_id}` — user clicked 👍 (rating = +1)
- `feedback_dislike_{article_id}` — user clicked 👎 (rating = −1)

**Response** `200 OK` — ephemeral message visible only to the user who clicked

```json
{
  "type": 4,
  "data": {
    "content": "Thanks for your feedback!",
    "flags": 64
  }
}
```

`flags: 64` marks the response as ephemeral (only visible to the user who clicked).

---

## Health

### `GET /health`

Liveness probe for load balancers and monitoring tools.

**Response** `200 OK`

```json
{
  "status": "ok"
}
```
