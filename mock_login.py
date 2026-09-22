with open('index.html', 'r') as f:
    html = f.read()

mock_code = """
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
"""

if 'window.handleAuth' in html:
    print("⚠️ Mock login already added.")
else:
    if '</body>' in html:
        html = html.replace('</body>', mock_code + '\n</body>')
    else:
        html += mock_code
    with open('index.html', 'w') as f:
        f.write(html)
    print("✅ Local mock login added! Refresh Chrome.")
