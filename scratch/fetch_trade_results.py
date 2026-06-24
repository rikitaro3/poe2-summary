import urllib.request
import json
import os
import sys

# apps/97_poe/config/.env から POESESSID を取得
env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config", ".env")
session_id = None
if os.path.exists(env_path):
    with open(env_path, "r", encoding="utf-8") as f:
        for line in f:
            if "POESESSID" in line:
                session_id = line.strip().split("=", 1)[1].strip('"').strip("'")

# テストするクエリ
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
                    {"id": "explicit.stat_1573130764", "value": {"min": 12}, "disabled": False}, # Adds Fire Damage to Attacks (Min 12)
                    {"id": "explicit.stat_3962278098", "value": {"min": 18}, "disabled": False}, # increased Fire Damage (Min 18%)
                    {"id": "explicit.stat_4080418644", "disabled": False}, # Strength
                    {"id": "explicit.stat_3917489142", "disabled": False}  # Rarity
                ]
            },
            {
                "type": "count",
                "value": {
                    "min": 1
                },
                "filters": [
                    {"id": "explicit.stat_3032590688", "disabled": False}, # Adds Physical Damage to Attacks
                    {"id": "explicit.stat_4067062424", "disabled": False}, # Adds Cold Damage to Attacks
                    {"id": "explicit.stat_1754445556", "disabled": False}  # Adds Lightning Damage to Attacks
                ]
            },
            {
                "type": "count",
                "value": {
                    "min": 1
                },
                "filters": [
                    {"id": "explicit.stat_3372524247", "disabled": False}, # Fire Resistance
                    {"id": "explicit.stat_4220027924", "disabled": False}, # Cold Resistance
                    {"id": "explicit.stat_1671376347", "disabled": False}, # Lightning Resistance
                    {"id": "explicit.stat_2923486259", "disabled": False}, # Chaos Resistance
                    {"id": "explicit.stat_2901986750", "disabled": False}  # all Elemental Resistances
                ]
            }
        ]
    }
}

league = "Runes of Aldur"
search_url = f"https://www.pathofexile.com/api/trade2/search/{urllib.parse.quote(league)}"
headers = {
    "User-Agent": "PoE2TradeHelper/1.0 (Contact: user-local-script)",
    "Content-Type": "application/json"
}
if session_id:
    headers["Cookie"] = f"POESESSID={session_id}"

# POSTリクエストで検索を実行
req_search = urllib.request.Request(
    search_url,
    data=json.dumps(query).encode("utf-8"),
    headers=headers,
    method="POST"
)
try:
    with urllib.request.urlopen(req_search) as response:
        search_res = json.loads(response.read().decode("utf-8"))
        search_id = search_res.get("id")
        result_hashes = search_res.get("result", [])
        total_count = search_res.get("total", 0)
        print(f"Total items found: {total_count}")
        print(f"Search ID: {search_id}")
except Exception as e:
    print(f"Error fetching search results: {e}")
    sys.exit(1)

if not result_hashes:
    print("No items found.")
    sys.exit(0)

# 2. 最初のリザルト（最大5個）の詳細データをフェッチ
fetch_hashes = result_hashes[:5]
fetch_url = f"https://www.pathofexile.com/api/trade2/fetch/{','.join(fetch_hashes)}?query={search_id}"

req_fetch = urllib.request.Request(fetch_url, headers=headers)
try:
    with urllib.request.urlopen(req_fetch) as response:
        fetch_res = json.loads(response.read().decode("utf-8"))
        items = fetch_res.get("result", [])
        
        parsed_items = []
        for item_data in items:
            item = item_data.get("item", {})
            listing = item_data.get("listing", {})
            
            # 価格情報の抽出
            price_info = listing.get("price", {})
            price_amount = price_info.get("amount", "N/A")
            price_currency = price_info.get("currency", "")
            
            name = item.get("name", "Rare Item")
            base_type = item.get("typeLine", "")
            ilvl = item.get("ilvl", 0)
            
            implicit_mods = item.get("implicitMods", [])
            explicit_mods = item.get("explicitMods", [])
            
            parsed_items.append({
                "name": name,
                "base_type": base_type,
                "ilvl": ilvl,
                "price": f"{price_amount} {price_currency}",
                "implicit": implicit_mods,
                "explicit": explicit_mods
            })
            
        # 結果をJSONで出力
        print(json.dumps(parsed_items, indent=2, ensure_ascii=False))
except Exception as e:
    print(f"Error fetching item details: {e}")
