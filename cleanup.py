with open('index.html', 'r') as f:
    html = f.read()

# Remove the mock login script
html = html.replace("""
<script>
window.handleAuth = async function() {
    var e = document.getElementById('authError');
    var em = document.getElementById('authEmail').value.trim();
    var pw = document.getElementById('authPassword').value;
    var b = document.getElementById('authBtn');
    if (!em || !pw) { if(e) e.textContent = 'Fill both fields.'; return; }
    if(e) e.textContent = 'Logging in locally...';
    if(b) b.disabled = true;
    setTimeout(function() {
        currentUser = { email: em };
        if(b) { b.disabled = false; b.textContent = 'Log In'; }
        if(typeof enterApp === 'function') enterApp();
    }, 500);
};
</script>
""", "")

# Remove the bypass button script
import re
html = re.sub(r'<script>\s*document\.addEventListener\(\'DOMContentLoaded\', function\(\) \{\s*var bypassBtn.*?bypassBtn\.style\.display = \'none\'.*?\}\);\s*\}\);\s*</script>', '', html, flags=re.DOTALL)

with open('index.html', 'w') as f:
    f.write(html)
print("✅ Cleaned up mock and bypass scripts.")
