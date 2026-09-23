import re

with open('index.html', 'r') as f:
    html = f.read()

# 1. Remove any old blocker scripts
html = re.sub(r'<style id="video-blocker-style">.*?</style>', '', html, flags=re.DOTALL)
html = re.sub(r'<script id="video-blocker-script">.*?</script>', '', html, flags=re.DOTALL)
html = re.sub(r'<script id="master-player-script">.*?</script>', '', html, flags=re.DOTALL)

# 2. Add the FINAL Blocker CSS
css = """
<style id="video-blocker-style">
#videoBlocker {
    display: none;
    position: absolute;
    top: 0; left: 0;
    width: 100%; height: 100%;
    z-index: 100 !important; /* Higher than everything else */
    background: rgba(0, 0, 0, 0.95);
    color: white;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    cursor: pointer;
}
#videoBlocker .blocker-text {
    font-size: 14px;
    color: #aaa;
    margin-bottom: 15px;
}
#videoBlocker .blocker-btn {
    background: #00e0d0;
    color: #000;
    border: none;
    border-radius: 25px;
    padding: 12px 24px;
    font-size: 16px;
    font-weight: bold;
    display: flex;
    align-items: center;
    gap: 8px;
}
</style>
"""
if '</head>' in html:
    html = html.replace('</head>', css + '\n</head>')

# 3. Add the FINAL Blocker JavaScript
js = """
<script id="video-blocker-script">
document.addEventListener('DOMContentLoaded', function() {
    var fab = document.getElementById('fullArtBox');
    var fsBtn = document.getElementById('fsOverlayBtn');
    var yp = document.getElementById('youtube-player');
    var fa = document.getElementById('fullArt');
    var blocker = document.createElement('div');
    
    blocker.id = 'videoBlocker';
    blocker.innerHTML = '<div class="blocker-text">Up Next from Similar Songs</div><button class="blocker-btn">▶ Play Next Song</button>';
    if (fab) { fab.appendChild(blocker); }

    // 1. Fullscreen Toggle
    if (fsBtn) {
        fsBtn.addEventListener('click', function(e) {
            e.stopPropagation();
            var isFull = fab.classList.contains('is-fullscreen');
            if (!isFull) {
                fab.classList.add('is-fullscreen');
                if (fab.requestFullscreen) fab.requestFullscreen();
            } else {
                fab.classList.remove('is-fullscreen');
                if (document.exitFullscreen) document.exitFullscreen();
            }
        });
    }
    document.addEventListener('fullscreenchange', function() {
        if (!document.fullscreenElement) fab.classList.remove('is-fullscreen');
    });

    // 2. Show/Hide Video logic
    var originalPlayYoutube = window.playYoutube;
    window.playYoutube = function(i) {
        if (originalPlayYoutube) originalPlayYoutube(i);
        if (yp) yp.style.display = 'block';
        if (fa) fa.style.display = 'none';
        if (fsBtn) fsBtn.style.display = 'block';
        if (blocker) blocker.style.display = 'none';
    };

    var originalPlayDbSong = window.playDbSong;
    window.playDbSong = function(i) {
        if (originalPlayDbSong) originalPlayDbSong(i);
        if (yp) yp.style.display = 'none';
        if (fa) fa.style.display = 'block';
        if (fsBtn) fsBtn.style.display = 'none';
        if (blocker) blocker.style.display = 'none';
        fab.classList.remove('is-fullscreen');
    };

    // 3. When the user clicks the custom "Play Next" button
    if (blocker) {
        blocker.onclick = function() {
            blocker.style.display = 'none';
            if (yp) yp.style.display = 'block'; // Show the iframe again
            
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
                if (typeof nextTrack === 'function') nextTrack();
            }
        };
    }

    // 4. THE TRAP: Constantly check if the YouTube player exists and hook into its END event
    var checkPlayer = setInterval(function() {
        if (window.ytPlayer && typeof window.ytPlayer.addEventListener === 'function' && !window.ytPlayer._endHookAttached) {
            window.ytPlayer._endHookAttached = true; // Make sure we only attach once
            
            window.ytPlayer.addEventListener('onStateChange', function(e) {
                if (e.data === 1) { // Playing
                    if (blocker) blocker.style.display = 'none';
                    if (yp) yp.style.display = 'block';
                } else if (e.data === 2) { // Paused
                    if (blocker) blocker.style.display = 'none';
                } else if (e.data === 0) { // ENDED
                    // THE TRAP SPRINGS! Hide YouTube completely and show our custom button.
                    if (yp) yp.style.display = 'none';
                    if (blocker) blocker.style.display = 'flex';
                }
            });
        }
    }, 500);
});
</script>
"""
if '</body>' in html:
    html = html.replace('</body>', js + '\n</body>')

with open('index.html', 'w') as f:
    f.write(html)
print("✅ YouTube iframe trap installed! It will be hidden when the video ends.")
