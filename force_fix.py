import re

with open('index.html', 'r') as f:
    html = f.read()

# 1. Remove any existing db declarations to avoid conflicts
html = re.sub(r"var db\s*=\s*supabase\.createClient\([^)]*\);", "", html)
html = re.sub(r"db\s*=\s*supabase\.createClient\([^)]*\);", "", html)

# 2. Find SUPABASE_KEY and inject the global db variable right after it
match = re.search(r"var SUPABASE_KEY\s*=\s*['\"].*?['\"];", html)
if match:
    key_line = match.group(0)
    global_db_code = key_line + "\n    window.db = supabase.createClient(SUPABASE_URL, SUPABASE_KEY);"
    html = html.replace(key_line, global_db_code)
    print("✅ Moved database connection to global scope.")
else:
    print("❌ Could not find SUPABASE_KEY line. Check your file.")

# 3. Add a debug alert inside handleAuth to verify it's firing and db exists
# Look for 'async function handleAuth(' and add alert right after the first brace
if "async function handleAuth(" in html:
    parts = html.split("async function handleAuth(", 1)
    # Find the first '{' after the function declaration
    brace_idx = parts[1].find('{')
    if brace_idx != -1:
        alert_code = "{\n        alert('Button clicked! DB status: ' + (typeof window.db !== 'undefined' ? 'CONNECTED' : 'MISSING'));"
        parts[1] = parts[1][:brace_idx] + alert_code + parts[1][brace_idx+1:]
        html = parts[0] + "async function handleAuth(" + parts[1]
        print("✅ Added debug alert to login button.")
else:
    print("❌ Could not find the handleAuth function.")

with open('index.html', 'w') as f:
    f.write(html)
