with open('index.html', 'r') as f:
    html = f.read()

# Find the catch block in the handleAuth function and add an alert
old_catch = "catch(x){e.textContent='Error: '+x.message;b.disabled=false;b.textContent=isLoginMode?'Log In':'Register';}"
new_catch = "catch(x){alert('LOGIN FAILED: ' + x.message);e.textContent='Error: '+x.message;b.disabled=false;b.textContent=isLoginMode?'Log In':'Register';}"

if old_catch in html:
    html = html.replace(old_catch, new_catch)
    with open('index.html', 'w') as f:
        f.write(html)
    print("✅ Debug alert added! Refresh Chrome and try to log in.")
elif "LOGIN FAILED" in html:
    print("⚠️ Debug alert is already there. Refresh Chrome and try again.")
else:
    print("❌ Could not find the error handler. The code might be slightly different.")
