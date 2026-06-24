import base64
import zlib

with open("scratch/user_raw_pob.txt", "r", encoding="utf-8") as f:
    s = f.read()

s = "".join(c for c in s if c.isalnum() or c in "+/_-")
s_padded = s.replace("-", "+").replace("_", "/")
s_padded += "=" * ((4 - len(s_padded) % 4) % 4)
data = base64.b64decode(s_padded)

dco = zlib.decompressobj()
decompressed = b""
try:
    decompressed = dco.decompress(data)
except Exception as e:
    # Get what we could decompress
    decompressed = dco.flush()

# Let's do it safely
dco = zlib.decompressobj()
decompressed_safe = b""
for i in range(len(data)):
    try:
        decompressed_safe += dco.decompress(data[i:i+1])
    except Exception as e:
        print(f"Failed at byte {i} with error: {e}")
        break

print("Length of decompressed data:", len(decompressed_safe))
print("Decompressed XML:")
print(decompressed_safe.decode('utf-8', errors='replace'))
