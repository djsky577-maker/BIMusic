import re

with open('index.html', 'r') as f:
    html = f.read()

# 1. Remove the old global ambient script to avoid conflicts
html = re.sub(r'<style id="ambient-glow-style">.*?</style>', '', html, flags=re.DOTALL)
html = re.sub(r'<script id="ambient-glow-script">.*?</script>', '', html, flags=re.DOTALL)

# 2. Add the new Ambient Glow CSS specifically for the Full Player
css = """
<style id="full-player-ambient-style">
/* Make the full player background transparent so the glow shows through */
#fullPlayer {
    background: rgba(0, 0, 0, 0.85) !important; 
    overflow: hidden !important;
}

/* The ambient glow layer */
#fullPlayerAmbient {
    position: absolute;
    top: 0; left: 0;
    width: 100%; height: 100%;
    z-index: 0; /* Behind everything else in the player */
    background-size: cover;
    background-position: center;
    filter: blur(80px) saturate(180%) brightness(0.3); /* Soft, dark, colorful blur */
    transform: scale(1.3); /* Scales up to hide blurred edges */
    transition: background-image 1s ease-in-out;
    pointer-events: none; /* Ensures it NEVER blocks clicks */
    will-change: transform, background-image;
}

/* Ensure all content (video, buttons) sits ON TOP of the glow */
#fullPlayer > *:not(#fullPlayerAmbient), 
#fullContent > * {
    position: relative;
    z-index: 1;
}
</style>
"""
if '</head>' in html:
    html = html.replace('</head>', css + '\n</head>')

# 3. Add the JavaScript to inject the layer and update it
js = """
<script id="full-player-ambient-script">
document.addEventListener('DOMContentLoaded', function() {
    var fullPlayer = document.getElementById('fullPlayer');
    if (!fullPlayer) return;

    // Create the ambient background div and put it inside the full player
    var ambientBg = document.createElement('div');
    ambientBg.id = 'fullPlayerAmbient';
    fullPlayer.insertBefore(ambientBg, fullPlayer.firstChild);

    function updateFullPlayerBg(imageUrl) {
        if (!imageUrl) return;
        ambientBg.style.backgroundImage = 'url(' + imageUrl + ')';
    }

    // Hook into playYoutube (uses the official thumbnail as the safe source)
    var originalPlayYoutube = window.playYoutube;
    window.playYoutube = function(i) {
        if (originalPlayYoutube) originalPlayYoutube(i);
        var t = window.ytResults[i];
        if (t && t.id && t.id.videoId) {
            var imgUrl = 'https://img.youtube.com/vi/' + t.id.videoId + '/hqdefault.jpg';
            updateFullPlayerBg(imgUrl);
        }
    };

    // Hook into playDbSong (uses the cover art as the source)
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
print("✅ Ambient Glow added INSIDE the Full Player screen!")
