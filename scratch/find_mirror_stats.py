import urllib.request
import json

url = "https://www.pathofexile.com/api/trade2/data/stats"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

req = urllib.request.Request(url, headers=headers)

search_keywords = ["mirror", "shard", "fracturing", "delirium"]

try:
    with urllib.request.urlopen(req) as response:
        data = json.loads(response.read().decode("utf-8"))
        
        results = []
        for group in data.get("result", []):
            group_label = group.get("label", "")
            for entry in group.get("entries", []):
                text = entry.get("text", "").lower()
                stat_id = entry.get("id", "")
                
                for kw in search_keywords:
                    if kw in text:
                        results.append({
                            "group": group_label,
                            "id": stat_id,
                            "text": entry.get("text")
                        })
                        break

        # 結果を表示する
        for r in results:
            if r["group"] in ["Explicit", "Implicit", "Pseudo"]:
                print(f"[{r['group']}] {r['id']} : {r['text']}")
except Exception as e:
    print(f"Error: {e}")
