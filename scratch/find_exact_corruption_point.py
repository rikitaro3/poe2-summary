import base64
import zlib

with open("scratch/user_raw_pob.txt", "r", encoding="utf-8") as f:
    s = f.read()

s = "".join(c for c in s if c.isalnum() or c in "+/_-")

# We will test prefixes of the base64 string
# For each prefix of length L, we decode it and decompress it.
# We measure how many bytes of XML are successfully decompressed before an exception is raised.
# This will show us exactly at which base64 character index the decompression starts to fail or degrade.

print("Length of s:", len(s))

last_success_len = 0
for L in range(100, 1000):
    test_s = s[:L]
    # pad
    test_padded = test_s.replace("-", "+").replace("_", "/")
    test_padded += "=" * ((4 - len(test_padded) % 4) % 4)
    
    try:
        data = base64.b64decode(test_padded)
        dco = zlib.decompressobj()
        decompressed = dco.decompress(data)
        # If we successfully decompressed, let's see how much we got
        dec_len = len(decompressed)
        if dec_len != last_success_len:
            print(f"B64 Length L={L:3d} -> Decompressed {dec_len:3d} bytes of XML")
            last_success_len = dec_len
    except Exception as e:
        # If it failed, print why
        pass
