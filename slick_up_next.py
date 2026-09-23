import re

with open('index.html', 'r') as f:
    html = f.read()

# 1. Remove all previous blocker scripts and styles
html = re.sub(r'<style id="video-blocker-style">.*?</style>', '', html, flags=re.DOTALL)
html = re.sub(r'<script id="police-patrol-script">.*?</script>', '', html, flags=re.DOTALL)
html = re.sub(r'<script id="video-blocker-script">.*?</script>', '', html, flags=re.DOTALL)

# 2. Add the sleek CSS
css = """
<style id="up-next-style">
#videoBlocker {
    display: none;
    position: absolute;
    bottom: 0; left: 0;
    width: 100%;
    height: 85px;
    z-index: 99999 !important;
    background: rgba(10, 10, 10, 0.95);
    color: white;
    padding: 10px 15px;
    box-sizing: border-box;
    align-items: center;
    gap: 12px;
    cursor: pointer;
    border-radius: 0 0 12px 12px;
    border-top: 2px solid #00e0d0;
    box-shadow: 0 -4px 15px rgba(0,0,0,0.5);
    transition: transform 0.3s ease-in-out;
}
#videoBlocker.show {
    display: flex;
}
#nextSongImg {
    width: 55px;
    height: 55px;
    border-radius: 6px;
    object-fit: cover;
}
#nextSongDetails {
    flex: 1;
    display: flex;
    flex-direction: column;
    overflow: hidden;
}
#nextSongTitle {
    font-size: 14px;
    font-weight: bold;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    color: #fff;
}
#nextSongArtist {
    font-size: 12px;
    color: #aaa;
    margin-top: 2px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}
#nextSongBtn {
    background: #00e0d0;
    color: #000;
    border: none;
    border-radius: 20px;
    padding: 8px 16px;
    font-size: 14px;
    font-weight: bold;
    cursor: pointer;
}
</style>
"""
if '</head>' in html:
    html = html.replace('</head>', css + '\n</head>')

# 3. Add the JavaScript logic
js = """
<script id="up-next-script">
document.addEventListener('DOMContentLoaded', function() {
    var fab = document.getElementById('fullArtBox');
    var fsBtn = document.getElementById('fsOverlayBtn');
    var yp = document.getElementById('youtube-player');
    var fa = document.getElementById('fullArt');
    
    // Create the Up Next card
    var blocker = document.createElement('div');
    blocker.id = 'videoBlocker';
    blocker.innerHTML = '<img id="nextSongImg" src=""><div id="nextSongDetails"><div id="nextSongTitle">Up Next</div><div id="nextSongArtist">Artist</div></div><button id="nextSongBtn">▶ Play</button>';
    if (fab) { fab.appendChild(blocker); }

    var nextSongIndex = -1; // Tracks the random song we picked

    // Fullscreen Toggle
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

    // Show/Hide Video logic
    var originalPlayYoutube = window.playYoutube;
    window.playYoutube = function(i) {
        if (originalPlayYoutube) originalPlayYoutube(i);
        if (yp) yp.style.display = 'block';
        if (fa) fa.style.display = 'none';
        if (fsBtn) fsBtn.style.display = 'block';
        if (blocker) { blocker.classList.remove('show'); blocker.style.display = 'none'; }
        nextSongIndex = -1; // Reset next song on new play
    };

    var originalPlayDbSong = window.playDbSong;
    window.playDbSong = function(i) {
        if (originalPlayDbSong) originalPlayDbSong(i);
        if (yp) yp.style.display = 'none';
        if (fa) fa.style.display = 'block';
        if (fsBtn) fsBtn.style.display = 'none';
        if (blocker) { blocker.classList.remove('show'); blocker.style.display = 'none'; }
        fab.classList.remove('is-fullscreen');
    };

    // Click handler for the Up Next card
    if (blocker) {
        blocker.onclick = function() {
            blocker.classList.remove('show');
            blocker.style.display = 'none';
            if (yp) yp.style.display = 'block'; 
            
            if (nextSongIndex !== -1 && window.simPool && window.simPool.length > 0) {
                // Play the pre-selected song
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
                window.playYoutube(nextSongIndex);
            } else {
                // Fallback if no next song was picked
                if (typeof nextTrack === 'function') nextTrack();
            }
        };
    }

    // --- THE POLICE PATROL (Runs every 0.5 seconds) ---
    setInterval(function() {
        if (window.currentSource !== 'youtube') return;
        if (!window.ytPlayer || typeof window.ytPlayer.getPlayerState !== 'function') return;
        
        try {
            var state = window.ytPlayer.getPlayerState();
            var curTime = window.ytPlayer.getCurrentTime() || 0;
            var dur = window.ytPlayer.getDuration() || 0;

            // 1. Playing state
            if (state === 1) { 
                // If 10 seconds or less are left, show the Up Next card
                if (dur > 0 && (dur - curTime) <= 10) {
                    
                    // Pick a random similar song if we haven't already
                    if (nextSongIndex === -1 && window.simPool && window.simPool.length > 0) {
                        nextSongIndex = Math.floor(Math.random() * window.simPool.length);
                        var next = window.simPool[nextSongIndex];
                        document.getElementById('nextSongImg').src = next.thumbnail;
                        document.getElementById('nextSongTitle').textContent = next.title;
                        document.getElementById('nextSongArtist').textContent = next.uploaderName;
                    }
                    
                    // Show the card
                    if (blocker && !blocker.classList.contains('show')) {
                        blocker.style.display = 'flex';
                        setTimeout(function() { blocker.classList.add('show'); }, 10);
                    }
                }
            } 
            // 2. Ended state
            else if (state === 0) { 
                // Force the card to show if it hasn't already
                if (blocker && !blocker.classList.contains('show')) {
                    if (nextSongIndex === -1 && window.simPool && window.simPool.length > 0) {
                        nextSongIndex = Math.floor(Math.random() * window.simPool.length);
                        var next = window.simPool[nextSongIndex];
                        document.getElementById('nextSongImg').src = next.thumbnail;
                        document.getElementById('nextSongTitle').textContent = next.title;
                        document.getElementById('nextSongArtist').textContent = next.uploaderName;
                    }
                    blocker.style.display = 'flex';
                    setTimeout(function() { blocker.classList.add('show'); }, 10);
                }
            }
            // 3. Paused state (Hide the card if user pauses before the end)
            else if (state === 2) {
                if (blocker) {
                    blocker.classList.remove('show');
                    blocker.style.display = 'none';
                }
            }
        } catch(e) {}
    }, 500);
});
</script>
"""
if '</body>' in html:
    html = html.replace('</body>', js + '\n</body>')

with open('index.html', 'w') as f:
    f.write(html)
print("✅ Slick 'Up Next' card with cover art and details added!")
