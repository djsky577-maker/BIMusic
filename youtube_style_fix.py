import re

with open('index.html', 'r') as f:
    html = f.read()

# 1. Remove ALL the previous size control garbage
html = re.sub(r'<style id="size-control-style">.*?</style>', '', html, flags=re.DOTALL)
html = re.sub(r'<div id="sizeControlPanel">.*?</div>', '', html, flags=re.DOTALL)
html = re.sub(r'<script id="size-control-script">.*?</script>', '', html, flags=re.DOTALL)
html = re.sub(r'<style id="fs-btn-style">.*?</style>', '', html, flags=re.DOTALL)
html = re.sub(r'<script id="fs-btn-script">.*?</script>', '', html, flags=re.DOTALL)
html = re.sub(r'<button id="fsBtn".*?</button>', '', html, flags=re.DOTALL)

# 2. Add the clean YouTube-style CSS
css = """
<style id="youtube-style-video">
#fullArtBox {
    position: relative !important;
    width: 100% !important;
    height: 240px !important;  /* Standard mobile YouTube size */
    overflow: hidden !important;
    border-radius: 12px !important;
    margin-bottom: 15px !important;
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
    object-fit: contain !important; /* Keeps the video shape, doesn't stretch */
}
#fullArt {
    width: 100% !important;
    height: 100% !important;
    object-fit: cover !important;
    border-radius: 12px !important;
    display: block;
}
</style>
"""
if '</head>' in html:
    html = html.replace('</head>', css + '\n</head>')

# 3. Re-apply the clean show/hide logic
js = """
<script id="youtube-style-script">
document.addEventListener('DOMContentLoaded', function() {
    // Physically move the youtube-player div inside the fullArtBox to trap it
    var yp = document.getElementById('youtube-player');
    var fab = document.getElementById('fullArtBox');
    if (yp && fab) { fab.appendChild(yp); }

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
print("✅ Cleaned up! Video is now YouTube-sized, allowing you to scroll down.")
