with open('index.html', 'r') as f:
    html = f.read()

# 1. Global Error Catcher (Catches syntax errors before the page loads)
error_handler = """
<script>
window.onerror = function(msg, url, line) {
    alert("🚨 SCRIPT CRASHED AT LINE " + line + ": " + msg);
    return false;
};
</script>
"""
if 'window.onerror' not in html:
    if '</head>' in html:
        html = html.replace('</head>', error_handler + '</head>')
    else:
        html = error_handler + html
    print("✅ Global error catcher added.")

# 2. Button Click Tester (Forces the button to trigger)
button_debug = """
<script>
document.addEventListener('DOMContentLoaded', function() {
    setTimeout(function() {
        var btn = document.getElementById('authBtn');
        if (btn) {
            btn.onclick = function(e) {
                e.preventDefault();
                alert("👆 Button clicked! Checking handleAuth...");
                if (typeof handleAuth === 'function') {
                    handleAuth();
                } else {
                    alert("❌ FATAL: handleAuth is NOT defined! The script crashed before this point.");
                }
            };
        } else {
            alert("❌ Button with ID 'authBtn' not found.");
        }
    }, 500);
});
</script>
"""
if 'Button clicked! Checking handleAuth' not in html:
    if '</body>' in html:
        html = html.replace('</body>', button_debug + '</body>')
    else:
        html += button_debug
    print("✅ Button click tester added.")

with open('index.html', 'w') as f:
    f.write(html)
print("✅ Done! Now restart your server and test.")
