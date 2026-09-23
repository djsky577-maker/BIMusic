with open('index.html', 'r') as f: html = f.read()

if 'rel="manifest"' not in html:
    html = html.replace('</head>', '<link rel="manifest" href="manifest.json">\n<meta name="theme-color" content="#00e0d0">\n</head>')

if 'serviceWorker.register' not in html:
    sw_script = """
<script>
if ('serviceWorker' in navigator) {
  window.addEventListener('load', function() {
    navigator.serviceWorker.register('service-worker.js');
  });
}
</script>
"""
    html = html.replace('</body>', sw_script + '\n</body>')

with open('index.html', 'w') as f: f.write(html)
print("✅ PWA files fixed!")
