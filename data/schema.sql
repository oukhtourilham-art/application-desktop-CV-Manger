-- Table des utilisateurs
CREATE TABLE IF NOT EXISTS users (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    username    TEXT NOT NULL UNIQUE,
    password    TEXT NOT NULL,
    role        TEXT NOT NULL CHECK(role IN ('etudiant', 'rh')),
    created_at  TEXT DEFAULT (datetime('now'))
);

-- Table des CV
CREATE TABLE IF NOT EXISTS cvs (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id     INTEGER NOT NULL,
    filename    TEXT NOT NULL,
    score       REAL DEFAULT 0,
    uploaded_at TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Table des compétences
CREATE TABLE IF NOT EXISTS skills (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    cv_id       INTEGER NOT NULL,
    name        TEXT NOT NULL,
    domain      TEXT NOT NULL,
    FOREIGN KEY (cv_id) REFERENCES cvs(id)
);

--Donnée de test
INSERT OR IGNORE INTO users (username, password, role)
VALUES ('adim_rh', '2a724e801c5d5b994bbe0c26bed69688a6e54d6dad8b1e2e47c7b0d37e0b1d99', 'rh'),
 ('etudiant1', 'c6a529d6ac7fd3c2db3b20f57a54e2d35a0fc1da0082616f0c7e59f89d23e0d3', 'etudiant');