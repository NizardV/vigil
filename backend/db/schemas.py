from datetime import datetime
from pydantic import BaseModel, field_validator

# ── Global constants ────────────────────────────────────────────

VALID_TAGS = {"relevant", "off-topic", "already-known", "to-dig-deeper", "actionable"}

# ── Themes ──────────────────────────────────────────────

class ThemeCreate(BaseModel):
    name: str
    description: str | None = None
    keywords: list[str] | None = None
    digest_hour: int = 7
    digest_enabled: bool = True

class ThemeOut(ThemeCreate):
    id: int
    created_at: datetime
    class Config:
        from_attributes = True


# ── Sources ─────────────────────────────────────────────

class SourceCreate(BaseModel):
    theme_id: int
    name: str | None = None
    url: str
    type: str = "rss"
    active: bool = True
    fetch_interval_hours: int = 2

class SourceOut(SourceCreate):
    id: int
    created_at: datetime
    class Config:
        from_attributes = True


# ── Articles ─────────────────────────────────────────────

class AnalysisOut(BaseModel):
    summary: str | None
    relevance_score: float | None
    theme_match: str | None
    key_points: list[str] | None = None
    created_at: datetime
    class Config:
        from_attributes = True

class ArticleOut(BaseModel):
    id: int
    title: str
    url: str
    published_at: datetime | None
    fetched_at: datetime
    processed: bool
    analysis: AnalysisOut | None = None
    class Config:
        from_attributes = True


# ── Feedback ─────────────────────────────────────────────

class FeedbackCreate(BaseModel):
    article_id: int
    rating: int
    tags: list[str] | None = None
    comment: str | None = None

    @field_validator("rating")
    @classmethod
    def rating_range(cls, v):
        if v not in range(1, 6):
            raise ValueError("Rating must be between 1 and 5")
        return v

    @field_validator("tags")
    @classmethod
    def tags_valid(cls, v):
        if v is None:
            return v
        invalid = set(v) - VALID_TAGS
        if invalid:
            raise ValueError(f"Invalid tags: {invalid}")
        return v

class FeedbackOut(BaseModel):
    id: int
    article_id: int
    rating: int
    tags: list[str] | None = None
    comment: str | None = None
    created_at: datetime
    class Config:
        from_attributes = True


# ── Digests ──────────────────────────────────────────────

class DigestOut(BaseModel):
    id: int
    theme_id: int
    content: str | None
    sent_at: datetime
    channel: str
    class Config:
        from_attributes = True


# ── Webhooks ─────────────────────────────────────────────

class WebhookCreate(BaseModel):
    theme_id: int
    url: str
    type: str = "discord"
    active: bool = True

class WebhookOut(WebhookCreate):
    id: int
    class Config:
        from_attributes = True