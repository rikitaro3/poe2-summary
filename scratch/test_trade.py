import urllib.request
import json
import urllib.parse
import sys

# apps/97_poe/config/.env から POESESSID を取得
import os
env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config", ".env")
session_id = None
if os.path.exists(env_path):
    with open(env_path, "r", encoding="utf-8") as f:
        for line in f:
            if "POESESSID" in line:
                session_id = line.strip().split("=", 1)[1].strip('"').strip("'")

query = {
    "query": {
        "status": {"option": "online"},
        "filters": {
            "type_filters": {
                "filters": {
                    "category": {
                        "option": "accessory.ring"
                    }
                }
            }
        },
        "stats": [
            {
                "type": "and",
                "filters": [
                    {"id": "explicit.stat_1573130764"}, # Adds Fire Damage to Attacks
                    {"id": "explicit.stat_4080418644"}, # Strength
                    {"id": "explicit.stat_3917489142"}  # Rarity
                ]
            },
            {
                "type": "count",
                "value": {
                    "min": 1
                },
                "filters": [
                    {"id": "explicit.stat_3032590688"}, # Adds Physical Damage to Attacks
                    {"id": "explicit.stat_4067062424"}, # Adds Cold Damage to Attacks
                    {"id": "explicit.stat_1754445556"}  # Adds Lightning Damage to Attacks
                ]
            }
        ]
    }
}

league = "Runes of Aldur" # "Runes of Aldur" is the current active league
encoded_league = urllib.parse.quote(league)
url = f"https://www.pathofexile.com/api/trade2/search/{encoded_league}"
print(f"URL: {url}")

headers = {
    "User-Agent": "PoE2TradeHelper/1.0 (Contact: user-local-script)",
    "Content-Type": "application/json"
}
if session_id:
    headers["Cookie"] = f"POESESSID={session_id}"

req = urllib.request.Request(
    url,
    data=json.dumps(query).encode("utf-8"),
    headers=headers,
    method="POST"
)

try:
    with urllib.request.urlopen(req) as response:
        print("Success!")
        print(response.read().decode("utf-8"))
except urllib.error.HTTPError as e:
    print(f"Error {e.code}: {e.read().decode('utf-8')}")
except Exception as e:
    print(f"Error: {e}")
