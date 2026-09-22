    <div class="view" id="view-trending"><div class="section-header"><h3>Trending Now</h3></div><div class="list-container" id="trendingList"></div></div>
    <div class="view" id="view-playlists"><div class="section-header"><h3>My Playlists</h3><a onclick="openCreatePlaylistModal()">+ Create</a></div><div class="list-container" id="playlistsList"></div></div>
    <div class="view" id="view-artists"><div class="section-header"><h3>Search Artists</h3></div><div style="display: flex; gap: 10px; margin-bottom: 20px;"><input type="text" id="artistSearchInput" placeholder="Type artist name..." style="flex:1; padding: 14px; border-radius: 12px; border: none; background: #16161c; color: white;"><button onclick="searchArtists()" style="padding: 0 20px; border-radius: 12px; border: none; background: #00bcd4; color: white; font-weight: bold;">Go</button></div><div class="list-container" id="artistsList"></div></div>
    <div class="view" id="view-genres"><div class="section-header"><h3>Browse Genres</h3></div><div class="genre-grid">
      <div class="genre-card" style="background: linear-gradient(135deg, #ff416c, #ff4b2b);" onclick="searchGenre('Afrobeat')"><span>Afrobeat</span></div>
      <div class="genre-card" style="background: linear-gradient(135deg, #1e9600, #fff200);" onclick="searchGenre('Hip Hop')"><span>Hip Hop</span></div>
      <div class="genre-card" style="background: linear-gradient(135deg, #00b4db, #0083b0);" onclick="searchGenre('Chill Vibes')"><span>Chill Vibes</span></div>
      <div class="genre-card" style="background: linear-gradient(135deg, #7b4397, #dc2430);" onclick="searchGenre('Dancehall')"><span>Dancehall</span></div>
      <div class="genre-card" style="background: linear-gradient(135deg, #f12711, #f5af19);" onclick="searchGenre('Gospel')"><span>Gospel</span></div>
      <div class="genre-card" style="background: linear-gradient(135deg, #11998e, #38ef7d);" onclick="searchGenre('Amapiano')"><span>Amapiano</span></div>
    </div><div class="list-container" id="genreResults" style="margin-top: 20px;"></div></div>
  </div>
EOF

cat >> index.html << 'EOF'
  <div class="mini-player" id="miniPlayer" onclick="openFullPlayer()">
    <img id="miniArt" src="" alt="">
    <div class="mini-info"><div class="mini-title" id="miniTitle">No song playing</div><div class="mini-artist" id="miniArtist">Select a track</div></div>
    <div class="mini-controls">
      <button class="icon-btn" onclick="event.stopPropagation(); prevTrack()"><svg viewBox="0 0 24 24"><path d="M6 6h2v12H6zm3.5 6l8.5 6V6z"/></svg></button>
      <button class="icon-btn play-btn" id="miniPlayPauseBtn" onclick="event.stopPropagation(); togglePlay()"><svg id="miniPlayIcon" viewBox="0 0 24 24"><path d="M8 5v14l11-7z"/></svg><svg id="miniPauseIcon" viewBox="0 0 24 24" style="display:none;"><path d="M6 19h4V5H6v14zm8-14v14h4V5h-4z"/></svg></button>
      <button class="icon-btn" onclick="event.stopPropagation(); nextTrack()"><svg viewBox="0 0 24 24"><path d="M6 18l8.5-6L6 6v12zM16 6v12h2V6h-2z"/></svg></button>
    </div>
  </div>
  <div class="full-player" id="fullPlayer">
    <button class="icon-btn close-btn" onclick="closeFullPlayer()"><svg viewBox="0 0 24 24"><path d="M7.41 8.59L12 13.17l4.59-4.58L18 10l-6 6-6-6 1.41-1.41z"/></svg></button>
    <div class="full-art"><img id="fullArt" src="" alt=""></div>
    <div class="full-info"><div class="full-title" id="fullTitle">No song playing</div><div class="full-artist" id="fullArtist">Select a track</div></div>
    <div class="full-progress"><div class="time-labels"><span id="fullCurrent">0:00</span><span id="fullDuration">0:00</span></div><input type="range" id="fullProgressBar" value="0" min="0" max="100" style="width:100%;"></div>
    <div class="full-controls">
      <button class="icon-btn" onclick="prevTrack()"><svg viewBox="0 0 24 24"><path d="M6 6h2v12H6zm3.5 6l8.5 6V6z"/></svg></button>
      <button class="icon-btn play-btn" id="fullPlayPauseBtn" onclick="togglePlay()"><svg id="fullPlayIcon" viewBox="0 0 24 24"><path d="M8 5v14l11-7z"/></svg><svg id="fullPauseIcon" viewBox="0 0 24 24" style="display:none;"><path d="M6 19h4V5H6v14zm8-14v14h4V5h-4z"/></svg></button>
      <button class="icon-btn" onclick="nextTrack()"><svg viewBox="0 0 24 24"><path d="M6 18l8.5-6L6 6v12zM16 6v12h2V6h-2z"/></svg></button>
    </div>
    <div class="full-extra">
      <button class="icon-btn" id="shuffleBtn" onclick="toggleShuffle()"><svg viewBox="0 0 24 24"><path d="M10.59 9.17L5.41 4 4 5.41l5.17 5.17 1.42-1.41zM14.5 4l2.04 2.04L4 18.59 5.41 20 17.96 7.46 20 9.5V4h-5.5zm.33 9.41l-1.41 1.41 3.13 3.13L14.5 20H20v-5.5l-2.04 2.04-3.13-3.13z"/></svg></button>
      <button class="icon-btn" id="repeatBtn" onclick="toggleRepeat()"><svg viewBox="0 0 24 24"><path d="M7 7h10v3l4-4-4-4v3H5v6h2V7zm10 10H7v-3l-4 4 4 4v-3h12v-6h-2v4z"/></svg></button>
      <button class="icon-btn" id="likeBtn" onclick="toggleLikeCurrent()"><svg viewBox="0 0 24 24"><path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"/></svg></button>
      <button class="icon-btn" id="downloadBtn" onclick="downloadCurrent()"><svg viewBox="0 0 24 24"><path d="M19 9h-4V3H9v6H5l7 7 7-7zM5 18v2h14v-2H5z"/></svg></button>
    </div>
  </div>
  <div id="youtube-player"></div>
  <script src="https://www.youtube.com/iframe_api"></script>
  <script>
    const API_KEY = 'AIzaSyAHry2KY5LLrfRWH7SaOYXYlKHvrZ6TZeY';
    let tracks = [], currentIndex = -1, isPlaying = false, isShuffle = false, repeatMode = 0, player, progressInterval, searchTimeout;
    let favorites = JSON.parse(localStorage.getItem('bi_favorites')) || [];
    let recentPlays = JSON.parse(localStorage.getItem('bi_recent')) || [];
    let playlists = JSON.parse(localStorage.getItem('bi_playlists')) || {};
    let currentTrack = null;

    function onYouTubeIframeAPIReady() { player = new YT.Player('youtube-player', { height: '1', width: '1', playerVars: { 'playsinline': 1, 'controls': 0 }, events: { 'onReady': onPlayerReady, 'onStateChange': onPlayerStateChange } }); }
    function onPlayerReady(event) { console.log("YouTube Player Ready"); }
    function onPlayerStateChange(event) {
      if (event.data == YT.PlayerState.PLAYING) { isPlaying = true; document.body.classList.add('playing-waves'); updateAllPlayIcons(); document.getElementById('miniPlayer').classList.add('active'); }
      else if (event.data == YT.PlayerState.PAUSED) { isPlaying = false; document.body.classList.remove('playing-waves'); updateAllPlayIcons(); }
      else if (event.data == YT.PlayerState.ENDED) { document.body.classList.remove('playing-waves'); if (repeatMode === 2) { player.seekTo(0); player.playVideo(); } else { nextTrack(); } }
    }
    function switchTab(tabId, element) {
      document.querySelectorAll('.view').forEach(v => v.classList.remove('active'));
      document.getElementById('view-' + tabId).classList.add('active');
      document.querySelectorAll('.nav-tab').forEach(t => t.classList.remove('active'));
      if (element) element.classList.add('active');
      document.querySelectorAll('.nav-item').forEach(t => t.classList.remove('active'));
      const navItems = document.querySelectorAll('.nav-item');
      if (tabId === 'home') navItems[0].classList.add('active');
      if (tabId === 'trending') navItems[1].classList.add('active');
      if (tabId === 'playlists') navItems[3].classList.add('active');
      if (tabId === 'home') loadHomeData();
      if (tabId === 'trending') searchYouTube("Trending music 2024", 'trendingList', 15);
      if (tabId === 'playlists') renderPlaylists();
      if (tabId === 'artists') document.getElementById('artistsList').innerHTML = '<p style="color:#888; text-align:center; margin-top:50px;">Search for an artist above.</p>';
      if (tabId === 'genres') document.getElementById('genreResults').innerHTML = '';
    }
    async function loadHomeData() { renderRecentlyPlayed(); renderPlaylistsHorizontal(); if (tracks.length === 0) searchYouTube("Top Hits 2024", 'trendingList', 15); }
    function renderRecentlyPlayed() {
      const container = document.getElementById('recentlyPlayedContainer'); container.innerHTML = '';
      if (recentPlays.length === 0) { container.innerHTML = '<p style="color:#888; font-size:0.8rem;">No recent plays yet.</p>'; return; }
      recentPlays.slice(0, 5).forEach(track => {
        const el = document.createElement('div'); el.className = 'card'; el.onclick = () => playTrack(track, recentPlays);
        el.innerHTML = `<div class="card-img"><img src="${track.snippet.thumbnails.high.url}" alt=""><div class="card-play"><svg viewBox="0 0 24 24"><path d="M8 5v14l11-7z"/></svg></div></div><div class="card-title">${track.snippet.title}</div><div class="card-sub">${track.snippet.channelTitle}</div>`;
        container.appendChild(el);
      });
    }
    function renderPlaylistsHorizontal() {
      const container = document.getElementById('playlistsContainer'); container.innerHTML = '';
      const names = Object.keys(playlists);
      if (names.length === 0) { container.innerHTML = '<p style="color:#888; font-size:0.8rem;">Create a playlist to see it here!</p>'; return; }
      names.slice(0, 5).forEach(name => {
        const el = document.createElement('div'); el.className = 'card'; el.onclick = () => { switchTab('playlists', document.querySelectorAll('.nav-tab')[2]); };
        el.innerHTML = `<div class="card-img" style="background: linear-gradient(135deg, #7b4397, #dc2430); display:flex; justify-content:center; align-items:center;"><svg style="width:40px;height:40px;fill:#fff;" viewBox="0 0 24 24"><path d="M12 3v10.55c-.59-.34-1.27-.55-2-.55-2.21 0-4 1.79-4 4s1.79 4 4 4 4-1.79 4-4V7h4V3h-6z"/></svg></div><div class="card-title">${name}</div><div class="card-sub">${playlists[name].length} songs</div>`;
        container.appendChild(el);
      });
    }
    async function searchYouTube(query, containerId, limit = 15) {
      const container = document.getElementById(containerId); container.innerHTML = '<p style="color:white; text-align:center;">Searching...</p>';
      try {
        const res = await fetch(`https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=${limit}&q=${encodeURIComponent(query)}&type=video&key=${API_KEY}`);
        const data = await res.json(); if (data.error) { container.innerHTML = `<p style="color:red;">Error: ${data.error.message}</p>`; return; }
        renderListItems(data.items, containerId);
      } catch (e) { container.innerHTML = '<p style="color:red;">Network error.</p>'; }
    }
    function renderListItems(items, containerId) {
      const container = document.getElementById(containerId); container.innerHTML = '';
      if (items.length === 0) { container.innerHTML = '<p style="color:#888; text-align:center;">No results.</p>'; return; }
      items.forEach((track) => {
        const el = document.createElement('div'); el.className = 'list-item'; el.onclick = () => playTrack(track, items);
        const isLiked = favorites.some(f => f.id.videoId === track.id.videoId);
        el.innerHTML = `<img src="${track.snippet.thumbnails.default.url}" alt=""><div class="list-info"><div class="list-title">${track.snippet.title}</div><div class="list-sub">${track.snippet.channelTitle}</div></div><div class="list-actions"><button onclick="event.stopPropagation(); downloadSongFromList('${track.id.videoId}')"><svg viewBox="0 0 24 24"><path d="M19 9h-4V3H9v6H5l7 7 7-7zM5 18v2h14v-2H5z"/></svg></button><button class="${isLiked ? 'liked' : ''}" onclick="event.stopPropagation(); toggleLikeFromList(${JSON.stringify(track).replace(/"/g, '&quot;')})"><svg viewBox="0 0 24 24"><path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"/></svg></button></div>`;
        container.appendChild(el);
      });
    }
    function triggerMainSearch() { const query = document.getElementById('mainSearchInput').value.trim(); if (!query) return; switchTab('home', document.querySelectorAll('.nav-tab')[0]); document.getElementById('view-home').innerHTML = `<div class="section-header"><h3>Search Results</h3></div><div class="list-container" id="searchResults"></div>`; searchYouTube(query, 'searchResults', 20); }
    function searchArtists() { const query = document.getElementById('artistSearchInput').value.trim(); if (!query) return; searchYouTube(query + " top songs", 'artistsList', 10); }
    function searchGenre(genre) { document.getElementById('genreResults').innerHTML = `<div class="section-header"><h3>${genre} Hits</h3></div><div class="list-container" id="genreList"></div>`; searchYouTube(genre + " music", 'genreList', 15); }
    function playTrack(track, trackList) {
      currentTrack = track; tracks = trackList; currentIndex = tracks.findIndex(t => t.id.videoId === track.id.videoId);
      document.getElementById('miniArt').src = track.snippet.thumbnails.high.url; document.getElementById('miniTitle').textContent = track.snippet.title; document.getElementById('miniArtist').textContent = track.snippet.channelTitle;
      document.getElementById('fullArt').src = track.snippet.thumbnails.high.url; document.getElementById('fullTitle').textContent = track.snippet.title; document.getElementById('fullArtist').textContent = track.snippet.channelTitle;
      player.loadVideoById(track.id.videoId); isPlaying = true; updateAllPlayIcons(); addToRecent(track); document.getElementById('miniPlayer').classList.add('active'); updateLikeButton(track.id.videoId);
      clearInterval(progressInterval); progressInterval = setInterval(updateProgress, 1000);
    }
    function updateProgress() { if (player && player.getCurrentTime) { const current = player.getCurrentTime(); const total = player.getDuration(); if (total > 0) { document.getElementById('fullProgressBar').value = (current / total) * 100; document.getElementById('fullCurrent').textContent = formatTime(current); document.getElementById('fullDuration').textContent = formatTime(total); } } }
    function togglePlay() { if (!player || !player.getVideoData || !player.getVideoData().video_id) return; if (isPlaying) { player.pauseVideo(); isPlaying = false; } else { player.playVideo(); isPlaying = true; } updateAllPlayIcons(); }
    function updateAllPlayIcons() {
      const playIcons = ['miniPlayIcon', 'fullPlayIcon']; const pauseIcons = ['miniPauseIcon', 'fullPauseIcon'];
      if (isPlaying) { playIcons.forEach(id => document.getElementById(id).style.display = 'none'); pauseIcons.forEach(id => document.getElementById(id).style.display = 'block'); }
      else { playIcons.forEach(id => document.getElementById(id).style.display = 'block'); pauseIcons.forEach(id => document.getElementById(id).style.display = 'none'); }
    }
    function nextTrack() { if (tracks.length === 0) return; if (isShuffle) { currentIndex = Math.floor(Math.random() * tracks.length); } else { currentIndex = (currentIndex + 1) % tracks.length; } playTrack(tracks[currentIndex], tracks); }
    function prevTrack() { if (tracks.length === 0) return; currentIndex = (currentIndex - 1 + tracks.length) % tracks.length; playTrack(tracks[currentIndex], tracks); }
    function toggleShuffle() { isShuffle = !isShuffle; document.getElementById('shuffleBtn').classList.toggle('active', isShuffle); }
    function toggleRepeat() { repeatMode = (repeatMode + 1) % 3; const btn = document.getElementById('repeatBtn'); if (repeatMode === 0) { btn.classList.remove('active'); } else if (repeatMode === 1) { btn.classList.add('active'); } else if (repeatMode === 2) { btn.classList.add('active'); alert("Repeat 1: Current song will loop."); } }
    function openFullPlayer() { document.getElementById('fullPlayer').classList.add('active'); }
    function closeFullPlayer() { document.getElementById('fullPlayer').classList.remove('active'); }
    function toggleLikeCurrent() { if (!currentTrack) return; toggleLike(currentTrack); updateLikeButton(currentTrack.id.videoId); }
    function toggleLikeFromList(track) { toggleLike(track); }
    function toggleLike(track) { const idx = favorites.findIndex(f => f.id.videoId === track.id.videoId); if (idx === -1) { favorites.push(track); } else { favorites.splice(idx, 1); } localStorage.setItem('bi_favorites', JSON.stringify(favorites)); }
    function updateLikeButton(videoId) { const isLiked = favorites.some(f => f.id.videoId === videoId); document.getElementById('likeBtn').classList.toggle('active', isLiked); }
    function openCreatePlaylistModal() { document.getElementById('createPlaylistModal').classList.add('active'); }
    function closeCreatePlaylistModal() { document.getElementById('createPlaylistModal').classList.remove('active'); }
    function saveNewPlaylist() {
      const name = document.getElementById('newPlaylistName').value.trim(); if (!name) return alert("Please enter a name");
      if (!playlists[name]) { playlists[name] = []; localStorage.setItem('bi_playlists', JSON.stringify(playlists)); document.getElementById('newPlaylistName').value = ''; closeCreatePlaylistModal(); renderPlaylists(); renderPlaylistsHorizontal(); } else { alert("Playlist already exists!"); }
    }
    function renderPlaylists() {
      const container = document.getElementById('playlistsList'); container.innerHTML = ''; const names = Object.keys(playlists);
      if (names.length === 0) { container.innerHTML = '<p style="color:#888; text-align:center; margin-top:50px;">No playlists yet. Create one!</p>'; return; }
      names.forEach(name => {
        const el = document.createElement('div'); el.className = 'list-item';
        el.onclick = () => { tracks = playlists[name]; switchTab('home', document.querySelectorAll('.nav-tab')[0]); document.getElementById('view-home').innerHTML = `<div class="section-header"><h3>Playlist: ${name}</h3></div><div class="list-container" id="playlistViewList"></div>`; renderListItems(tracks, 'playlistViewList'); };
        el.innerHTML = `<div style="width:50px;height:50px;border-radius:8px;background:linear-gradient(135deg,#7b4397,#dc2430);display:flex;justify-content:center;align-items:center;"><svg style="width:24px;height:24px;fill:#fff;" viewBox="0 0 24 24"><path d="M12 3v10.55c-.59-.34-1.27-.55-2-.55-2.21 0-4 1.79-4 4s1.79 4 4 4 4-1.79 4-4V7h4V3h-6z"/></svg></div><div class="list-info"><div class="list-title">${name}</div><div class="list-sub">${playlists[name].length} songs</div></div>`;
        container.appendChild(el);
      });
    }
    function addToRecent(track) { recentPlays = recentPlays.filter(t => t.id.videoId !== track.id.videoId); recentPlays.unshift(track); if (recentPlays.length > 20) recentPlays.pop(); localStorage.setItem('bi_recent', JSON.stringify(recentPlays)); renderRecentlyPlayed(); }
    function downloadCurrent() { if (currentTrack) downloadSongFromList(currentTrack.id.videoId); }
    function downloadSongFromList(videoId) { navigator.clipboard.writeText(`https://www.youtube.com/watch?v=${videoId}`).then(() => { alert("Link copied! Opening downloader..."); }); window.open(`https://ssyoutube.com/watch?v=${videoId}`, '_blank'); }
    function playHeroSong() { searchYouTube("Top Hits 2024", 'trendingList', 15).then(() => { if (tracks.length > 0) playTrack(tracks[0], tracks); }); switchTab('trending', document.querySelectorAll('.nav-tab')[1]); }
    function formatTime(seconds) { if (isNaN(seconds)) return '0:00'; const m = Math.floor(seconds / 60); const s = Math.floor(seconds % 60); return `${m}:${s < 10 ? '0' : ''}${s}`; }
    document.getElementById('fullProgressBar').addEventListener('input', () => { if (player && player.getDuration) { player.seekTo((document.getElementById('fullProgressBar').value / 100) * player.getDuration(), true); } });
    window.onload = () => { loadHomeData(); };
  </script>
</body>
</html>
EOF

python -m http.server 8080
pkill -f "http.server"
python -m http.server 8080
rm index.html
cat > index.html << 'EOF'
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no">
  <title>B.I Music 🎵</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; -webkit-tap-highlight-color: transparent; }
    body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; background: #0a0a0f; color: #ffffff; height: 100vh; display: flex; flex-direction: column; overflow: hidden; }
    .wave-container { position: fixed; bottom: 0; left: 0; width: 100%; height: 100%; z-index: 0; overflow: hidden; opacity: 0.15; pointer-events: none; }
    .wave { position: absolute; bottom: 0; left: 0; width: 200%; height: 200px; background: linear-gradient(90deg, #00bcd4, #7c3aed, #00bcd4); border-radius: 45%; animation: waveAnim 12s linear infinite; animation-play-state: paused; }
    body.playing-waves .wave { animation-play-state: running; animation-duration: 4s; }
    @keyframes waveAnim { 0% { transform: translateX(-50%) rotate(0deg); } 100% { transform: translateX(-50%) rotate(360deg); } }
    ::-webkit-scrollbar { display: none; }
    .header { display: flex; justify-content: space-between; align-items: center; padding: 15px 20px; z-index: 10; position: relative; }
    .header h1 { font-size: 1.5rem; font-weight: 900; letter-spacing: -1px; }
    .header h1 span { color: #00bcd4; }
    .header-icons { display: flex; gap: 15px; }
    .header-icons svg { width: 24px; height: 24px; fill: #fff; cursor: pointer; }
    .main-content { flex: 1; overflow-y: auto; padding: 20px; padding-bottom: 120px; z-index: 10; position: relative; }
    .view { display: none; }
    .view.active { display: block; }
    
    .tabs { display: flex; gap: 10px; margin-bottom: 20px; }
    .tab { padding: 10px 20px; border-radius: 20px; background: #16161c; color: #a0a0b0; cursor: pointer; font-weight: 600; font-size: 0.9rem; }
    .tab.active { background: #00bcd4; color: #fff; }
    .controls-group { display: none; }
    .controls-group.active { display: block; }

    .search-bar { display: flex; gap: 10px; margin-bottom: 20px; }
    .search-bar input { flex: 1; padding: 14px; border-radius: 12px; border: none; background: #16161c; color: white; font-size: 1rem; }
    .search-bar button { padding: 0 20px; border-radius: 12px; border: none; background: #00bcd4; color: white; font-weight: bold; cursor: pointer; }

    .auth-box { background: #16161c; padding: 25px; border-radius: 20px; max-width: 400px; margin: 40px auto; text-align: center; border: 1px solid #333; }
    .auth-box h2 { margin-bottom: 20px; color: #00bcd4; }
    .auth-box input { width: 100%; padding: 14px; margin-bottom: 15px; border-radius: 12px; border: none; background: #1e1e28; color: white; font-size: 1rem; }
    .auth-box button { width: 100%; padding: 14px; border-radius: 12px; border: none; background: #00bcd4; color: white; font-weight: bold; font-size: 1rem; cursor: pointer; margin-bottom: 10px; }
    .auth-box button.secondary { background: #333; }
    
    .upload-box { background: #16161c; padding: 20px; border-radius: 20px; max-width: 500px; margin: 0 auto 20px auto; border: 1px solid #333; }
    .upload-box h2 { margin-bottom: 15px; color: #00bcd4; }
    .upload-box input { width: 100%; padding: 12px; margin-bottom: 12px; border-radius: 10px; border: none; background: #1e1e28; color: white; }
    .upload-box button { width: 100%; padding: 14px; border-radius: 10px; border: none; background: #22c55e; color: white; font-weight: bold; font-size: 1rem; cursor: pointer; }

    .song-item { display: flex; align-items: center; gap: 15px; padding: 12px; border-radius: 12px; background: #16161c; margin-bottom: 10px; cursor: pointer; border: 1px solid #222; }
    .song-item img { width: 50px; height: 50px; border-radius: 8px; object-fit: cover; background: #2a2a35; }
    .song-info { flex: 1; overflow: hidden; }
    .song-title { font-size: 0.95rem; font-weight: 600; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
    .song-artist { font-size: 0.8rem; color: #a0a0b0; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }

    .player-bar { position: fixed; bottom: 0; left: 0; width: 100%; background: #16161c; border-top: 1px solid #333; padding: 10px 20px; display: flex; align-items: center; gap: 15px; z-index: 100; transform: translateY(100%); transition: 0.3s; }
    .player-bar.active { transform: translateY(0); }
    .player-bar img { width: 45px; height: 45px; border-radius: 8px; object-fit: cover; }
    .player-info { flex: 1; overflow: hidden; }
    .player-title { font-size: 0.85rem; font-weight: 600; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
    .player-artist { font-size: 0.7rem; color: #a0a0b0; }
    .player-controls { display: flex; gap: 15px; align-items: center; }
    .player-controls button { background: none; border: none; cursor: pointer; }
    .player-controls svg { width: 28px; height: 28px; fill: #fff; }
    .player-controls .play-btn { width: 45px; height: 45px; background: #00bcd4; border-radius: 50%; display: flex; justify-content: center; align-items: center; }
    .player-controls .play-btn svg { fill: #000; width: 20px; height: 20px; }
    audio { display: none; }
  </style>
</head>
<body>
EOF

cat >> index.html << 'EOF'
<div class="wave-container"><div class="wave"></div><div class="wave"></div><div class="wave"></div></div>
<div class="header">
  <h1>B<span>.</span>I Music</h1>
  <div class="header-icons">
    <svg viewBox="0 0 24 24" onclick="showView('upload')"><path d="M19 13h-6v6h-2v-6H5v-2h6V5h2v6h6v2z"/></svg>
    <svg viewBox="0 0 24 24" onclick="logout()"><path d="M17 7l-1.41 1.41L18.17 11H8v2h10.17l-2.58 2.58L17 17l5-5zM4 5h8V3H4c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h8v-2H4V5z"/></svg>
  </div>
</div>
<div class="main-content" id="mainContent">
  <div class="view active" id="view-auth">
    <div class="auth-box">
      <h2 id="authTitle">Welcome to B.I Music</h2>
      <input type="email" id="authEmail" placeholder="Email">
      <input type="password" id="authPassword" placeholder="Password">
      <button id="authBtn" onclick="handleAuth()">Log In</button>
      <button class="secondary" onclick="toggleAuthMode()" id="authSwitchBtn">Need an account? Register</button>
    </div>
  </div>

  <div class="view" id="view-home">
    <div class="tabs">
      <div class="tab active" onclick="switchHomeTab('supabase', this)">My Uploads</div>
      <div class="tab" onclick="switchHomeTab('youtube', this)">YouTube</div>
    </div>
    <div class="controls-group active" id="group-supabase">
      <div id="songList"></div>
    </div>
    <div class="controls-group" id="group-youtube">
      <div class="search-bar">
        <input id="ytSearchInput" placeholder="Search YouTube..." onkeydown="if(event.key === 'Enter') searchYouTube()">
        <button onclick="searchYouTube()">Search</button>
      </div>
      <div id="ytResults"></div>
    </div>
  </div>

  <div class="view" id="view-upload">
    <div class="upload-box">
      <h2>Upload Your Music</h2>
      <input type="text" id="uploadTitle" placeholder="Song Title">
      <input type="text" id="uploadArtist" placeholder="Artist Name">
      <label style="color:#a0a0b0; font-size:0.8rem;">Audio File (MP3)</label>
      <input type="file" id="uploadAudio" accept="audio/*">
      <label style="color:#a0a0b0; font-size:0.8rem;">Cover Art (Image)</label>
      <input type="file" id="uploadCover" accept="image/*">
      <button onclick="uploadSong()">Upload Song</button>
    </div>
  </div>
</div>

<div class="player-bar" id="playerBar">
  <img id="playerArt" src="" alt="">
  <div class="player-info">
    <div class="player-title" id="playerTitle">No song playing</div>
    <div class="player-artist" id="playerArtist">Select a track</div>
  </div>
  <div class="player-controls">
    <button onclick="togglePlay()" id="playPauseBtn">
      <svg id="playIcon" viewBox="0 0 24 24"><path d="M8 5v14l11-7z"/></svg>
      <svg id="pauseIcon" viewBox="0 0 24 24" style="display:none;"><path d="M6 19h4V5H6v14zm8-14v14h4V5h-4z"/></svg>
    </button>
  </div>
</div>
<audio id="audioPlayer"></audio>
<div id="youtube-player"></div>
EOF

cat >> index.html << 'EOF'
  <script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js/+esm"></script>
  <script src="https://www.youtube.com/iframe_api"></script>
  <script>
    const SUPABASE_URL = 'https://fugfrgyosrugsrardytk.supabase.co';
    const SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZ1Z2ZyZ3lvc3J1Z3NyYXJkeXRrIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODk4MDI2NzMsImV4cCI6MjEwNTM3ODY3M30.tNzCEJwV23z9dT75CUytYhirOuxF25GS1CffzpeghPY';
    const YOUTUBE_API_KEY = 'AIzaSyAHry2KY5LLrfRWH7SaOYXYlKHvrZ6TZeY';
    const supabase = createClient(SUPABASE_URL, SUPABASE_KEY);
    
    let isLoginMode = true;
    let currentUser = null;
    let ytPlayer;
    let currentSource = 'supabase'; // 'supabase' or 'youtube'
    let songs = [], ytResults = [];
    let currentIndex = -1, isPlaying = false;

    // --- AUTHENTICATION ---
    function toggleAuthMode() {
      isLoginMode = !isLoginMode;
      document.getElementById('authTitle').textContent = isLoginMode ? 'Welcome Back' : 'Create an Account';
      document.getElementById('authBtn').textContent = isLoginMode ? 'Log In' : 'Register';
      document.getElementById('authSwitchBtn').textContent = isLoginMode ? 'Need an account? Register' : 'Already have an account? Log In';
    }

    async function handleAuth() {
      const email = document.getElementById('authEmail').value;
      const password = document.getElementById('authPassword').value;
      if (!email || !password) return alert("Please fill in both fields.");
      let result = isLoginMode ? await supabase.auth.signInWithPassword({ email, password }) : await supabase.auth.signUp({ email, password });
      if (result.error) return alert(result.error.message);
      if (result.data.user && !result.data.session) return alert("Check your email for the confirmation link!");
      currentUser = result.data.user;
      showView('home'); loadSongs();
    }

    async function logout() {
      await supabase.auth.signOut(); currentUser = null; showView('auth');
    }

    supabase.auth.getSession().then(({ data: { session } }) => {
      if (session) { currentUser = session.user; showView('home'); loadSongs(); } 
      else { showView('auth'); }
    });

    // --- VIEW SWITCHING ---
    function showView(viewName) {
      document.querySelectorAll('.view').forEach(v => v.classList.remove('active'));
      document.getElementById('view-' + viewName).classList.add('active');
    }

    function switchHomeTab(tab, element) {
      document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
      element.classList.add('active');
      document.querySelectorAll('.controls-group').forEach(g => g.classList.remove('active'));
      document.getElementById('group-' + tab).classList.add('active');
      currentSource = tab;
      if (tab === 'supabase') loadSongs();
    }

    // --- SUPABASE UPLOAD & LIST ---
    async function uploadSong() {
      const title = document.getElementById('uploadTitle').value;
      const artist = document.getElementById('uploadArtist').value;
      const audioFile = document.getElementById('uploadAudio').files[0];
      const coverFile = document.getElementById('uploadCover').files[0];
      if (!title || !artist || !audioFile) return alert("Please fill all fields and select an audio file.");
      if (!currentUser) return alert("You must be logged in to upload.");
      try {
        const audioExt = audioFile.name.split('.').pop();
        const audioPath = `${currentUser.id}/${Date.now()}.${audioExt}`;
        const { error: audioError } = await supabase.storage.from('Songs').upload(audioPath, audioFile);
        if (audioError) throw audioError;
        const audioUrl = supabase.storage.from('Songs').getPublicUrl(audioPath).data.publicUrl;
        let coverUrl = null;
        if (coverFile) {
          const coverExt = coverFile.name.split('.').pop();
          const coverPath = `${currentUser.id}/${Date.now()}.${coverExt}`;
          const { error: coverError } = await supabase.storage.from('Cover').upload(coverPath, coverFile);
          if (coverError) throw coverError;
          coverUrl = supabase.storage.from('Cover').getPublicUrl(coverPath).data.publicUrl;
        }
        const { error: dbError } = await supabase.from('songs').insert({ title, artist_name: artist, audio_url: audioUrl, cover_art_url: coverUrl, user_id: currentUser.id });
        if (dbError) throw dbError;
        alert("Song uploaded successfully! 🎵");
        showView('home'); loadSongs();
      } catch (err) { alert("Upload failed: " + err.message); }
    }

    async function loadSongs() {
      const { data, error } = await supabase.from('songs').select('*').order('id', { ascending: false });
      if (error) { console.log(error); return; }
      songs = data; renderSongList();
    }

    function renderSongList() {
      const container = document.getElementById('songList');
      container.innerHTML = songs.length === 0 ? '<p style="color:#888;text-align:center;">No songs uploaded yet.</p>' : '';
      songs.forEach((song, index) => {
        const el = document.createElement('div'); el.className = 'song-item'; el.onclick = () => playSong(index, 'supabase');
        el.innerHTML = `<img src="${song.cover_art_url || 'https://via.placeholder.com/150'}" alt=""><div class="song-info"><div class="song-title">${song.title}</div><div class="song-artist">${song.artist_name}</div></div>`;
        container.appendChild(el);
      });
    }

    // --- YOUTUBE SEARCH ---
    async function searchYouTube() {
      const query = document.getElementById('ytSearchInput').value.trim();
      if (!query) return;
      const container = document.getElementById('ytResults');
      container.innerHTML = '<p style="color:white;text-align:center;">Searching...</p>';
      try {
        const res = await fetch(`https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=15&q=${encodeURIComponent(query)}&type=video&key=${YOUTUBE_API_KEY}`);
        const data = await res.json();
        if (data.error) { container.innerHTML = `<p style="color:red;">Error: ${data.error.message}</p>`; return; }
        ytResults = data.items; renderYoutubeList();
      } catch (e) { container.innerHTML = '<p style="color:red;">Network error.</p>'; }
    }

    function renderYoutubeList() {
      const container = document.getElementById('ytResults'); container.innerHTML = '';
      ytResults.forEach((track, index) => {
        const el = document.createElement('div'); el.className = 'song-item'; el.onclick = () => playYoutubeTrack(index);
        el.innerHTML = `<img src="${track.snippet.thumbnails.default.url}" alt=""><div class="song-info"><div class="song-title">${track.snippet.title}</div><div class="song-artist">${track.snippet.channelTitle}</div></div>`;
        container.appendChild(el);
      });
    }

    // --- PLAYER LOGIC (HYBRID) ---
    function onYouTubeIframeAPIReady() {
      ytPlayer = new YT.Player('youtube-player', { height: '1', width: '1', playerVars: { 'playsinline': 1, 'controls': 0 }, events: { 'onStateChange': onPlayerStateChange } });
    }

    function onPlayerStateChange(event) {
      if (event.data == YT.PlayerState.PLAYING) { isPlaying = true; document.body.classList.add('playing-waves'); updatePlayIcon(); }
      else if (event.data == YT.PlayerState.PAUSED) { isPlaying = false; document.body.classList.remove('playing-waves'); updatePlayIcon(); }
    }

    function playSong(index, source) {
      currentSource = source; currentIndex = index;
      const player = document.getElementById('audioPlayer');
      if (source === 'supabase') {
        if (ytPlayer && ytPlayer.pauseVideo) ytPlayer.pauseVideo();
        const song = songs[index];
        document.getElementById('playerArt').src = song.cover_art_url || 'https://via.placeholder.com/150';
        document.getElementById('playerTitle').textContent = song.title;
        document.getElementById('playerArtist').textContent = song.artist_name;
        player.src = song.audio_url; player.play();
      }
      isPlaying = true; updatePlayIcon(); document.getElementById('playerBar').classList.add('active'); document.body.classList.add('playing-waves');
    }

    function playYoutubeTrack(index) {
      currentSource = 'youtube'; currentIndex = index;
      const player = document.getElementById('audioPlayer');
      player.pause(); // Pause Supabase audio
      const track = ytResults[index];
      document.getElementById('playerArt').src = track.snippet.thumbnails.high.url;
      document.getElementById('playerTitle').textContent = track.snippet.title;
      document.getElementById('playerArtist').textContent = track.snippet.channelTitle;
      if (ytPlayer && ytPlayer.loadVideoById) ytPlayer.loadVideoById(track.id.videoId);
      document.getElementById('playerBar').classList.add('active');
    }

    function togglePlay() {
      const player = document.getElementById('audioPlayer');
      if (currentSource === 'youtube') {
        if (!ytPlayer || !ytPlayer.getPlayerState) return;
        if (isPlaying) { ytPlayer.pauseVideo(); document.body.classList.remove('playing-waves'); } 
        else { ytPlayer.playVideo(); document.body.classList.add('playing-waves'); }
        isPlaying = !isPlaying; updatePlayIcon();
      } else {
        if (!player.src) return;
        if (isPlaying) { player.pause(); document.body.classList.remove('playing-waves'); } 
        else { player.play(); document.body.classList.add('playing-waves'); }
        isPlaying = !isPlaying; updatePlayIcon();
      }
    }

    function updatePlayIcon() {
      document.getElementById('playIcon').style.display = isPlaying ? 'none' : 'block';
      document.getElementById('pauseIcon').style.display = isPlaying ? 'block' : 'none';
    }

    document.getElementById('audioPlayer').addEventListener('ended', () => {
      if (currentSource === 'supabase' && currentIndex < songs.length - 1) playSong(currentIndex + 1, 'supabase');
      else { isPlaying = false; updatePlayIcon(); document.body.classList.remove('playing-waves'); }
    });
  </script>
</body>
</html>
EOF

python -m http.server 8080
