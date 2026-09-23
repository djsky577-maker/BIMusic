with open('index.html', 'r') as f: html = f.read()
if 'rel="manifest"' not in html:
    html = html.replace('</head>', '<link rel="manifest" href="manifest.json">\n<meta name="theme-color" content="#00e0d0">\n</head>')
    with open('index.html', 'w') as f: f.write(html)
    print("✅ Linked!")
