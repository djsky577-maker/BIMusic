import re

with open('index.html', 'r') as f:
    html = f.read()

# 1. Remove the broken draggable script and CSS
html = re.sub(r'<style id="draggable-mini-style">.*?</style>', '', html, flags=re.DOTALL)
html = re.sub(r'<script id="draggable-mini-script">.*?</script>', '', html, flags=re.DOTALL)
html = re.sub(r'<style id="fixed-mini-player-style">.*?</style>', '', html, flags=re.DOTALL)

# 2. Add the RESTORED CSS (Original size/place, but visible over artist profile)
css = """
<style id="fixed-mini-player-style">
/* Restore original size and place */
#miniPlayer {
    position: fixed !important;
    bottom: 65px !important; /* Sits right above the bottom nav */
    left: 0 !important;
    width: 100% !important;
    margin: 0 !important;
    border-radius: 0 !important;
    z-index: 1500 !important; /* HIGHER than artist modal, LOWER than full player */
    box-shadow: 0 -5px 20px rgba(0,0,0,0.7) !important;
    transition: transform 0.3s ease !important;
}

/* Ensure the artist modal sits BELOW the mini player so it stays visible */
#artistModal {
    z-index: 1000 !important;
}

/* Ensure the full player sits ABOVE the mini player */
#fullPlayer {
    z-index: 9999 !important;
}

/* Add padding to the bottom of the artist modal so the last song isn't hidden behind the mini player */
#artistModal .modal-content, #artistModal > div {
    padding-bottom: 80px !important;
}
</style>
"""
if '</head>' in html:
    html = html.replace('</head>', css + '\n</head>')

with open('index.html', 'w') as f:
    f.write(html)
print("✅ Mini-player restored to original size and place, but stays visible over artist profiles!")
