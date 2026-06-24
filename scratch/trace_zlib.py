import base64
import zlib

with open("scratch/user_raw_pob.txt", "r", encoding="utf-8") as f:
    s = f.read()

s = "".join(c for c in s if c.isalnum() or c in "+/_-")
print("Total length:", len(s))

# Base64 decode the full string (ignoring corruption if any, just decode what we have)
# Note: if there is corruption, decoding the whole thing will give a bytearray,
# but the bytearray itself will contain duplicate compressed data.
s_padded = s.replace("-", "+").replace("_", "/")
s_padded += "=" * ((4 - len(s_padded) % 4) % 4)
data = base64.b64decode(s_padded)
print("Decoded byte length:", len(data))

# Now use decompressobj to see how far we can go
dco = zlib.decompressobj()
try:
    decompressed = dco.decompress(data)
    print("Decompressed size:", len(decompressed))
    print("Unused data size:", len(dco.unused_data))
    if dco.eof:
        print("Reached EOF successfully!")
    else:
        print("Did not reach EOF.")
except Exception as e:
    print("Failed during full decompress:", e)

# Let's decompress byte by byte or chunk by chunk to find where it fails
dco = zlib.decompressobj()
chunk_size = 1
decompressed_data = b""
bytes_consumed = 0
try:
    for i in range(len(data)):
        # Feed 1 byte at a time
        chunk = data[i:i+1]
        res = dco.decompress(chunk)
        decompressed_data += res
        bytes_consumed += 1
        if dco.eof:
            print(f"Reached EOF at byte {bytes_consumed}!")
            break
except Exception as e:
    print(f"Failed at byte {bytes_consumed}: {e}")
    # Print the last few decompressed chars
    print("Last decompressed XML snippet:")
    print(decompressed_data[-200:].decode('utf-8', errors='replace'))
