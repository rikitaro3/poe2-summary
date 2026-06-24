import base64
import zlib
import xml.etree.ElementTree as ET
import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

def parse_pob(pob_code):
    try:
        # Base64デコードのためのクリーニング
        cleaned_code = pob_code.strip().replace('-', '+').replace('_', '/')
        # パディングの補正
        missing_padding = len(cleaned_code) % 4
        if missing_padding:
            cleaned_code += '=' * (4 - missing_padding)
            
        compressed_data = base64.b64decode(cleaned_code)
        xml_text = zlib.decompress(compressed_data).decode('utf-8')
        
        print("Successfully decompressed PoB XML!")
        with open(os.path.join(SCRIPT_DIR, "pob_decoded.xml"), "w", encoding="utf-8") as f:
            f.write(xml_text)
        print("Saved decoded XML to pob_decoded.xml")
        # 最初の500文字をプレビュー表示
        print("\nXML Preview:")
        print(xml_text[:500])
        print("...\n")
        
        # XMLをパースしてアイテム情報を抽出してみる
        root = ET.fromstring(xml_text)
        items_element = root.find("Items")
        if items_element is not None:
            print("Found Items section in PoB code:")
            # 装備中のアイテムとスロットのマッピングを調べる
            slots = {}
            for slot in items_element.findall("Slot"):
                name = slot.get("name")
                item_id = slot.get("itemId")
                if name and item_id:
                    slots[item_id] = name
                    
            for item in items_element.findall("Item"):
                item_id = item.get("id")
                # 装備中のアイテムのみ表示
                if item_id in slots:
                    slot_name = slots[item_id]
                    # アイテムのテキストは子要素のテキストまたは本体のテキスト
                    raw_text = item.text.strip() if item.text else ""
                    # 最初の1行を表示（アイテム名）
                    first_line = raw_text.split('\n')[0] if raw_text else "Unknown"
                    print(f" - [{slot_name}] (ID: {item_id}): {first_line}")
        else:
            print("Items section not found.")
            
    except Exception as e:
        print(f"Error parsing PoB code: {str(e)}", file=sys.stderr)

if __name__ == "__main__":
    # ユーザーが貼り付けたコードのプレフィックス
    pob_code = (
        "eNrtPdty2ziyz6OvYLlqz0uchADvPs6c8t1O7MSx7GRmX6ZAEpQ4pkiFFzvK1v776QZIipRFiUqcXc8kUzWORHQ3gL6huwlAu__3eRIpdzzNwiR-tUVeqFsKj73ED-PRq62b6-Pn9tb__TrYvWT5-F2wX4QRttBfB7_sii9KxO949GrLcLYUL2JZ9pZN-Kut0yLOU55lWwrLPB77B_Om4TRMw1z5yKJbnm4pOUtHPP9QDUD9gwChMUuZl_P0HInvFXlykfiAGrAo41vKhIXxMPFueX6SJsUUOt9S7kJ-L4Gur46OtmB8v-xeRmzG02HOciWDP6-29mCebMRPwxwQWFQAtLr1ciXsfpFm-SGbwMf1OMMp5_4c7AVRbUqN8i_pwjoAdlwUUR5OoxA5UqLTLngY_sGYxd58QETtHNJ1krPo8HK4fvASMunBmo9hPt6PYKq96CL02SgOc94b_DIJsyTeaNS9gA-KKALt7QV7xTOe3rE87DmQg2TihnFPnhwkSeQn93EN6bygehfwBYvZQZLNBaOrq0AveQoWl7cw1iEMuZeAkbY6eaFRR1X18m-PHpfT6ez6PAx4f8iNZlUibDqar5vH0bAv3MaEv25AV-Cr-kEOkyLqCZnPHZOhd9vMpyagZnUBHvLPc9U3VpBrAlqd_Z7Feb_RNQF1s3t0dwnafQ_vk4ZukfOeburo9HLusnXdeQGWZRpEc5zOteFyPMtCj0UX7HM4KSbg-q_ZLZ-PjBBb71bp0TiPx"
        "eNrtPdty2ziyz6OvYLlqz0uchADvPs6c8t1O7MSx7GRmX6ZAEpQ4pkiFFzvK1v776QZIipRFiUqcXc8kUzWORHQ3gL6huwlAu__3eRIpdzzNwiR-tUVeqFsKj73ED-PRq62b6-Pn9tb__TrYvWT5-F2wX4QRttBfB7_sii9KxO949GrLcLYUL2JZ9pZN-Kut0yLOU55lWwrLPB77B_Om4TRMw1z5yKJbnm4pOUtHPP9QDUD9gwChMUuZl_P0HInvFXlykfiAGrAo41vKhIXxMPFueX6SJsUUOt9S7kJ-L4Gur46OtmB8v-xeRmzG02HOciWDP6-29mCebMRPwxwQWFQAtLr1ciXsfpFm-SGbwMf1OMMp5_4c7AVRbUqN8i_pwjoAdlwUUR5OoxA5UqLTLngY_sGYxd58QETtHNJ1krPo8HK4fvASMunBmo9hPt6PYKq96CL02SgOc94b_DIJsyTeaNS9gA-KKALt7QV7xTOe3rE87DmQg2TihnFPnhwkSeQn93EN6bygehfwBYvZQZLNBaOrq0AveQoWl7cw1iEMuZeAkbY6eaFRR1X18m-PHpfT6ez6PAx4f8iNZlUibDqar5vH0bAv3MaEv25AV-Cr-kEOkyLqCZnPHZOhd9vMpyagZnUBHvLPc9U3VpBrAlqd_Z7Feb_RNQF1s3t0dwnafQ_vk4ZukfOeburo9HLusnXdeQGWZRpEc5zOteFyPMtCj0UX7HM4KSbg-q_ZLZ-PjBBb71bp0TiPkg"
    )
    # pob_code.txtからコードを読み込む
    txt_path = os.path.join(SCRIPT_DIR, "pob_code.txt")
    if os.path.exists(txt_path):
        with open(txt_path, "r", encoding="utf-8") as f:
            pob_code = f.read().strip()
            
    # XMLのパースとステータスの出力
    try:
        cleaned_code = pob_code.strip().replace('-', '+').replace('_', '/')
        missing_padding = len(cleaned_code) % 4
        if missing_padding:
            cleaned_code += '=' * (4 - missing_padding)
            
        compressed_data = base64.b64decode(cleaned_code)
        xml_text = zlib.decompress(compressed_data).decode('utf-8')
        
        with open(os.path.join(SCRIPT_DIR, "pob_decoded.xml"), "w", encoding="utf-8") as f:
            f.write(xml_text)
        print("Saved decoded XML to pob_decoded.xml")
        
        root = ET.fromstring(xml_text)
        
        # ステータスの抽出
        print("\n=== Player Stats ===")
        build_element = root.find("Build")
        if build_element is not None:
            stats_to_find = [
                "Str", "Dex", "Int", "Life", "Spec:LifeMin", "Spec:LifeMax", 
                "Evasion", "DeflectionRating", "DeflectionChance", 
                "FireResist", "ColdResist", "LightningResist", "ChaosResist",
                "FireResistOverCap", "ColdResistOverCap", "LightningResistOverCap", "ChaosResistOverCap",
                "SkillDPS"
            ]
            stats = {}
            for stat_elem in build_element.findall("PlayerStat"):
                stat_name = stat_elem.get("stat")
                stat_val = stat_elem.get("value")
                if stat_name in stats_to_find:
                    stats[stat_name] = stat_val
            
            for k, v in stats.items():
                print(f"{k}: {v}")
        
        # スキルとジェムの抽出
        skills_element = root.find("Skills")
        if skills_element is not None:
            print("\n=== Active Skills & Gems ===")
            for skill_set in skills_element.findall(".//Skill"):
                # メインのスキルグループのみ表示、もしくは装備中
                enabled = skill_set.get("enabled")
                slot = skill_set.get("slot")
                label = skill_set.get("label", "")
                gem_names = []
                for gem in skill_set.findall("Gem"):
                    gem_name = gem.get("nameSpec")
                    gem_lv = gem.get("level")
                    gem_qual = gem.get("quality", "0")
                    gem_names.append(f"{gem_name} (Lv{gem_lv}/Q{gem_qual})")
                if gem_names:
                    slot_str = f" [{slot}]" if slot else ""
                    enabled_str = " (Active)" if enabled == "true" else " (Inactive)"
                    print(f" -{slot_str} {label}: {', '.join(gem_names)}{enabled_str}")

        items_element = root.find("Items")
        if items_element is not None:
            print("\n=== Equipped Items ===")
            slots = {}
            for slot in items_element.findall("Slot"):
                name = slot.get("name")
                item_id = slot.get("itemId")
                if name and item_id:
                    slots[item_id] = name
                    
            for item in items_element.findall("Item"):
                item_id = item.get("id")
                if item_id in slots:
                    slot_name = slots[item_id]
                    raw_text = item.text.strip() if item.text else ""
                    first_line = raw_text.split('\n')[0] if raw_text else "Unknown"
                    print(f" - [{slot_name}] (ID: {item_id}): {first_line}")
        else:
            print("Items section not found.")
            
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)

if __name__ == "__main__":
    parse_pob(pob_code)

