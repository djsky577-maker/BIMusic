import re

with open('index.html', 'r') as f:
    html = f.read()

# 1. Remove any previous auto-shuffle scripts to avoid conflicts
html = re.sub(r'<script id="final-player-script">.*?</script>', '', html, flags=re.DOTALL)
html = re.sub(r'<script id="auto-shuffle-script">.*?</script>', '', html, flags=re.DOTALL)
html = re.sub(r'<script id="ultimate-player-script">.*?</script>', '', html, flags=re.DOTALL)

# 2. Inject the NEW logic specifically for the "More Videos" replacement
js = """
<script id="final-player-script">
document.addEventListener('DOMContentLoaded', function() {
    var fab = document.getElementById('fullArtBox');
    var fsBtn = document.getElementById('fsOverlayBtn');
    var yp = document.getElementById('youtube-player');
    var fa = document.getElementById('fullArt');

    if (yp && fab) { fab.appendChild(yp); }
    if (fsBtn && fab) { fab.appendChild(fsBtn); }

    // ONLY the ⛶ button toggles fullscreen (no accidental fullscreen on video tap)
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

    var originalPlayYoutube = window.playYoutube;
    window.playYoutube = function(i) {
        if (originalPlayYoutube) originalPlayYoutube(i);
        if (yp) yp.style.display = 'block';
        if (fa) fa.style.display = 'none';
        if (fsBtn) fsBtn.style.display = 'block';
    };

    var originalPlayDbSong = window.playDbSong;
    window.playDbSong = function(i) {
        if (originalPlayDbSong) originalPlayDbSong(i);
        if (yp) yp.style.display = 'none';
        if (fa) fa.style.display = 'block';
        if (fsBtn) fsBtn.style.display = 'none';
        fab.classList.remove('is-fullscreen');
    };
});

// INTERCEPT YOUTUBE END SCREEN
window.onYouTubeIframeAPIReady = function() {
    ytPlayer = new YT.Player('youtube-player', {
        height: '100%',
        width: '100%',
        playerVars: {
            playsinline: 1,
            controls: 1,
            autoplay: 1,
            rel: 0, // Kills YouTube's "More Videos" end screen
            modestbranding: 1,
            enablejsapi: 1
        },
        events: {
            'onReady': function() { ytReady = true; },
            'onStateChange': function(e) {
                if (e.data === 1) { 
                    isPlaying = true; updateAllIcons();
                } else if (e.data === 2) { 
                    isPlaying = false; updateAllIcons();
                } else if (e.data === 0) { 
                    // VIDEO ENDED! 
                    // Instead of shuffling the MAIN queue, we grab a random song from SIMILAR SONGS
                    if (window.simPool && window.simPool.length > 0) {
                        // Pick a random song from Similar Songs (Mixed)
                        var randomIndex = Math.floor(Math.random() * window.simPool.length);
                        
                        // Temporarily set the queue to Similar Songs so "Next" goes through them
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
                        
                        // Play the random Similar Song
                        window.playYoutube(randomIndex);
                    } else {
                        // Fallback if no Similar Songs are loaded yet
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
print("✅ Done! End screen replaced with mixed Similar Songs.")
