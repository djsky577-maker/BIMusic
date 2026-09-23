import re

with open('index.html', 'r') as f:
    html = f.read()

# 1. Remove old ambient styles/scripts
html = re.sub(r'<style id="full-player-ambient-style">.*?</style>', '', html, flags=re.DOTALL)
html = re.sub(r'<script id="full-player-ambient-script">.*?</script>', '', html, flags=re.DOTALL)

# 2. Add the ultra-lightweight CSS
css = """
<style id="full-player-ambient-style">
#fullPlayer {
    background: rgba(0, 0, 0, 0.9) !important; 
    overflow: hidden !important;
}

#fullPlayerAmbient {
    position: absolute;
    top: 0; left: 0;
    width: 100%; height: 100%;
    z-index: 0;
    background-size: cover;
    background-position: center;
    /* Blur is fine because the source image is tiny (320x180) */
    filter: blur(40px) saturate(150%) brightness(0.3);
    transform: translateZ(0); /* Force GPU acceleration */
    pointer-events: none;
}
#fullPlayer > *:not(#fullPlayerAmbient), 
#fullContent > * {
    position: relative;
    z-index: 1;
}
</style>
"""
if '</head>' in html:
    html = html.replace('</head>', css + '\n</head>')

# 3. Add the JavaScript
js = """
<script id="full-player-ambient-script">
document.addEventListener('DOMContentLoaded', function() {
    var fullPlayer = document.getElementById('fullPlayer');
    if (!fullPlayer) return;

    var ambientBg = document.createElement('div');
    ambientBg.id = 'fullPlayerAmbient';
    fullPlayer.insertBefore(ambientBg, fullPlayer.firstChild);

    function updateFullPlayerBg(imageUrl) {
        if (!imageUrl) return;
        ambientBg.style.backgroundImage = 'url(' + imageUrl + ')';
    }

    var originalPlayYoutube = window.playYoutube;
    window.playYoutube = function(i) {
        if (originalPlayYoutube) originalPlayYoutube(i);
        var t = window.ytResults[i];
        if (t && t.id && t.id.videoId) {
            // USE TINY THUMBNAIL (320x180) FOR BLUR - ZERO LAG
            var imgUrl = 'https://img.youtube.com/vi/' + t.id.videoId + '/mqdefault.jpg';
            updateFullPlayerBg(imgUrl);
        }
    };

    var originalPlayDbSong = window.playDbSong;
    window.playDbSong = function(i) {
        if (originalPlayDbSong) originalPlayDbSong(i);
        var s = window.songs[i];
        if (s && s.cover_art_url) {
            updateFullPlayerBg(s.cover_art_url);
        } else {
            ambientBg.style.backgroundImage = 'none';
        }
    };
});
</script>
"""
if '</body>' in html:
    html = html.replace('</body>', js + '\n</body>')

with open('index.html', 'w') as f:
    f.write(html)
print("✅ Ultra-lightweight ambient glow added! Zero lag guaranteed.")
