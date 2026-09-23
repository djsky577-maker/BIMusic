import re

with open('index.html', 'r') as f:
    html = f.read()

# 1. Remove the old generic glass style
html = re.sub(r'<style id="liquid-glass-style">.*?</style>', '', html, flags=re.DOTALL)

# 2. Add the new Teal-Tinted Liquid Glass CSS
css = """
<style id="teal-glass-style">
/* Deep dark base so the teal pops */
body { background: #050505 !important; }

/* 1. Cards (Home, For You, Genres) */
.card, .list-item, .artist-box {
    background: rgba(0, 224, 208, 0.05) !important;
    backdrop-filter: blur(16px) !important;
    -webkit-backdrop-filter: blur(16px) !important;
    border: 1px solid rgba(0, 224, 208, 0.15) !important;
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.6), inset 0 0 10px rgba(0, 224, 208, 0.05) !important;
    border-radius: 16px !important;
    transition: all 0.3s ease !important;
}

/* When you tap them, they glow brighter teal */
.card:active, .list-item:active, .artist-box:active {
    background: rgba(0, 224, 208, 0.25) !important;
    border: 1px solid rgba(0, 224, 208, 0.6) !important;
    box-shadow: 0 0 20px rgba(0, 224, 208, 0.4) !important;
    transform: scale(0.97);
}

/* 2. Bottom Navigation & Mini Player */
.bottom-nav, nav, .mini-player {
    background: rgba(0, 15, 15, 0.85) !important;
    backdrop-filter: blur(25px) !important;
    -webkit-backdrop-filter: blur(25px) !important;
    border-top: 1px solid rgba(0, 224, 208, 0.25) !important;
    box-shadow: 0 -8px 32px 0 rgba(0, 0, 0, 0.9), 0 -2px 15px rgba(0, 224, 208, 0.1) !important;
}

/* 3. Login Box (Auth) */
.auth-box {
    background: rgba(0, 15, 15, 0.8) !important;
    backdrop-filter: blur(20px) !important;
    -webkit-backdrop-filter: blur(20px) !important;
    border: 1px solid rgba(0, 224, 208, 0.2) !important;
    border-radius: 20px !important;
    box-shadow: 0 15px 50px rgba(0, 0, 0, 0.8), 0 0 30px rgba(0, 224, 208, 0.15) !important;
}

/* Login Inputs */
.auth-box input {
    background: rgba(0, 0, 0, 0.5) !important;
    border: 1px solid rgba(0, 224, 208, 0.2) !important;
    border-radius: 10px !important;
    color: #fff !important;
    backdrop-filter: blur(5px) !important;
    transition: all 0.3s ease !important;
}
.auth-box input:focus {
    border-color: #00e0d0 !important;
    box-shadow: 0 0 15px rgba(0, 224, 208, 0.4) !important;
}

/* 4. The 'Up Next' card in the video player */
#videoBlocker {
    background: rgba(0, 15, 15, 0.9) !important;
    backdrop-filter: blur(20px) !important;
    -webkit-backdrop-filter: blur(20px) !important;
    border-top: 1px solid rgba(0, 224, 208, 0.5) !important;
    box-shadow: 0 -4px 20px rgba(0, 224, 208, 0.2) !important;
}
</style>
"""
if '</head>' in html:
    html = html.replace('</head>', css + '\n</head>')

with open('index.html', 'w') as f:
    f.write(html)
print("✅ Teal Liquid Glass UI injected successfully!")
