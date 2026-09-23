import re

with open('index.html', 'r') as f:
    html = f.read()

# 1. Clean up old injections
html = re.sub(r'<style id="sticky-fs-style">.*?</style>', '', html, flags=re.DOTALL)
html = re.sub(r'<script id="sticky-fs-script">.*?</script>', '', html, flags=re.DOTALL)
html = re.sub(r'<button id="fsOverlayBtn".*?</button>', '', html, flags=re.DOTALL)
html = re.sub(r'<script id="auto-shuffle-script">.*?</script>', '', html, flags=re.DOTALL)

# 2. Inject the new Bulletproof CSS
css = """
<style id="ultimate-player-style">
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
    cursor: pointer;
}
#fullArtBox.is-fullscreen {
    position: fixed !important;
    top: 0 !important; left: 0 !important;
    width: 100vw !important; height: 100vh !important;
    max-width: 100vw !important;
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
    pointer-events: none; /* Prevents YouTube from stealing clicks or showing its own end screen */
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

# 3. Inject the new JavaScript logic
js = """
<button id="fsOverlayBtn" title="Toggle Fullscreen">⛶</button>
<script id="ultimate-player-script">
document.addEventListener('DOMContentLoaded', function() {
    var fab = document.getElementById('fullArtBox');
    var fsBtn = document.getElementById('fsOverlayBtn');
    var yp = document.getElementById('youtube-player');
    var fa = document.getElementById('fullArt');

    if (yp && fab) { fab.appendChild(yp); }
    if (fsBtn && fab) { fab.appendChild(fsBtn); }

    // Fullscreen Toggle
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

    if (fab) {
        fab.addEventListener('click', function(e) {
            if (e.target.tagName === 'IFRAME') return;
            toggleFS();
        });
    }
    if (fsBtn) {
        fsBtn.addEventListener('click', function(e) {
            e.stopPropagation();
            toggleFS();
        });
    }
    document.addEventListener('fullscreenchange', function() {
        if (!document.fullscreenElement) fab.classList.remove('is-fullscreen');
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

// Override YouTube player initialization to intercept END state and fix errors
window.onYouTubeIframeAPIReady = function() {
    ytPlayer = new YT.Player('youtube-player', {
        height: '100%',
        width: '100%',
        playerVars: {
            playsinline: 1,
            controls: 0,
            autoplay: 1,
            rel: 0,
            modestbranding: 1,
            enablejsapi: 1
        },
        events: {
            'onReady': function() { ytReady = true; },
            'onStateChange': function(e) {
                if (e.data === 1) { // Playing
                    isPlaying = true; updateAllIcons();
                } else if (e.data === 2) { // Paused
                    isPlaying = false; updateAllIcons();
                } else if (e.data === 0) { // ENDED
                    // Auto-shuffle from Similar Songs!
                    if (window.simPool && window.simPool.length > 0) {
                        var ri = Math.floor(Math.random() * window.simPool.length);
                        window.ytResults = window.simPool.map(function(x) {
                            return {
                                id: { videoId: x.id },
                                snippet: {
                                    title: x.title,
                                    channelTitle: x.uploaderName,
                                    thumbnails: { default: { url: x.thumbnail }, high: { url: x.thumbnail } }
                                }
                            };
                        });
                        window.playQueue = window.ytResults;
                        window.playYoutube(ri);
                    } else {
                        // Fallback to normal nextTrack if no similar songs loaded
                        if (typeof nextTrack === 'function') nextTrack();
                    }
                }
            }
        }
    });
};
</script>
"""
if '</body>' in html:
    html = html.replace('</body>', js + '\n</body>')

with open('index.html', 'w') as f:
    f.write(html)
print("✅ Fixed! Auto-shuffle from Similar Songs is ON, Fullscreen is vertical, and 'More Videos' is blocked.")
