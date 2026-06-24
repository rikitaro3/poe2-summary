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
        print(f"Failed to load config: {str(e)}", file=sys.stderr)
        sys.exit(1)

    client = TradeClient(league=league)
    results = {}

    keys = [
        ("low", "tablet_low_investment", "低投資"),
        ("med", "tablet_medium_investment", "中投資"),
        ("high", "tablet_high_investment", "高投資"),
        ("unid", "tablet_crafting", "クラフト用")
    ]

    for key, config_key, label in keys:
        print(f"Generating {label} Trade URL...")
        try:
            url = client.send_request(queries[config_key])
            results[key] = url
        except Exception as e:
            print(f"Error generating {label} URL: {str(e)}", file=sys.stderr)
            results[key] = None
        time.sleep(1.5)  # レートリミットに配慮したインターバル

    print("\n==========================================")
    print("[SUCCESS] 投資レベル別Delirium石板用トレードURLの生成に成功しました！")
    print(f"リーグ: {league}")
    print("------------------------------------------")
    if results.get("low"):
        print(f"👉 【低投資】新品(10回) ＋ スプリンター24%+ ＋ [Effectiveness/MonsterRarity/RareMonsters]から1つ以上")
        print(f"   URL: {results['low']}")
    if results.get("med"):
        print(f"👉 【中投資】新品(10回) ＋ 鏡の破片Modあり(値指定なし) ＋ ボス出現Modあり(値指定なし) ＋ [Effectiveness/MonsterRarity/RareMonsters]から1つ以上")
        print(f"   URL: {results['med']}")
    if results.get("high"):
        print(f"👉 【高投資】新品(10回) ＋ 鏡の破片Modあり(値指定なし) ＋ スプリンター24%+ ＋ [Effectiveness/MonsterRarity/RareMonsters]から1つ以上")
        print(f"   URL: {results['high']}")
    if results.get("unid"):
        print(f"👉 【クラフト用】新品(10回) ＋ マジック未鑑定 Delirium Tablet")
        print(f"   URL: {results['unid']}")
    print("==========================================\n")

if __name__ == "__main__":
    main()
