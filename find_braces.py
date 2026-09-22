import re
with open('index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

stack = []
for i, line in enumerate(lines, 1):
    clean_line = re.sub(r'".*?"', '""', line)
    clean_line = re.sub(r"'.*?'", "''", clean_line)
    
    for char in clean_line:
        if char == '{':
            stack.append(i) 
        elif char == '}':
            if stack:
                stack.pop()
            else:
                print(f"❌ Extra closing brace on line {i}")

if stack:
    print(f"\n❌ Missing {len(stack)} closing brace(s)!")
    print(f"👉 These opening braces were never closed on lines: {stack}")
    print("Go to those exact lines in your index.html and add } at the end of those blocks.")
else:
    print("✅ Braces are perfectly balanced!")
