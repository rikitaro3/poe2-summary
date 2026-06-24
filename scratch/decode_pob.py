import base64
import zlib
import re
import xml.etree.ElementTree as ET

transcript_path = r"C:\Users\4in4o\.gemini\antigravity-ide\brain\d89f4000-4b93-4a47-99a5-db0d7f286aaf\.system_generated\logs\transcript.jsonl"

with open(transcript_path, "r", encoding="utf-8") as f:
    full_text = f.read()

# Find the PoB code starting with eNrtPWtz20a
# Allow backslashes and JSON escape characters like \n, \r, \/, and spaces
match = re.search(r'eNrtPWtz20a[a-zA-Z0-9_\-\s\\/\+=]+', full_text)
if not match:
    print("Could not find the PoB code prefix in the transcript.")
    exit(1)

raw_code = match.group(0)
# Clean escape sequences first
pob_code = raw_code.replace("\\n", "").replace("\\r", "").replace("\\/", "/")
pob_code = "".join(pob_code.split())

# Filter only valid base64 chars
pob_code = "".join(c for c in pob_code if c.isalnum() or c in "+/_-")

print("Found PoB code in transcript. Length:", len(pob_code))
print("Start of code:", pob_code[:50])
print("End of code:", pob_code[-50:])

start_idx = full_text.find(raw_code)
end_idx = start_idx + len(raw_code)
print("Context after raw_code:", repr(full_text[end_idx:end_idx+100]))

# Decode
pob_code = pob_code.replace("-", "+").replace("_", "/")
pob_code += "=" * ((4 - len(pob_code) % 4) % 4)
decoded_data = base64.b64decode(pob_code)

try:
    # Try decompressing with fallback
    xml_data = None
    try:
        xml_data = zlib.decompress(decoded_data)
    except Exception:
        try:
            xml_data = zlib.decompress(decoded_data, zlib.MAX_WBITS | 32)
        except Exception:
            xml_data = zlib.decompress(decoded_data, -zlib.MAX_WBITS)
            
    print("Decompression success! Decoded length:", len(xml_data))
    
    with open("scratch/recovered.xml", "wb") as f:
        f.write(xml_data)
        
    root = ET.fromstring(xml_data)
    
    # 1. Print all ItemSets to see weapon sets
    print("\n=== ITEM SETS ===")
    for item_set in root.findall(".//ItemSet"):
        print(f"ItemSet: {item_set.attrib.get('title', 'Default')} (id: {item_set.attrib.get('id')})")
        for slot in item_set.findall("Slot"):
            name = slot.attrib.get("name", "")
            if "weapon" in name.lower():
                print(f"  Slot name: {name}, itemId: {slot.attrib.get('itemId')}")

    # 2. Print all Items that are Spears / Weapons
    print("\n=== DETECTED SPEARS ===")
    for item in root.findall(".//Items/Item"):
        item_id = item.attrib.get("id")
        content = item.text.strip() if item.text else ""
        if "spear" in content.lower() or "spere" in content.lower():
            print(f"Item ID {item_id}:")
            print(content)
            print("-" * 40)

except Exception as e:
    print("Error during decompression/parse:", e)
