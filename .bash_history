    j = s.find('{', m.end())
    if j < 0: 
        print(m.group(2), ': no brace'); continue
    depth=0
    k=j
    end=None
    while k < len(s):
        if s[k]=='{': depth+=1
        elif s[k]=='}':
            depth-=1
            if depth==0:
                end=k+1
                break
        k+=1
    name=m.group(2)
    if end is None:
        print('>>> BROKEN:', name, 'starts at char', start)
    else:
        print(name, 'OK')
"
cd ~
python3 << 'PYEOF'
with open('index.html') as f: h=f.read()

# Fix: add the missing } at end of onYouTubeIframeAPIReady
old = "if(repeatMode===2){ytPlayer.seekTo(0);ytPlayer.playVideo();}else nextTrack();}}});"
new = "if(repeatMode===2){ytPlayer.seekTo(0);ytPlayer.playVideo();}else nextTrack();}}});}"

count = h.count(old)
print('Occurrences found:', count)

if count >= 1:
    h = h.replace(old, new, 1)
    print('Missing brace added ✓')
else:
    print('Target not found — showing actual line:')
    i = h.find('onYouTubeIframeAPIReady')
    print(h[i:i+350])

# Verify
import re
scripts = re.findall(r'<script>([\s\S]*?)</script>', h)
for i,m in enumerate(scripts):
    ob=m.count('{'); cb=m.count('}')
    op=m.count('('); cp=m.count(')')
    status='OK' if ob==cb and op==cp else f'BROKEN braces {ob}/{cb} parens {op}/{cp}'
    print(f'Script {i}: {status}')

open('index.html','w').write(h)
print('SAVED')
PYEOF

python -m http.server 8080
cd ~
python3 << 'PYEOF'
with open('index.html') as f: h=f.read()

# Replace the broken onYouTubeIframeAPIReady entirely
start = h.find('function onYouTubeIframeAPIReady')
end = h.find('function ensurePlayer')

if start < 0 or end < 0 or end < start:
    print('Markers not found!')
else:
    new_fn = "function onYouTubeIframeAPIReady(){ytPlayer=new YT.Player('youtube-player',{height:'1',width:'1',playerVars:{playsinline:1,controls:0,autoplay:1},events:{onReady:function(){ytReady=true;},onStateChange:function(e){if(e.data===1){isPlaying=true;updateAllIcons();}else if(e.data===2){isPlaying=false;updateAllIcons();}else if(e.data===0){if(repeatMode===2){ytPlayer.seekTo(0);ytPlayer.playVideo();}else nextTrack();}}}}});}\n"
    h = h[:start] + new_fn + h[end:]
    print('onYouTubeIframeAPIReady rebuilt ✓')

# Verify balance
import re
s = re.findall(r'<script>([\s\S]*?)</script>', h)[0]
ob = s.count('{'); cb = s.count('}')
op = s.count('('); cp = s.count(')')
print('Braces:', ob, '/', cb, '| Parens:', op, '/', cp)
print('Balanced!' if ob==cb and op==cp else 'STILL BROKEN!')

open('index.html','w').write(h)
print('SAVED')
PYEOF

python -m http.server 8080
cd ~
python3 << 'PYEOF'
with open('index.html') as f: h=f.read()

# Find where the brace count goes negative (extra close) inside the script
import re
s_start = h.find('<script>', h.find('iframe_api')) + 8
s_end = h.find('</script>', s_start)
s = h[s_start:s_end]

depth = 0
bad_pos = -1
for i, c in enumerate(s):
    if c == '{': depth += 1
    elif c == '}':
        depth -= 1
        if depth < 0:
            bad_pos = i
            break

if bad_pos >= 0:
    print('Extra } found at script position', bad_pos)
    print('Context:', repr(s[bad_pos-80:bad_pos+20]))
    # Remove that one character from the full file
    full_pos = s_start + bad_pos
    h = h[:full_pos] + h[full_pos+1:]
    print('Removed one stray }')
else:
    print('No negative depth found. Depth at end:', depth)

# Verify
s2 = re.findall(r'<script>([\s\S]*?)</script>', h)[0]
print('Now braces:', s2.count('{'), '/', s2.count('}'), '| parens:', s2.count('('), '/', s2.count(')'))

open('index.html','w').write(h)
print('SAVED')
PYEOF

python -m http.server 8080
cd ~
python3 << 'PYEOF'
with open('index.html') as f: h=f.read()

# Known-correct version of the function
correct = "function onYouTubeIframeAPIReady(){ytPlayer=new YT.Player('youtube-player',{height:'1',width:'1',playerVars:{playsinline:1,controls:0,autoplay:1},events:{onReady:function(){ytReady=true;},onStateChange:function(e){if(e.data===1){isPlaying=true;updateAllIcons();}else if(e.data===2){isPlaying=false;updateAllIcons();}else if(e.data===0){if(repeatMode===2){ytPlayer.seekTo(0);ytPlayer.playVideo();}else{nextTrack();}}}});}"

start = h.find('function onYouTubeIframeAPIReady')
end = h.find('function ensurePlayer')

if start < 0 or end < 0:
    print('Markers not found!')
else:
    h = h[:start] + correct + "\n" + h[end:]
    print('Replaced with balanced version ✓')

# Verify balance
import re
s = re.findall(r'<script>([\s\S]*?)</script>', h)[0]
ob = s.count('{'); cb = s.count('}')
op = s.count('('); cp = s.count(')')
print('Braces:', ob, '/', cb, '| Parens:', op, '/', cp)
print('BALANCED ✓' if ob==cb and op==cp else 'STILL BROKEN')

open('index.html','w').write(h)
print('SAVED')
PYEOF

python -m http.server 8080
cd ~
python3 << 'PYEOF'
with open('index.html') as f: h=f.read()

# Find where the script balance goes wrong and fix the missing brace
import re
# Find the script block
script_matches = list(re.finditer(r'<script>([\s\S]*?)</script>', h))
# Use the big one (has onYouTubeIframeAPIReady)
for sm in script_matches:
    if 'onYouTubeIframeAPIReady' in sm.group(1):
        s = sm.group(1)
        s_start = sm.start(1)
        break
else:
    print('Could not find target script')
    raise SystemExit

# Walk through and find where depth fails to reach 0 at end
depth = 0
last_good = 0
for i, c in enumerate(s):
    if c == '{': depth += 1
    elif c == '}':
        depth -= 1
        if depth == 0:
            last_good = i

print('Depth at end:', depth, '(need 0)')

if depth == 1:
    # Need one more } somewhere. Add at the very end of the script content.
    new_h = h[:s_start + len(s)] + '}' + h[s_start + len(s):]
    h = new_h
    print('Added one } at end of script block')
elif depth == -1:
    # Remove one } — find last extra close
    depth2 = 0
    for i, c in enumerate(s):
        if c == '{': depth2 += 1
        elif c == '}':
            depth2 -= 1
            if depth2 < 0:
                h = h[:s_start + i] + h[s_start + i + 1:]
                print('Removed stray } at script pos', i)
                break
else:
    print('Depth is', depth, '— unsure how to auto-fix')

# Verify
sm2 = None
for sm in re.finditer(r'<script>([\s\S]*?)</script>', h):
    if 'onYouTubeIframeAPIReady' in sm.group(1):
        sm2 = sm
        break
s2 = sm2.group(1)
print('Braces now:', s2.count('{'), '/', s2.count('}'), '| Parens:', s2.count('('), '/', s2.count(')'))
print('BALANCED ✓' if s2.count('{')==s2.count('}') and s2.count('(')==s2.count(')') else 'STILL BROKEN')

open('index.html','w').write(h)
print('SAVED')
PYEOF

python -m http.server 8080
cd ~
python3 << 'PYEOF'
with open('index.html') as f: h=f.read()

start = h.find('function onYouTubeIframeAPIReady')
next_fn = h.find('function ensurePlayer', start)

if start < 0 or next_fn < 0:
    print('Markers not found')
else:
    new_fn = """function onYouTubeIframeAPIReady(){
try{
ytPlayer=new YT.Player('youtube-player',{
height:'1',width:'1',
playerVars:{playsinline:1,controls:0,autoplay:1},
events:{
onReady:function(){ytReady=true;},
onStateChange:function(e){
if(e.data===1){isPlaying=true;updateAllIcons();}
else if(e.data===2){isPlaying=false;updateAllIcons();}
else if(e.data===0){
if(repeatMode===2){ytPlayer.seekTo(0);ytPlayer.playVideo();}
else{nextTrack();}
}
}
}
});
}catch(err){console.log('YT init failed',err);}
}
"""
    # Verify new_fn is balanced BEFORE using it
    ob = new_fn.count('{'); cb = new_fn.count('}')
    op = new_fn.count('('); cp = new_fn.count(')')
    print('New function braces:', ob, '/', cb, '| parens:', op, '/', cp)
    if ob == cb and op == cp:
        h = h[:start] + new_fn + h[next_fn:]
        # Verify full script
        import re
        for m in re.finditer(r'<script>([\s\S]*?)</script>', h):
            if 'onYouTubeIframeAPIReady' in m.group(1):
                s = m.group(1)
                print('Full script braces:', s.count('{'), '/', s.count('}'))
                print('Full script parens:', s.count('('), '/', s.count(')'))
                break
        open('index.html','w').write(h)
        print('SAVED')
    else:
        print('Not balanced, will NOT save')
PYEOF

python -m http.server 8080
cd ~
python3 << 'PYEOF'
with open('index.html') as f: h=f.read()
import re

# Find the target script block
for m in re.finditer(r'<script>([\s\S]*?)</script>', h):
    if 'onYouTubeIframeAPIReady' in m.group(1):
        s = m.group(1)
        s_start = m.start(1)
        break
else:
    print('Script not found')
    raise SystemExit

# Walk through, track depth, report where it goes negative
depth = 0
for i, c in enumerate(s):
    if c == '{': depth += 1
    elif c == '}':
        depth -= 1
        if depth < 0:
            print('Extra } at script pos', i)
            print('Context before:', repr(s[max(0,i-100):i]))
            print('Context after :', repr(s[i:i+80]))
            # Remove that one character from full file
            pos = s_start + i
            h2 = h[:pos] + h[pos+1:]
            # Verify
            for m2 in re.finditer(r'<script>([\s\S]*?)</script>', h2):
                if 'onYouTubeIframeAPIReady' in m2.group(1):
                    s2 = m2.group(1)
                    print('After fix:', s2.count('{'), '/', s2.count('}'), '| parens:', s2.count('('), '/', s2.count(')'))
                    break
            open('index.html','w').write(h2)
            print('SAVED')
            break
else:
    print('Depth never went negative. End depth:', depth)
    # If end depth is +1, add a } at end of script
    if depth == 1:
        pos = s_start + len(s)
        h2 = h[:pos] + '}' + h[pos:]
        open('index.html','w').write(h2)
        print('Added one } at end of script. SAVED')
PYEOF

python -m http.server 8080
cd ~
cp index.html index-working-v1.html
termux-setup-storage
cp ~/index.html /sdcard/Download/
ls -la /sdcard/Download/index.html
pkg install termux-api -y
termux-media-scan /sdcard/Download/index.html
cd ~
git remote remove origin
git remote add origin https://github.com/djsky577-maker/B.I-Music.git
git push -u origin main
pkg install git -y
cd ~
git init
git add index.html
pkg install git -y
termux-change-repo
pkg install git -y
git init
git add index.html
git commit -m "first version"
git branch -M main
git remote add origin https://github.com/djsky577-maker/B.I-Music.git
git push -u origin main
git config --global user.email "djsky577@gmail.com"
git config --global user.name "djsky577-maker"
git add index.html
git commit -m "first version"
git branch -M main
git push -u origin main
cd ~
git push -u origin main
cd ~
git ls-files
ls -la ~/*.html
cd ~
git ls-files
git log --oneline
cd ~
pwd
git status
cd ~
git add index.html
git status
cd ~
ls -la index.html
cd ~ && git ls-files
cd ~ && git log --oneline
cd ~ && git show HEAD:index.html | wc -c
cd ~
nano index.html
cd ~ && python3 -c "
h = open('index.html').read()
s = '<script data-goatcounter=\"https://bimusic.goatcounter.com/count\" async src=\"//gc.zgo.at/count.js\"></script>'
if 'goatcounter' in h:
    print('Already added')
else:
    h = h.replace('</body>', s + '\n</body>', 1)
    open('index.html','w').write(h)
    print('Script added')
"
git add index.html
git commit -m "analytics"
git push
cd ~ && git remote set-url origin https://github.com/djsky577-maker/BIMusic.git
cd ~
python3 << 'PYEOF'
with open('index.html') as f: h=f.read()

# Find and replace loadMoreArtistSongs with STRICT filter
start = h.find('async function loadMoreArtistSongs')
end = h.find('function updateFollowButton')

new_fn = """async function loadMoreArtistSongs(){
if(artistSongLoading)return;
if(artistSongPool.length>=200)return;
artistSongLoading=true;
for(var b=0;b<3;b++){
  if(artistSongPool.length>=200)break;
  var base=currentArtist.name;
  var q=base+' songs';
  try{
    var d=await pget('/search?q='+encodeURIComponent(q)+'&filter=videos');
    var items=(d.items||[]).filter(function(v){return v.url&&isRealSong(v);});
    var nm=base.toLowerCase().trim();
    var sc=document.getElementById('modalArtistSongs');
    if(!sc)break;
    if(artistSongPool.length===0)sc.innerHTML='';
    items.forEach(function(v){
      if(artistSongPool.length>=200)return;
      var un=(v.uploaderName||'').toLowerCase().trim().replace(/\\s*-\\s*topic$/,'').replace(/vevo$/,'').trim();
      var ti=(v.title||'').toLowerCase();
      // STRICT: only accept if uploader matches artist OR title starts with artist name
      var matchUp=un.indexOf(nm)>=0||nm.indexOf(un)>=0;
      var matchTitle=ti.indexOf(nm)===0||ti.indexOf(nm+'-')===0||ti.indexOf(nm+' -')===0||ti.indexOf(nm+' ft')>=0&&ti.indexOf(nm)<15;
      if(!matchUp&&!matchTitle)return;
      var vid=(v.url||'').replace('/watch?v=','');
      if(artistSongPool.some(function(x){return x.id===vid;}))return;
      var obj={id:vid,title:v.title,channelTitle:v.uploaderName,thumbnail:v.thumbnail};
      artistSongPool.push(obj);
      var ix=artistSongPool.length-1;
      var el=document.createElement('div');el.className='list-item';
      el.onclick=function(){playQueue=artistSongPool.map(function(x){return{id:{videoId:x.id},snippet:{title:x.title,channelTitle:x.channelTitle,thumbnails:{default:{url:x.thumbnail},high:{url:x.thumbnail}}}};});ytResults=playQueue;playYoutube(ix);};
      el.innerHTML='<img src="'+obj.thumbnail+'"><div class="list-info"><div class="list-title">'+obj.title+'</div><div class="list-sub">'+obj.channelTitle+'</div></div><button class="dl-btn" onclick="event.stopPropagation();dlId(\\''+vid+'\\')"><svg viewBox="0 0 24 24"><path d="M5 20h14v-2H5v2zM19 9h-4V3H9v6H5l7 7 7-7z"/></svg></button>';
      sc.appendChild(el);
    });
    if(artistSongPool.length===0){sc.innerHTML='<p style="color:#666;text-align:center;padding:20px">No songs found for this artist.</p>';}
  }catch(e){}
}
artistSongLoading=false;
}

"""

if start < 0 or end < 0:
    print('Markers not found')
else:
    h = h[:start] + new_fn + h[end:]
    print('Artist filter fixed ✓')

# Also remove the preload from openArtistProfile (was firing 3x on open)
h = h.replace('for(var i=0;i<3;i++)await loadMoreArtistSongs();}','await loadMoreArtistSongs();}')

# Verify brace balance
import re
for m in re.finditer(r'<script>([\s\S]*?)</script>', h):
    if 'onYouTubeIframeAPIReady' in m.group(1):
        s=m.group(1)
        print('Braces:', s.count('{'), '/', s.count('}'), '| Parens:', s.count('('), '/', s.count(')'))
        break

open('index.html','w').write(h)
print('SAVED')
PYEOF

python -m http.server 8080
git add index.html
git commit -m "fix artist filter"
git push
cd ~
cat > manifest.json << 'EOF'
{
  "name": "B.I Music",
  "short_name": "B.I",
  "description": "Free music streaming app",
  "start_url": "/BIMusic/",
  "scope": "/BIMusic/",
  "display": "standalone",
  "orientation": "portrait",
  "background_color": "#050508",
  "theme_color": "#00e0d0",
  "icons": [
    {
      "src": "icon-192.png",
      "sizes": "192x192",
      "type": "image/png"
    },
    {
      "src": "icon-512.png",
      "sizes": "512x512",
      "type": "image/png"
    }
  ]
}
EOF

cd ~
git add index.html manifest.json icon-192.png icon-512.png
git commit -m "add pwa"
git push
cd ~
git push
cd ~ && git config --global http.postBuffer 524288000
cd ~ && git config --global http.lowSpeedLimit 0
cd ~ && git config --global http.lowSpeedTime 999999
git push
cd ~ && git config --global http.postBuffer 524288000
cd ~ && git config --global http.lowSpeedLimit 0
cd ~ && git config --global http.lowSpeedTime 999999
git push
cd ~
ls *.html *.json
git add -A
git commit -m "add pwa"
git push
cd ~ && git remote set-url origin https://djsky577-maker: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@github.com/djsky577-maker/BIMusic.git
git push
termux-setup-storage
