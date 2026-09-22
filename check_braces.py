import re
with open('index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()
depth = 0
for i, line in enumerate(lines, 1):
    clean_line = re.sub(r'".*?"', '""', line)
    clean_line = re.sub(r"'.*?'", "''", clean_line)
    for char in clean_line:
        if char == '{': depth += 1
        elif char == '}':
            depth -= 1
            if depth < 0:
                print(f"❌ Extra closing brace on line {i}")
                depth = 0
if depth > 0: print(f"❌ Missing {depth} closing brace(s) at the end.")
elif depth == 0: print("✅ Braces are perfectly balanced!")
