import xml.etree.ElementTree as ET
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
xml_path = os.path.join(SCRIPT_DIR, "pob_decoded.xml")

if not os.path.exists(xml_path):
    print("pob_decoded.xml not found")
    exit(1)

root = ET.parse(xml_path).getroot()
items_elem = root.find("Items")

if items_elem is None:
    print("Items element not found")
    exit(1)

print("=== ALL ITEMS IN POB LIST ===")
for item in items_elem.findall("Item"):
    item_id = item.get("id")
    raw_text = item.text.strip() if item.text else ""
    lines = [l.strip() for l in raw_text.split('\n') if l.strip()]
    
    rarity = "Unknown"
    name_lines = []
    mods = []
    
    # 簡単なパース
    for line in lines:
        if line.startswith("Rarity:"):
            rarity = line.split(":", 1)[1].strip()
        elif any(line.startswith(p) for p in ["Unique ID:", "Item Level:", "Quality:", "Sockets:", "Rune:", "LevelReq:", "Implicits:", "Requirements:", "Armour:", "Evasion:", "Energy Shield:", "Spirit:", "--------"]):
            continue
        else:
            if len(name_lines) < 2:
                name_lines.append(line)
            else:
                mods.append(line)
                
    item_name = " ".join(name_lines)
    print(f"ID {item_id}: [{rarity}] {item_name}")
    # 攻撃速度Modがあるかチェック
    for mod in mods:
        if "Attack Speed" in mod or "attack speed" in mod.lower():
            print(f"  -> Mod: {mod}")
