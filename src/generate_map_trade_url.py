import os
import sys
import json
import time
from trade_client import TradeClient

def load_query_config():
    config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config", "trade_queries.json")
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)

def main():
    if sys.stdout.encoding != 'utf-8':
        try:
            sys.stdout.reconfigure(encoding='utf-8')
        except AttributeError:
            pass

    league = "Runes of Aldur"
    try:
        config = load_query_config()
        queries = config["static_queries"]
    except Exception as e:
        print(f"Failed to load config/query: {str(e)}", file=sys.stderr)
        sys.exit(1)

    print("Generating Waystone Trade URLs...")
    client = TradeClient(league=league)
    results = {}
    
    keys = [
        ("standard", "waystone_t15_8mod", "T15 8modマップ"),
        ("simulacrum", "waystone_simulacrum_iir50", "シミュラクラム用 (IIR 50%+) マップ")
    ]

    for key, config_key, label in keys:
        print(f"Generating {label} Trade URL...")
        try:
            url = client.send_request(queries[config_key])
            results[key] = url
        except Exception as e:
            print(f"Error generating {label} URL: {str(e)}", file=sys.stderr)
            results[key] = None
        time.sleep(1.5)

    print("\n==========================================")
    print("[SUCCESS] ウェイストーン用トレードURLの生成に成功しました！")
    print(f"リーグ: {league}")
    print("------------------------------------------")
    if results.get("standard"):
        print(f"👉 【通常】T15 ＋ Rare ＋ 8mod確定 ＋ 最大価格 30 Exalted")
        print(f"   URL: {results['standard']}")
    if results.get("simulacrum"):
        print(f"👉 【シミュラクラム用】T15 ＋ Rare ＋ Corrupted ＋ 8mod確定 ＋ IIR 50%+ ＋ 最大価格 30 Exalted")
        print(f"   URL: {results['simulacrum']}")
    print("==========================================\n")

if __name__ == "__main__":
    main()
