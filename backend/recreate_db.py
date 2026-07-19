import os
import sqlite3

from app.database import Base, engine

print('removing db file')
if os.path.exists('carepilot.db'):
    os.remove('carepilot.db')

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)
print('created tables')
conn = sqlite3.connect('carepilot.db')
print(conn.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name").fetchall())
conn.close()
