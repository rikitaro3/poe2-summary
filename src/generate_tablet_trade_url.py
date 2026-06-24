import os
import sys
import json
import urllib.request
import urllib.parse
import urllib.error
import time

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

def fetch_trade_url(league, query, session_id):
    encoded_league = urllib.parse.quote(league)
    url = f"https://www.pathofexile.com/api/trade2/search/{encoded_league}"

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
            res_data = json.loads(response.read().decode("utf-8"))
            search_id = res_data.get("id")
            return f"https://www.pathofexile.com/trade2/search/{encoded_league}/{search_id}"
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8")
        print(f"API Error (HTTP {e.code}): {error_body}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        return None

def main():
    # ターミナルのエンコード設定
    if sys.stdout.encoding != 'utf-8':
        try:
            sys.stdout.reconfigure(encoding='utf-8')
        except AttributeError:
            pass

    session_id = os.environ.get("POESESSID") or load_env_session()
    
    # Suffixes
    stat_remaining_uses = "pseudo.pseudo_number_of_uses_remaining"
    stat_fracturing_mirrors = "explicit.stat_551040294"   # Delirium Fog in Map spawns #% increased Fracturing Mirrors
    stat_mirror_shards = "explicit.stat_900933517"         # Delirium Fog in Map spawns #% increased MirrorShards
    stat_splinters = "explicit.stat_3836551197"           # #% increased Stack size of Simulacrum Splinters found in Map
    stat_unique_bosses = "explicit.stat_3962960008"        # Delirium Encounters in Map are #% more likely to spawn Unique Bosses

    # Prefixes (User Requested)
    stat_rare_monsters_count = "explicit.stat_3793155082"  # Map has #% increased number of Rare Monsters
    stat_monsters_effectiveness = "explicit.stat_2065500219" # Monsters have #% increased Effectiveness
    stat_monster_rarity = "explicit.stat_4142653832"        # Map has #% increased Monster Rarity

    league = "Runes of Aldur"

    # 共通Prefixグループ (3つのうち1つ以上)
    prefix_count_group = {
        "type": "count",
        "value": {"min": 1},
        "filters": [
            {"id": stat_rare_monsters_count, "value": {"min": 25}},
            {"id": stat_monsters_effectiveness, "value": {"min": 10}},
            {"id": stat_monster_rarity, "value": {"min": 15}}
        ]
    }

    # 1. 低投資: スプリンター24%アップ ＋ Prefixから1つ以上
    query_low = {
        "query": {
            "status": {"option": "securable"},
            "stats": [
                {
                    "type": "and",
                    "filters": [
                        {"id": stat_remaining_uses, "value": {"min": 10}},
                        {"id": stat_splinters, "value": {"min": 24}}
                    ]
                },
                prefix_count_group
            ]
        }
    }

    # 2. 中投資: 鏡の破片 ＋ ボスドロップ ＋ Prefixから1つ以上
    query_med = {
        "query": {
            "status": {"option": "securable"},
            "stats": [
                {
                    "type": "and",
                    "filters": [
                        {"id": stat_remaining_uses, "value": {"min": 10}},
                        {"id": stat_mirror_shards, "value": {"min": 5}},
                        {"id": stat_unique_bosses, "value": {"min": 5}}
                    ]
                },
                prefix_count_group
            ]
        }
    }

    # 3. 高投資: 割れた鏡 ＋ スプリンター ＋ Prefixから1つ以上
    query_high = {
        "query": {
            "status": {"option": "securable"},
            "stats": [
                {
                    "type": "and",
                    "filters": [
                        {"id": stat_remaining_uses, "value": {"min": 10}},
                        {"id": stat_fracturing_mirrors, "value": {"min": 5}},
                        {"id": stat_splinters, "value": {"min": 15}}
                    ]
                },
                prefix_count_group
            ]
        }
    }

    # 4. クラフト用: マジック未鑑定 ＋ 新品
    query_unid = {
        "query": {
            "status": {"option": "securable"},
            "type": "Delirium Tablet",
            "stats": [
                {
                    "type": "and",
                    "filters": [
                        {"id": stat_remaining_uses, "value": {"min": 10}}
                    ]
                }
            ],
            "filters": {
                "misc_filters": {
                    "filters": {
                        "identified": {"option": "false"},
                        "rarity": {"option": "magic"}
                    }
                }
            }
        }
    }

    print("Generating Low-investment Trade URL...")
    url_low = fetch_trade_url(league, query_low, session_id)
    
    time.sleep(1.5)  # レートリミット回避

    print("Generating Medium-investment Trade URL...")
    url_med = fetch_trade_url(league, query_med, session_id)
    
    time.sleep(1.5)  # レートリミット回避

    print("Generating High-investment Trade URL...")
    url_high = fetch_trade_url(league, query_high, session_id)

    time.sleep(1.5)  # レートリミット回避

    print("Generating Unidentified Magic Trade URL...")
    url_unid = fetch_trade_url(league, query_unid, session_id)

    print("\n==========================================")
    print("[SUCCESS] 投資レベル別Delirium石板用トレードURLの生成に成功しました！")
    print(f"リーグ: {league}")
    print("------------------------------------------")
    if url_low:
        print(f"👉 【低投資】新品(10回) ＋ スプリンター24%+ ＋ [Effectiveness/MonsterRarity/RareMonsters]から1つ以上")
        print(f"   URL: {url_low}")
    if url_med:
        print(f"👉 【中投資】新品(10回) ＋ 鏡の破片5%+ ＋ ボス出現5%+ ＋ [Effectiveness/MonsterRarity/RareMonsters]から1つ以上")
        print(f"   URL: {url_med}")
    if url_high:
        print(f"👉 【高投資】新品(10回) ＋ 分裂ミラー5%+ ＋ スプリンター15%+ ＋ [Effectiveness/MonsterRarity/RareMonsters]から1つ以上")
        print(f"   URL: {url_high}")
    if url_unid:
        print(f"👉 【クラフト用】新品(10回) ＋ マジック未鑑定 Delirium Tablet")
        print(f"   URL: {url_unid}")
    print("==========================================\n")


if __name__ == "__main__":
    main()
