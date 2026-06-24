with open("scratch/user_raw_pob.txt", "r", encoding="utf-8") as f:
    user_s = f.read()
user_s = "".join(c for c in user_s if c.isalnum() or c in "+/_-")

with open("scratch/ref_pob_code.txt", "r", encoding="utf-8") as f:
    ref_s = f.read()
ref_s = "".join(c for c in ref_s if c.isalnum() or c in "+/_-")

print(f"User POB head (first 500 chars):")
print(user_s[:500])
print("\n" + "="*50 + "\n")
print(f"Reference POB head (first 500 chars):")
print(ref_s[:500])

# Let's compare where they diverge in decompression
import zlib
import base64

def get_xml_head(b64_str):
    b64_str = b64_str.replace("-", "+").replace("_", "/")
    b64_str += "=" * ((4 - len(b64_str) % 4) % 4)
    try:
        data = base64.b64decode(b64_str)
        dco = zlib.decompressobj()
        return dco.decompress(data)
    except Exception as e:
        try:
            return dco.flush()
        except:
            return b""

user_xml = get_xml_head(user_s[:366])
ref_xml = get_xml_head(ref_s[:1000])

print("\n" + "="*50 + "\n")
print("User XML head decompressed (366 chars):")
print(user_xml.decode('utf-8', errors='replace'))
print("\n" + "="*50 + "\n")
print("Reference XML head decompressed (first 1000 bytes):")
print(ref_xml[:1000].decode('utf-8', errors='replace'))
