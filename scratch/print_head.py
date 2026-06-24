with open("scratch/user_raw_pob.txt", "r", encoding="utf-8") as f:
    s = f.read()

s = "".join(c for c in s if c.isalnum() or c in "+/_-")
print("Total length:", len(s))
print("First 1500 chars:")
for i in range(0, 1500, 100):
    print(f"{i:4d}: {s[i:i+100]}")
