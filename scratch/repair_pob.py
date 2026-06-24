import base64
import zlib
import string

with open("scratch/user_raw_pob.txt", "r", encoding="utf-8") as f:
    s = f.read()

s = "".join(c for c in s if c.isalnum() or c in "+/_-")
print("Original length:", len(s))

# Base64 alphabet used in this string
b64_chars = string.ascii_letters + string.digits + "+/_-="

def check_string(test_str):
    # Convert and pad
    test_padded = test_str.replace("-", "+").replace("_", "/")
    test_padded += "=" * ((4 - len(test_padded) % 4) % 4)
    try:
        data = base64.b64decode(test_padded)
        dco = zlib.decompressobj()
        decompressed = b""
        # We only need to check if we can go past 500 bytes of decompressed XML
        # to know if we fixed the early corruption.
        # Feed in chunks
        for i in range(0, len(data), 100):
            chunk = data[i:i+100]
            decompressed += dco.decompress(chunk)
            if len(decompressed) > 1000:
                return len(decompressed), decompressed
        return len(decompressed), decompressed
    except Exception as e:
        # Return whatever was decompressed before failure
        try:
            return len(decompressed), decompressed
        except:
            return 0, b""

# Base test
base_len, base_data = check_string(s)
print(f"Base decompressed length: {base_len}")

# Let's try single deletions in the first 500 chars
print("Trying single deletions in the first 500 characters...")
for i in range(min(500, len(s))):
    test_s = s[:i] + s[i+1:]
    l, d = check_string(test_s)
    if l > 1000:
        print(f"SUCCESS with deletion at index {i}! Decompressed length: {l}")
        print("XML Snippet:", d[:200].decode('utf-8', errors='replace'))
        # Save and exit
        with open("scratch/user_repaired_del.xml", "wb") as out:
            out.write(d)
        # Also try full decompression to make sure it finishes
        # (it might fail later, but this is a huge step)

# Let's try single insertions in the first 500 chars
print("Trying single insertions in the first 500 characters...")
# To speed up, we can try inserting a dummy character or try all base64 chars
# But first let's see if we can find any index that yields > 1000 bytes
# We can try inserting 'A' first, as a test
for i in range(min(500, len(s))):
    for char in ['A', 'a', '0', '/', '-', '_']: # Try a subset of representative chars first
        test_s = s[:i] + char + s[i:]
        l, d = check_string(test_s)
        if l > 1000:
            print(f"SUCCESS with insertion of '{char}' at index {i}! Decompressed length: {l}")
            break
