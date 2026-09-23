import re

with open('index.html', 'r') as f:
    html = f.read()

# 1. Remove old script if it exists
html = re.sub(r'<script id="hide-mini-on-full-script">.*?</script>', '', html, flags=re.DOTALL)

# 2. Add the JavaScript to hide/show the mini player
js = """
<script id="hide-mini-on-full-script">
document.addEventListener('DOMContentLoaded', function() {
    var miniPlayer = document.getElementById('miniPlayer');
    
    // Hook into openFullPlayer
    var originalOpenFullPlayer = window.openFullPlayer;
    window.openFullPlayer = function() {
        if (originalOpenFullPlayer) originalOpenFullPlayer();
        if (miniPlayer) {
            miniPlayer.style.display = 'none'; // Hide the mini player
        }
    };

    // Hook into closeFullPlayer
    var originalCloseFullPlayer = window.closeFullPlayer;
    window.closeFullPlayer = function() {
        if (originalCloseFullPlayer) originalCloseFullPlayer();
        if (miniPlayer) {
            // Only show the mini player if a song is actually playing/loaded
            if (miniPlayer.classList.contains('active')) {
                miniPlayer.style.display = 'flex'; // Bring it back
            }
        }
    };
});
</script>
"""
if '</body>' in html:
    html = html.replace('</body>', js + '\n</body>')

with open('index.html', 'w') as f:
    f.write(html)
print("✅ Mini-player will now hide when Full Player is open!")
