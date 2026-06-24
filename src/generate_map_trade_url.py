import os
import sys
import json
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
        query = config["static_queries"]["waystone_t15_8mod"]
    except Exception as e:
        print(f"Failed to load config/query: {str(e)}", file=sys.stderr)
        sys.exit(1)

    print("Generating T15 8mod Map Trade URL...")
    client = TradeClient(league=league)
    try:
        trade_url = client.send_request(query)
        if trade_url:
            print(f"\n[SUCCESS] T15 8modマップ検索用URLの生成に成功しました！")
            print(f"リーグ: {league}")
            print(f"条件: Tier 15 Rare Waystone ＋ Corrupted ＋ 8mod確定 ＋ 最大価格 30 Exalted")
            print(f"URL: {trade_url}\n")
    except Exception as e:
        print(f"Error generating URL: {str(e)}", file=sys.stderr)

if __name__ == "__main__":
    main()
