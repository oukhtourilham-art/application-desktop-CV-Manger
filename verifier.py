import sqlite3

conn = sqlite3.connect('data/cv_manager.db')

tables = [r[0] for r in conn.execute(
    "SELECT name FROM sqlite_master WHERE type='table'"
)]
print("Tables :", tables)

colonnes = [r[1] for r in conn.execute("PRAGMA table_info(cvs)")]
print("Colonnes cvs :", colonnes)

conn.close()