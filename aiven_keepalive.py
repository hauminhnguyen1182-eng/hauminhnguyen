import os
import psycopg2
from opensearchpy import OpenSearch
import requests
from datetime import datetime
from pathlib import Path

# Load env
env_path = Path("/workspace/.env")
if env_path.exists():
    for line in env_path.read_text().splitlines():
        if "=" in line and not line.startswith("#"):
            key, val = line.split("=", 1)
            os.environ[key.strip()] = val.strip()

def keepalive_postgres():
    try:
        conn = psycopg2.connect(
            host=os.environ.get('PG_HOST', 'pg-2137e692-hauminhnguyen1182-7219.l.aivencloud.com'),
            port=os.environ.get('PG_PORT', '23274'),
            dbname=os.environ.get('PG_DB', 'defaultdb'),
            user=os.environ.get('PG_USER', 'avnadmin'),
            password=os.environ.get('PG_PASS', ''),
            sslmode='require'
        )
        cur = conn.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS keepalive (id SERIAL PRIMARY KEY, timestamp TIMESTAMP)")
        cur.execute("INSERT INTO keepalive (timestamp) VALUES (NOW())")
        conn.commit()
        cur.close()
        conn.close()
        print(f"✅ PostgreSQL: OK")
    except Exception as e:
        print(f"❌ PostgreSQL: {e}")

def keepalive_opensearch():
    try:
        client = OpenSearch(
            hosts=[{'host': os.environ.get('OS_HOST', 'os-8509b23-hauminhnguyen1182-7219.l.aivencloud.com'), 'port': int(os.environ.get('OS_PORT', '23274'))}],
            http_auth=(os.environ.get('OS_USER', 'avnadmin'), os.environ.get('OS_PASS', '')),
            use_ssl=True, verify_certs=False, ssl_assert_hostname=False, ssl_show_warn=False
        )
        client.index(index='keepalive', id='1', body={'timestamp': datetime.now().isoformat()})
        print(f"✅ OpenSearch: OK")
    except Exception as e:
        print(f"❌ OpenSearch: {e}")

def keepalive_kafka():
    try:
        resp = requests.post(
            f"https://kafka-17dd3441-hauminhnguyen1182-7219.b.aivencloud.com:23278/topics/nghiencuuAI",
            auth=(os.environ.get('KAFKA_USER', 'avnadmin'), os.environ.get('KAFKA_PASS', '')),
            json={'records': [{'value': {'type': 'keepalive', 'timestamp': datetime.now().isoformat()}}]},
            headers={'Content-Type': 'application/vnd.kafka.json.v2+json'}
        )
        print(f"✅ Kafka: OK")
    except Exception as e:
        print(f"❌ Kafka: {e}")

if __name__ == "__main__":
    print(f"🔄 Keepalive: {datetime.now()}")
    keepalive_postgres()
    keepalive_opensearch()
    keepalive_kafka()