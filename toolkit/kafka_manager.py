import os
import json
import requests
import uuid
from pathlib import Path

env_path = Path("/workspace/.env")
if env_path.exists():
    for line in env_path.read_text().splitlines():
        if "=" in line and not line.startswith("#"):
            key, val = line.split("=", 1)
            os.environ[key.strip()] = val.strip()

KAFKA_REST_URL = "https://kafka-17dd3441-hauminhnguyen1182-7219.b.aivencloud.com:23278"
KAFKA_USER = "avnadmin"
KAFKA_PASS = os.environ.get("KAFKA_PASS", "")

class KafkaManager:
    def __init__(self):
        self.rest_url = KAFKA_REST_URL
        self.auth = (KAFKA_USER, KAFKA_PASS)

    def list_topics(self):
        resp = requests.get(f"{self.rest_url}/topics", auth=self.auth)
        return resp.json()

    def produce(self, topic, message, key=None):
        payload = {"records": [{"value": message}]}
        if key:
            payload["records"][0]["key"] = key

        resp = requests.post(
            f"{self.rest_url}/topics/{topic}",
            auth=self.auth,
            json=payload,
            headers={"Content-Type": "application/vnd.kafka.json.v2+json"}
        )
        if resp.status_code == 200:
            print(f"✅ Produced to {topic}")
            return True
        print(f"❌ Error: {resp.status_code}")
        return False

    def consume(self, topic, group_id="mimocode", max_messages=10):
        instance_id = f"inst-{uuid.uuid4().hex[:8]}"

        # Create consumer
        resp = requests.post(
            f"{self.rest_url}/consumers/{group_id}/instances/{instance_id}",
            auth=self.auth,
            json={"format": "json", "auto.offset.reset": "earliest"},
            headers={"Content-Type": "application/vnd.kafka.json.v2+json"}
        )
        if resp.status_code != 200:
            return []

        base_uri = resp.json().get("base_uri", "")

        # Subscribe
        requests.post(
            f"{base_uri}/subscription",
            auth=self.auth,
            json={"topics": [topic]},
            headers={"Content-Type": "application/vnd.kafka.json.v2+json"}
        )

        # Get records
        resp = requests.get(
            f"{base_uri}/records",
            auth=self.auth,
            params={"max_bytes": 102400},
            headers={"Accept": "application/vnd.kafka.json.v2+json"}
        )

        messages = resp.json()[:max_messages] if resp.status_code == 200 else []

        # Delete consumer
        requests.delete(f"{base_uri}", auth=self.auth)

        return messages

    def send_event(self, event_type, data):
        return self.produce("nghiencuuAI", {"type": event_type, "data": data})

if __name__ == "__main__":
    kafka = KafkaManager()
    print(f"✅ Kafka REST connected!")
    print(f"📋 Topics: {kafka.list_topics()}")