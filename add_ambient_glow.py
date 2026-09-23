import re

with open('index.html', 'r') as f:
    html = f.read()

# 1. Remove old ambient scripts if they exist
html = re.sub(r'<style id="ambient-glow-style">.*?</style>', '', html, flags=re.DOTALL)
html = re.sub(r'<script id="ambient-glow-script">.*?</script>', '', html, flags=re.DOTALL)

# 2. Add the Ambient Glow CSS
css = """
<style id="ambient-glow-style">
#ambientBackground {
    position: fixed;
    top: 0; left: 0;
    width: 100vw; height: 100vh;
    z-index: -1; /* Behind everything */
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    filter: blur(80px) saturate(200%) brightness(0.4); /* Heavy blur, vibrant, dark */
    transform: scale(1.3); /* Scale up to hide blurred edges */
    transition: background-image 1s ease-in-out, opacity 0.5s ease-in-out;
    pointer-events: none; /* Prevents it from blocking any clicks */
    opacity: 0; /* Hidden by default */
}
#ambientBackground.active {
    opacity: 1; /* Fade in when a song plays */
}
</style>
"""
if '</head>' in html:
    html = html.replace('</head>', css + '\n</head>')

# 3. Add the Ambient Glow JavaScript
js = """
<script id="ambient-glow-script">
document.addEventListener('DOMContentLoaded', function() {
    // Create the background element
    var ambientBg = document.createElement('div');
    ambientBg.id = 'ambientBackground';
    document.body.appendChild(ambientBg);

    function updateAmbientBg(imageUrl) {
        if (!imageUrl) return;
        ambientBg.style.backgroundImage = 'url(' + imageUrl + ')';
        ambientBg.classList.add('active');
    }

    function hideAmbientBg() {
        ambientBg.classList.remove('active');
    }

    // Hook into playYoutube
    var originalPlayYoutube = window.playYoutube;
    window.playYoutube = function(i) {
        if (originalPlayYoutube) originalPlayYoutube(i);
        var t = window.ytResults[i];
        if (t && t.id && t.id.videoId) {
            // Use the high-quality thumbnail as the safe fallback
            var imgUrl = 'https://img.youtube.com/vi/' + t.id.videoId + '/hqdefault.jpg';
            updateAmbientBg(imgUrl);
        }
    };

    // Hook into playDbSong
    var originalPlayDbSong = window.playDbSong;
    window.playDbSong = function(i) {
        if (originalPlayDbSong) originalPlayDbSong(i);
        var s = window.songs[i];
        if (s && s.cover_art_url) {
            updateAmbientBg(s.cover_art_url);
        } else {
            hideAmbientBg();
        }
    };

    // Hide background when closing the full player to save battery
    var originalCloseFullPlayer = window.closeFullPlayer;
    window.closeFullPlayer = function() {
        if (originalCloseFullPlayer) originalCloseFullPlayer();
        hideAmbientBg();
    };
});
</script>
"""
if '</body>' in html:
    html = html.replace('</body>', js + '\n</body>')

with open('index.html', 'w') as f:
    f.write(html)
print("✅ Ambient Glow effect added! It will safely use thumbnails as the source.")
