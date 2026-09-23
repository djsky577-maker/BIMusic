import re

with open('index.html', 'r') as f:
    html = f.read()

# 1. Remove ALL previous size control, fullscreen, and button scripts/styles
html = re.sub(r'<style id="size-control-style">.*?</style>', '', html, flags=re.DOTALL)
html = re.sub(r'<div id="sizeControlPanel">.*?</div>', '', html, flags=re.DOTALL)
html = re.sub(r'<script id="size-control-script">.*?</script>', '', html, flags=re.DOTALL)
html = re.sub(r'<style id="fs-btn-style">.*?</style>', '', html, flags=re.DOTALL)
html = re.sub(r'<button id="fsBtn".*?</button>', '', html, flags=re.DOTALL)
html = re.sub(r'<script id="fs-btn-script">.*?</script>', '', html, flags=re.DOTALL)

# 2. Add the clean YouTube-style CSS
css = """
<style id="youtube-clean-style">
#fullArtBox {
    position: relative !important;
    width: 100% !important;
    max-width: 450px !important;
    aspect-ratio: 16 / 9 !important; /* Perfect YouTube video shape */
    height: auto !important;
    overflow: hidden !important;
    border-radius: 12px !important;
    margin: 0 auto 15px auto !important;
    background: #000 !important;
}
#youtube-player {
    position: absolute !important;
    top: 0 !important; left: 0 !important;
    width: 100% !important; height: 100% !important;
    display: none;
    z-index: 10 !important;
}
#youtube-player iframe {
    width: 100% !important; height: 100% !important;
    border: none !important;
}
#fullArt {
    width: 100% !important;
    height: 100% !important;
    object-fit: cover !important;
    display: block !important;
}
</style>
"""
if '</head>' in html:
    html = html.replace('</head>', css + '\n</head>')

# 3. Add the show/hide logic
js = """
<script id="youtube-clean-script">
document.addEventListener('DOMContentLoaded', function() {
    // Physically move the youtube-player into the art box
    var yp = document.getElementById('youtube-player');
    var fab = document.getElementById('fullArtBox');
    if (yp && fab) { fab.appendChild(yp); }

    // Override playYoutube to show video
    var originalPlayYoutube = window.playYoutube;
    window.playYoutube = function(i) {
        if (originalPlayYoutube) originalPlayYoutube(i);
        var yp = document.getElementById('youtube-player');
        var fa = document.getElementById('fullArt');
        if (yp) yp.style.display = 'block';
        if (fa) fa.style.display = 'none';
    };

    // Override playDbSong to show album art
    var originalPlayDbSong = window.playDbSong;
    window.playDbSong = function(i) {
        if (originalPlayDbSong) originalPlayDbSong(i);
        var yp = document.getElementById('youtube-player');
        var fa = document.getElementById('fullArt');
        if (yp) yp.style.display = 'none';
        if (fa) fa.style.display = 'block';
    };
});
</script>
"""
if '</body>' in html:
    html = html.replace('</body>', js + '\n</body>')

with open('index.html', 'w') as f:
    f.write(html)
print("✅ Cleaned up! Video is now a perfect 16:9 YouTube box.")
