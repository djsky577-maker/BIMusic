with open('index.html', 'r') as f:
    html = f.read()

# 1. Resize the YouTube player from 1x1 to 100%
html = html.replace("height:'1',width:'1'", "height:'100%',width:'100%'")

# 2. Add CSS to make the video player fit inside the album art box
css_code = """
<style>
#youtube-player {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    border-radius: 12px;
    overflow: hidden;
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
    else:
        html = css_code + html

# 3. Update playYoutube to show the video and hide the art
html = html.replace(
    "function playYoutube(i){currentSource='youtube';currentIndex=i;document.getElementById('audioPlayer').pause();",
    "function playYoutube(i){currentSource='youtube';currentIndex=i;document.getElementById('audioPlayer').pause();var yp=document.getElementById('youtube-player');var fa=document.getElementById('fullArt');if(yp)yp.style.display='block';if(fa)fa.style.display='none';"
)

# 4. Update playDbSong to show the art and hide the video
html = html.replace(
    "function playDbSong(i){currentSource='db';currentIndex=i;if(ytPlayer&&ytPlayer.pauseVideo)ytPlayer.pauseVideo();",
    "function playDbSong(i){currentSource='db';currentIndex=i;if(ytPlayer&&ytPlayer.pauseVideo)ytPlayer.pauseVideo();var yp=document.getElementById('youtube-player');var fa=document.getElementById('fullArt');if(yp)yp.style.display='none';if(fa)fa.style.display='block';"
)

with open('index.html', 'w') as f:
    f.write(html)
print("✅ Video display enabled! YouTube videos will now show in the player.")
