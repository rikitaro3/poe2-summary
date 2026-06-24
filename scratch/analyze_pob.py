import base64
import zlib
import re
import collections
import xml.etree.ElementTree as ET

# Load raw PoB code
with open("scratch/user_raw_pob.txt", "r", encoding="utf-8") as f:
    pob_code = f.read()

# Filter base64 valid characters
pob_code = "".join(c for c in pob_code if c.isalnum() or c in "+/_-")
print("Original base64 length:", len(pob_code))

# Auto-detect duplicating pattern of length 100
chunk_size = 100
chunks = [pob_code[i:i+chunk_size] for i in range(len(pob_code) - chunk_size)]
counts = collections.Counter(chunks)
most_common = counts.most_common(1)

if most_common and most_common[0][1] > 1:
    chunk = most_common[0][0]
    first_idx = pob_code.find(chunk)
    second_idx = pob_code.find(chunk, first_idx + 1)
    
    # Extend duplicate block
    length = chunk_size
    while first_idx + length < second_idx and second_idx + length < len(pob_code):
        if pob_code[first_idx:first_idx+length+1] == pob_code[second_idx:second_idx+length+1]:
            length += 1
        else:
            break
            
    dup_pattern = pob_code[first_idx:first_idx+length]
    print(f"Detected duplicate block B at index {first_idx} to {first_idx+len(dup_pattern)} (len {len(dup_pattern)})")
    print(f"Second occurrence at index {second_idx} to {second_idx+len(dup_pattern)}")
    
    # Method 1: Remove second occurrence (Keep A + B + C + E)
    # A is pob_code[:first_idx]
    # B is pob_code[first_idx:first_idx+len(dup_pattern)]
    # C is pob_code[first_idx+len(dup_pattern):second_idx]
    # E is pob_code[second_idx+len(dup_pattern):]
    # So we just cut out pob_code[second_idx:second_idx+len(dup_pattern)]
    cleaned_m1 = pob_code[:second_idx] + pob_code[second_idx+len(dup_pattern):]
    
    # Method 2: Remove first occurrence (Keep A + C + B + E)
    # So we cut out pob_code[first_idx:first_idx+len(dup_pattern)]
    cleaned_m2 = pob_code[:first_idx] + pob_code[first_idx+len(dup_pattern):]
    
    methods = [("Method 1 (Remove 2nd)", cleaned_m1), ("Method 2 (Remove 1st)", cleaned_m2)]
else:
    print("No duplicating pattern detected.")
    methods = [("No Change", pob_code)]

for name, cleaned_code in methods:
    print(f"\n--- Testing {name} ---")
    print("Cleaned base64 length:", len(cleaned_code))
    
    # Decode base64
    cleaned_b64 = cleaned_code.replace("-", "+").replace("_", "/")
    cleaned_b64 += "=" * ((4 - len(cleaned_b64) % 4) % 4)
    try:
        decoded_bytes = base64.b64decode(cleaned_b64)
        xml_data = zlib.decompress(decoded_bytes)
        print("SUCCESS! Decompressed XML length:", len(xml_data))
        
        # Save recovered XML
        with open("scratch/user_recovered.xml", "wb") as f:
            f.write(xml_data)
            
        # Parse items
        root = ET.fromstring(xml_data)
        
        # Check ItemSets
        print("\n=== EQUIP SLOTS IN CURRENT ITEMSET ===")
        active_set_id = 1
        items_elem = root.find("Items")
        if items_elem is not None:
            active_set_id_str = items_elem.attrib.get("activeItemSet", "1")
            print("Active Item Set ID:", active_set_id_str)
            active_set_id = int(active_set_id_str)
            
        item_sets = root.findall(".//ItemSet")
        target_set = None
        if item_sets:
            for iset in item_sets:
                if iset.attrib.get("id") == str(active_set_id):
                    target_set = iset
                    break
            if not target_set:
                target_set = item_sets[0]
                
            print(f"Using Item Set: id={target_set.attrib.get('id')}, name={target_set.attrib.get('name')}")
            
            equipped_item_ids = {}
            for slot in target_set.findall("Slot"):
                slot_name = slot.attrib.get("name")
                item_id = int(slot.attrib.get("itemId", "0"))
                equipped_item_ids[slot_name] = item_id
                print(f"Slot: {slot_name} -> Item ID {item_id}")
                
            # Get details of weapons
            print("\n=== WEAPON DETAILS ===")
            for slot_name in ["Weapon 1", "Weapon 2", "Weapon 1 Swap", "Weapon 2 Swap"]:
                item_id = equipped_item_ids.get(slot_name, 0)
                if item_id > 0:
                    item_elem = root.find(f".//Items/Item[@id='{item_id}']")
                    if item_elem is not None:
                        print(f"[{slot_name}] Item ID {item_id}:")
                        print(item_elem.text.strip() if item_elem.text else "")
                        print("-" * 50)
                    else:
                        print(f"[{slot_name}] Item ID {item_id} (Not found in <Items>)")
                else:
                    print(f"[{slot_name}]: None")
        break # Exit loop on success
    except Exception as e:
        print("Failed:", e)
