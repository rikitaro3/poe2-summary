import os
import sys
import json
import argparse
from trade_client import TradeClient

def load_query_config():
    config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config", "trade_queries.json")
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)

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

    # セッションIDとトークンの解決
    session_id = args.session
    poe_token = os.environ.get("POETOKEN")

    # PoE2 Mod IDのマッピング定義（外部JSONからロード）
    try:
        config = load_query_config()
        mod_map = config["mod_map"]
    except Exception as e:
        print(f"Failed to load config (mod_map): {str(e)}", file=sys.stderr)
        sys.exit(1)

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
            query["query"]["type"] = args.type

    trade_filters = {}
    if args.max_price > 0:
        trade_filters["price"] = {"max": args.max_price, "option": args.currency}

    if trade_filters:
        query["query"].setdefault("filters", {})["trade_filters"] = {
            "filters": trade_filters
        }

    # TradeClientを使用したリクエスト送信
    client = TradeClient(league=args.league, session_id=session_id, poe_token=poe_token)
    try:
        trade_url = client.send_request(query)
        print(f"\n\033[92m[SUCCESS] PoE2トレードURLの生成に成功しました：\033[0m")
        print(f"\033[96m{trade_url}\033[0m\n")
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)

if __name__ == "__main__":
    main()
