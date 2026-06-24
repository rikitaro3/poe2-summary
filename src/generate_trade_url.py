import os
import sys
import json
import urllib.request
import urllib.parse
import urllib.error
import argparse
import time

def load_env_session():
    # 1階層上の config/.env を見るように修正
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

def check_rate_limits(limit_hdr, state_hdr):
    try:
        limits = limit_hdr.split(",")
        states = state_hdr.split(",")
        for limit, state in zip(limits, states):
            l_parts = limit.split(":")
            s_parts = state.split(":")
            if len(l_parts) == 3 and len(s_parts) == 3:
                max_req = int(l_parts[0])
                time_window = int(l_parts[1])
                cur_req = int(s_parts[0])
                penalty = int(s_parts[2])
                
                if penalty > 0:
                    print(f"⚠️ Rate limit cooldown active: sleeping for {penalty} seconds.", file=sys.stderr)
                    time.sleep(penalty + 1)
                elif cur_req >= max_req * 0.8:
                    sleep_time = max(1, int(time_window * 0.5))
                    print(f"⚠️ Rate limit warning ({cur_req}/{max_req} used for {time_window}s window). Safe-sleeping for {sleep_time} seconds...", file=sys.stderr)
                    time.sleep(sleep_time)
    except Exception:
        pass

def send_request_with_retry(req, max_retries=3):
    for attempt in range(max_retries):
        try:
            with urllib.request.urlopen(req) as response:
                limit_hdr = response.headers.get("X-Rate-Limit-Ip")
                state_hdr = response.headers.get("X-Rate-Limit-Ip-State")
                if limit_hdr and state_hdr:
                    check_rate_limits(limit_hdr, state_hdr)
                return json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            if e.code == 429:
                retry_after = e.headers.get("Retry-After")
                wait_time = int(retry_after) if retry_after else 10
                state_hdr = e.headers.get("X-Rate-Limit-Ip-State")
                if state_hdr:
                    penalty_times = []
                    for state in state_hdr.split(","):
                        parts = state.split(":")
                        if len(parts) == 3:
                            penalty_times.append(int(parts[2]))
                    max_penalty = max(penalty_times) if penalty_times else 0
                    if max_penalty > 0:
                        wait_time = max(wait_time, max_penalty)
                
                print(f"⚠️ Rate limit hit (HTTP 429). Waiting for {wait_time} seconds before retry (Attempt {attempt+1}/{max_retries})...", file=sys.stderr)
                time.sleep(wait_time + 1)
                continue
            else:
                raise e
    raise RuntimeError("Max retries exceeded due to rate limit (HTTP 429)")

def main():
    # Windowsターミナルでのエンコードエラー・文字化けを防ぐために標準出力をUTF-8に強制再設定
    if sys.stdout.encoding != 'utf-8':
        try:
            sys.stdout.reconfigure(encoding='utf-8')
        except AttributeError:
            pass
            
    parser = argparse.ArgumentParser(description="PoE2 Trade URL Generator")
    parser.add_argument("--type", default=None, help="Item type (e.g. Ring, Amulet, Helmet, Body Armour, Boots, Gloves, Belt, Shield)")
    parser.add_argument("--life", type=int, default=0, help="Minimum Life")
    parser.add_argument("--res", type=int, default=0, help="Minimum Total Resistance")
    parser.add_argument("--res-fire", type=int, default=0, help="Minimum Fire Resistance")
    parser.add_argument("--res-cold", type=int, default=0, help="Minimum Cold Resistance")
    parser.add_argument("--res-lightning", type=int, default=0, help="Minimum Lightning Resistance")
    parser.add_argument("--res-chaos", type=int, default=0, help="Minimum Chaos Resistance")
    parser.add_argument("--speed", type=int, default=0, help="Minimum Movement Speed %%")
    parser.add_argument("--atk-speed", type=int, default=0, help="Minimum Attack Speed %%")
    parser.add_argument("--spell-dmg", type=int, default=0, help="Minimum Spell Damage %%")
    parser.add_argument("--phys", action="store_true", help="Include Physical Damage to Attacks (weight)")
    parser.add_argument("--cold", action="store_true", help="Include Cold Damage to Attacks (weight)")
    parser.add_argument("--fire", action="store_true", help="Include Fire Damage to Attacks (weight)")
    parser.add_argument("--lightning", action="store_true", help="Include Lightning Damage to Attacks (weight)")
    parser.add_argument("--cast", action="store_true", help="Include Cast Speed (weight)")
    parser.add_argument("--fire-spell", action="store_true", help="Include Fire Damage to Spells (weight)")
    parser.add_argument("--cold-spell", action="store_true", help="Include Cold Damage to Spells (weight)")
    parser.add_argument("--lightning-spell", action="store_true", help="Include Lightning Damage to Spells (weight)")
    parser.add_argument("--league", default="Runes of Aldur", help="League name")
    parser.add_argument("--session", default=None, help="POESESSID session cookie")
    parser.add_argument("--max-price", type=int, default=0, help="Maximum price")
    parser.add_argument("--currency", default="chaos", choices=["chaos", "exalted"], help="Currency type for max price (default: chaos)")
    parser.add_argument("--any-status", action="store_true", help="Search offline players too (default: online only)")
    parser.add_argument("--all-sales", action="store_true", help="Search all sale types including non-instant buyout")
    parser.add_argument("--custom-ring", action="store_true", help="Generate custom ring query for fire + flat + rarity + strength")
    
    args = parser.parse_args()

    # 購入方式・オンラインステータスの決定 (PoE2ではsecurableで即時購入制限)
    status_option = "securable" # デフォルトは即時購入のみ
    if args.all_sales:
        status_option = "online" # すべてのオンライン出品
    elif args.any_status:
        status_option = "any" # オフライン含む

    # セッションIDの解決 (引数 -> 環境変数 -> .envファイル)
    session_id = args.session
    if not session_id:
        session_id = os.environ.get("POESESSID")
    if not session_id:
        session_id = load_env_session()
    poe_token = os.environ.get("POETOKEN") or load_env_token()

    # PoE2 Mod IDのマッピング定義
    mod_map = {
        "pseudo_life": "pseudo.pseudo_total_life",
        "pseudo_res": "pseudo.pseudo_total_resistance",
        "pseudo_fire": "pseudo.pseudo_total_fire_resistance",
        "pseudo_cold": "pseudo.pseudo_total_cold_resistance",
        "pseudo_lightning": "pseudo.pseudo_total_lightning_resistance",
        "pseudo_chaos": "pseudo.pseudo_total_chaos_resistance",
        "movement_speed": "explicit.stat_2100679358",
        "attack_speed": "explicit.stat_210067635",
        "spell_damage": "explicit.stat_1241851921",
        "flat_phys": "explicit.stat_1940865751",
        "flat_cold": "explicit.stat_1037193709",
        "flat_phys_attacks": "pseudo.pseudo_adds_physical_damage_to_attacks",
        "flat_cold_attacks": "pseudo.pseudo_adds_cold_damage_to_attacks",
        "flat_fire_attacks": "pseudo.pseudo_adds_fire_damage_to_attacks",
        "flat_lightning_attacks": "pseudo.pseudo_adds_lightning_damage_to_attacks",
        "cast_speed": "explicit.stat_2624005898",
        "flat_fire_spells": "explicit.stat_131165481",
        "flat_cold_spells": "explicit.stat_322861266",
        "flat_lightning_spells": "explicit.stat_2041285220"
    }

    # クエリ条件の構築 (ANDフィルター)
    and_filters = []
    if args.life > 0:
        and_filters.append({"id": mod_map["pseudo_life"], "value": {"min": args.life}})
    if args.res > 0:
        and_filters.append({"id": mod_map["pseudo_res"], "value": {"min": args.res}})
    if args.res_fire > 0:
        and_filters.append({"id": mod_map["pseudo_fire"], "value": {"min": args.res_fire}})
    if args.res_cold > 0:
        and_filters.append({"id": mod_map["pseudo_cold"], "value": {"min": args.res_cold}})
    if args.res_lightning > 0:
        and_filters.append({"id": mod_map["pseudo_lightning"], "value": {"min": args.res_lightning}})
    if args.res_chaos > 0:
        and_filters.append({"id": mod_map["pseudo_chaos"], "value": {"min": args.res_chaos}})
    if args.speed > 0:
        and_filters.append({"id": mod_map["movement_speed"], "value": {"min": args.speed}})
    if args.atk_speed > 0:
        and_filters.append({"id": mod_map["attack_speed"], "value": {"min": args.atk_speed}})
    if args.spell_dmg > 0:
        and_filters.append({"id": mod_map["spell_damage"], "value": {"min": args.spell_dmg}})

    # 加点条件の構築 (Weightフィルター)
    weight_filters = []
    if args.phys:
        weight_filters.append({"id": mod_map["flat_phys"], "value": {"weight": 1.0}})
    if args.cold:
        weight_filters.append({"id": mod_map["flat_cold"], "value": {"weight": 1.0}})
    if args.fire:
        pass # Fireの確実なIDが現在不明なため一時的に除外
    if args.lightning:
        pass # Lightningも同様
    if args.cast:
        weight_filters.append({"id": mod_map["cast_speed"], "value": {"weight": 1.5}})
    if args.fire_spell:
        weight_filters.append({"id": mod_map["flat_fire_spells"], "value": {"weight": 1.0}})
    if args.cold_spell:
        weight_filters.append({"id": mod_map["flat_cold_spells"], "value": {"weight": 1.0}})
    if args.lightning_spell:
        weight_filters.append({"id": mod_map["flat_lightning_spells"], "value": {"weight": 1.0}})

    stats = []
    if and_filters:
        stats.append({"type": "and", "filters": and_filters})
    if weight_filters:
        stats.append({"type": "weight", "value": {"min": 1}, "filters": weight_filters})

    if args.custom_ring:
        query = {
            "query": {
                "status": {"option": status_option},
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
                            {"id": "explicit.stat_1573130764", "value": {"min": 12}, "disabled": False},
                            {"id": "explicit.stat_3962278098", "value": {"min": 18}, "disabled": False}, # increased Fire Damage
                            {"id": "explicit.stat_4080418644", "disabled": False},
                            {"id": "explicit.stat_3917489142", "disabled": False}
                        ]
                    },
                    {
                        "type": "count",
                        "value": {
                            "min": 1
                        },
                        "filters": [
                            {"id": "explicit.stat_3032590688", "disabled": False},
                            {"id": "explicit.stat_4067062424", "disabled": False},
                            {"id": "explicit.stat_1754445556", "disabled": False}
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
    else:
        query = {
            "query": {
                "status": {"option": status_option},
                "stats": stats
            }
        }
    if args.type:
        # カテゴリフィルター用のマッピング
        category_map = {
            "ring": "accessory.ring",
            "amulet": "accessory.amulet",
            "belt": "accessory.belt",
            "helmet": "armour.helmet",
            "body armour": "armour.chest",
            "chest": "armour.chest",
            "boots": "armour.boots",
            "gloves": "armour.gloves",
            "shield": "armour.shield",
            "weapon": "weapon",
            "spear": "weapon.spear"
        }
        cat_key = args.type.lower()
        if cat_key in category_map:
            query["query"].setdefault("filters", {}).setdefault("type_filters", {}).setdefault("filters", {})["category"] = {"option": category_map[cat_key]}
        else:
            # マッピングにない場合は従来のtype検索（特定のベース名などを検索する場合）
            query["query"]["type"] = args.type

    # 追加の取引フィルター（価格上限）
    trade_filters = {}
    if args.max_price > 0:
        trade_filters["price"] = {"max": args.max_price, "option": args.currency}

    if trade_filters:
        query["query"].setdefault("filters", {})["trade_filters"] = {
            "filters": trade_filters
        }

    # リーグ名のスペース等をURLエンコード
    encoded_league = urllib.parse.quote(args.league)
    
    # APIリクエストの送信
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
        res_data = send_request_with_retry(req)
        search_id = res_data.get("id")
        trade_url = f"https://www.pathofexile.com/trade2/search/{encoded_league}/{search_id}"
        
        print(f"\n\033[92m[SUCCESS] PoE2トレードURL of 生成に成功しました：\033[0m")
        print(f"\033[96m{trade_url}\033[0m\n")
            
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8")
        try:
            error_json = json.loads(error_body)
            print(f"Error: {error_json['error']['message']}", file=sys.stderr)
        except Exception:
            print(f"Error: {e.reason} ({error_body})", file=sys.stderr)
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)

if __name__ == "__main__":
    main()
