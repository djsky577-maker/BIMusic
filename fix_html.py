with open('index.html', 'r') as f:
    content = f.read()

# Check if it's missing the HTML boilerplate
if not content.strip().startswith('<!DOCTYPE html>') and not content.strip().startswith('<html'):
    # Find where the JavaScript starts (usually 'const SUPABASE_URL' or 'async function')
    if '<script>' not in content:
        content = '<script>\n' + content + '\n</script>'
    
    new_content = '''<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>B.I Music</title>
</head>
<body>
''' + content + '''
</body>
</html>'''
    
    with open('index.html', 'w') as f:
        f.write(new_content)
    print("✅ Fixed! Wrapped the JavaScript in proper HTML tags.")
else:
    print("✅ HTML structure already looks correct.")

