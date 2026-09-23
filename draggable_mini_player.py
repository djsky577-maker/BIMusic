import re

with open('index.html', 'r') as f:
    html = f.read()

# 1. Remove old draggable scripts if they exist
html = re.sub(r'<style id="draggable-mini-style">.*?</style>', '', html, flags=re.DOTALL)
html = re.sub(r'<script id="draggable-mini-script">.*?</script>', '', html, flags=re.DOTALL)

# 2. Add the CSS to make the mini-player float and be draggable
css = """
<style id="draggable-mini-style">
#miniPlayer {
    position: fixed !important;
    bottom: 75px !important; /* Sits just above the bottom nav */
    left: 10px !important;
    width: calc(100% - 20px) !important;
    max-width: 400px !important;
    z-index: 999999 !important; /* Floats above the artist modal */
    touch-action: none !important; /* Prevents scrolling while dragging */
    cursor: grab;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.8) !important;
    transition: transform 0.1s ease-out, opacity 0.3s ease;
    border-radius: 12px !important;
}
#miniPlayer:active {
    cursor: grabbing;
}
/* Prevent text selection while dragging */
#miniPlayer * {
    user-select: none;
    -webkit-user-select: none;
}
</style>
"""
if '</head>' in html:
    html = html.replace('</head>', css + '\n</head>')

# 3. Add the JavaScript to handle the dragging logic
js = """
<script id="draggable-mini-script">
document.addEventListener('DOMContentLoaded', function() {
    var miniPlayer = document.getElementById('miniPlayer');
    if (!miniPlayer) return;

    var isDragging = false;
    var startX = 0, startY = 0;
    var currentX = 0, currentY = 0;
    var hasMoved = false;

    // Initialize its starting position based on its CSS bottom/left
    var rect = miniPlayer.getBoundingClientRect();
    var initialLeft = rect.left;
    var initialTop = rect.top;

    // Change to absolute positioning so we can move it freely
    miniPlayer.style.bottom = 'auto';
    miniPlayer.style.left = initialLeft + 'px';
    miniPlayer.style.top = initialTop + 'px';

    function dragStart(e) {
        // If the user is clicking a button inside, don't drag
        if (e.target.closest('button') || e.target.closest('.mini-play-btn')) {
            return;
        }
        
        isDragging = true;
        hasMoved = false;
        
        var touch = e.touches ? e.touches[0] : e;
        startX = touch.clientX - miniPlayer.offsetLeft;
        startY = touch.clientY - miniPlayer.offsetTop;
        
        miniPlayer.style.transition = 'none'; // Disable transition for instant drag
    }

    function dragMove(e) {
        if (!isDragging) return;
        
        e.preventDefault(); // Stop scrolling
        var touch = e.touches ? e.touches[0] : e;
        
        var newX = touch.clientX - startX;
        var newY = touch.clientY - startY;
        
        // Keep it within screen bounds
        var maxX = window.innerWidth - miniPlayer.offsetWidth;
        var maxY = window.innerHeight - miniPlayer.offsetHeight;
        
        newX = Math.max(0, Math.min(newX, maxX));
        newY = Math.max(0, Math.min(newY, maxY));
        
        // If it moved more than 5 pixels, it's a drag, not a tap
        if (Math.abs(newX - miniPlayer.offsetLeft) > 5 || Math.abs(newY - miniPlayer.offsetTop) > 5) {
            hasMoved = true;
        }
        
        miniPlayer.style.left = newX + 'px';
        miniPlayer.style.top = newY + 'px';
    }

    function dragEnd(e) {
        if (!isDragging) return;
        isDragging = false;
        miniPlayer.style.transition = 'transform 0.1s ease-out';
        
        // If it didn't move much, let the click pass through
        if (!hasMoved && e.type === 'touchend') {
            // This was a tap, do nothing special, let the click fire
        }
    }

    // Touch events for mobile
    miniPlayer.addEventListener('touchstart', dragStart, {passive: false});
    document.addEventListener('touchmove', dragMove, {passive: false});
    document.addEventListener('touchend', dragEnd);

    // Mouse events for desktop testing
    miniPlayer.addEventListener('mousedown', dragStart);
    document.addEventListener('mousemove', dragMove);
    document.addEventListener('mouseup', dragEnd);
});
</script>
"""
if '</body>' in html:
    html = html.replace('</body>', js + '\n</body>')

with open('index.html', 'w') as f:
    f.write(html)
print("✅ Draggable Mini-Player added! You can now move it anywhere.")
