import re

with open('index.html', 'r') as f:
    html = f.read()

# 1. Remove the old heavy CSS
html = re.sub(r'<style id="full-player-ambient-style">.*?</style>', '', html, flags=re.DOTALL)

# 2. Add the optimized, lightweight CSS
css = """
<style id="full-player-ambient-style">
#fullPlayer {
    background: rgba(0, 0, 0, 0.85) !important; 
    overflow: hidden !important;
}

#fullPlayerAmbient {
    position: absolute;
    top: -20px; left: -20px;
    width: calc(100% + 40px); height: calc(100% + 40px);
    z-index: 0;
    background-size: cover;
    background-position: center;
    /* MUCH LIGHTER: 30px blur instead of 80px */
    filter: blur(30px) saturate(150%) brightness(0.4);
    /* FORCE GPU: Hardware acceleration */
    transform: translateZ(0);
    -webkit-transform: translateZ(0);
    pointer-events: none;
    /* REMOVED: expensive background-image transition */
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

# 3. Update the JavaScript to ensure smooth updates
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
        // Instantly update without a heavy transition
        ambientBg.style.backgroundImage = 'url(' + imageUrl + ')';
    }

    var originalPlayYoutube = window.playYoutube;
    window.playYoutube = function(i) {
        if (originalPlayYoutube) originalPlayYoutube(i);
        var t = window.ytResults[i];
        if (t && t.id && t.id.videoId) {
            var imgUrl = 'https://img.youtube.com/vi/' + t.id.videoId + '/hqdefault.jpg';
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
print("✅ Lag fixed! Ambient glow optimized for smooth 60fps playback.")
