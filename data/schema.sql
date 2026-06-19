CREATE TABLE IF NOT EXISTS users (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    username    TEXT NOT NULL UNIQUE,
    password    TEXT NOT NULL,
    role        TEXT NOT NULL CHECK(role IN ('etudiant', 'rh')),
    created_at  TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS cvs (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id     INTEGER NOT NULL,
    filename    TEXT NOT NULL,
    filepath    TEXT NOT NULL,
    score       REAL DEFAULT 0,
    uploaded_at TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS skills (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    cv_id       INTEGER NOT NULL,
    name        TEXT NOT NULL,
    domain      TEXT NOT NULL,
    FOREIGN KEY (cv_id) REFERENCES cvs(id)
);