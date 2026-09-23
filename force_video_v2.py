import re

with open('index.html', 'r') as f:
    html = f.read()

# Remove any old attempts
html = re.sub(r'<style id="video-player-style">.*?</style>', '', html, flags=re.DOTALL)
html = re.sub(r'<script id="video-player-script">.*?</script>', '', html, flags=re.DOTALL)

# 1. Inject CSS for the video player
css = """
<style id="video-player-style">
#fullArtBox { position: relative; overflow: hidden; border-radius: 12px; }
#youtube-player { position: absolute; top: 0; left: 0; width: 100%; height: 100%; display: none; z-index: 10; background: #000; }
#youtube-player iframe { width: 100% !important; height: 100% !important; object-fit: cover; }
</style>
"""
if '</head>' in html:
    html = html.replace('</head>', css + '\n</head>')

# 2. Inject a script at the end that OVERRIDES the player functions
js = """
<script id="video-player-script">
document.addEventListener('DOMContentLoaded', function() {
    // Override playYoutube to show video
    window.playYoutube = function(i) {
        currentSource = 'youtube';
        currentIndex = i;
        document.getElementById('audioPlayer').pause();
        var t = ytResults[i];
        if (!t) return;
        var yp = document.getElementById('youtube-player');
        var fa = document.getElementById('fullArt');
        if (yp) yp.style.display = 'block';
        if (fa) fa.style.display = 'none';
        setTrackInfo(t.snippet.thumbnails.high.url, t.snippet.title, t.snippet.channelTitle);
        ensurePlayer(t.id.videoId);
        simPool = []; simSimilar = []; simTitle = t.snippet.title; simQIdx = 0;
        document.getElementById('similarGrid').innerHTML = '';
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
print("✅ Video player script injected successfully!")
