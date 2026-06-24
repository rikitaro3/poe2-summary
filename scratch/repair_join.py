import base64
import zlib
import string

with open("scratch/user_raw_pob.txt", "r", encoding="utf-8") as f:
    s = f.read()

s = "".join(c for c in s if c.isalnum() or c in "+/_-")
print("Original length of s:", len(s))

# We suspect corruption around index 385 (the transition from 1st line to 2nd line)
# Let's define the join index
join_idx = 385

b64_chars = string.ascii_letters + string.digits + "+/_-="

def check_string(test_str):
    test_padded = test_str.replace("-", "+").replace("_", "/")
    test_padded += "=" * ((4 - len(test_padded) % 4) % 4)
    try:
        data = base64.b64decode(test_padded)
        dco = zlib.decompressobj()
        decompressed = b""
        for i in range(0, len(data), 100):
            chunk = data[i:i+100]
            decompressed += dco.decompress(chunk)
            if len(decompressed) > 5000: # Successfully decompressed a large portion
                return len(decompressed), decompressed
        return len(decompressed), decompressed
    except Exception as e:
        try:
            return len(decompressed), decompressed
        except:
            return 0, b""

# Try deleting characters around join_idx (from 380 to 390)
print("Testing deletions around join_idx...")
for idx in range(375, 395):
    for num_to_delete in range(1, 5):
        test_s = s[:idx] + s[idx+num_to_delete:]
        l, d = check_string(test_s)
        if l > 1000:
            print(f"SUCCESS! Deleted {num_to_delete} chars at {idx}. Decompressed len: {l}")
            with open("scratch/user_recovered_join.xml", "wb") as out:
                out.write(d)
            break

# Try inserting characters around join_idx
print("Testing insertions around join_idx...")
for idx in range(375, 395):
    for char1 in ['A', 'a', '0', '/', '-', '_', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T']:
        test_s = s[:idx] + char1 + s[idx:]
        l, d = check_string(test_s)
        if l > 1000:
            print(f"SUCCESS! Inserted '{char1}' at {idx}. Decompressed len: {l}")
            break
        # Try double insertions
        for char2 in ['A', 'a', '0', '/', '-', '_']:
            test_s = s[:idx] + char1 + char2 + s[idx:]
            l, d = check_string(test_s)
            if l > 1000:
                print(f"SUCCESS! Inserted '{char1}{char2}' at {idx}. Decompressed len: {l}")
                break
