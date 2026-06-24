import base64
import zlib
import re

# Load raw POB
with open("scratch/user_raw_pob.txt", "r", encoding="utf-8") as f:
    raw_s = f.read()

# Clean up
s = "".join(c for c in raw_s if c.isalnum() or c in "+/_-")
print("Total length of s:", len(s))

# Method to try decompressing a base64 string
def try_decompress(b64_str):
    # Convert URL-safe to standard base64 if needed
    b64_str = b64_str.replace("-", "+").replace("_", "/")
    # Add padding
    b64_str += "=" * ((4 - len(b64_str) % 4) % 4)
    try:
        data = base64.b64decode(b64_str)
        # Try decompression
        decompressed = zlib.decompress(data)
        return decompressed
    except Exception as e:
        return None

# Try prefixes of s (in case it just has extra data at the end)
print("Testing prefixes...")
for length in range(1000, len(s) + 1, 10):
    res = try_decompress(s[:length])
    if res:
        print(f"SUCCESS with prefix length {length}!")
        with open("scratch/user_recovered.xml", "wb") as out:
            out.write(res)
        break

# If that didn't work, let's try the double paste reconstruction.
# The duplicate block B was detected around:
# first_idx = 1310, length = 5246, second_idx = 6990
# We can search for the boundary shifts.
# We want to form a string like: s[:split1] + s[split2:]
# Let's search split1 in [1300..1320] and split2 in [6550..6995]
# Or split1 in [6550..6565] and split2 in [12230..12240]
print("Searching for split combinations...")
found = False
for split1 in range(1290, 1330):
    for split2 in range(6540, 7010):
        test_s = s[:split1] + s[split2:]
        res = try_decompress(test_s)
        if res:
            print(f"SUCCESS! split1={split1}, split2={split2}, len={len(test_s)}")
            with open("scratch/user_recovered.xml", "wb") as out:
                out.write(res)
            found = True
            break
    if found:
        break

if not found:
    # Try another combination: split1 in [6550..6570], split2 in [12220..12240]
    for split1 in range(6540, 6580):
        for split2 in range(12220, 12240):
            test_s = s[:split1] + s[split2:]
            res = try_decompress(test_s)
            if res:
                print(f"SUCCESS! split1={split1}, split2={split2}, len={len(test_s)}")
                with open("scratch/user_recovered.xml", "wb") as out:
                    out.write(res)
                found = True
                break
        if found:
            break

if not found:
    print("No simple split found. Let's do a broader search of split1 and split2.")
    # Broader search
    # Let's try split1 from 1000 to 7000, split2 from split1+100 to len(s)
    # This might be slow in Python if not optimized, but let's test a subset or use heuristic.
