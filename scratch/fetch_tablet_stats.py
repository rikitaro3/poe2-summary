import urllib.request
import json
import re

url = "https://www.pathofexile.com/api/trade2/data/stats"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

req = urllib.request.Request(url, headers=headers)

try:
    with urllib.request.urlopen(req) as response:
        data = json.loads(response.read().decode("utf-8"))
        
        # すべてのModからDelirium, Precursor, Tablet, Mirror, Splinter, Uses などに関連するものを抽出
        results = []
        for group in data.get("result", []):
            group_label = group.get("label", "")
            for entry in group.get("entries", []):
                text = entry.get("text", "")
                stat_id = entry.get("id", "")
                
                # Pseudoグループをすべて抽出
                matched = (group_label == "Pseudo")
                
                if matched:
                    results.append({
                        "group": group_label,
                        "id": stat_id,
                        "text": text
                    })



                    
        print(json.dumps(results, indent=2, ensure_ascii=False))
except Exception as e:
    print(f"Error: {e}")
