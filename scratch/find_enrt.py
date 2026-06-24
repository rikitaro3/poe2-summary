with open("scratch/user_raw_pob.txt", "r", encoding="utf-8") as f:
    s = f.read()

s = "".join(c for c in s if c.isalnum() or c in "+/_-")
print("Total length:", len(s))

# Find all occurrences of "eNrt"
pos = s.find("eNrt")
while pos != -1:
    print(f"Found 'eNrt' at index {pos}")
    # Print the next 50 chars
    print(f"  Snippet: {s[pos:pos+100]}")
    pos = s.find("eNrt", pos + 1)
