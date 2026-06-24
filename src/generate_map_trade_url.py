import os
import sys
import json
import urllib.request
import urllib.parse
import urllib.error

def load_env_session():
    # apps/97_poe/config/.env から POESESSID を取得
    env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config", ".env")
    if os.path.exists(env_path):
        try:
            with open(env_path, "r", encoding="utf-8") as f:
                for line in f:
                    if line.strip() and not line.startswith("#"):
                        parts = line.strip().split("=", 1)
                        if len(parts) == 2 and parts[0].strip() == "POESESSID":
                            return parts[1].strip().strip('"').strip("'")
        except Exception:
            pass
    return None

def load_env_token():
    env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config", ".env")
    if os.path.exists(env_path):
        try:
            with open(env_path, "r", encoding="utf-8") as f:
                for line in f:
                    if line.strip() and not line.startswith("#"):
                        parts = line.strip().split("=", 1)
                        if len(parts) == 2 and parts[0].strip() == "POETOKEN":
                            return parts[1].strip().strip('"').strip("'")
        except Exception:
            pass
    return None

def main():
    if sys.stdout.encoding != 'utf-8':
        try:
            sys.stdout.reconfigure(encoding='utf-8')
        except AttributeError:
            pass

    session_id = os.environ.get("POESESSID") or load_env_session()
    poe_token = os.environ.get("POETOKEN") or load_env_token()

    # 8modの条件設定 (明示Mod数が合計8個以上)
    stat_affix_mods = "pseudo.pseudo_number_of_affix_mods"

    stats = [
        {
            "type": "and",
            "filters": [
                {"id": stat_affix_mods, "value": {"min": 8}}
            ]
        }
    ]

    query = {
        "query": {
            "status": {"option": "securable"}, # インスタントバイアウト(即時購入)のみ
            "type": "Waystone (Tier 15)",
            "stats": stats,
            "filters": {
                "trade_filters": {
                    "filters": {
                        "price": {"max": 30, "option": "exalted"} # max 30 Exalted
                    }
                }
            }
        }
    }








    league = "Runes of Aldur"
    encoded_league = urllib.parse.quote(league)
    url = f"https://www.pathofexile.com/api/trade2/search/{encoded_league}"

    headers = {
        "User-Agent": "PoE2TradeHelper/1.0 (Contact: user-local-script)",
        "Content-Type": "application/json"
    }
    if session_id:
        headers["Cookie"] = f"POESESSID={session_id}"
    elif poe_token:
        headers["Authorization"] = f"Bearer {poe_token}"

    req = urllib.request.Request(
        url,
        data=json.dumps(query).encode("utf-8"),
        headers=headers,
        method="POST"
    )

    try:
        with urllib.request.urlopen(req) as response:
            res_data = json.loads(response.read().decode("utf-8"))
            search_id = res_data.get("id")
            trade_url = f"https://www.pathofexile.com/trade2/search/{encoded_league}/{search_id}"
            
            print(f"\n[SUCCESS] T15 8modマップ検索用URLの生成に成功しました！")
            print(f"リーグ: {league}")
            print(f"条件: Tier 15 Rare Waystone ＋ Corrupted ＋ 8mod確定 ＋ 最大価格 30 Exalted")
            print(f"URL: {trade_url}\n")
            
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8")
        print(f"API Error (HTTP {e.code}): {error_body}", file=sys.stderr)
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)

if __name__ == "__main__":
    main()
