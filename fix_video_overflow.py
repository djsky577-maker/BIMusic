import re

with open('index.html', 'r') as f:
    html = f.read()

# 1. Extract the youtube-player div (if it exists)
match = re.search(r'<div id="youtube-player"[^>]*></div>', html)
player_div = match.group(0) if match else '<div id="youtube-player"></div>'

# 2. Remove it from its current location
if match:
    html = html.replace(player_div, '')

# 3. Find the fullArtBox and place the player inside it
# Look for the opening tag of fullArtBox
box_match = re.search(r'(<div[^>]*id="fullArtBox"[^>]*>)', html)
if box_match:
    box_tag = box_match.group(1)
    # Insert the player div right after the opening tag
    html = html.replace(box_tag, box_tag + '\n' + player_div)
    print("✅ Moved video player inside the art box!")
else:
    print("❌ Could not find fullArtBox. Check HTML.")

# 4. Add strict CSS to keep it contained
css = """
<style id="video-fix-style">
#fullArtBox { position: relative !important; overflow: hidden !important; border-radius: 12px !important; }
#youtube-player { position: absolute !important; top: 0 !important; left: 0 !important; width: 100% !important; height: 100% !important; z-index: 10 !important; }
#youtube-player iframe { width: 100% !important; height: 100% !important; object-fit: cover !important; }
</style>
"""
# Remove old style if exists
html = re.sub(r'<style id="video-fix-style">.*?</style>', '', html, flags=re.DOTALL)
if '</head>' in html:
    html = html.replace('</head>', css + '\n</head>')

with open('index.html', 'w') as f:
    f.write(html)
print("✅ Video overflow fixed!")
