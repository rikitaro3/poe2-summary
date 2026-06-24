import base64
import zlib
import xml.etree.ElementTree as ET
import sys
import urllib.request
import ssl
import json
import re

def parse_mods_for_stats(item):
    life = 0
    fire_res = 0
    cold_res = 0
    lightning_res = 0
    chaos_res = 0
    
    mods = item.get("implicitMods", []) + item.get("explicitMods", [])
    for mod in mods:
        # Life
        life_match = re.search(r'\+(\d+) to maximum Life', mod)
        if life_match:
            life += int(life_match.group(1))
        # Fire Resistance
        fire_match = re.search(r'\+(\d+)% to Fire Resistance', mod)
        if fire_match:
            fire_res += int(fire_match.group(1))
        # Cold Resistance
        cold_match = re.search(r'\+(\d+)% to Cold Resistance', mod)
        if cold_match:
            cold_res += int(cold_match.group(1))
        # Lightning Resistance
        lightning_match = re.search(r'\+(\d+)% to Lightning Resistance', mod)
        if lightning_match:
            lightning_res += int(lightning_match.group(1))
        # Chaos Resistance
        chaos_match = re.search(r'\+(\d+)% to Chaos Resistance', mod)
        if chaos_match:
            chaos_res += int(chaos_match.group(1))
        # all Elemental Resistances
        all_res_match = re.search(r'\+(\d+)% to all Elemental Resistances', mod)
        if all_res_match:
            val = int(all_res_match.group(1))
            fire_res += val
            cold_res += val
            lightning_res += val
        # double Resistances
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
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    if not lines:
        return None
        
    rarity = "Normal"
    item_name = ""
    base_type = ""
    
    # Rarity
    if lines[0].startswith("Rarity:"):
        rarity = lines[0].split(":", 1)[1].strip()
        lines = lines[1:]
        
    # Name
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
            
    # メタデータ行を弾く
    meta_prefixes = [
        "Unique ID:", "Item Level:", "Quality:", "Sockets:", "Rune:", 
        "LevelReq:", "Implicits:", "Requirements:", "Evasion:", "Armour:", 
        "Energy Shield:", "Ward:", "Spirit:", "Charm Slots:", "Level:",
        "--------"
    ]
    
    mods = []
    for line in lines:
        is_meta = False
        for prefix in meta_prefixes:
            if line.startswith(prefix):
                is_meta = True
                break
        if is_meta:
            continue
        mods.append(line)
        
    implicit_mods = []
    explicit_mods = []
    for mod in mods:
        is_implicit = any(tag in mod for tag in ["{enchant}", "{rune}", "{implicit}", "(implicit)"])
        cleaned = mod.replace("{enchant}", "").replace("{rune}", "").replace("{implicit}", "").replace("{explicit}", "").replace("{desecrated}", "").strip()
        if is_implicit:
            implicit_mods.append(cleaned)
        else:
            explicit_mods.append(cleaned)
            
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

def fetch_and_parse(pob_url):
    raw_url = pob_url.strip()
    if not raw_url.endswith("/raw"):
        raw_url = raw_url.rstrip("/") + "/raw"
        
    print(f"Fetching from: {raw_url}")
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    req = urllib.request.Request(raw_url, headers=headers, method="GET")
    
    # SSLコンテキストを無効化
    ctx = ssl._create_unverified_context()
    
    with urllib.request.urlopen(req, context=ctx) as response:
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
        raise ValueError("No Items section in PoB XML")
        
    slots = {}
    for slot in items_element.findall(".//Slot"):
        name = slot.get("name")
        item_id = slot.get("itemId")
        if name and item_id:
            slots[item_id] = name
            
    valid_slots = {
        "Helmet": "Helmet",
        "Body Armour": "Body Armour",
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

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python get_pob_data.py <pobb_url> <output_name>")
        sys.exit(1)
        
    url = sys.argv[1]
    out_name = sys.argv[2]
    
    try:
        data = fetch_and_parse(url)
        with open(out_name, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"Success! Saved to {out_name}")
    except Exception as e:
        import traceback
        traceback.print_exc()
        sys.exit(1)
