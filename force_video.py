import re

with open('index.html', 'r') as f:
    html = f.read()

# 1. Change the YouTube player size from 1x1 to 100%
html = html.replace("height:'1',width:'1'", "height:'100%',width:'100%'")

# 2. Inject CSS to make the video player fit perfectly and hide by default
css_code = """
<style>
#fullArtBox { position: relative; overflow: hidden; border-radius: 12px; }
#youtube-player {
    position: absolute;
    top: 0; left: 0;
    width: 100%; height: 100%;
    display: none;
    z-index: 10;
    background: #000;
}
#youtube-player iframe {
    width: 100% !important;
    height: 100% !important;
    object-fit: cover;
}
</style>
"""
if '#youtube-player {' not in html:
    if '</head>' in html:
        html = html.replace('</head>', css_code + '\n</head>')

# 3. Rewrite playYoutube to show the video and hide the album art
# Find the exact playYoutube function and replace it
html = re.sub(
    r'function playYoutube\(i\)\{.*?\}(?=function playFromQueue)',
    "function playYoutube(i){currentSource='youtube';currentIndex=i;document.getElementById('audioPlayer').pause();var t=ytResults[i];if(!t)return;var yp=document.getElementById('youtube-player');var fa=document.getElementById('fullArt');if(yp)yp.style.display='block';if(fa)fa.style.display='none';setTrackInfo(t.snippet.thumbnails.high.url,t.snippet.title,t.snippet.channelTitle);ensurePlayer(t.id.videoId);simPool=[];simSimilar=[];simTitle=t.snippet.title;simQIdx=0;document.getElementById('similarGrid').innerHTML='';for(var k=0;k<5;k++)loadSimilarSongs();}",
    html,
    flags=re.DOTALL
)

# 4. Rewrite playDbSong to hide the video and show the album art
html = re.sub(
    r'function playDbSong\(i\)\{.*?\}(?=function playYoutube)',
    "function playDbSong(i){currentSource='db';currentIndex=i;if(ytPlayer&&ytPlayer.pauseVideo)ytPlayer.pauseVideo();var yp=document.getElementById('youtube-player');var fa=document.getElementById('fullArt');if(yp)yp.style.display='none';if(fa)fa.style.display='block';var s=songs[i];if(!s)return;setTrackInfo(s.cover_art_url||'https://via.placeholder.com/150',s.title,s.artist_name);var p=document.getElementById('audioPlayer');p.src=s.audio_url;p.playbackRate=playbackSpeed;p.play();isPlaying=true;updateAllIcons();}",
    html,
    flags=re.DOTALL
)

with open('index.html', 'w') as f:
    f.write(html)
print("✅ Video player logic forced into the code!")
