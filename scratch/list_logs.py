import os

base_dir = r"C:\Users\4in4o\.gemini\antigravity-ide\brain\d89f4000-4b93-4a47-99a5-db0d7f286aaf"
if os.path.exists(base_dir):
    print("Base dir exists!")
    for root, dirs, files in os.walk(base_dir):
        print(f"Dir: {root}")
        for f in files:
            print(f"  File: {f} (Size: {os.path.getsize(os.path.join(root, f))})")
else:
    print("Base dir does not exist at", base_dir)
