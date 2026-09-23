import re

with open('index.html', 'r') as f:
    html = f.read()

# 1. Remove any old version of this script to avoid stacking wrappers
html = re.sub(r'<script id="auto-shuffle-script">.*?</script>', '', html, flags=re.DOTALL)

# 2. Inject the new auto-shuffle logic
js = """
<script id="auto-shuffle-script">
document.addEventListener('DOMContentLoaded', function() {
    // Wrap the existing nextTrack function
    var originalNextTrack = window.nextTrack;
    window.nextTrack = function() {
        // If playing YouTube and we have similar songs loaded, play a random one
        if (currentSource === 'youtube' && window.simPool && window.simPool.length > 0) {
            // Pick a random song from the similar songs list
            var randomIndex = Math.floor(Math.random() * window.simPool.length);
            
            // Convert the simPool format to the ytResults format the player expects
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
            
            // Play the random song
            if (typeof window.playYoutube === 'function') {
                window.playYoutube(randomIndex);
            }
        } else {
            // Fallback to normal behavior if simPool is empty
            if (originalNextTrack) originalNextTrack();
        }
    };
});
</script>
"""

if '</body>' in html:
    html = html.replace('</body>', js + '\n</body>')

with open('index.html', 'w') as f:
    f.write(html)
print("✅ Auto-shuffle from Similar Songs is now active!")
