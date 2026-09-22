with open('index.html', 'r') as f:
    html = f.read()

bypass_code = """
<script>
document.addEventListener('DOMContentLoaded', function() {
    var bypassBtn = document.createElement('button');
    bypassBtn.innerHTML = '🚀 BYPASS LOGIN';
    bypassBtn.style.cssText = 'position:fixed;top:10px;right:10px;z-index:99999;padding:12px;background:#ff4d4d;color:#fff;border:none;border-radius:8px;font-weight:bold;font-size:14px;';
    bypassBtn.onclick = function() {
        // Hide the auth screen
        var authView = document.getElementById('view-auth');
        if (authView) {
            authView.classList.remove('active');
            authView.style.display = 'none';
        }
        // Show the main app
        var main = document.getElementById('mainContent');
        if (main) main.style.display = 'block';
        var nav = document.querySelector('.bottom-nav') || document.querySelector('nav');
        if (nav) nav.style.display = 'flex';
        
        // Force load some data into the home tab
        if (typeof loadHomeMore === 'function') loadHomeMore();
        if (typeof renderFollowedArtists === 'function') renderFollowedArtists();
        if (typeof renderRecentlyPlayed === 'function') renderRecentlyPlayed();
        
        bypassBtn.style.display = 'none'; // Hide the button after clicking
    };
    document.body.appendChild(bypassBtn);
});
</script>
"""

if '🚀 BYPASS LOGIN' in html:
    print("⚠️ Bypass button already exists.")
else:
    if '</body>' in html:
        html = html.replace('</body>', bypass_code + '\n</body>')
    else:
        html += bypass_code
    with open('index.html', 'w') as f:
        f.write(html)
    print("✅ Bypass button injected! Refresh Chrome.")
