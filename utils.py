import redis
import sqlite3
import json
import uuid

# Redis Setup
redis_client = redis.Redis(host='localhost', port=6379, db=0)

def check_cache(query):
    cached = redis_client.get(query)
    if cached:
        return json.loads(cached)
    return None

def save_to_cache(query, data):
    redis_client.set(query, json.dumps(data))

# SQLite Setup
conn = sqlite3.connect('logs.db')
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS logs (
        id TEXT PRIMARY KEY,
        query TEXT,
        response TEXT,
        sources TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
""")
conn.commit()

def log_to_db(query, response, sources):
    cursor.execute("""
        INSERT INTO logs (id, query, response, sources)
        VALUES (?, ?, ?, ?)
    """, (str(uuid.uuid4()), query, response, json.dumps(sources)))
    conn.commit()
