with open('index.html', 'r') as f:
    lines = f.readlines()
for i in [274, 275, 276, 290, 291, 292]:
    if i < len(lines):
        print(f"--- Line {i+1} ---")
        print(lines[i][:600])
