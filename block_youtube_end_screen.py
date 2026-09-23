import re

with open('index.html', 'r') as f:
    html = f.read()

# 1. Remove any old blocker scripts
html = re.sub(r'<style id="video-blocker-style">.*?</style>', '', html, flags=re.DOTALL)
html = re.sub(r'<script id="video-blocker-script">.*?</script>', '', html, flags=re.DOTALL)

# 2. Add CSS for the custom end screen blocker
css = """
<style id="video-blocker-style">
#videoBlocker {
    display: none;
    position: absolute;
    top: 0; left: 0;
    width: 100%; height: 100%;
    z-index: 20; /* Higher than the iframe (z-index 10), lower than the fullscreen button (z-index 50) */
    background: rgba(0, 0, 0, 0.85);
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
    margin-bottom: 10px;
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

# 3. Add the HTML for the blocker
js = """
<script id="video-blocker-script">
document.addEventListener('DOMContentLoaded', function() {
    var fab = document.getElementById('fullArtBox');
    if (!fab) return;

    // Create the blocker element
    var blocker = document.createElement('div');
    blocker.id = 'videoBlocker';
    blocker.innerHTML = '<div class="blocker-text">Up Next from Similar Songs</div><button class="blocker-btn">▶ Play Next Song</button>';
    
    fab.appendChild(blocker);

    // When the user clicks the blocker, play a random similar song
    blocker.onclick = function() {
        blocker.style.display = 'none';
        
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
            // Fallback if no similar songs are loaded yet
            if (typeof nextTrack === 'function') nextTrack();
        }
    };

    // INTERCEPT YOUTUBE PLAYER STATE CHANGES
    // We use a setInterval to make sure we attach to the player as soon as it's ready
    var checkPlayer = setInterval(function() {
        if (window.ytPlayer && typeof window.ytPlayer.addEventListener === 'function') {
            clearInterval(checkPlayer);
            
            window.ytPlayer.addEventListener('onStateChange', function(e) {
                if (e.data === 1) { // Playing
                    blocker.style.display = 'none';
                } else if (e.data === 2) { // Paused
                    blocker.style.display = 'none';
                } else if (e.data === 0) { // ENDED
                    // Show our custom blocker instead of YouTube's end screen!
                    blocker.style.display = 'flex';
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
print("✅ YouTube end screen blocked and replaced with custom button!")
