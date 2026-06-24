with open("scratch/user_raw_pob.txt", "r", encoding="utf-8") as f:
    s = f.read()

s = "".join(c for c in s if c.isalnum() or c in "+/_-")

# Find duplicates of length >= 100
print("Length of string:", len(s))

# We can search for the duplicate of the last block or find any repeating block
# Let's count matching chunks
import collections

chunk_size = 100
chunks = [s[i:i+chunk_size] for i in range(len(s) - chunk_size)]
counts = collections.Counter(chunks)
most_common = counts.most_common(5)
print("Most common chunks of length 100:")
for chunk, count in most_common:
    if count > 1:
        print(f"Count: {count}, Chunk: {chunk[:50]}...{chunk[-20:]}")
        # Find how long this repeating block actually is
        # We find occurrences of the chunk
        first_idx = s.find(chunk)
        second_idx = s.find(chunk, first_idx + 1)
        
        # Extend the match to find the full duplicate block
        length = chunk_size
        while first_idx + length < second_idx and second_idx + length < len(s):
            if s[first_idx:first_idx+length+1] == s[second_idx:second_idx+length+1]:
                length += 1
            else:
                break
        
        full_pattern = s[first_idx:first_idx+length]
        print(f"  Detected duplicate pattern length: {len(full_pattern)}")
        print(f"  Start: {full_pattern[:40]}")
        print(f"  End: {full_pattern[-40:]}")
        print(f"  Occurrences of full pattern: {s.count(full_pattern)}")
        break
else:
    print("No repeating chunks found.")
