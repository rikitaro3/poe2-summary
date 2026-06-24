import urllib.request
import json

url = "https://www.pathofexile.com/api/trade2/data/filters"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

req = urllib.request.Request(url, headers=headers)

try:
    with urllib.request.urlopen(req) as response:
        data = json.loads(response.read().decode("utf-8"))
        with open("scratch/filters_output.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print("Success: Wrote filters to scratch/filters_output.json")
except Exception as e:
    print(f"Error: {e}")

