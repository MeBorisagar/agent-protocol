import redis
import json

r = redis.Redis(host="localhost", port=6379, decode_responses=True)

KEY = "capability_registry"


class CapabilityRegistry:

    def register(self, agent_name: str, url: str, capabilities: list):
        data = json.loads(r.get(KEY) or "{}")

        for cap in capabilities:
            data[cap["name"]] = url

        r.set(KEY, json.dumps(data))

    def resolve(self, action: str):
        data = json.loads(r.get(KEY) or "{}")
        return data.get(action)

    def all(self):
        return json.loads(r.get(KEY) or "{}")