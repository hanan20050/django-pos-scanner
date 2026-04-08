import sqlite3
import os

db_path = 'db.sqlite3'
conn = sqlite3.connect(db_path)
conn.execute('PRAGMA journal_mode=WAL')
conn.commit()
conn.close()

print(f'Created {db_path}, size: {os.path.getsize(db_path)} bytes')
