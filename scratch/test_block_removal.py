import base64
import zlib

with open("scratch/user_raw_pob.txt", "r", encoding="utf-8") as f:
    s = f.read()

s = "".join(c for c in s if c.isalnum() or c in "+/_-")
print("Original length of s:", len(s))

# We will test removing blocks of various sizes around index 130 to 385.
# Specifically, we suspect the block between 130 and 385 is an accidental insert.
# Let's try removing s[split1:split2] where split1 is around 130 and split2 is around 385.
# We will do a grid search for split1 in [120..140] and split2 in [370..395].

found = False
for split1 in range(115, 145):
    for split2 in range(365, 405):
        test_s = s[:split1] + s[split2:]
        # Pad
        test_padded = test_s.replace("-", "+").replace("_", "/")
        test_padded += "=" * ((4 - len(test_padded) % 4) % 4)
        
        try:
            data = base64.b64decode(test_padded)
            dco = zlib.decompressobj()
            decompressed = dco.decompress(data)
            # If it succeeds and produces more than 1000 bytes, we found it!
            if len(decompressed) > 1000:
                print(f"SUCCESS! split1={split1}, split2={split2}, decompressed={len(decompressed)} bytes")
                # Try to decompress the rest
                try:
                    full_xml = zlib.decompress(data)
                    print("  Full decompression SUCCESS!")
                    with open("scratch/user_recovered_block.xml", "wb") as out:
                        out.write(full_xml)
                    found = True
                    break
                except Exception as e2:
                    print(f"  Partial success (first chunk ok, but full decompress failed later): {e2}")
        except Exception as e:
            pass
    if found:
        break

if not found:
    print("No combination of split1/split2 succeeded.")
