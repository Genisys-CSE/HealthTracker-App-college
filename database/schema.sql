-- HA-5: HealthTracker database schema (users, daily health metrics, sync status)
CREATE TABLE users (
    id            INTEGER PRIMARY KEY,
    email         TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    created_at    TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE health_metrics (
    id          INTEGER PRIMARY KEY,
    user_id     INTEGER NOT NULL REFERENCES users(id),
    metric_date DATE NOT NULL,
    steps       INTEGER,
    weight_kg   REAL,
    sleep_hours REAL,
    heart_rate  INTEGER,
    sync_status TEXT NOT NULL DEFAULT 'pending',
    UNIQUE (user_id, metric_date)
);

CREATE INDEX idx_health_metrics_user_date ON health_metrics (user_id, metric_date);
