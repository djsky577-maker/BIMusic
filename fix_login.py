import re
import sys

print("=== B.I Music Login Fixer ===")
url = input("Paste your Supabase Project URL: ").strip()
key = input("Paste your Supabase Anon Key: ").strip()

if not url or not key:
    print("❌ Error: URL and Key cannot be empty.")
    sys.exit(1)

with open('index.html', 'r') as f:
    html = f.read()

# 1. Add Supabase CDN if missing
cdn_tag = '<script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>'
if 'supabase-js@2' not in html:
    if '</head>' in html:
        html = html.replace('</head>', f'    {cdn_tag}\n</head>')
    else:
        html = cdn_tag + '\n' + html
    print("✅ Added Supabase CDN to <head>")
else:
    print("✅ Supabase CDN already present")

# 2. Add db initialization right after the first <script> tag
js_init = f"\n    const SUPABASE_URL = '{url}';\n    const SUPABASE_ANON_KEY = '{key}';\n    const db = supabase.createClient(SUPABASE_URL, SUPABASE_ANON_KEY);\n"

if 'const db = supabase.createClient' in html:
    print("✅ Supabase initialization already exists in the code.")
else:
    # Find the first script tag that does NOT have a src attribute
    match = re.search(r'<script(?![^>]*src=)[^>]*>', html)
    if match:
        insert_pos = match.end()
        html = html[:insert_pos] + js_init + html[insert_pos:]
        print("✅ Inserted Supabase initialization into the main <script> block.")
    else:
        print("❌ Error: Could not find a plain <script> tag to insert the code into.")

with open('index.html', 'w') as f:
    f.write(html)

print("✅ Done! Your index.html has been updated.")
