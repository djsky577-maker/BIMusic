with open('index.html', 'r') as f:
    lines = f.readlines()

# Line 275 (index 274) is missing 3 closing braces
lines[274] = lines[274].rstrip() + '}}}\n'

# Line 291 (index 290) is missing 1 closing brace
lines[290] = lines[290].rstrip() + '}\n'

with open('index.html', 'w') as f:
    f.writelines(lines)

print("✅ Added 3 braces to line 275 and 1 brace to line 291!")
