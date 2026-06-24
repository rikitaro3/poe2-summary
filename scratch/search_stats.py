import urllib.request
import json

url = "https://www.pathofexile.com/api/trade2/data/stats"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

req = urllib.request.Request(url, headers=headers)

search_keywords = ["strength", "rarity", "fire damage", "cold damage", "lightning damage", "physical damage", "resistance"]

try:
    with urllib.request.urlopen(req) as response:
        data = json.loads(response.read().decode("utf-8"))
        
        results = []
        for group in data.get("result", []):
            group_label = group.get("label", "")
            for entry in group.get("entries", []):
                text = entry.get("text", "").lower()
                stat_id = entry.get("id", "")
                
                # キーワードがマッチするかチェック
                for kw in search_keywords:
                    if kw in text:
                        results.append({
                            "group": group_label,
                            "id": stat_id,
                            "text": entry.get("text")
                        })
                        break

        # 結果をファイルに書き出す
        with open("scratch/search_stats_output.json", "w", encoding="utf-8") as out_f:
            json.dump(results, out_f, indent=2, ensure_ascii=False)
        print("Success: results written to scratch/search_stats_output.json")
except Exception as e:
    print(f"Error: {e}")
