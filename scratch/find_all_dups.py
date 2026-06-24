with open("scratch/user_raw_pob.txt", "r", encoding="utf-8") as f:
    s = f.read()

s = "".join(c for c in s if c.isalnum() or c in "+/_-")
print("Total length:", len(s))

# Find repeating substrings of various lengths
# We can search for the longest repeating substring using suffix tree or a simple heuristic.
# Let's write a simple function to find repeating substrings.
def find_longest_repeats(text, min_len=50):
    repeats = []
    # We can slide a window of size min_len, find its occurrences, and extend them.
    # To avoid too many overlaps, we keep track of seen start indices.
    seen_indices = set()
    i = 0
    while i < len(text) - min_len:
        if i in seen_indices:
            i += 1
            continue
        window = text[i:i+min_len]
        count = text.count(window)
        if count > 1:
            # Found a repeating block. Let's extend it to the right as far as possible
            # for all occurrences.
            # Let's find all start positions of this window
            positions = []
            pos = text.find(window)
            while pos != -1:
                positions.append(pos)
                pos = text.find(window, pos + 1)
            
            # Extend length
            length = min_len
            while True:
                # Check if all occurrences can be extended by 1 char and still match
                if positions[0] + length >= len(text):
                    break
                next_char = text[positions[0] + length]
                ok = True
                for p in positions[1:]:
                    if p + length >= len(text) or text[p + length] != next_char:
                        ok = False
                        break
                if ok:
                    length += 1
                else:
                    break
            
            pattern = text[positions[0] : positions[0] + length]
            repeats.append((pattern, positions))
            # Mark all these positions and their range as seen to avoid duplicate reporting
            for p in positions:
                for idx in range(p, p + length):
                    seen_indices.add(idx)
            i += length
        else:
            i += 1
    return repeats

repeats = find_longest_repeats(s, min_len=20)
print(f"Found {len(repeats)} repeating patterns:")
for idx, (pat, positions) in enumerate(repeats):
    print(f"Pattern {idx}: len={len(pat)}, count={len(positions)}, positions={positions}")
    print(f"  Start: {pat[:50]}...")
    print(f"  End: {pat[-50:]}...")
