import base64
import zlib
import xml.etree.ElementTree as ET
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
code_path = os.path.join(SCRIPT_DIR, "ref_pob_code.txt")
xml_path = os.path.join(SCRIPT_DIR, "ref_pob_decoded.xml")

if os.path.exists(code_path):
    with open(code_path, "r", encoding="utf-8") as f:
        code = f.read().strip()
        
    cleaned_code = code.replace('-', '+').replace('_', '/')
    missing_padding = len(cleaned_code) % 4
    if missing_padding:
        cleaned_code += '=' * (4 - missing_padding)
        
    compressed_data = base64.b64decode(cleaned_code)
    xml_text = zlib.decompress(compressed_data).decode('utf-8')
    
    with open(xml_path, "w", encoding="utf-8") as f:
        f.write(xml_text)
        
    root = ET.fromstring(xml_text)
    items_elem = root.find("Items")
    if items_elem is not None:
        itemset = items_elem.find("ItemSet")
        if itemset is not None:
            slots = {}
            for slot in itemset.findall("Slot"):
                name = slot.get("name")
                item_id = slot.get("itemId")
                if name and item_id and item_id != "0":
                    slots[item_id] = name
                    
            print("--- Equipped Items in Reference Build ---")
            for item in items_elem.findall("Item"):
                item_id = item.get("id")
                if item_id in slots:
                    slot_name = slots[item_id]
                    raw_text = item.text.strip() if item.text else ""
                    lines = raw_text.split('\n')
                    print(f"[{slot_name}]: {lines[0]} | {lines[1] if len(lines) > 1 else ''}")
