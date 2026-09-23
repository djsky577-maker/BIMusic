import re

with open('index.html', 'r') as f:
    html = f.read()

# 1. Remove the old blue glass style
html = re.sub(r'<style id="blue-glass-back-style">.*?</style>', '', html, flags=re.DOTALL)

# 2. Add the new Liquid Blue Glass CSS for the Scroll Up Button (#bttBtn)
css = """
<style id="blue-glass-style">
/* Scroll Up Button Liquid Blue Glass */
#bttBtn {
    background: rgba(40, 80, 200, 0.3) !important;
    backdrop-filter: blur(15px) !important;
    -webkit-backdrop-filter: blur(15px) !important;
    border: 1px solid rgba(80, 130, 255, 0.4) !important;
    border-radius: 50% !important;
    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.5), 0 0 15px rgba(40, 80, 200, 0.4) !important;
    color: #fff !important;
    transition: all 0.3s ease !important;
    display: flex;
    align-items: center;
    justify-content: center;
}
#bttBtn:active {
    background: rgba(60, 120, 255, 0.6) !important;
    box-shadow: 0 0 25px rgba(60, 120, 255, 0.8) !important;
    transform: scale(0.9);
}
#bttBtn svg {
    fill: #fff !important;
    filter: drop-shadow(0 0 4px rgba(60, 120, 255, 0.9));
}

/* Keep the back button nice and clean too */
.back-btn, .back-button, #backBtn, [onclick*="back"], [onclick*="close"] {
    display: inline-flex !important;
    align-items: center !important;
    gap: 5px !important;
    color: #fff !important;
    font-weight: bold !important;
}
</style>
"""
if '</head>' in html:
    html = html.replace('</head>', css + '\n</head>')

# 3. Add JavaScript to inject the arrow into the back button
js = """
<script id="back-arrow-script">
document.addEventListener('DOMContentLoaded', function() {
    // Find all possible back buttons
    var backBtns = document.querySelectorAll('#backBtn, .back-btn, .back-button, [onclick*="back"], [onclick*="close"], #closeArtistModal, #closeFullPlayer');
    
    // The SVG arrow
    var arrowSVG = '<svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" style="margin-right: 5px;"><line x1="19" y1="12" x2="5" y2="12"></line><polyline points="12 19 5 12 12 5"></polyline></svg>';

    backBtns.forEach(function(btn) {
        // Only add the arrow if it doesn't already have one
        if (!btn.querySelector('svg')) {
            btn.innerHTML = arrowSVG + ' ' + btn.innerHTML;
        }
    });
});
</script>
"""
if '</body>' in html:
    html = html.replace('</body>', js + '\n</body>')

with open('index.html', 'w') as f:
    f.write(html)
print("✅ Scroll Up button turned Blue Glass! Back button arrow injected!")
