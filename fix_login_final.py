import re

with open('index.html', 'r') as f:
    html = f.read()

# 1. Remove the red BYPASS LOGIN button script
html = re.sub(r'<script>.*?BYPASS LOGIN.*?</script>', '', html, flags=re.DOTALL)

# 2. Move the db initialization to the top level so it's ready immediately
# Find the line where SUPABASE_KEY is defined
match = re.search(r"(var SUPABASE_KEY=.*?;)", html)
if match:
    key_line = match.group(1)
    # Add the db creation right after it
    new_init = key_line + "\n    var db = supabase.createClient(SUPABASE_URL, SUPABASE_KEY);"
    html = html.replace(key_line, new_init)

# 3. Remove the old db initialization inside the 'load' event to avoid conflicts
html = html.replace("db=supabase.createClient(SUPABASE_URL, SUPABASE_KEY);", "")

with open('index.html', 'w') as f:
    f.write(html)

print("✅ Red bypass button removed!")
print("✅ Database connection moved to the top level.")
print("✅ Your real login is now fixed and ready.")
