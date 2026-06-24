import os
import sys
import json
import re
import base64
import zlib
import xml.etree.ElementTree as ET
import urllib.request
import urllib.parse
import urllib.error
import argparse

def load_env_session():
    # Relative path to config/.env
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

def parse_mods_for_stats(item):
    """
    アイテムのModからライフや耐性の数値を抽出する簡易パース処理
    """
    life = 0
    fire_res = 0
    cold_res = 0
    lightning_res = 0
    chaos_res = 0
    
    # 解析対象のModリスト
    mods = item.get("implicitMods", []) + item.get("explicitMods", [])
    if not mods:
        mods = item.get("implicit_mods", []) + item.get("explicit_mods", [])
        
    for mod in mods:
        # Lifeの抽出
        life_match = re.search(r'\+(\d+) to maximum Life', mod)
        if life_match:
            life += int(life_match.group(1))
            
        # 単一耐性の抽出
        fire_match = re.search(r'\+(\d+)% to Fire Resistance', mod)
        if fire_match:
            fire_res += int(fire_match.group(1))
            
        cold_match = re.search(r'\+(\d+)% to Cold Resistance', mod)
        if cold_match:
            cold_res += int(cold_match.group(1))
            
        lightning_match = re.search(r'\+(\d+)% to Lightning Resistance', mod)
        if lightning_match:
            lightning_res += int(lightning_match.group(1))
            
        chaos_match = re.search(r'\+(\d+)% to Chaos Resistance', mod)
        if chaos_match:
            chaos_res += int(chaos_match.group(1))
            
        # 全耐性の抽出 (+X% to all Elemental Resistances)
        all_res_match = re.search(r'\+(\d+)% to all Elemental Resistances', mod)
        if all_res_match:
            val = int(all_res_match.group(1))
            fire_res += val
            cold_res += val
            lightning_res += val
            
        # 二属性耐性の抽出 (+X% to Cold and Lightning / Fire and Cold / Fire and Lightning)
        double_res_match = re.search(r'\+(\d+)% to (Fire|Cold|Lightning) and (Fire|Cold|Lightning) Resistances', mod)
        if double_res_match:
            val = int(double_res_match.group(1))
            r1 = double_res_match.group(2)
            r2 = double_res_match.group(3)
            for r in [r1, r2]:
                if r == "Fire": fire_res += val
                elif r == "Cold": cold_res += val
                elif r == "Lightning": lightning_res += val

    return {
        "life": life,
        "fire_res": fire_res,
        "cold_res": cold_res,
        "lightning_res": lightning_res,
        "chaos_res": chaos_res,
        "total_ele_res": fire_res + cold_res + lightning_res
    }

def parse_raw_item_text(text, slot_name):
    """
    ゲーム内 Ctrl+C または PoB 内の生のアイテムテキストをパースする
    """
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    if not lines:
        return None
        
    rarity = "Normal"
    item_name = ""
    base_type = ""
    implicit_mods = []
    explicit_mods = []
    
    # Rarity の判定
    if lines[0].startswith("Rarity:"):
        rarity = lines[0].split(":", 1)[1].strip()
        lines = lines[1:]
        
    # アイテム名のパース
    if rarity in ["Rare", "Unique"]:
        if len(lines) >= 2:
            item_name = lines[0]
            base_type = lines[1]
            lines = lines[2:]
    else:
        if len(lines) >= 1:
            item_name = lines[0]
            base_type = lines[0]
            lines = lines[1:]
            
    # モッドの抽出
    in_requirements = False
    for line in lines:
        if line.startswith("--------"):
            in_requirements = False
            continue
        if line.startswith("Requirements:") or line.startswith("Level:") or line.startswith("Item Level:"):
            in_requirements = True
            continue
        if in_requirements:
            continue
            
        # 不要な情報はスキップ
        if line.startswith("Sockets:") or line.startswith("Quality:") or line.startswith("Quality:"):
            continue
            
        is_implicit = "{implicit}" in line or "(implicit)" in line
        cleaned_line = line.replace("{implicit}", "").replace("{explicit}", "").strip()
        
        if is_implicit:
            implicit_mods.append(cleaned_line)
        else:
            # 簡易的に、数値や耐性、ライフを含む行をModとして扱う
            explicit_mods.append(cleaned_line)
            
    # パースされたModからライフ・耐性を抽出
    item_obj = {
        "implicitMods": implicit_mods,
        "explicitMods": explicit_mods
    }
    parsed_stats = parse_mods_for_stats(item_obj)
    
    return {
        "slot_name": slot_name,
        "item_name": f"{item_name} {base_type}".strip() if rarity in ["Rare", "Unique"] else item_name,
        "base_type": base_type,
        "rarity": rarity,
        "implicit_mods": implicit_mods,
        "explicit_mods": explicit_mods,
        "parsed_stats": parsed_stats
    }

def import_from_pob_url(pob_url):
    """
    pobb.inの共有URLからXMLデータをダウンロードし、装備データをデコード・パースする
    """
    raw_url = pob_url.strip()
    if not raw_url.endswith("/raw"):
        raw_url = raw_url.rstrip("/") + "/raw"
        
    print(f"Fetching PoB XML from: {raw_url}...")
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    req = urllib.request.Request(raw_url, headers=headers, method="GET")
    try:
        with urllib.request.urlopen(req) as response:
            pob_code = response.read().decode("utf-8").strip()
            
        cleaned_code = pob_code.replace('-', '+').replace('_', '/')
        missing_padding = len(cleaned_code) % 4
        if missing_padding:
            cleaned_code += '=' * (4 - missing_padding)
            
        compressed_data = base64.b64decode(cleaned_code)
        xml_text = zlib.decompress(compressed_data).decode('utf-8')
        
        root = ET.fromstring(xml_text)
        items_element = root.find("Items")
        if items_element is None:
            print("Error: No Items section in PoB XML.", file=sys.stderr)
            return None
            
        slots = {}
        for slot in items_element.findall("Slot"):
            name = slot.get("name")
            item_id = slot.get("itemId")
            if name and item_id:
                slots[item_id] = name
                
        # PoE2で使われる装備スロットIDの統一マッピング
        valid_slots = {
            "Helmet": "Helm",
            "Body Armour": "Chest",
            "Gloves": "Gloves",
            "Boots": "Boots",
            "Ring 1": "Ring1",
            "Ring 2": "Ring2",
            "Amulet": "Amulet",
            "Belt": "Belt",
            "Weapon 1": "Weapon",
            "Weapon 2": "Offhand"
        }
        
        gear_data = {}
        for item in items_element.findall("Item"):
            item_id = item.get("id")
            if item_id in slots:
                slot_name = slots[item_id]
                if slot_name in valid_slots:
                    poe_slot = valid_slots[slot_name]
                    raw_text = item.text.strip() if item.text else ""
                    parsed_item = parse_raw_item_text(raw_text, slot_name)
                    if parsed_item:
                        gear_data[poe_slot] = parsed_item
                        
        return gear_data
    except Exception as e:
        print(f"Error fetching/parsing pobb.in build: {str(e)}", file=sys.stderr)
        return None

def fetch_from_poe_api(account, character, realm, session_id):
    """
    PoE公式APIから現在装備JSONデータを取得
    """
    # GETパラメータのクエリを構築
    params = urllib.parse.urlencode({
        "accountName": account,
        "character": character,
        "realm": realm
    })
    url = f"https://www.pathofexile.com/character-window/get-items?{params}"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    if session_id:
        headers["Cookie"] = f"POESESSID={session_id}"

    req = urllib.request.Request(url, headers=headers, method="GET")

    print(f"Connecting to PoE API: {url}...")
    try:
        with urllib.request.urlopen(req) as response:
            raw_body = response.read().decode("utf-8")
            try:
                res_data = json.loads(raw_body)
                return res_data
            except json.JSONDecodeError as je:
                print(f"Error parsing JSON: {str(je)}", file=sys.stderr)
                print("Raw response preview (Could be Login/Forbidden page HTML):", file=sys.stderr)
                print(raw_body[:1000], file=sys.stderr)
                return None
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8")
        print(f"HTTP Error {e.code}: {e.reason}", file=sys.stderr)
        print("💡 Hint: If your account is private, ensure your POESESSID is correctly set in config/.env", file=sys.stderr)
        return None
    except Exception as e:
        print(f"Error calling API: {str(e)}", file=sys.stderr)
        return None

def main():
    if sys.stdout.encoding != 'utf-8':
        try:
            sys.stdout.reconfigure(encoding='utf-8')
        except AttributeError:
            pass

    parser = argparse.ArgumentParser(description="PoE2 Character Gear Downloader")
    parser.add_argument("account_or_url", help="PoE Account Name OR pobb.in URL (e.g. https://pobb.in/xxxxx)")
    parser.add_argument("character", nargs="?", default=None, help="PoE2 Character Name (Optional if using pobb.in URL)")
    parser.add_argument("--session", default=None, help="POESESSID session cookie")
    parser.add_argument("--realm", default="poe2", help="Realm of the character (e.g. pc, poe2)")
    parser.add_argument("--analyze", action="store_true", help="Analyze gear and output recommendations")
    args = parser.parse_args()

    session_id = args.session or os.environ.get("POESESSID") or load_env_session()
    
    gear_data = {}
    
    # 入力値が pobb.in のURLかどうか判定
    if args.account_or_url.startswith("https://pobb.in/"):
        print("Detected pobb.in URL. Starting PoB XML import...")
        imported_gear = import_from_pob_url(args.account_or_url)
        if imported_gear:
            gear_data = imported_gear
            print(f"Successfully imported {len(gear_data)} slots from pobb.in!")
        else:
            print("Failed to import from pobb.in.", file=sys.stderr)
            return
    else:
        # 通常の公式API経由
        if not args.character:
            print("Error: Character name is required when using PoE Account Name.", file=sys.stderr)
            return
            
        res_data = fetch_from_poe_api(args.account_or_url, args.character, args.realm, session_id)
        if not res_data or "items" not in res_data:
            print("Failed to retrieve items from official API.", file=sys.stderr)
            return
            
        items = res_data["items"]
        valid_slots = {
            "Helm": "Helmet",
            "Chest": "Body Armour",
            "Gloves": "Gloves",
            "Boots": "Boots",
            "Ring1": "Ring (Left)",
            "Ring2": "Ring (Right)",
            "Amulet": "Amulet",
            "Belt": "Belt",
            "Weapon": "Weapon 1",
            "Offhand": "Weapon 2 / Offhand"
        }
        
        for item in items:
            slot_id = item.get("inventoryId")
            if slot_id in valid_slots:
                name = item.get("name", "").strip()
                type_line = item.get("typeLine", "").strip()
                full_name = f"{name} {type_line}".strip()
                implicit_mods = item.get("implicitMods", [])
                explicit_mods = item.get("explicitMods", [])
                parsed_stats = parse_mods_for_stats(item)
                
                gear_data[slot_id] = {
                    "slot_name": valid_slots[slot_id],
                    "item_name": full_name,
                    "base_type": type_line,
                    "rarity": "Unique" if item.get("frameType") == 3 else "Rare" if item.get("frameType") == 2 else "Magic" if item.get("frameType") == 1 else "Normal",
                    "implicit_mods": implicit_mods,
                    "explicit_mods": explicit_mods,
                    "parsed_stats": parsed_stats
                }

    if not gear_data:
        print("No gear data found to process.", file=sys.stderr)
        return

    # 全身の合計値を計算
    total_stats = {"life": 0, "fire_res": 0, "cold_res": 0, "lightning_res": 0, "chaos_res": 0}
    for slot_id, item in gear_data.items():
        st = item["parsed_stats"]
        total_stats["life"] += st["life"]
        total_stats["fire_res"] += st["fire_res"]
        total_stats["cold_res"] += st["cold_res"]
        total_stats["lightning_res"] += st["lightning_res"]
        total_stats["chaos_res"] += st["chaos_res"]

    # 新しいフォルダ構成に対応した出力パス (apps/97_poe/output/ 配下)
    output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "output")
    os.makedirs(output_dir, exist_ok=True)
    
    output_json_path = os.path.join(output_dir, "current_gear.json")
    with open(output_json_path, "w", encoding="utf-8") as f:
        json.dump({
            "source": args.account_or_url,
            "character": args.character or "pobb.in_imported",
            "gear": gear_data,
            "total_gear_stats": total_stats
        }, f, indent=2, ensure_ascii=False)
    print(f"Saved raw gear data to: {output_json_path}")

    output_md_path = os.path.join(output_dir, "current_gear_summary.md")
    with open(output_md_path, "w", encoding="utf-8") as f:
        f.write(f"# PoE2 現在装備サマリー\n\n")
        f.write(f"*   **取得元**: `{args.account_or_url}`\n")
        if args.character:
            f.write(f"*   **キャラクター名**: `{args.character}`\n")
        f.write(f"\n")
        
        f.write(f"## 📊 装備から得られているステータス合計 (防御面)\n")
        f.write(f"> [!NOTE]\n")
        f.write(f"> パッシブツリーやアセンダシー、基本値、アクト進行ペナルティ等は**含まれていません**。純粋に装備のModから抽出した値です。\n\n")
        f.write(f"*   **最大ライフ (Life)**: +{total_stats['life']}\n")
        f.write(f"*   **火属性耐性 (Fire Res)**: +{total_stats['fire_res']}%\n")
        f.write(f"*   **冷気属性耐性 (Cold Res)**: +{total_stats['cold_res']}%\n")
        f.write(f"*   **雷属性耐性 (Lightning Res)**: +{total_stats['lightning_res']}%\n")
        f.write(f"*   **カオス耐性 (Chaos Res)**: +{total_stats['chaos_res']}%\n")
        f.write(f"*   **元素耐性合計 (Total Ele Res)**: +{total_stats['fire_res'] + total_stats['cold_res'] + total_stats['lightning_res']}%\n\n")
        
        f.write(f"## ⚔️ 部位別装備詳細\n\n")
        slot_order = ["Weapon", "Offhand", "Helm", "Chest", "Gloves", "Boots", "Amulet", "Ring1", "Ring2", "Belt"]
        for slot_id in slot_order:
            # pobb.inパース時のキー表記揺れに対応するため、柔軟に取得
            item = gear_data.get(slot_id)
            if not item:
                # 装備中スロットから探す
                continue
                
            f.write(f"### {item['slot_name']}: {item['item_name']} ({item['rarity']})\n")
            st = item["parsed_stats"]
            details = []
            if st["life"] > 0: details.append(f"Life +{st['life']}")
            if st["fire_res"] > 0: details.append(f"Fire Res +{st['fire_res']}%")
            if st["cold_res"] > 0: details.append(f"Cold Res +{st['cold_res']}%")
            if st["lightning_res"] > 0: details.append(f"Lightning Res +{st['lightning_res']}%")
            if st["chaos_res"] > 0: details.append(f"Chaos Res +{st['chaos_res']}%")
            if details:
                f.write(f"*   **主要抽出ステータス**: {', '.join(details)}\n")
            
            if item.get("implicit_mods"):
                f.write(f"*   **Implicit Mods**:\n")
                for mod in item["implicit_mods"]:
                    f.write(f"    *   `{mod}`\n")
            if item.get("explicit_mods"):
                f.write(f"*   **Explicit Mods**:\n")
                for mod in item["explicit_mods"]:
                    f.write(f"    *   `{mod}`\n")
            f.write(f"\n")
            
    print(f"Saved readable summary to: {output_md_path}")

    if args.analyze:
        print("\n" + "="*50)
        print("🧠 簡易装備分析 & 更新アドバイス")
        print("="*50)
        print(f"現在の装備ライフ合計: +{total_stats['life']}")
        print(f"耐性合計 - 火: {total_stats['fire_res']}%, 冷気: {total_stats['cold_res']}%, 雷: {total_stats['lightning_res']}%, カオス: {total_stats['chaos_res']}%")
        
        weak_spots = []
        valid_slots = {
            "Helm": "Helmet", "Chest": "Body Armour", "Gloves": "Gloves", "Boots": "Boots",
            "Ring1": "Ring", "Ring2": "Ring", "Amulet": "Amulet", "Belt": "Belt"
        }
        for slot_id, name in valid_slots.items():
            if slot_id in gear_data:
                item = gear_data[slot_id]
                st = item["parsed_stats"]
                if st["life"] < 30 and st["total_ele_res"] < 30:
                    weak_spots.append((name, slot_id, "ライフ・耐性ともに低水準"))
                elif st["life"] < 30:
                    weak_spots.append((name, slot_id, "ライフ値が低い"))
                elif st["total_ele_res"] < 25:
                    weak_spots.append((name, slot_id, "元素耐性値が低い"))
            else:
                weak_spots.append((name, slot_id, "未装備または解析データなし"))

        if weak_spots:
            print("\n🚨 優先的に更新を推奨する部位:")
            for name, slot_id, reason in weak_spots:
                print(f"  * {name}: {reason}")
                print(f"    👉 更新用コマンド例:")
                print(f"      python generate_trade_url.py --type \"{name}\" --life 50 --res 50")
        else:
            print("\n✨ 現在の装備のライフ・耐性のバランスは良好です！")

if __name__ == "__main__":
    main()
