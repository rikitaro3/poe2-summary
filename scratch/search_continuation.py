import base64
import zlib

with open("scratch/user_raw_pob.txt", "r", encoding="utf-8") as f:
    s = f.read()

s = "".join(c for c in s if c.isalnum() or c in "+/_-")
print("Original length of s:", len(s))

# We know s[:366] is perfectly valid.
# We want to find a start index K >= 367 such that s[:366] + s[K:] can be decompressed
# past the 274 bytes barrier.

found = False
for K in range(367, len(s)):
    test_s = s[:366] + s[K:]
    # pad
    test_padded = test_s.replace("-", "+").replace("_", "/")
    test_padded += "=" * ((4 - len(test_padded) % 4) % 4)
    
    try:
        data = base64.b64decode(test_padded)
        dco = zlib.decompressobj()
        decompressed = dco.decompress(data)
        dec_len = len(decompressed)
        if dec_len > 300: # Successfully broke the 274 byte barrier!
            print(f"SUCCESS! Found continuation at K={K}. Decompressed length: {dec_len} bytes")
            # Try full decompress
            try:
                full_xml = zlib.decompress(data)
                print("  FULL DECOMPRESSION SUCCESS!")
                with open("scratch/user_recovered_k.xml", "wb") as out:
                    out.write(full_xml)
                found = True
                break
            except Exception as e2:
                print(f"  Partial success (first chunk ok, but full decompress failed later): {e2}")
    except Exception as e:
        pass

if not found:
    print("No continuation index K found that broke the barrier.")
