CREATE TABLE IF NOT EXISTS opinion_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    topic_id TEXT NOT NULL,
    source TEXT NOT NULL,             -- 'reddit' | 'news'
    external_id TEXT NOT NULL,
    title TEXT NOT NULL,
    url TEXT,
    created_utc INTEGER NOT NULL,     -- unix timestamp of the original post/article
    fetched_utc INTEGER NOT NULL,
    score REAL,                       -- reddit upvotes, null for news
    sentiment REAL,                   -- compound score, -1..1
    sentiment_method TEXT,            -- 'hf_roberta' (real ML classifier) | 'vader' (rule-based fallback)
    UNIQUE(topic_id, source, external_id)
);

CREATE INDEX IF NOT EXISTS idx_items_topic_created ON opinion_items(topic_id, created_utc);

CREATE TABLE IF NOT EXISTS daily_sentiment (
    topic_id TEXT NOT NULL,
    day TEXT NOT NULL,               -- ISO date, UTC
    mean_sentiment REAL NOT NULL,
    item_count INTEGER NOT NULL,
    PRIMARY KEY (topic_id, day)
);

CREATE TABLE IF NOT EXISTS forecasts (
    topic_id TEXT NOT NULL,
    generated_utc INTEGER NOT NULL,
    horizon_day TEXT NOT NULL,       -- ISO date being forecast
    predicted_sentiment REAL NOT NULL,
    PRIMARY KEY (topic_id, generated_utc, horizon_day)
);

CREATE TABLE IF NOT EXISTS promise_atoms (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    party_id TEXT NOT NULL,
    page INTEGER NOT NULL,
    number TEXT,
    text TEXT NOT NULL,
    taxonomy_category TEXT NOT NULL,
    taxonomy_method TEXT NOT NULL DEFAULT 'keyword',  -- 'llm' (Groq classifier) | 'keyword' (fallback)
    matched_keywords TEXT,            -- JSON array, for auditability of the tag (keyword method only)
    quantified INTEGER NOT NULL       -- 0/1: has a number/amount/date, vs. purely directional
);

CREATE INDEX IF NOT EXISTS idx_atoms_category ON promise_atoms(taxonomy_category);
CREATE INDEX IF NOT EXISTS idx_atoms_party ON promise_atoms(party_id);
