import re

with open('index.html', 'r') as f:
    html = f.read()

# 1. Remove any old back button styles if they exist
html = re.sub(r'<style id="blue-glass-back-style">.*?</style>', '', html, flags=re.DOTALL)

# 2. Add the Liquid Blue Glass CSS
css = """
<style id="blue-glass-back-style">
/* Target common back, close, and header navigation buttons */
#backBtn, .back-btn, .back-button, .close-btn, #closeArtistModal, #closeFullPlayer, [onclick*="back"], [onclick*="close"], [onclick*="switchTab('home')"] {
    background: rgba(40, 80, 200, 0.25) !important; /* Soft translucent blue */
    backdrop-filter: blur(12px) !important;
    -webkit-backdrop-filter: blur(12px) !important;
    border: 1px solid rgba(80, 130, 255, 0.4) !important; /* Soft blue border */
    border-radius: 12px !important;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.4), 0 0 10px rgba(40, 80, 200, 0.3) !important;
    color: #fff !important;
    transition: all 0.3s ease !important;
    padding: 8px 12px !important;
    display: inline-flex !important;
    align-items: center !important;
    justify-content: center !important;
    cursor: pointer !important;
}

/* When you tap it, it glows brighter blue */
#backBtn:active, .back-btn:active, .back-button:active, .close-btn:active, #closeArtistModal:active, #closeFullPlayer:active, [onclick*="back"]:active, [onclick*="close"]:active, [onclick*="switchTab('home')"]:active {
    background: rgba(60, 120, 255, 0.45) !important;
    box-shadow: 0 0 20px rgba(60, 120, 255, 0.6) !important;
    transform: scale(0.95);
    border: 1px solid rgba(100, 150, 255, 0.8) !important;
}

/* If the back button contains an SVG icon, give it a blue glow */
#backBtn svg, .back-btn svg, .back-button svg, .close-btn svg {
    fill: #fff !important;
    filter: drop-shadow(0 0 5px rgba(60, 120, 255, 0.8));
}
</style>
"""
if '</head>' in html:
    html = html.replace('</head>', css + '\n</head>')

with open('index.html', 'w') as f:
    f.write(html)
print("✅ Liquid Blue Glass back button added!")
