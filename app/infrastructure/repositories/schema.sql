-- NeuroMesh Postgres schema.
-- Plain SQL, no ORM/migration-tool magic, by design --
-- see ADR 0004 (psycopg over SQLAlchemy).

CREATE TABLE IF NOT EXISTS nodes (
    id                    UUID PRIMARY KEY,
    capacity_cpu_cores    INTEGER NOT NULL,
    capacity_memory_mib   INTEGER NOT NULL,
    capacity_vram_mib     INTEGER NOT NULL,
    available_cpu_cores   INTEGER NOT NULL,
    available_memory_mib  INTEGER NOT NULL,
    available_vram_mib    INTEGER NOT NULL,
    labels                JSONB NOT NULL DEFAULT '{}'::jsonb,
    last_seen_at          TIMESTAMPTZ NOT NULL,
    draining              BOOLEAN NOT NULL DEFAULT false
);

CREATE TABLE IF NOT EXISTS jobs (
    id                 UUID PRIMARY KEY,
    cpu_cores          INTEGER NOT NULL,
    memory_mib         INTEGER NOT NULL,
    vram_mib           INTEGER NOT NULL DEFAULT 0,
    priority           INTEGER NOT NULL DEFAULT 0,
    constraints        JSONB NOT NULL DEFAULT '{}'::jsonb,
    max_retries        INTEGER NOT NULL DEFAULT 0,
    retry_count        INTEGER NOT NULL DEFAULT 0,
    status             TEXT NOT NULL,
    assigned_node_id   UUID REFERENCES nodes(id) ON DELETE SET NULL,
    submitted_at       TIMESTAMPTZ NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_jobs_status ON jobs (status);
CREATE INDEX IF NOT EXISTS idx_nodes_draining ON nodes (draining);
