import re

with open('index.html', 'r') as f:
    html = f.read()

# 1. Remove all previous messy video CSS and scripts
html = re.sub(r'<style id="youtube-clean-style">.*?</style>', '', html, flags=re.DOTALL)
html = re.sub(r'<script id="youtube-clean-script">.*?</script>', '', html, flags=re.DOTALL)
html = re.sub(r'<style id="size-control-style">.*?</style>', '', html, flags=re.DOTALL)
html = re.sub(r'<div id="sizeControlPanel">.*?</div>', '', html, flags=re.DOTALL)
html = re.sub(r'<script id="size-control-script">.*?</script>', '', html, flags=re.DOTALL)
html = re.sub(r'<style id="fs-btn-style">.*?</style>', '', html, flags=re.DOTALL)
html = re.sub(r'<button id="fsBtn".*?</button>', '', html, flags=re.DOTALL)
html = re.sub(r'<script id="fs-btn-script">.*?</script>', '', html, flags=re.DOTALL)

# 2. Add the Sticky & Fullscreen CSS
css = """
<style id="sticky-fs-style">
/* Sticky container */
#fullArtBox {
    position: sticky !important;
    top: 0 !important;
    z-index: 500 !important;
    width: 100% !important;
    max-width: 450px !important;
    aspect-ratio: 16 / 9 !important;
    height: auto !important;
    overflow: hidden !important;
    border-radius: 12px !important;
    margin: 0 auto 15px auto !important;
    background: #000 !important;
    transition: border-radius 0.3s ease, width 0.3s ease, height 0.3s ease;
    cursor: pointer;
}
/* Fullscreen override */
#fullArtBox.is-fullscreen {
    position: fixed !important;
    top: 0 !important; left: 0 !important;
    width: 100vw !important; height: 100vh !important;
    max-width: 100vw !important;
    aspect-ratio: auto !important;
    border-radius: 0 !important;
    margin: 0 !important;
    z-index: 99999 !important;
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
    width: 100% !important; height: 100% !important;
    object-fit: cover !important;
    display: block !important;
}
/* Fullscreen icon overlay */
#fsOverlayBtn {
    position: absolute;
    bottom: 10px; right: 10px;
    z-index: 50;
    background: rgba(0,0,0,0.6);
    color: white;
    border: none; border-radius: 5px;
    padding: 5px 10px;
    font-size: 18px;
    display: none;
}
</style>
"""
if '</head>' in html:
    html = html.replace('</head>', css + '\n</head>')

# 3. Add the overlay button and the JavaScript logic
js = """
<button id="fsOverlayBtn" title="Toggle Fullscreen">⛶</button>
<script id="sticky-fs-script">
document.addEventListener('DOMContentLoaded', function() {
    var fab = document.getElementById('fullArtBox');
    var fsBtn = document.getElementById('fsOverlayBtn');
    var yp = document.getElementById('youtube-player');
    var fa = document.getElementById('fullArt');

    // Move elements into place
    if (yp && fab) { fab.appendChild(yp); }
    if (fsBtn && fab) { fab.appendChild(fsBtn); }

    // Toggle Fullscreen Function
    window.toggleFS = function() {
        var isFull = fab.classList.contains('is-fullscreen');
        if (!isFull) {
            fab.classList.add('is-fullscreen');
            if (fab.requestFullscreen) fab.requestFullscreen();
        } else {
            fab.classList.remove('is-fullscreen');
            if (document.exitFullscreen) document.exitFullscreen();
        }
    };

    // Tap on the video box to go fullscreen
    if (fab) {
        fab.addEventListener('click', function(e) {
            // If they click the YouTube iframe itself (to play/pause), don't trigger fullscreen
            if (e.target.tagName === 'IFRAME') return;
            toggleFS();
        });
    }

    // Fullscreen button tap
    if (fsBtn) {
        fsBtn.addEventListener('click', function(e) {
            e.stopPropagation();
            toggleFS();
        });
    }

    // Listen for native fullscreen exit
    document.addEventListener('fullscreenchange', function() {
        if (!document.fullscreenElement) {
            fab.classList.remove('is-fullscreen');
        }
    });

    // Override playYoutube to show video and fullscreen button
    var originalPlayYoutube = window.playYoutube;
    window.playYoutube = function(i) {
        if (originalPlayYoutube) originalPlayYoutube(i);
        if (yp) yp.style.display = 'block';
        if (fa) fa.style.display = 'none';
        if (fsBtn) fsBtn.style.display = 'block';
    };

    // Override playDbSong to show album art and hide fullscreen button
    var originalPlayDbSong = window.playDbSong;
    window.playDbSong = function(i) {
        if (originalPlayDbSong) originalPlayDbSong(i);
        if (yp) yp.style.display = 'none';
        if (fa) fa.style.display = 'block';
        if (fsBtn) fsBtn.style.display = 'none';
        fab.classList.remove('is-fullscreen');
    };
});
</script>
"""
if '</body>' in html:
    html = html.replace('</body>', js + '\n</body>')

with open('index.html', 'w') as f:
    f.write(html)
print("✅ Sticky video player + Tap-to-Fullscreen added!")
