import re

with open('index.html', 'r') as f:
    html = f.read()

# 1. Add CSS for the size control panel
css = """
<style id="size-control-style">
#sizeControlPanel {
    display: none;
    position: absolute;
    top: 50px;
    left: 10px;
    right: 10px;
    z-index: 100;
    justify-content: center;
    gap: 10px;
}
.size-btn {
    background: rgba(0,224,208,0.2);
    color: #00e0d0;
    border: 1px solid #00e0d0;
    padding: 5px 12px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: bold;
    cursor: pointer;
}
.size-btn.active { background: #00e0d0; color: #000; }
.player-size-small { width: 60% !important; height: 180px !important; margin: 0 auto; }
.player-size-medium { width: 85% !important; height: 240px !important; margin: 0 auto; }
.player-size-large { width: 100% !important; height: 350px !important; }
.player-size-fullscreen {
    position: fixed !important;
    top: 0 !important; left: 0 !important;
    width: 100vw !important; height: 100vh !important;
    z-index: 99999 !important;
    border-radius: 0 !important;
    background: #000 !important;
}
</style>
"""
if '#sizeControlPanel {' not in html:
    if '</head>' in html:
        html = html.replace('</head>', css + '\n</head>')

# 2. Add the HTML buttons into the fullArtBox
if 'id="sizeControlPanel"' not in html:
    html = re.sub(
        r'(<div[^>]*id="fullArtBox"[^>]*>)',
        r'\1\n<div id="sizeControlPanel"><button class="size-btn" onclick="setPlayerSize(\'small\')">Small</button><button class="size-btn active" onclick="setPlayerSize(\'medium\')">Medium</button><button class="size-btn" onclick="setPlayerSize(\'large\')">Large</button><button class="size-btn" onclick="setPlayerSize(\'full\')">Fullscreen</button></div>',
        html
    )

# 3. Add the JavaScript logic
js = """
<script id="size-control-script">
document.addEventListener('DOMContentLoaded', function() {
    window.setPlayerSize = function(size) {
        var fab = document.getElementById('fullArtBox');
        if (!fab) return;
        
        // Remove previous classes
        fab.classList.remove('player-size-small', 'player-size-medium', 'player-size-large', 'player-size-fullscreen');
        
        // Add selected class
        if (size === 'small') fab.classList.add('player-size-small');
        else if (size === 'medium') fab.classList.add('player-size-medium');
        else if (size === 'large') fab.classList.add('player-size-large');
        else if (size === 'full') fab.classList.add('player-size-fullscreen');
        
        // Update button active state
        var btns = document.querySelectorAll('.size-btn');
        btns.forEach(function(b) { b.classList.remove('active'); });
        if (event && event.target) event.target.classList.add('active');
    };

    // Wrap the existing playYoutube to show the size panel
    var originalPlayYoutube = window.playYoutube;
    window.playYoutube = function(i) {
        if (originalPlayYoutube) originalPlayYoutube(i);
        var panel = document.getElementById('sizeControlPanel');
        if (panel) panel.style.display = 'flex';
    };

    // Wrap the existing playDbSong to hide the size panel
    var originalPlayDbSong = window.playDbSong;
    window.playDbSong = function(i) {
        if (originalPlayDbSong) originalPlayDbSong(i);
        var panel = document.getElementById('sizeControlPanel');
        if (panel) panel.style.display = 'none';
        var fab = document.getElementById('fullArtBox');
        if (fab) fab.classList.remove('player-size-small', 'player-size-medium', 'player-size-large', 'player-size-fullscreen');
    };
});
</script>
"""
if 'id="size-control-script"' not in html:
    if '</body>' in html:
        html = html.replace('</body>', js + '\n</body>')

with open('index.html', 'w') as f:
    f.write(html)
print("✅ Customizable size panel added! (Small, Medium, Large, Fullscreen)")
