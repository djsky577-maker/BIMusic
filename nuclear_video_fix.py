import re

with open('index.html', 'r') as f:
    html = f.read()

# Remove any old failed attempts
html = re.sub(r'<style id="video-fix-style">.*?</style>', '', html, flags=re.DOTALL)
html = re.sub(r'<script id="video-player-script">.*?</script>', '', html, flags=re.DOTALL)

# 1. Bulletproof CSS
css = """
<style id="video-fix-style">
#fullArtBox { position: relative !important; overflow: hidden !important; border-radius: 12px !important; }
#youtube-player { position: absolute !important; top: 0 !important; left: 0 !important; width: 100% !important; height: 100% !important; z-index: 10 !important; display: none; }
#youtube-player iframe { width: 100% !important; height: 100% !important; position: absolute !important; top: 0 !important; left: 0 !important; }
</style>
"""
if '</head>' in html:
    html = html.replace('</head>', css + '\n</head>')

# 2. JavaScript DOM Mover and Function Override
js = """
<script id="video-player-script">
document.addEventListener('DOMContentLoaded', function() {
    // Physically move the youtube-player div inside the fullArtBox
    var yp = document.getElementById('youtube-player');
    var fab = document.getElementById('fullArtBox');
    if (yp && fab) {
        fab.appendChild(yp);
    }

    // Override playYoutube to show video
    window.playYoutube = function(i) {
        currentSource = 'youtube';
        currentIndex = i;
        var ap = document.getElementById('audioPlayer');
        if(ap) ap.pause();
        var t = ytResults[i];
        if (!t) return;
        var yp = document.getElementById('youtube-player');
        var fa = document.getElementById('fullArt');
        if (yp) yp.style.display = 'block';
        if (fa) fa.style.display = 'none';
        setTrackInfo(t.snippet.thumbnails.high.url, t.snippet.title, t.snippet.channelTitle);
        ensurePlayer(t.id.videoId);
        simPool = []; simSimilar = []; simTitle = t.snippet.title; simQIdx = 0;
        var sg = document.getElementById('similarGrid');
        if(sg) sg.innerHTML = '';
        for (var k = 0; k < 5; k++) loadSimilarSongs();
    };

    // Override playDbSong to show album art
    window.playDbSong = function(i) {
        currentSource = 'db';
        currentIndex = i;
        if (ytPlayer && ytPlayer.pauseVideo) ytPlayer.pauseVideo();
        var yp = document.getElementById('youtube-player');
        var fa = document.getElementById('fullArt');
        if (yp) yp.style.display = 'none';
        if (fa) fa.style.display = 'block';
        var s = songs[i];
        if (!s) return;
        setTrackInfo(s.cover_art_url || 'https://via.placeholder.com/150', s.title, s.artist_name);
        var p = document.getElementById('audioPlayer');
        p.src = s.audio_url;
        p.playbackRate = playbackSpeed;
        p.play();
        isPlaying = true;
        updateAllIcons();
    };
});
</script>
"""
if '</body>' in html:
    html = html.replace('</body>', js + '\n</body>')

with open('index.html', 'w') as f:
    f.write(html)
print("✅ Nuclear video fix applied!")
