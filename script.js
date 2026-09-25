
var PIPES=['https://pipedapi.kavin.rocks','https://pipedapi.adminforge.de','https://api.piped.private.coffee','https://pipedapi.reallyaweso.me'];
var pipeIdx=0;
async function pget(path){for(var i=0;i<PIPES.length;i++){var idx=(pipeIdx+i)%PIPES.length;try{var r=await fetch(PIPES[idx]+path);if(!r.ok)throw 0;var d=await r.json();pipeIdx=idx;return d;}catch(e){}}throw new Error('busy');}
var SUPABASE_URL='https://fugfrgyosrugsrardytk.supabase.co';
var SUPABASE_KEY='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZ1Z2ZyZ3lvc3J1Z3NyYXJkeXRrIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODk4MDI2NzMsImV4cCI6MjEwNTM3ODY3M30.tNzCEJwV23z9dT75CUytYhirOuxF25GS1CffzpeghPY';
var db=null,isLoginMode=true,currentUser=null,ytPlayer=null,ytReady=false;
var currentSource='db',songs=[],ytResults=[],playQueue=[],currentIndex=-1,isPlaying=false,isShuffle=false,repeatMode=0,playbackSpeed=1;
var followedArtists=JSON.parse(localStorage.getItem('bi_followed')||'[]'),currentArtist={name:'',img:''};
var trendingPool=[],trendingIdx=0,trendingLoading=false;
var hotPool=[],hotIdx=0,hotLoading=false;
var mixPool=[],mixIdx=0,mixLoading=false;
var artistPool=[],artistIdx=0,artistLoading=false;
var genrePool=[],genreQuery='',genreIdx=0,genreLoading=false;
var artistSongPool=[],artistSongLoading=false;
var simPool=[],simTitle='',simLoading=false,simQIdx=0,simSimilar=[];
var homePool=[],homeQIdx=0,homeLoading=false;
var CURATED_ARTISTS=['Drake','Kendrick Lamar','J. Cole','Future','21 Savage','Travis Scott','Metro Boomin','The Weeknd','Post Malone','SZA','Doja Cat','Ariana Grande','Taylor Swift','Billie Eilish','Rihanna','Chris Brown','Beyoncé','Nicki Minaj','Cardi B','Megan Thee Stallion','Burna Boy','Wizkid','Davido','Asake','Rema','Tems','Olamide','Fireboy DML','Omah Lay','Ayra Starr','Ruger','BNXN','Kizz Daniel','Tekno','Yemi Alade','Tiwa Savage','2Baba','Phyno','Flavour','Don Jazzy','Sarkodie','Stonebwoy','Shatta Wale','Black Sherif','Gyakie','Sauti Sol','Nyashinski','Diamond Platnumz','Harmonize','Zuchu','Rayvanny','Alikiba','Tyla','Master KG','Nasty C','DJ Maphorisa','Kabza De Small','Focalistic','Konshens','Popcaan','Busy Signal','Shenseea','Skillibeng','Vybz Kartel','Alkaline','Mavado','Sean Paul','Shaggy','Chronixx','Koffee','Masicka','Bob Marley','Ed Sheeran','Adele','Harry Styles','Dua Lipa','Sam Smith','Lewis Capaldi','ZAYN','One Direction','Little Mix','Stormzy','Central Cee','Dave','J Hus','Aitch','Rita Ora','Calvin Harris','Ellie Goulding','Arctic Monkeys','The 1975','Alan Walker','Kygo','Martin Garrix','Tiësto','Avicii','Swedish House Mafia','David Guetta','DJ Snake','Bad Bunny','Daddy Yankee','Ozuna','J Balvin','Maluma','Karol G','Shakira','BTS','BLACKPINK','TWICE','Stray Kids','NewJeans','Yoasobi','Arijit Singh','Diljit Dosanjh','Aya Nakamura','Stromae','Lorde','Sia','Iggy Azalea','Tame Impala','Troye Sivan','Hozier','Niall Horan','Eminem','50 Cent','Dr. Dre','Jay-Z','Lil Wayne','Usher','Trey Songz','Bryson Tiller','Miguel','Brent Faiyaz','Steve Lacy','Lil Baby','Gunna','Young Thug','Lil Durk','King Von','Polo G','Roddy Ricch','DaBaby','Lil Nas X','Jack Harlow','Doechii','Tyler The Creator','Mac Miller','Kid Cudi','Kanye West','Pusha T','Big Sean','Meek Mill','Rick Ross','2 Chainz','Michael Jackson','Bruno Mars','Olivia Rodrigo','Miley Cyrus','Demi Lovato','Selena Gomez','Halsey','Kehlani','Charlie Puth','Maroon 5','Imagine Dragons','OneRepublic','Sheebah','Spice Diana','Vinka','Fik Fameica','Winnie Nwagi','Jose Chameleone','Bebe Cool','Eddy Kenzo','Joshua Baraka','Pallaso','Azawi','Lydia Jazmine','T Paul','Kapeke','Maurice Kirya'];
var CURATED_SIMILAR={'drake':['Kendrick Lamar','J. Cole','Future','21 Savage'],'kendrick lamar':['J. Cole','Drake','Travis Scott','Future'],'burna boy':['Wizkid','Davido','Asake','Rema'],'wizkid':['Burna Boy','Davido','Rema','Tems'],'davido':['Wizkid','Burna Boy','Asake','Rema'],'asake':['Burna Boy','Olamide','Davido','Rema'],'rema':['Burna Boy','Wizkid','Asake','Davido'],'tems':['Wizkid','Burna Boy','SZA','Arya Starr'],'nicki minaj':['Cardi B','Megan Thee Stallion','Doja Cat','Ariana Grande'],'cardi b':['Nicki Minaj','Megan Thee Stallion','Doja Cat','City Girls'],'rihanna':['Beyoncé','Nicki Minaj','Ariana Grande','Doja Cat'],'the weeknd':['Post Malone','Bruno Mars','Doja Cat','SZA'],'sza':['Doja Cat','Summer Walker','Frank Ocean','Jhené Aiko'],'doja cat':['SZA','Ariana Grande','Nicki Minaj','Megan Thee Stallion'],'ariana grande':['Taylor Swift','Doja Cat','Dua Lipa','Selena Gomez'],'taylor swift':['Ariana Grande','Selena Gomez','Ed Sheeran','Olivia Rodrigo'],'billie eilish':['Ariana Grande','Olivia Rodrigo','Dua Lipa','Selena Gomez'],'ed sheeran':['Shawn Mendes','Lewis Capaldi','Sam Smith','James Arthur'],'chris brown':['Usher','Trey Songz','Bryson Tiller','Miguel'],'konshens':['Popcaan','Busy Signal','Shenseea','Skillibeng'],'popcaan':['Konshens','Busy Signal','Vybz Kartel','Alkaline'],'busy signal':['Konshens','Popcaan','Mavado','Aidonia'],'shenseea':['Spice','Konshens','Skillibeng','Popcaan'],'vybz kartel':['Popcaan','Alkaline','Mavado','Konshens'],'alan walker':['Kygo','Martin Garrix','Avicii','The Chainsmokers'],'kygo':['Alan Walker','The Chainsmokers','Martin Garrix','Sigala'],'martin garrix':['Tiësto','Afrojack','Avicii','Hardwell'],'bad bunny':['Daddy Yankee','Ozuna','J Balvin','Anuel AA'],'bts':['BLACKPINK','TWICE','Stray Kids','NewJeans'],'blackpink':['BTS','TWICE','Stray Kids','NewJeans'],'sheebah':['Spice Diana','Vinka','Winnie Nwagi','Fik Fameica'],'spice diana':['Sheebah','Vinka','Winnie Nwagi','Fik Fameica'],'eddy kenzo':['Sheebah','Fik Fameica','Spice Diana','Vinka'],'jose chameleone':['Eddy Kenzo','Bebe Cool','Sheebah','Fik Fameica'],'bebe cool':['Jose Chameleone','Eddy Kenzo','Sheebah','Fik Fameica'],'maurice kirya':['Kenneth Mugabi','Azawi','Eddy Kenzo','Joshua Baraka'],'azawi':['Sheebah','Spice Diana','Vinka','Maurice Kirya'],'fireboy dml':['Joeboy','Omah Lay','Kizz Daniel','BNXN'],'omah lay':['Fireboy DML','Joeboy','BNXN','Kizz Daniel'],'joeboy':['Fireboy DML','Omah Lay','BNXN','Kizz Daniel'],'kizz daniel':['Tekno','Fireboy DML','Omah Lay','BNXN'],'ayra starr':['Tems','Tyla','Wizkid','Rema'],'tyla':['Tems','Ayra Starr','Master KG','Focalistic'],'master kg':['Kabza De Small','DJ Maphorisa','Focalistic','Tyla']};
var COUNTRY={'sheebah':'🇺🇬','spice diana':'🇺🇬','vinka':'🇺🇬','fik fameica':'🇺🇬','winnie nwagi':'🇺🇬','jose chameleone':'🇺🇬','bebe cool':'🇺🇬','eddy kenzo':'🇺🇬','joshua baraka':'🇺🇬','pallaso':'🇺🇬','azawi':'🇺🇬','lydia jazmine':'🇺🇬','t paul':'🇺🇬','kapeke':'🇺🇬','maurice kirya':'🇺🇬','burna boy':'🇳🇬','wizkid':'🇳🇬','davido':'🇳🇬','asake':'🇳🇬','rema':'🇳🇬','tems':'🇳🇬','olamide':'🇳🇬','fireboy dml':'🇳🇬','joeboy':'🇳🇬','kizz daniel':'🇳🇬','tekno':'🇳🇬','yemi alade':'🇳🇬','tiwa savage':'🇳🇬','ayra starr':'🇳🇬','ruger':'🇳🇬','omah lay':'🇳🇬','bnxn':'🇳🇬','2baba':'🇳🇬','phyno':'🇳🇬','flavour':'🇳🇬','don jazzy':'🇳🇬','sarkodie':'🇬🇭','stonebwoy':'🇬🇭','shatta wale':'🇬🇭','black sherif':'🇬🇭','gyakie':'🇬🇭','sauti sol':'🇰🇪','nyashinski':'🇰🇪','diamond platnumz':'🇹🇿','harmonize':'🇹🇿','zuchu':'🇹🇿','rayvanny':'🇹🇿','alikiba':'🇹🇿','tyla':'🇿🇦','master kg':'🇿🇦','nasty c':'🇿🇦','dj maphorisa':'🇿🇦','kabza de small':'🇿🇦','focalistic':'🇿🇦','drake':'🇨🇦','the weeknd':'🇨🇦','justin bieber':'🇨🇦','shawn mendes':'🇨🇦','tate mcrae':'🇨🇦','chris brown':'🇺🇸','sza':'🇺🇸','doja cat':'🇺🇸','ariana grande':'🇺🇸','taylor swift':'🇺🇸','billie eilish':'🇺🇸','post malone':'🇺🇸','travis scott':'🇺🇸','future':'🇺🇸','21 savage':'🇺🇸','kendrick lamar':'🇺🇸','j. cole':'🇺🇸','juice wrld':'🇺🇸','lil baby':'🇺🇸','gunna':'🇺🇸','young thug':'🇺🇸','megan thee stallion':'🇺🇸','cardi b':'🇺🇸','nicki minaj':'🇺🇸','beyoncé':'🇺🇸','frank ocean':'🇺🇸','summer walker':'🇺🇸','metro boomin':'🇺🇸','lil wayne':'🇺🇸','eminem':'🇺🇸','50 cent':'🇺🇸','dr. dre':'🇺🇸','jay-z':'🇺🇸','usher':'🇺🇸','trey songz':'🇺🇸','bryson tiller':'🇺🇸','miguel':'🇺🇸','brent faiyaz':'🇺🇸','steve lacy':'🇺🇸','lil uzi vert':'🇺🇸','playboi carti':'🇺🇸','lil durk':'🇺🇸','king von':'🇺🇸','polo g':'🇺🇸','roddy ricch':'🇺🇸','dababy':'🇺🇸','lil nas x':'🇺🇸','jack harlow':'🇺🇸','doechii':'🇺🇸','tyler the creator':'🇺🇸','mac miller':'🇺🇸','kid cudi':'🇺🇸','kanye west':'🇺🇸','bruno mars':'🇺🇸','olivia rodrigo':'🇺🇸','miley cyrus':'🇺🇸','demi lovato':'🇺🇸','selena gomez':'🇺🇸','halsey':'🇺🇸','kehlani':'🇺🇸','charlie puth':'🇺🇸','maroon 5':'🇺🇸','imagine dragons':'🇺🇸','onerepublic':'🇺🇸','ed sheeran':'🇬🇧','coldplay':'🇬🇧','adele':'🇬🇧','harry styles':'🇬🇧','dua lipa':'🇬🇧','sam smith':'🇬🇧','lewis capaldi':'🇬🇧','zayn':'🇬🇧','one direction':'🇬🇧','little mix':'🇬🇧','stormzy':'🇬🇧','central cee':'🇬🇧','dave':'🇬🇧','j hus':'🇬🇧','aitch':'🇬🇧','rita ora':'🇬🇧','calvin harris':'🇬🇧','ellie goulding':'🇬🇧','arctic monkeys':'🇬🇧','the 1975':'🇬🇧','hozier':'🇮🇪','niall horan':'🇮🇪','sia':'🇦🇺','iggy azalea':'🇦🇺','tame impala':'🇦🇺','troye sivan':'🇦🇺','lorde':'🇳🇿','rihanna':'🇧🇧','bob marley':'🇯🇲','konshens':'🇯🇲','busy signal':'🇯🇲','popcaan':'🇯🇲','sean paul':'🇯🇲','shaggy':'🇯🇲','skillibeng':'🇯🇲','shenseea':'🇯🇲','spice':'🇯🇲','vybz kartel':'🇯🇲','alkaline':'🇯🇲','mavado':'🇯🇲','buju banton':'🇯🇲','chronixx':'🇯🇲','koffee':'🇯🇲','masicka':'🇯🇲','shakira':'🇨🇴','maluma':'🇨🇴','karol g':'🇨🇴','j balvin':'🇨🇴','bad bunny':'🇵🇷','daddy yankee':'🇵🇷','ozuna':'🇵🇷','rosalía':'🇪🇸','enrique iglesias':'🇪🇸','aya nakamura':'🇫🇷','dj snake':'🇫🇷','david guetta':'🇫🇷','stromae':'🇧🇪','alan walker':'🇳🇴','kygo':'🇳🇴','aurora':'🇳🇴','martin garrix':'🇳🇱','tiësto':'🇳🇱','armin van buuren':'🇳🇱','avicii':'🇸🇪','swedish house mafia':'🇸🇪','zara larsson':'🇸🇪','bts':'🇰🇷','blackpink':'🇰🇷','twice':'🇰🇷','stray kids':'🇰🇷','newjeans':'🇰🇷','yoasobi':'🇯🇵','arijit singh':'🇮🇳','diljit dosanjh':'🇮🇳','peso pluma':'🇲🇽','anitta':'🇧🇷'};
var BAD_TITLE=/\b(mix|nonstop|non-stop|mixtape|compilation|best of|megamix|full album|playlist|lofi|lo-fi|afro house|study|sleep|ambient|lounge|radio show|podcast|episode|hour|hours|instrumental|type beat|karaoke|bootleg|unofficial|remake|rework|ai cover|style x|mashup|24\/7|vol\.|volume|pt\.|part\s*\d|extended\s+mix)\b/i;
var HOME_QUERIES=['afrobeats 2025 hits','hip hop 2025 hits','rnb 2025 hits','amapiano 2025 hits','dancehall 2025 hits','afro pop 2025 hits','trap 2025 hits','gospel 2025 hits','afro soul 2025','drill 2025 hits','naija 2025 hits','ugandan music 2025','reggae 2025 hits','soul 2025 hits','pop hits 2025'];
var VIBE_SAD=['Adele','Sam Smith','Lewis Capaldi','Olivia Rodrigo','Lauv','Ariana Grande'];
var VIBE_PARTY=['David Guetta','Calvin Harris','Kygo','The Chainsmokers','Martin Garrix','Avicii'];
var VIBE_HIPHOP=['Drake','Travis Scott','Future','21 Savage','Metro Boomin','Kendrick Lamar'];
var VIBE_RNB=['SZA','Doja Cat','Summer Walker','Brent Faiyaz','Kehlani'];
var VIBE_GOSPEL=['Kirk Franklin','Sinach','Nathaniel Bassey','Hillsong','Elevation Worship'];
var VIBE_CHILL=['Kygo','The Chainsmokers','Calvin Harris','Sigala','Jonas Blue'];
var VIBE_LATENIGHT=['The Weeknd','Post Malone','SZA','Drake','Frank Ocean'];
function isRealSong(v){var t=(v.title||'').toLowerCase();if(BAD_TITLE.test(t))return false;if(v.duration&&v.duration>0){if(v.duration<45||v.duration>600)return false;}return true;}
function isRealArtistName(name){if(!name)return false;var n=name.trim();if(n.length<2)return false;var bad=/(whats|that song|love ?& ?hip|hip.?hop|universe|nation|world|media|studio|records|entertainment|network|channel|radio|podcast|official|music group|group$|crew|band$|tribute|cover|chart|billboard|dj\s|mix|mashup|hour|24|live|concert|festival|tv$|ent\.|house|beats$|what'?s)/i;if(bad.test(n))return false;if(/^[0-9]+$/.test(n))return false;return true;}
function cleanArtistName(name){if(!name)return '';return name.replace(/\s*-\s*Topic$/i,'').replace(/VEVO$/i,'').replace(/Official$/i,'').trim();}
function detectVibeKey(title){var t=(title||'').toLowerCase();if(/love|heart|miss|sad|broken|cry|alone|goodbye|sorry|hurt|tears|forever|loved|without you/.test(t))return 'sad';if(/party|turn up|club|tonight|dance|floor|move|shake|wild|lit|bounce/.test(t))return 'party';if(/money|cash|hustle|grind|trap|drip|rich|bands|stack/.test(t))return 'hiphop';if(/baby|girl|boy|shawty|honey|touch|kiss/.test(t))return 'rnb';if(/pray|god|faith|bless|heaven|holy|jesus|amen|worship/.test(t))return 'gospel';if(/summer|sun|beach|island|tropical|wave/.test(t))return 'chill';if(/night|moon|dark|late|city|street|lights/.test(t))return 'latenight';return '';}
function vibeList(key){if(key==='sad')return VIBE_SAD;if(key==='party')return VIBE_PARTY;if(key==='hiphop')return VIBE_HIPHOP;if(key==='rnb')return VIBE_RNB;if(key==='gospel')return VIBE_GOSPEL;if(key==='chill')return VIBE_CHILL;if(key==='latenight')return VIBE_LATENIGHT;return [];}
function pickVibeArtist(key){var l=vibeList(key);if(!l.length)return '';return l[Math.floor(Math.random()*l.length)];}
window.addEventListener('load',function(){if(typeof supabase==='undefined'){document.getElementById('authError').textContent='Loading failed';return;}db=supabase.createClient(SUPABASE_URL,SUPABASE_KEY);db.auth.getSession().then(function(r){if(r.data.session){currentUser=r.data.session.user;enterApp();}else showView('auth');}).catch(function(){showView('auth');});bindHoldBtn();});
function toggleAuthMode(){isLoginMode=!isLoginMode;document.getElementById('authTitle').textContent=isLoginMode?'Log In':'Create Account';document.getElementById('authSubtitle').textContent=isLoginMode?'Welcome back to B.I Music':'Join B.I Music today';document.getElementById('authBtn').textContent=isLoginMode?'Log In':'Register';document.getElementById('authSwitchBtn').textContent=isLoginMode?'Need an account? Register':'Already have an account? Log In';document.getElementById('authError').textContent='';}
async function handleAuth(){var e=document.getElementById('authError');e.textContent='';if(!db){e.textContent='Loading';return;}var em=document.getElementById('authEmail').value.trim(),pw=document.getElementById('authPassword').value,b=document.getElementById('authBtn');if(!em||!pw){e.textContent='Fill both fields.';return;}if(pw.length<6){e.textContent='Password 6+ characters.';return;}b.disabled=true;b.textContent=isLoginMode?'Logging in...':'Creating...';try{var r=isLoginMode?await db.auth.signInWithPassword({email:em,password:pw}):await db.auth.signUp({email:em,password:pw});if(r.error){e.textContent=r.error.message;b.disabled=false;b.textContent=isLoginMode?'Log In':'Register';return;}if(!r.data.session){e.textContent='Check email to confirm.';b.disabled=false;b.textContent=isLoginMode?'Log In':'Register';return;}currentUser=r.data.user;b.disabled=false;b.textContent=isLoginMode?'Log In':'Register';enterApp();}catch(x){e.textContent='Error: '+x.message;b.disabled=false;b.textContent=isLoginMode?'Log In':'Register';}}
async function logout(){if(db)await db.auth.signOut();currentUser=null;showView('auth');document.getElementById('authPassword').value='';}
function enterApp(){document.getElementById('profileEmail').textContent=currentUser.email||'';switchTab('home',document.querySelectorAll('.nav-item')[0]);}
function showView(name){document.querySelectorAll('.view').forEach(function(v){v.classList.remove('active');});var t=document.getElementById('view-'+name);if(t)t.classList.add('active');var isAuth=(name==='auth');document.getElementById('mainHeader').style.display=isAuth?'none':'flex';document.getElementById('mainSearchRow').style.display=(name==='home')?'flex':'none';document.getElementById('mainNavTabs').style.display=(name==='home')?'flex':'none';document.getElementById('bottomNav').classList.toggle('active',!isAuth);}
function switchTab(tab,el){document.querySelectorAll('.nav-item').forEach(function(t){t.classList.remove('active');});if(el)el.classList.add('active');if(tab==='home'){showView('home');loadHomeData();}else if(tab==='search')showView('search');else if(tab==='library'){showView('library');loadMyUploads();}else if(tab==='profile')showView('profile');}
function switchHomeTab(tab,el){document.querySelectorAll('.nav-tab').forEach(function(t){t.classList.remove('active');});if(el)el.classList.add('active');document.querySelectorAll('.home-tab').forEach(function(t){t.style.display='none';});var t=document.getElementById('tab-'+tab);if(t)t.style.display='block';if(tab==='trending'){refreshTrending();}if(tab==='mixtape'&&mixPool.length===0){for(var i=0;i<3;i++)loadMixtapes();}if(tab==='artists'&&artistPool.length===0){for(var j=0;j<3;j++)loadArtistsNext();}if(tab==='genres')document.getElementById('genreResults').innerHTML='';}
function shareApp(){var url=window.location.href;if(navigator.share){navigator.share({title:'B.I Music 🎵',text:'Listen to music for free on B.I Music!',url:url}).catch(function(){});}else{navigator.clipboard.writeText(url).then(function(){alert('Link copied!');}).catch(function(){prompt('Copy:',url);});}}
function contactUs(){window.open('https://wa.me/256707103377?text='+encodeURIComponent('Hi! I am using B.I Music and I need help.'),'_blank');}
var _soonFeature='';
function comingSoon(name){_soonFeature=name;var icons={'Artist Dashboard':'📊','Upload Music':'🎵','Promote Your Music':'🚀'};document.getElementById('soonIcon').textContent=icons[name]||'🚀';document.getElementById('soonTitle').textContent=name+' is Coming Soon';document.getElementById('soonText').textContent='This feature is under development. Want us to notify you when it launches?';document.getElementById('soonModal').classList.add('show');}
function closeSoon(){document.getElementById('soonModal').classList.remove('show');}
function contactFromSoon(){closeSoon();window.open('https://wa.me/256707103377?text='+encodeURIComponent('Hi! Notify me when '+_soonFeature+' launches on B.I Music.'),'_blank');}
async function loadMyUploads(){if(!db)return;var r=await db.from('songs').select('*').order('id',{ascending:false});var c=document.getElementById('myUploadsList');if(r.error||!r.data||r.data.length===0){c.innerHTML='<p style="color:#666;text-align:center;padding:40px">No uploads yet.</p>';return;}c.innerHTML='';r.data.forEach(function(s){var el=document.createElement('div');el.className='list-item';el.onclick=function(){playDbSong(r.data.indexOf(s));};el.innerHTML='<img src="'+(s.cover_art_url||'https://via.placeholder.com/150')+'"><div class="list-info"><div class="list-title">'+s.title+'</div><div class="list-sub">'+s.artist_name+'</div></div>';c.appendChild(el);});}
async function loadHomeData(){if(!db)return;try{var r=await db.from('songs').select('*').order('id',{ascending:false}).limit(20);songs=r.data||[];}catch(e){songs=[];}renderRecentlyPlayed();renderFollowedArtists();renderPopularArtists();loadForYou();for(var i=0;i<4;i++)loadHomeMore();}
function renderPopularArtists(){loadArtistGrid('popularArtists',CURATED_ARTISTS.slice(0,9));}
async function loadHomeMore(){if(homeLoading)return;if(homePool.length>=400)return;homeLoading=true;for(var b=0;b<3;b++){if(homePool.length>=400)break;var q=HOME_QUERIES[homeQIdx%HOME_QUERIES.length];homeQIdx++;try{var d=await pget('/search?q='+encodeURIComponent(q)+'&filter=videos');var items=(d.items||[]).filter(function(v){return v.url&&isRealSong(v);});var c=document.getElementById('youMightLike');if(!c)break;items.forEach(function(v){if(homePool.length>=400)return;var vid=(v.url||'').replace('/watch?v=','');if(homePool.some(function(x){return x.id===vid;}))return;var obj={id:vid,title:v.title,uploaderName:v.uploaderName,thumbnail:v.thumbnail};homePool.push(obj);var idx=homePool.length-1;var el=document.createElement('div');el.className='card';el.onclick=function(){playQueue=homePool.map(function(x){return{id:{videoId:x.id},snippet:{title:x.title,channelTitle:x.uploaderName,thumbnails:{default:{url:x.thumbnail},high:{url:x.thumbnail}}}};});ytResults=playQueue;playYoutube(idx);};el.innerHTML='<div class="card-img"><img src="'+obj.thumbnail+'"></div><div class="card-title">'+obj.title+'</div><div class="card-sub">'+obj.uploaderName+'</div>';c.appendChild(el);});}catch(e){}}homeLoading=false;}
async function loadTrending(){if(trendingLoading)return;if(trendingPool.length>=500)return;trendingLoading=true;var c=document.getElementById('trendingList');if(!c){trendingLoading=false;return;}if(trendingPool.length===0)c.innerHTML='<p style="color:#666;text-align:center;padding:20px">Loading...</p>';var queries=['new songs 2025','trending music 2025','top hits 2025','billboard hot 100','spotify top 50','apple music top songs','new afrobeats 2025','new hip hop 2025','new rnb 2025','new dancehall 2025','new amapiano 2025','official music video 2025','latest songs this week','new pop 2025','top afrobeats songs','top hip hop songs','top rnb songs','new drill 2025','new afro pop 2025','new gospel 2025','new soul 2025','new trap 2025','naija top songs','uk top songs','us top songs','african top songs','chart songs 2025','viral songs 2025','radio hits 2025','new releases this month','hot new songs','fresh music 2025','top 40 songs','new nigeria songs','new ghana songs','new kenya songs','new south africa songs','new uganda songs','top afrobeats video','top hip hop video','top rnb video','top dancehall video','top amapiano video','official audio 2025','lyric video 2025','music video 2025'];if(trendingIdx>=queries.length){queries.sort(function(){return Math.random()-0.5;});trendingIdx=0;}for(var b=0;b<2;b++){if(trendingPool.length>=500)break;var q=queries[trendingIdx%queries.length];trendingIdx++;try{var d=await pget('/search?q='+encodeURIComponent(q)+'&filter=videos');var items=(d.items||[]).filter(function(v){return v.url&&isRealSong(v);});items.forEach(function(v){if(trendingPool.length>=500)return;var vid=(v.url||'').replace('/watch?v=','');if(trendingPool.some(function(x){return x.id===vid;}))return;var u=(v.uploaderName||'').toLowerCase();var t=(v.title||'').toLowerCase();var verified=/vevo$|topic$|official|records|music$/.test(u)||/official|music video|audio|visualizer|lyric/.test(t);if(!verified)return;var obj={id:vid,title:v.title,uploaderName:v.uploaderName,thumbnail:v.thumbnail};trendingPool.push(obj);var ix=trendingPool.length-1;var el=document.createElement('div');el.className='list-item';el.onclick=function(){playQueue=trendingPool.map(function(x){return{id:{videoId:x.id},snippet:{title:x.title,channelTitle:x.uploaderName,thumbnails:{default:{url:x.thumbnail},high:{url:x.thumbnail}}}};});ytResults=playQueue;playYoutube(ix);};el.innerHTML='<img src="'+obj.thumbnail+'"><div class="list-info"><div class="list-title">'+obj.title+'</div><div class="list-sub">'+obj.uploaderName+'</div></div><button class="dl-btn" onclick="event.stopPropagation();dlId(\''+vid+'\')"><svg viewBox="0 0 24 24"><path d="M5 20h14v-2H5v2zM19 9h-4V3H9v6H5l7 7 7-7z"/></svg></button>';c.appendChild(el);});}catch(e){}}trendingLoading=false;var tb=document.getElementById('trendingLoadBtn');if(tb)tb.style.display='block';}
function refreshTrending(){trendingPool=[];trendingIdx=0;trendingLoading=false;hotPool=[];hotIdx=0;hotLoading=false;var c=document.getElementById('trendingList');if(c)c.innerHTML='';var hc=document.getElementById('hotList');if(hc)hc.innerHTML='';loadTrending();loadHot();}
async function loadHot(){if(hotLoading)return;if(hotPool.length>=400)return;hotLoading=true;var c=document.getElementById('hotList');if(!c){hotLoading=false;return;}if(hotPool.length===0)c.innerHTML='<p style="color:#666;text-align:center;padding:20px">Loading...</p>';var queries=['new songs 2025 release','new music this week','fresh afrobeats 2025','new hip hop 2025','new rnb 2025','new dancehall 2025','new amapiano 2025','latest hits 2025','just released 2025','brand new music','this week music','new single 2025','new album 2025','fresh drops 2025','new naija 2025','new uk music','new us music','new african music'];if(hotIdx>=queries.length){queries.sort(function(){return Math.random()-0.5;});hotIdx=0;}for(var b=0;b<2;b++){if(hotPool.length>=400)break;var q=queries[hotIdx%queries.length];hotIdx++;try{var d=await pget('/search?q='+encodeURIComponent(q)+'&filter=videos');var items=(d.items||[]).filter(function(v){return v.url&&isRealSong(v);});items.forEach(function(v){if(hotPool.length>=400)return;var vid=(v.url||'').replace('/watch?v=','');if(hotPool.some(function(x){return x.id===vid;}))return;var obj={id:vid,title:v.title,uploaderName:v.uploaderName,thumbnail:v.thumbnail};hotPool.push(obj);var ix=hotPool.length-1;var el=document.createElement('div');el.className='list-item';el.onclick=function(){playQueue=hotPool.map(function(x){return{id:{videoId:x.id},snippet:{title:x.title,channelTitle:x.uploaderName,thumbnails:{default:{url:x.thumbnail},high:{url:x.thumbnail}}}};});ytResults=playQueue;playYoutube(ix);};el.innerHTML='<img src="'+obj.thumbnail+'"><div class="list-info"><div class="list-title">'+obj.title+'</div><div class="list-sub">'+obj.uploaderName+'</div></div><button class="dl-btn" onclick="event.stopPropagation();dlId(\''+vid+'\')"><svg viewBox="0 0 24 24"><path d="M5 20h14v-2H5v2zM19 9h-4V3H9v6H5l7 7 7-7z"/></svg></button>';c.appendChild(el);});}catch(e){}}hotLoading=false;var hb=document.getElementById('hotLoadBtn');if(hb)hb.style.display='block';}
async function loadMixtapes(){if(mixLoading)return;if(mixPool.length>=300)return;mixLoading=true;for(var b=0;b<3;b++){if(mixPool.length>=300)break;var q=['DJ nonstop mix 2025','mixtape 2025 hip hop','afrobeats nonstop mix','amapiano mix 2025','dancehall mix 2025','afrobeat dj mix 2025','gospel mix 2025','rnb mixtape 2025'][mixIdx%8];mixIdx++;try{var d=await pget('/search?q='+encodeURIComponent(q)+'&filter=videos');var items=(d.items||[]).slice(0,8);var c=document.getElementById('mixtapeList');if(!c)break;items.forEach(function(v){if(mixPool.length>=300)return;var vid=(v.url||'').replace('/watch?v=','');if(mixPool.some(function(x){return x.id===vid;}))return;var obj={id:vid,title:v.title,uploaderName:v.uploaderName,thumbnail:v.thumbnail};mixPool.push(obj);var ix=mixPool.length-1;var el=document.createElement('div');el.className='mix-list-item';el.onclick=function(){playQueue=mixPool.map(function(x){return{id:{videoId:x.id},snippet:{title:x.title,channelTitle:x.uploaderName,thumbnails:{default:{url:x.thumbnail},high:{url:x.thumbnail}}}};});ytResults=playQueue;playYoutube(ix);};el.innerHTML='<img src="'+obj.thumbnail+'"><div class="mix-info"><div class="mix-title">'+obj.title+'</div><div class="mix-sub">'+obj.uploaderName+'</div></div><button class="dl-btn" onclick="event.stopPropagation();dlId(\''+vid+'\')"><svg viewBox="0 0 24 24"><path d="M5 20h14v-2H5v2zM19 9h-4V3H9v6H5l7 7 7-7z"/></svg></button>';c.appendChild(el);});}catch(e){}}mixLoading=false;var mb=document.getElementById('mixLoadBtn');if(mb)mb.style.display='block';}
async function loadArtistsNext(){if(artistLoading)return;if(artistPool.length>=400)return;artistLoading=true;for(var b=0;b<3;b++){if(artistPool.length>=400)break;var q=['afrobeats artists','hip hop artists','rnb artists','amapiano artists','dancehall artists','gospel artists','naija artists','ugandan artists','reggae artists','afro pop artists'][artistIdx%10];artistIdx++;try{var d=await pget('/search?q='+encodeURIComponent(q)+'&filter=channels');var items=(d.items||[]).slice(0,8);var c=document.getElementById('artistsList');if(!c)break;items.forEach(function(v){var name=cleanArtistName(v.name);if(!isRealArtistName(name))return;if(artistPool.indexOf(name)>=0)return;artistPool.push(name);var isF=followedArtists.some(function(a){return a.name===name;});var imgId='artistsList-img-'+Date.now()+'-'+artistPool.length;var el=document.createElement('div');el.className='artist-box';el.innerHTML='<div class="artist-img" id="'+imgId+'"><img src="'+(v.thumbnail||'https://ui-avatars.com/api/?name='+encodeURIComponent(name)+'&background=00e0d0&color=000&size=200')+'"></div><div class="artist-name">'+name+'</div><button class="follow-btn'+(isF?' following':'')+'" onclick="event.stopPropagation();toggleFollow(\''+name.replace(/'/g,"\\'")+'\',this,\''+imgId+'\')">'+(isF?'Following':'Follow')+'</button>';el.querySelector('.artist-img').onclick=function(){openArtistProfile(name,document.querySelector('#'+imgId+' img').src);};el.querySelector('.artist-name').onclick=function(){openArtistProfile(name,document.querySelector('#'+imgId+' img').src);};c.appendChild(el);});}catch(e){}}artistLoading=false;var ab=document.getElementById('artistLoadBtn');if(ab)ab.style.display='block';}
async function searchArtist(){var q=document.getElementById('artistSearchInput').value.trim();if(!q)return;var c=document.getElementById('artistsList');c.innerHTML='<p style="color:#666;text-align:center;padding:20px">Searching...</p>';artistPool=[];artistIdx=0;try{var d=await pget('/search?q='+encodeURIComponent(q)+'&filter=channels');var items=(d.items||[]).slice(0,15);c.innerHTML='';items.forEach(function(v){var name=cleanArtistName(v.name);if(!isRealArtistName(name))return;if(artistPool.indexOf(name)>=0)return;artistPool.push(name);var isF=followedArtists.some(function(a){return a.name===name;});var imgId='artistsList-img-'+Date.now()+'-'+Math.random();var el=document.createElement('div');el.className='artist-box';el.innerHTML='<div class="artist-img" id="'+imgId+'"><img src="'+(v.thumbnail||'https://ui-avatars.com/api/?name='+encodeURIComponent(name)+'&background=00e0d0&color=000&size=200')+'"></div><div class="artist-name">'+name+'</div><button class="follow-btn'+(isF?' following':'')+'" onclick="event.stopPropagation();toggleFollow(\''+name.replace(/'/g,"\\'")+'\',this,\''+imgId+'\')">'+(isF?'Following':'Follow')+'</button>';el.querySelector('.artist-img').onclick=function(){openArtistProfile(name,document.querySelector('#'+imgId+' img').src);};el.querySelector('.artist-name').onclick=function(){openArtistProfile(name,document.querySelector('#'+imgId+' img').src);};c.appendChild(el);});}catch(x){c.innerHTML='<p style="color:#ff5555;text-align:center">Search failed.</p>';}}
function loadArtistGrid(targetId,names){var c=document.getElementById(targetId);if(!c)return;c.innerHTML='';names=names.filter(function(n,i,a){return a.indexOf(n)===i;});names.forEach(function(name,i){var isF=followedArtists.some(function(a){return a.name===name;});var el=document.createElement('div');el.className='artist-box';var imgId=targetId+'-img-'+Date.now()+'-'+i;el.innerHTML='<div class="artist-img" id="'+imgId+'"><img src="https://ui-avatars.com/api/?name='+encodeURIComponent(name)+'&background=00e0d0&color=000&size=200"></div><div class="artist-name">'+name+'</div><button class="follow-btn'+(isF?' following':'')+'" onclick="event.stopPropagation();toggleFollow(\''+name.replace(/'/g,"\\'")+'\',this,\''+imgId+'\')">'+(isF?'Following':'Follow')+'</button>';el.querySelector('.artist-img').onclick=function(){openArtistProfile(name,document.querySelector('#'+imgId+' img').src);};el.querySelector('.artist-name').onclick=function(){openArtistProfile(name,document.querySelector('#'+imgId+' img').src);};c.appendChild(el);loadThumb(name,imgId);});}
async function loadThumb(name,imgId){try{var d=await pget('/search?q='+encodeURIComponent(name)+'&filter=channels');var channels=(d.items||[]).slice(0,5);var img=document.querySelector('#'+imgId+' img');if(!img)return;var nm=name.toLowerCase().trim();for(var i=0;i<channels.length;i++){var cn=(channels[i].name||'').toLowerCase().replace(/\s*-\s*topic$/,'').replace(/vevo$/,'').trim();if(cn===nm||cn.indexOf(nm)===0||nm.indexOf(cn)===0){if(channels[i].thumbnail){img.src=channels[i].thumbnail;return;}}}var d2=await pget('/search?q='+encodeURIComponent(name+' official video')+'&filter=videos');var vids=(d2.items||[]).slice(0,5);for(var j=0;j<vids.length;j++){var un=(vids[j].uploaderName||'').toLowerCase().replace(/\s*-\s*topic$/,'').replace(/vevo$/,'').trim();if(un.indexOf(nm)>=0||nm.indexOf(un)>=0){img.src=vids[j].thumbnail;return;}}}catch(e){}}
function fetchSimilars(name){return new Promise(function(resolve){var key=name.toLowerCase().trim().replace(/[^a-z0-9 ]/g,'');var picks=CURATED_SIMILAR[key];var gen=['Burna Boy','Wizkid','Drake','Rema'];var genOut=function(){return gen.map(function(n){return{name:n,img:'https://ui-avatars.com/api/?name='+encodeURIComponent(n)+'&background=00e0d0&color=000&size=200'};});};if(picks&&picks.length){resolve(picks.map(function(n){return{name:n,img:'https://ui-avatars.com/api/?name='+encodeURIComponent(n)+'&background=00e0d0&color=000&size=200'};}));return;}pget('/search?q='+encodeURIComponent(name+' similar artists')+'&filter=channels').then(function(d){var items=d.items||[];var fn=key.split(' ')[0];var other={};items.forEach(function(v){var un=cleanArtistName(v.name);if(!isRealArtistName(un))return;var ul=un.toLowerCase();if(ul.indexOf(fn)>=0)return;other[un]=v.thumbnail||('https://ui-avatars.com/api/?name='+encodeURIComponent(un)+'&background=00e0d0&color=000&size=200');});var out=Object.keys(other).slice(0,4).map(function(n){return{name:n,img:other[n]};});if(out.length>=3){resolve(out);return;}resolve(genOut());}).catch(function(){resolve(genOut());});});}
async function toggleFollow(name,btn,imgId){var idx=followedArtists.findIndex(function(a){return a.name===name;});var img=imgId?document.querySelector('#'+imgId+' img'):null;if(idx>=0){followedArtists.splice(idx,1);if(btn){btn.classList.remove('following');btn.textContent='Follow';}localStorage.setItem('bi_followed',JSON.stringify(followedArtists));renderFollowedArtists();loadForYou();}else{followedArtists.push({name:name,img:img?img.src:''});if(btn){btn.classList.add('following');btn.textContent='Following';}renderFollowedArtists();try{var sims=await fetchSimilars(name);var myPos=followedArtists.findIndex(function(a){return a.name===name;});if(myPos<0)myPos=followedArtists.length-1;var ins=0;for(var i=0;i<sims.length;i++){var s=sims[i];if(!followedArtists.some(function(x){return x.name.toLowerCase()===s.name.toLowerCase();})){followedArtists.splice(myPos+ins,0,s);ins++;}}}catch(e){}localStorage.setItem('bi_followed',JSON.stringify(followedArtists));renderFollowedArtists();loadForYou();}if(currentArtist.name===name)updateFollowButton();}
function renderFollowedArtists(){var c=document.getElementById('followedArtists');if(!c)return;if(followedArtists.length===0){c.innerHTML='<p style="color:#666;font-size:.75rem;grid-column:1/-1">Follow artists to see them here.</p>';return;}c.innerHTML='';followedArtists.forEach(function(a){var el=document.createElement('div');el.className='artist-box';el.innerHTML='<div class="artist-img"><img src="'+(a.img||'https://ui-avatars.com/api/?name='+encodeURIComponent(a.name)+'&background=00e0d0&color=000&size=200')+'"></div><div class="artist-name">'+a.name+'</div><button class="follow-btn following" onclick="event.stopPropagation();toggleFollow(\''+a.name.replace(/'/g,"\\'")+'\',this,null)">Following</button>';el.querySelector('.artist-img').onclick=function(){openArtistProfile(a.name,a.img);};c.appendChild(el);});}
async function loadForYou(){var sec=document.getElementById('forYouSection'),c=document.getElementById('forYou');if(!c)return;if(followedArtists.length===0){sec.style.display='none';return;}sec.style.display='block';c.innerHTML='<p style="color:#666;font-size:.75rem">Loading...</p>';var all=[];for(var i=0;i<Math.min(followedArtists.length,5);i++){try{var d=await pget('/search?q='+encodeURIComponent(followedArtists[i].name+' official video')+'&filter=videos');var items=(d.items||[]).filter(function(v){return isRealSong(v);}).slice(0,4);items.forEach(function(v){all.push({id:(v.url||'').replace('/watch?v=',''),title:v.title,uploaderName:v.uploaderName,thumbnail:v.thumbnail});});}catch(e){}}if(all.length===0){c.innerHTML='<p style="color:#666;font-size:.75rem">No songs found.</p>';return;}c.innerHTML='';all.forEach(function(t){var el=document.createElement('div');el.className='card';el.onclick=function(){playQueue=all.map(function(x){return{id:{videoId:x.id},snippet:{title:x.title,channelTitle:x.uploaderName,thumbnails:{default:{url:x.thumbnail},high:{url:x.thumbnail}}}};});ytResults=playQueue;var idx=all.indexOf(t);if(idx>=0)playYoutube(idx);};el.innerHTML='<div class="card-img"><img src="'+t.thumbnail+'"></div><div class="card-title">'+t.title+'</div><div class="card-sub">'+t.uploaderName+'</div>';c.appendChild(el);});}
async function searchGenre(g){genrePool=[];genreQuery=g;genreIdx=0;genreLoading=false;document.getElementById('genreResults').innerHTML='<h3 style="margin-bottom:10px">'+g+' Hits</h3><div id="genreList"></div><div class="load-more-wrap"><button onclick="loadGenreMore()">Load More</button></div>';for(var i=0;i<4;i++)await loadGenreMore();}
async function loadGenreMore(){if(genreLoading)return;if(genrePool.length>=1000)return;genreLoading=true;var c=document.getElementById('genreList');if(!c){genreLoading=false;return;}var base=genreQuery;var variants=[base+' hit songs',base+' official video',base+' 2025',base+' best songs',base+' top songs',base+' music video',base+' new song',base+' latest',base+' trending',base+' album',base+' single',base+' audio',base+' visualizer',base+' official audio',base+' chart',base+' ft',base+' remix',base+' live',base+' 2024',base+' 2023',base+' classic',base+' throwback','best of '+base,'top 10 '+base,base+' greatest',base+' essentials'];if(genreIdx>=variants.length){variants.sort(function(){return Math.random()-0.5;});genreIdx=0;}var added=0;var tries=0;while(added<15&&tries<12){if(genrePool.length>=1000)break;if(genreIdx>=variants.length){variants.sort(function(){return Math.random()-0.5;});genreIdx=0;}var q=variants[genreIdx];genreIdx++;tries++;try{var d=await pget('/search?q='+encodeURIComponent(q)+'&filter=videos');var items=(d.items||[]).filter(function(v){return v.url&&isRealSong(v);});items.forEach(function(v){if(genrePool.length>=1000)return;var vid=(v.url||'').replace('/watch?v=','');if(genrePool.some(function(x){return x.id===vid;}))return;var obj={id:vid,title:v.title,uploaderName:v.uploaderName,thumbnail:v.thumbnail};genrePool.push(obj);added++;var ix=genrePool.length-1;var el=document.createElement('div');el.className='list-item';el.onclick=function(){playQueue=genrePool.map(function(x){return{id:{videoId:x.id},snippet:{title:x.title,channelTitle:x.uploaderName,thumbnails:{default:{url:x.thumbnail},high:{url:x.thumbnail}}}};});ytResults=playQueue;playYoutube(ix);};el.innerHTML='<img src="'+obj.thumbnail+'"><div class="list-info"><div class="list-title">'+obj.title+'</div><div class="list-sub">'+obj.uploaderName+'</div></div><button class="dl-btn" onclick="event.stopPropagation();dlId(\''+vid+'\')"><svg viewBox="0 0 24 24"><path d="M5 20h14v-2H5v2zM19 9h-4V3H9v6H5l7 7 7-7z"/></svg></button>';c.appendChild(el);});}catch(e){}}genreLoading=false;}
async function openArtistProfile(name,img){currentArtist={name:name,img:img};artistSongPool=[];artistSongLoading=false;document.getElementById('modalArtistImg').src=img||'https://ui-avatars.com/api/?name='+encodeURIComponent(name)+'&background=00e0d0&color=000&size=200';document.getElementById('modalArtistName').textContent=name;var ck=name.toLowerCase().trim().replace(/[^a-z0-9\. ]/g,'');var flag=COUNTRY[ck]||'';document.getElementById('modalArtistStats').textContent=flag?flag+' '+name:'';document.getElementById('modalArtistSongs').innerHTML='<p style="color:#666;text-align:center;padding:20px">Loading...</p>';document.getElementById('artistModal').classList.add('active');document.getElementById('artistModal').scrollTop=0;updateFollowButton();await loadMoreArtistSongs();}
async function loadMoreArtistSongs(){
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
      var un=(v.uploaderName||'').toLowerCase().trim().replace(/\s*-\s*topic$/,'').replace(/vevo$/,'').trim();
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
      el.innerHTML='<img src="'+obj.thumbnail+'"><div class="list-info"><div class="list-title">'+obj.title+'</div><div class="list-sub">'+obj.channelTitle+'</div></div><button class="dl-btn" onclick="event.stopPropagation();dlId(\''+vid+'\')"><svg viewBox="0 0 24 24"><path d="M5 20h14v-2H5v2zM19 9h-4V3H9v6H5l7 7 7-7z"/></svg></button>';
      sc.appendChild(el);
    });
    if(artistSongPool.length===0){sc.innerHTML='<p style="color:#666;text-align:center;padding:20px">No songs found for this artist.</p>';}
  }catch(e){}
}
artistSongLoading=false;
}

function updateFollowButton(){var b=document.getElementById('modalFollowBtn');if(!b)return;var isF=followedArtists.some(function(a){return a.name===currentArtist.name;});b.textContent=isF?'Following':'Follow';b.classList.toggle('following',isF);}
function toggleFollowCurrentArtist(){if(!currentArtist.name)return;toggleFollow(currentArtist.name,null,null);updateFollowButton();}
function closeArtistModal(){document.getElementById('artistModal').classList.remove('active');}
async function loadSimilarSongs(){if(simLoading)return;if(simPool.length>=500)return;simLoading=true;var base=simTitle.split('-')[0].trim()||simTitle;var cleanBase=base.replace(/official|video|lyrics|audio|music|remix|hd|4k|ft\.|feat\.|\(.*?\)|\[.*?\]/gi,'').trim();var key=cleanBase.toLowerCase();var q='';if(simQIdx===0){q=cleanBase+' official video';}else if(simQIdx===1){q=cleanBase+' songs';}else if(simQIdx===2){try{var d=await pget('/search?q='+encodeURIComponent(cleanBase+' similar artists')+'&filter=channels');var items=(d.items||[]).slice(0,10);var fn=key.split(' ')[0];simSimilar=[];items.forEach(function(v){var un=cleanArtistName(v.name);if(!isRealArtistName(un))return;if(un.toLowerCase().indexOf(fn)>=0)return;if(simSimilar.indexOf(un)<0)simSimilar.push(un);});}catch(e){}if(simSimilar.length<3){var picks=CURATED_SIMILAR[key];if(picks)simSimilar=picks.slice();}if(simSimilar.length>0){q=simSimilar[0]+' official video';}else{q=cleanBase+' hits';}}else if(simQIdx===3){var vibe=detectVibeKey(simTitle);var pick=vibe?pickVibeArtist(vibe):'';if(pick)q=pick+' songs';else if(simSimilar.length>1)q=simSimilar[1]+' songs';else q=cleanBase+' hits';}else{var vibe2=detectVibeKey(simTitle);if(simQIdx<10&&vibe2){var pick2=pickVibeArtist(vibe2);q=pick2?pick2+' songs':cleanBase+' hits';}else if(simSimilar.length>0){var ai=(simQIdx-4)%simSimilar.length;q=simSimilar[ai]+' songs';}else{q=cleanBase+' hits';}}simQIdx++;try{var d=await pget('/search?q='+encodeURIComponent(q)+'&filter=videos');var items=(d.items||[]).filter(function(v){return v.url&&isRealSong(v);});var c=document.getElementById('similarGrid');if(!c){simLoading=false;return;}if(simPool.length===0)c.innerHTML='';items.forEach(function(v){if(simPool.length>=500)return;var vid=(v.url||'').replace('/watch?v=','');if(simPool.some(function(x){return x.id===vid;}))return;var obj={id:vid,title:v.title,uploaderName:v.uploaderName,thumbnail:v.thumbnail};simPool.push(obj);var ix=simPool.length-1;var el=document.createElement('div');el.className='similar-card';el.onclick=function(){playQueue=simPool.map(function(x){return{id:{videoId:x.id},snippet:{title:x.title,channelTitle:x.uploaderName,thumbnails:{default:{url:x.thumbnail},high:{url:x.thumbnail}}}};});ytResults=playQueue;playYoutube(ix);};el.innerHTML='<div class="similar-card-img"><img src="'+obj.thumbnail+'"></div><div class="similar-card-title">'+obj.title+'</div><div class="similar-card-artist">'+obj.uploaderName+'</div>';c.appendChild(el);});}catch(e){}simLoading=false;}
function onYouTubeIframeAPIReady(){
try{
ytPlayer=new YT.Player('youtube-player',{
height:'100%',width:'100%',
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
function ensurePlayer(vid,tries){tries=tries||0;if(ytReady&&ytPlayer&&typeof ytPlayer.loadVideoById==='function'){try{ytPlayer.loadVideoById(vid);ytPlayer.playVideo();}catch(e){}isPlaying=true;updateAllIcons();return;}if(tries<40)setTimeout(function(){ensurePlayer(vid,tries+1);},200);}
function setTrackInfo(art,title,artist){document.getElementById('miniArt').src=art;document.getElementById('miniTitle').textContent=title;document.getElementById('miniArtist').textContent=artist;document.getElementById('fullArt').src=art;document.getElementById('fullTitle').textContent=title;document.getElementById('fullArtist').textContent=artist;document.getElementById('miniPlayer').classList.add('active');}
function playDbSong(i){currentSource='db';currentIndex=i;if(ytPlayer&&ytPlayer.pauseVideo)ytPlayer.pauseVideo();var yp=document.getElementById('youtube-player');var fa=document.getElementById('fullArt');if(yp)yp.style.display='none';if(fa)fa.style.display='block';var s=songs[i];if(!s)return;setTrackInfo(s.cover_art_url||'https://via.placeholder.com/150',s.title,s.artist_name);var p=document.getElementById('audioPlayer');p.src=s.audio_url;p.playbackRate=playbackSpeed;p.play();isPlaying=true;updateAllIcons();}
function playYoutube(i){currentSource='youtube';currentIndex=i;document.getElementById('audioPlayer').pause();var yp=document.getElementById('youtube-player');var fa=document.getElementById('fullArt');if(yp)yp.style.display='block';if(fa)fa.style.display='none';var t=ytResults[i];if(!t)return;setTrackInfo(t.snippet.thumbnails.high.url,t.snippet.title,t.snippet.channelTitle);ensurePlayer(t.id.videoId);simPool=[];simSimilar=[];simTitle=t.snippet.title;simQIdx=0;document.getElementById('similarGrid').innerHTML='';for(var k=0;k<5;k++)loadSimilarSongs();}
function playFromQueue(vid){var idx=playQueue.findIndex(function(t){return t.id&&t.id.videoId===vid;});if(idx<0)return;ytResults=playQueue;playYoutube(idx);}
function togglePlay(){if(currentSource==='youtube'){if(!ytReady||!ytPlayer)return;try{if(isPlaying){ytPlayer.pauseVideo();isPlaying=false;}else{ytPlayer.playVideo();isPlaying=true;}updateAllIcons();}catch(e){}}else{var p=document.getElementById('audioPlayer');if(!p.src)return;if(isPlaying){p.pause();isPlaying=false;}else{p.play();isPlaying=true;}updateAllIcons();}}
function updateAllIcons(){var sh=isPlaying?'none':'block',hd=isPlaying?'block':'none';['miniPlayIcon','fullPlayIcon'].forEach(function(id){var e=document.getElementById(id);if(e)e.style.display=sh;});['miniPauseIcon','fullPauseIcon'].forEach(function(id){var e=document.getElementById(id);if(e)e.style.display=hd;});}
function nextTrack(){if(currentSource==='db'&&songs.length>0){currentIndex=isShuffle?Math.floor(Math.random()*songs.length):(currentIndex+1)%songs.length;playDbSong(currentIndex);}else if(currentSource==='youtube'&&ytResults.length>0){currentIndex=isShuffle?Math.floor(Math.random()*ytResults.length):(currentIndex+1)%ytResults.length;playYoutube(currentIndex);}}
function prevTrack(){if(currentSource==='db'&&songs.length>0){currentIndex=(currentIndex-1+songs.length)%songs.length;playDbSong(currentIndex);}else if(currentSource==='youtube'&&ytResults.length>0){currentIndex=(currentIndex-1+ytResults.length)%ytResults.length;playYoutube(currentIndex);}}
function toggleShuffle(){isShuffle=!isShuffle;document.getElementById('shuffleBtn').classList.toggle('active',isShuffle);}
function toggleRepeat(){repeatMode=(repeatMode+1)%3;var b=document.getElementById('repeatBtn');b.classList.remove('active');if(repeatMode>=1)b.classList.add('active');}
function toggleSpeed(){var s=[0.5,1,1.5,2];var i=s.indexOf(playbackSpeed);playbackSpeed=s[(i+1)%s.length];document.getElementById('speedLabel').textContent=playbackSpeed+'x';if(currentSource==='db')document.getElementById('audioPlayer').playbackRate=playbackSpeed;else if(ytReady&&ytPlayer&&ytPlayer.setPlaybackRate)ytPlayer.setPlaybackRate(playbackSpeed);}
function toggleLikeCurrent(){document.getElementById('fullHeart').style.fill='#ff4d4d';}
function dlId(vid){if(!vid)return;try{navigator.clipboard.writeText('https://www.youtube.com/watch?v='+vid);}catch(e){}window.location.href='https://youtubegrab.com';}catch(e){}navigator.clipboard.writeText('https://www.youtube.com/watch?v='+vid);window.open('https://youtubegrab.com','_blank');}
function downloadCurrent(){var t=null;if(currentSource==='youtube')t=ytResults[currentIndex];else t=songs[currentIndex];if(!t)return alert('No song playing');var vid=t.id?t.id.videoId:t.id;if(!vid)return;dlId(vid);}
function playHeroSong(){if(songs.length>0)playDbSong(0);else switchTab('search',document.querySelectorAll('.nav-item')[1]);}
function openFullPlayer(){document.getElementById('fullPlayer').classList.add('active');}
function closeFullPlayer(){document.getElementById('fullPlayer').classList.remove('active');}
function mainSearchGo(){var q=document.getElementById('mainSearchInput').value.trim();if(!q)return;switchTab('search',document.querySelectorAll('.nav-item')[1]);document.getElementById('ytSearchInput').value=q;searchYouTube();}
async function searchYouTube(q,targetId){var query=typeof q==='string'?q:document.getElementById('ytSearchInput').value.trim();if(!query)return;var cid=targetId||'ytResults',c=document.getElementById(cid);if(!c)return;c.innerHTML='<p style="color:#666;text-align:center;padding:20px">Searching...</p>';try{var d=await pget('/search?q='+encodeURIComponent(query)+'&filter=videos');var items=(d.items||[]).filter(function(v){return v.url&&isRealSong(v);}).slice(0,30);ytResults=items.map(function(v){return{id:{videoId:(v.url||'').replace('/watch?v=','')},snippet:{title:v.title,channelTitle:v.uploaderName,thumbnails:{default:{url:v.thumbnail},high:{url:v.thumbnail}}}};});playQueue=ytResults;c.innerHTML='';ytResults.forEach(function(t){var el=document.createElement('div');el.className='list-item';el.onclick=function(){playFromQueue(t.id.videoId);};el.innerHTML='<img src="'+t.snippet.thumbnails.default.url+'"><div class="list-info"><div class="list-title">'+t.snippet.title+'</div><div class="list-sub">'+t.snippet.channelTitle+'</div></div><button class="dl-btn" onclick="event.stopPropagation();dlId(\''+t.id.videoId+'\')"><svg viewBox="0 0 24 24"><path d="M5 20h14v-2H5v2zM19 9h-4V3H9v6H5l7 7 7-7z"/></svg></button>';c.appendChild(el);});}catch(x){c.innerHTML='<p style="color:#ff5555;text-align:center;padding:20px">Search failed</p>';}}
function renderRecentlyPlayed(){var c=document.getElementById('recentlyPlayed');if(!c)return;c.innerHTML='';if(songs.length===0){c.innerHTML='<p style="color:#666;font-size:.75rem">Upload songs to see them here.</p>';return;}songs.slice(0,8).forEach(function(s){var el=document.createElement('div');el.className='card';el.onclick=function(){playDbSong(songs.indexOf(s));};el.innerHTML='<div class="card-img"><img src="'+(s.cover_art_url||'https://via.placeholder.com/150')+'"></div><div class="card-title">'+s.title+'</div><div class="card-sub">'+s.artist_name+'</div>';c.appendChild(el);});}
document.getElementById('audioPlayer').addEventListener('ended',function(){if(repeatMode===2){this.currentTime=0;this.play();}else nextTrack();});
document.getElementById('fullProgress').addEventListener('input',function(e){if(currentSource==='db'){var p=document.getElementById('audioPlayer');if(p.duration)p.currentTime=(e.target.value/100)*p.duration;}else if(ytReady&&ytPlayer&&ytPlayer.getDuration)ytPlayer.seekTo((e.target.value/100)*ytPlayer.getDuration(),true);});
setInterval(function(){var cur=0,dur=0;if(currentSource==='db'){var p=document.getElementById('audioPlayer');cur=p.currentTime||0;dur=p.duration||0;}else if(ytReady&&ytPlayer&&ytPlayer.getCurrentTime){cur=ytPlayer.getCurrentTime()||0;dur=ytPlayer.getDuration()||0;}if(dur>0){var pct=(cur/dur)*100;document.getElementById('fullProgress').value=pct;document.getElementById('fullCurrent').textContent=fmt(cur);document.getElementById('fullDuration').textContent=fmt(dur);}},1000);
function fmt(s){if(isNaN(s))return'0:00';var m=Math.floor(s/60);var sec=Math.floor(s%60);return m+':'+(sec<10?'0':'')+sec;}
var tx=0,ab=document.getElementById('fullArtBox');
ab.addEventListener('touchstart',function(e){tx=e.changedTouches[0].screenX;},{passive:true});
ab.addEventListener('touchend',function(e){var dx=e.changedTouches[0].screenX-tx;if(dx<-50)nextTrack();if(dx>50)prevTrack();},{passive:true});
document.getElementById('mainContent').addEventListener('scroll',function(){var st=this.scrollTop;if(st+this.clientHeight>=this.scrollHeight-300){var ht=document.getElementById('tab-home');if(ht&&ht.style.display!=='none'&&!homeLoading&&homePool.length<400)loadHomeMore();var mt=document.getElementById('tab-mixtape');if(mt&&mt.style.display!=='none'&&!mixLoading&&mixPool.length<300)loadMixtapes();var at=document.getElementById('tab-artists');if(at&&at.style.display!=='none'&&!artistLoading&&artistPool.length<400)loadArtistsNext();var gt=document.getElementById('tab-genres');if(gt&&gt.style.display!=='none'&&!genreLoading&&genrePool.length<1000)loadGenreMore();}});
document.getElementById('fullContent').addEventListener('scroll',function(){if(this.scrollTop+this.clientHeight>=this.scrollHeight-200&&currentSource==='youtube'&&!simLoading&&simPool.length<500)loadSimilarSongs();});
document.getElementById('artistModal').addEventListener('scroll',function(){if(this.scrollTop+this.clientHeight>=this.scrollHeight-200&&!artistSongLoading&&artistSongPool.length<200)loadMoreArtistSongs();});
var _holdIv=null;
function _findTarget(){var fpl=document.getElementById('fullPlayer');var fc=document.getElementById('fullContent');var am=document.getElementById('artistModal');var mc=document.getElementById('mainContent');if(fpl&&fpl.classList.contains('active')&&fc)return fc;if(am&&am.classList.contains('active'))return am;return mc;}
window.startHold=function(e){if(e&&e.preventDefault)e.preventDefault();if(_holdIv)clearInterval(_holdIv);var t=_findTarget();if(!t)return;_holdIv=setInterval(function(){if(t.scrollTop<=0){clearInterval(_holdIv);_holdIv=null;return;}t.scrollTop=Math.max(0,t.scrollTop-55);},25);};
window.stopHold=function(){if(_holdIv){clearInterval(_holdIv);_holdIv=null;}};
function bindHoldBtn(){var b=document.getElementById('bttBtn');if(!b||b._bound)return;b._bound=true;b.addEventListener('touchstart',window.startHold,{passive:false});b.addEventListener('touchend',window.stopHold);b.addEventListener('touchcancel',window.stopHold);b.addEventListener('mousedown',window.startHold);b.addEventListener('mouseup',window.stopHold);b.addEventListener('mouseleave',window.stopHold);b.addEventListener('contextmenu',function(e){e.preventDefault();});}
document.addEventListener('touchmove',window.stopHold,{passive:true});
document.addEventListener('touchend',window.stopHold);


document.addEventListener('DOMContentLoaded', function() {
    // Physically move the youtube-player div inside the fullArtBox
    var yp = document.getElementById('youtube-player');
    var fab = document.getElementById('fullArtBox');
    if (yp && fab) {
        fab.appendChild(yp);
    }

    // Override playYoutube to show video
    window.playYoutube = function(i) {
        currentSource = 'youtube';
        currentIndex = i;
        var ap = document.getElementById('audioPlayer');
        if(ap) ap.pause();
        var t = ytResults[i];
        if (!t) return;
        var yp = document.getElementById('youtube-player');
        var fa = document.getElementById('fullArt');
        if (yp) yp.style.display = 'block';
        if (fa) fa.style.display = 'none';
        setTrackInfo(t.snippet.thumbnails.high.url, t.snippet.title, t.snippet.channelTitle);
        ensurePlayer(t.id.videoId);
        simPool = []; simSimilar = []; simTitle = t.snippet.title; simQIdx = 0;
        var sg = document.getElementById('similarGrid');
        if(sg) sg.innerHTML = '';
        for (var k = 0; k < 5; k++) loadSimilarSongs();
    };

    // Override playDbSong to show album art
    window.playDbSong = function(i) {
        currentSource = 'db';
        currentIndex = i;
        if (ytPlayer && ytPlayer.pauseVideo) ytPlayer.pauseVideo();
        var yp = document.getElementById('youtube-player');
        var fa = document.getElementById('fullArt');
        if (yp) yp.style.display = 'none';
        if (fa) fa.style.display = 'block';
        var s = songs[i];
        if (!s) return;
        setTrackInfo(s.cover_art_url || 'https://via.placeholder.com/150', s.title, s.artist_name);
        var p = document.getElementById('audioPlayer');
        p.src = s.audio_url;
        p.playbackRate = playbackSpeed;
        p.play();
        isPlaying = true;
        updateAllIcons();
    };
});


document.addEventListener('DOMContentLoaded', function() {
    // Physically move the youtube-player div inside the fullArtBox to trap it
    var yp = document.getElementById('youtube-player');
    var fab = document.getElementById('fullArtBox');
    if (yp && fab) { fab.appendChild(yp); }

    window.playYoutube = function(i) {
        currentSource = 'youtube';
        currentIndex = i;
        var ap = document.getElementById('audioPlayer');
        if(ap) ap.pause();
        var t = ytResults[i];
        if (!t) return;
        var yp = document.getElementById('youtube-player');
        var fa = document.getElementById('fullArt');
        if (yp) yp.style.display = 'block';
        if (fa) fa.style.display = 'none';
        setTrackInfo(t.snippet.thumbnails.high.url, t.snippet.title, t.snippet.channelTitle);
        ensurePlayer(t.id.videoId);
        simPool = []; simSimilar = []; simTitle = t.snippet.title; simQIdx = 0;
        var sg = document.getElementById('similarGrid');
        if(sg) sg.innerHTML = '';
        for (var k = 0; k < 5; k++) loadSimilarSongs();
    };

    window.playDbSong = function(i) {
        currentSource = 'db';
        currentIndex = i;
        if (ytPlayer && ytPlayer.pauseVideo) ytPlayer.pauseVideo();
        var yp = document.getElementById('youtube-player');
        var fa = document.getElementById('fullArt');
        if (yp) yp.style.display = 'none';
        if (fa) fa.style.display = 'block';
        var s = songs[i];
        if (!s) return;
        setTrackInfo(s.cover_art_url || 'https://via.placeholder.com/150', s.title, s.artist_name);
        var p = document.getElementById('audioPlayer');
        p.src = s.audio_url;
        p.playbackRate = playbackSpeed;
        p.play();
        isPlaying = true;
        updateAllIcons();
    };
});


document.addEventListener('DOMContentLoaded', function() {
    var fab = document.getElementById('fullArtBox');
    var fsBtn = document.getElementById('fsOverlayBtn');
    var yp = document.getElementById('youtube-player');
    var fa = document.getElementById('fullArt');

    if (yp && fab) { fab.appendChild(yp); }
    if (fsBtn && fab) { fab.appendChild(fsBtn); }

    // ONLY toggle fullscreen when the button is clicked
    if (fsBtn) {
        fsBtn.addEventListener('click', function(e) {
            e.stopPropagation();
            var isFull = fab.classList.contains('is-fullscreen');
            if (!isFull) {
                fab.classList.add('is-fullscreen');
                if (fab.requestFullscreen) fab.requestFullscreen();
            } else {
                fab.classList.remove('is-fullscreen');
                if (document.exitFullscreen) document.exitFullscreen();
            }
        });
    }

    document.addEventListener('fullscreenchange', function() {
        if (!document.fullscreenElement) fab.classList.remove('is-fullscreen');
    });

    // Show video when YouTube plays
    var originalPlayYoutube = window.playYoutube;
    window.playYoutube = function(i) {
        if (originalPlayYoutube) originalPlayYoutube(i);
        if (yp) yp.style.display = 'block';
        if (fa) fa.style.display = 'none';
        if (fsBtn) fsBtn.style.display = 'block';
    };

    // Show art when local song plays
    var originalPlayDbSong = window.playDbSong;
    window.playDbSong = function(i) {
        if (originalPlayDbSong) originalPlayDbSong(i);
        if (yp) yp.style.display = 'none';
        if (fa) fa.style.display = 'block';
        if (fsBtn) fsBtn.style.display = 'none';
        fab.classList.remove('is-fullscreen');
    };
});

// Override YouTube initialization to auto-shuffle from Similar Songs
window.onYouTubeIframeAPIReady = function() {
    ytPlayer = new YT.Player('youtube-player', {
        height: '100%',
        width: '100%',
        playerVars: {
            playsinline: 1,
            controls: 1, // Enable controls so you can pause by tapping
            autoplay: 1,
            rel: 0,
            modestbranding: 1,
            enablejsapi: 1
        },
        events: {
            'onReady': function() { ytReady = true; },
            'onStateChange': function(e) {
                if (e.data === 1) { // Playing
                    isPlaying = true; updateAllIcons();
                } else if (e.data === 2) { // Paused
                    isPlaying = false; updateAllIcons();
                } else if (e.data === 0) { // ENDED
                    // Auto-shuffle from Similar Songs!
                    if (window.simPool && window.simPool.length > 0) {
                        var ri = Math.floor(Math.random() * window.simPool.length);
                        window.ytResults = window.simPool.map(function(x) {
                            return {
                                id: { videoId: x.id },
                                snippet: {
                                    title: x.title,
                                    channelTitle: x.uploaderName,
                                    thumbnails: { default: { url: x.thumbnail }, high: { url: x.thumbnail } }
                                }
                            };
                        });
                        window.playQueue = window.ytResults;
                        window.playYoutube(ri);
                    } else {
                        if (typeof nextTrack === 'function') nextTrack();
                    }
                }
            }
        }
    });
};


document.addEventListener('DOMContentLoaded', function() {
    var fab = document.getElementById('fullArtBox');
    var fsBtn = document.getElementById('fsOverlayBtn');
    var yp = document.getElementById('youtube-player');
    var fa = document.getElementById('fullArt');

    if (yp && fab) { fab.appendChild(yp); }
    if (fsBtn && fab) { fab.appendChild(fsBtn); }

    // ONLY the ⛶ button toggles fullscreen (no accidental fullscreen on video tap)
    if (fsBtn) {
        fsBtn.addEventListener('click', function(e) {
            e.stopPropagation();
            var isFull = fab.classList.contains('is-fullscreen');
            if (!isFull) {
                fab.classList.add('is-fullscreen');
                if (fab.requestFullscreen) fab.requestFullscreen();
            } else {
                fab.classList.remove('is-fullscreen');
                if (document.exitFullscreen) document.exitFullscreen();
            }
        });
    }

    document.addEventListener('fullscreenchange', function() {
        if (!document.fullscreenElement) fab.classList.remove('is-fullscreen');
    });

    var originalPlayYoutube = window.playYoutube;
    window.playYoutube = function(i) {
        if (originalPlayYoutube) originalPlayYoutube(i);
        if (yp) yp.style.display = 'block';
        if (fa) fa.style.display = 'none';
        if (fsBtn) fsBtn.style.display = 'block';
    };

    var originalPlayDbSong = window.playDbSong;
    window.playDbSong = function(i) {
        if (originalPlayDbSong) originalPlayDbSong(i);
        if (yp) yp.style.display = 'none';
        if (fa) fa.style.display = 'block';
        if (fsBtn) fsBtn.style.display = 'none';
        fab.classList.remove('is-fullscreen');
    };
});

// INTERCEPT YOUTUBE END SCREEN
window.onYouTubeIframeAPIReady = function() {
    ytPlayer = new YT.Player('youtube-player', {
        height: '100%',
        width: '100%',
        playerVars: {
            playsinline: 1,
            controls: 1,
            autoplay: 1,
            rel: 0, // Kills YouTube's "More Videos" end screen
            modestbranding: 1,
            enablejsapi: 1
        },
        events: {
            'onReady': function() { ytReady = true; },
            'onStateChange': function(e) {
                if (e.data === 1) { 
                    isPlaying = true; updateAllIcons();
                } else if (e.data === 2) { 
                    isPlaying = false; updateAllIcons();
                } else if (e.data === 0) { 
                    // VIDEO ENDED! 
                    // Instead of shuffling the MAIN queue, we grab a random song from SIMILAR SONGS
                    if (window.simPool && window.simPool.length > 0) {
                        // Pick a random song from Similar Songs (Mixed)
                        var randomIndex = Math.floor(Math.random() * window.simPool.length);
                        
                        // Temporarily set the queue to Similar Songs so "Next" goes through them
                        window.ytResults = window.simPool.map(function(x) {
                            return {
                                id: { videoId: x.id },
                                snippet: {
                                    title: x.title,
                                    channelTitle: x.uploaderName,
                                    thumbnails: { default: { url: x.thumbnail }, high: { url: x.thumbnail } }
                                }
                            };
                        });
                        window.playQueue = window.ytResults;
                        
                        // Play the random Similar Song
                        window.playYoutube(randomIndex);
                    } else {
                        // Fallback if no Similar Songs are loaded yet
                        if (typeof nextTrack === 'function') nextTrack();
                    }
                }
            }
        }
    });
};


document.addEventListener('DOMContentLoaded', function() {
    var fab = document.getElementById('fullArtBox');
    var fsBtn = document.getElementById('fsOverlayBtn');
    var yp = document.getElementById('youtube-player');
    var fa = document.getElementById('fullArt');
    
    // Create the Up Next card
    var blocker = document.createElement('div');
    blocker.id = 'videoBlocker';
    blocker.innerHTML = '<img id="nextSongImg" src=""><div id="nextSongDetails"><div id="nextSongTitle">Up Next</div><div id="nextSongArtist">Artist</div></div><button id="nextSongBtn">▶ Play</button>';
    if (fab) { fab.appendChild(blocker); }

    var nextSongIndex = -1; // Tracks the random song we picked

    // Fullscreen Toggle
    if (fsBtn) {
        fsBtn.addEventListener('click', function(e) {
            e.stopPropagation();
            var isFull = fab.classList.contains('is-fullscreen');
            if (!isFull) {
                fab.classList.add('is-fullscreen');
                if (fab.requestFullscreen) fab.requestFullscreen();
            } else {
                fab.classList.remove('is-fullscreen');
                if (document.exitFullscreen) document.exitFullscreen();
            }
        });
    }
    document.addEventListener('fullscreenchange', function() {
        if (!document.fullscreenElement) fab.classList.remove('is-fullscreen');
    });

    // Show/Hide Video logic
    var originalPlayYoutube = window.playYoutube;
    window.playYoutube = function(i) {
        if (originalPlayYoutube) originalPlayYoutube(i);
        if (yp) yp.style.display = 'block';
        if (fa) fa.style.display = 'none';
        if (fsBtn) fsBtn.style.display = 'block';
        if (blocker) { blocker.classList.remove('show'); blocker.style.display = 'none'; }
        nextSongIndex = -1; // Reset next song on new play
    };

    var originalPlayDbSong = window.playDbSong;
    window.playDbSong = function(i) {
        if (originalPlayDbSong) originalPlayDbSong(i);
        if (yp) yp.style.display = 'none';
        if (fa) fa.style.display = 'block';
        if (fsBtn) fsBtn.style.display = 'none';
        if (blocker) { blocker.classList.remove('show'); blocker.style.display = 'none'; }
        fab.classList.remove('is-fullscreen');
    };

    // Click handler for the Up Next card
    if (blocker) {
        blocker.onclick = function() {
            blocker.classList.remove('show');
            blocker.style.display = 'none';
            if (yp) yp.style.display = 'block'; 
            
            if (nextSongIndex !== -1 && window.simPool && window.simPool.length > 0) {
                // Play the pre-selected song
                window.ytResults = window.simPool.map(function(x) {
                    return {
                        id: { videoId: x.id },
                        snippet: {
                            title: x.title,
                            channelTitle: x.uploaderName,
                            thumbnails: { default: { url: x.thumbnail }, high: { url: x.thumbnail } }
                        }
                    };
                });
                window.playQueue = window.ytResults;
                window.playYoutube(nextSongIndex);
            } else {
                // Fallback if no next song was picked
                if (typeof nextTrack === 'function') nextTrack();
            }
        };
    }

    // --- THE POLICE PATROL (Runs every 0.5 seconds) ---
    setInterval(function() {
        if (window.currentSource !== 'youtube') return;
        if (!window.ytPlayer || typeof window.ytPlayer.getPlayerState !== 'function') return;
        
        try {
            var state = window.ytPlayer.getPlayerState();
            var curTime = window.ytPlayer.getCurrentTime() || 0;
            var dur = window.ytPlayer.getDuration() || 0;

            // 1. Playing state
            if (state === 1) { 
                // If 10 seconds or less are left, show the Up Next card
                if (dur > 0 && (dur - curTime) <= 10) {
                    
                    // Pick a random similar song if we haven't already
                    if (nextSongIndex === -1 && window.simPool && window.simPool.length > 0) {
                        nextSongIndex = Math.floor(Math.random() * window.simPool.length);
                        var next = window.simPool[nextSongIndex];
                        document.getElementById('nextSongImg').src = next.thumbnail;
                        document.getElementById('nextSongTitle').textContent = next.title;
                        document.getElementById('nextSongArtist').textContent = next.uploaderName;
                    }
                    
                    // Show the card
                    if (blocker && !blocker.classList.contains('show')) {
                        blocker.style.display = 'flex';
                        setTimeout(function() { blocker.classList.add('show'); }, 10);
                    }
                }
            } 
            // 2. Ended state
            else if (state === 0) { 
                // Force the card to show if it hasn't already
                if (blocker && !blocker.classList.contains('show')) {
                    if (nextSongIndex === -1 && window.simPool && window.simPool.length > 0) {
                        nextSongIndex = Math.floor(Math.random() * window.simPool.length);
                        var next = window.simPool[nextSongIndex];
                        document.getElementById('nextSongImg').src = next.thumbnail;
                        document.getElementById('nextSongTitle').textContent = next.title;
                        document.getElementById('nextSongArtist').textContent = next.uploaderName;
                    }
                    blocker.style.display = 'flex';
                    setTimeout(function() { blocker.classList.add('show'); }, 10);
                }
            }
            // 3. Paused state (Hide the card if user pauses before the end)
            else if (state === 2) {
                if (blocker) {
                    blocker.classList.remove('show');
                    blocker.style.display = 'none';
                }
            }
        } catch(e) {}
    }, 500);
});


document.addEventListener('DOMContentLoaded', function() {
    // Find all possible back buttons
    var backBtns = document.querySelectorAll('#backBtn, .back-btn, .back-button, [onclick*="back"], [onclick*="close"], #closeArtistModal, #closeFullPlayer');
    
    // The SVG arrow
    var arrowSVG = '<svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" style="margin-right: 5px;"><line x1="19" y1="12" x2="5" y2="12"></line><polyline points="12 19 5 12 12 5"></polyline></svg>';

    backBtns.forEach(function(btn) {
        // Only add the arrow if it doesn't already have one
        if (!btn.querySelector('svg')) {
            btn.innerHTML = arrowSVG + ' ' + btn.innerHTML;
        }
    });
});


document.addEventListener('DOMContentLoaded', function() {
    var fullPlayer = document.getElementById('fullPlayer');
    if (!fullPlayer) return;

    var ambientBg = document.createElement('div');
    ambientBg.id = 'fullPlayerAmbient';
    fullPlayer.insertBefore(ambientBg, fullPlayer.firstChild);

    function updateFullPlayerBg(imageUrl) {
        if (!imageUrl) return;
        ambientBg.style.backgroundImage = 'url(' + imageUrl + ')';
    }

    var originalPlayYoutube = window.playYoutube;
    window.playYoutube = function(i) {
        if (originalPlayYoutube) originalPlayYoutube(i);
        var t = window.ytResults[i];
        if (t && t.id && t.id.videoId) {
            // USE TINY THUMBNAIL (320x180) FOR BLUR - ZERO LAG
            var imgUrl = 'https://img.youtube.com/vi/' + t.id.videoId + '/mqdefault.jpg';
            updateFullPlayerBg(imgUrl);
        }
    };

    var originalPlayDbSong = window.playDbSong;
    window.playDbSong = function(i) {
        if (originalPlayDbSong) originalPlayDbSong(i);
        var s = window.songs[i];
        if (s && s.cover_art_url) {
            updateFullPlayerBg(s.cover_art_url);
        } else {
            ambientBg.style.backgroundImage = 'none';
        }
    };
});


document.addEventListener('DOMContentLoaded', function() {
    var miniPlayer = document.getElementById('miniPlayer');
    
    // Hook into openFullPlayer
    var originalOpenFullPlayer = window.openFullPlayer;
    window.openFullPlayer = function() {
        if (originalOpenFullPlayer) originalOpenFullPlayer();
        if (miniPlayer) {
            miniPlayer.style.display = 'none'; // Hide the mini player
        }
    };

    // Hook into closeFullPlayer
    var originalCloseFullPlayer = window.closeFullPlayer;
    window.closeFullPlayer = function() {
        if (originalCloseFullPlayer) originalCloseFullPlayer();
        if (miniPlayer) {
            // Only show the mini player if a song is actually playing/loaded
            if (miniPlayer.classList.contains('active')) {
                miniPlayer.style.display = 'flex'; // Bring it back
            }
        }
    };
});


if ('serviceWorker' in navigator) {
  window.addEventListener('load', function() {
    navigator.serviceWorker.register('service-worker.js');
  });
}


document.addEventListener('DOMContentLoaded', function() {
    var btn = document.getElementById('downloadApkBtn');
    if (!btn) return;
    var isInApp = /wv/.test(navigator.userAgent) || window.location.protocol === 'file:' || (window.Android && typeof window.Android !== 'undefined');
    if (isInApp) {
        btn.style.display = 'none';
    } else {
        btn.style.display = 'flex';
    }
});














// SMART BACK BTN
(function() {
    var historyStack = [];
    var isNavigatingBack = false;

    function getCurrentView() {
        // Returns a string ID for the current screen
        var artistModal = document.getElementById('artistModal');
        if (artistModal && artistModal.classList.contains('active')) {
            return { view: 'artist', id: window.currentArtist ? window.currentArtist.name : null };
        }
        var fullPlayer = document.getElementById('fullPlayer');
        if (fullPlayer && fullPlayer.classList.contains('active')) {
            return { view: 'fullPlayer' };
        }
        // Determine current tab
        var navItems = document.querySelectorAll('.nav-item');
        for (var i = 0; i < navItems.length; i++) {
            if (navItems[i].classList.contains('active') || navItems[i].style.color === 'rgb(0, 224, 208)') {
                return { view: 'tab', id: i };
            }
        }
        // Default: home tab
        var homeTab = document.getElementById('tab-home');
        if (homeTab && homeTab.style.display !== 'none') return { view: 'tab', id: 0 };
        return { view: 'unknown' };
    }

    function pushHistory() {
        if (isNavigatingBack) return;
        var current = getCurrentView();
        var last = historyStack[historyStack.length - 1];
        // Only push if it's different from the last entry
        if (!last || last.view !== current.view || last.id !== current.id) {
            historyStack.push(current);
            if (historyStack.length > 30) historyStack.shift(); // cap the stack
        }
    }

    function goBack() {
        if (historyStack.length < 2) {
            // Nothing to go back to — go home
            var navItems = document.querySelectorAll('.nav-item');
            if (navItems.length > 0) navItems[0].click();
            return;
        }
        isNavigatingBack = true;
        historyStack.pop(); // Remove current
        var prev = historyStack[historyStack.length - 1];

        if (prev.view === 'artist') {
            // Close full player if open
            var fp = document.getElementById('fullPlayer');
            if (fp && fp.classList.contains('active')) fp.classList.remove('active');
            // Open artist modal
            if (typeof window.openArtistProfile === 'function' && window.currentArtist) {
                // Artist is already shown, just make sure modal is active
                var am = document.getElementById('artistModal');
                if (am) am.classList.add('active');
            }
        } else if (prev.view === 'fullPlayer') {
            // Close artist modal if open
            var am = document.getElementById('artistModal');
            if (am && am.classList.contains('active')) am.classList.remove('active');
            // Open full player
            if (typeof window.openFullPlayer === 'function') window.openFullPlayer();
        } else if (prev.view === 'tab') {
            // Close modals
            var am2 = document.getElementById('artistModal');
            if (am2 && am2.classList.contains('active')) am2.classList.remove('active');
            var fp2 = document.getElementById('fullPlayer');
            if (fp2 && fp2.classList.contains('active')) fp2.classList.remove('active');
            // Switch to the previous tab
            var navItems = document.querySelectorAll('.nav-item');
            if (navItems[prev.id]) navItems[prev.id].click();
        }

        setTimeout(function() { isNavigatingBack = false; }, 300);
    }

    function initBackButton() {
        // Inject CSS
        if (!document.getElementById('backBtnStyle')) {
            var style = document.createElement('style');
            style.id = 'backBtnStyle';
            style.textContent = "#backBtnSmart{display:flex;position:fixed;bottom:90px;right:15px;z-index:999999;background:rgba(0,0,0,0.88);border:1px solid rgba(255,255,255,0.25);border-radius:50%;width:52px;height:52px;align-items:center;justify-content:center;cursor:pointer;box-shadow:0 4px 18px rgba(0,0,0,0.7);backdrop-filter:blur(10px);-webkit-backdrop-filter:blur(10px);transition:all 0.2s ease;}#backBtnSmart:active{transform:scale(0.9);background:rgba(0,224,208,0.35);border-color:#00e0d0;}#backBtnSmart svg{width:24px;height:24px;fill:#fff;}";
            document.head.appendChild(style);
        }

        // Create button
        if (!document.getElementById('backBtnSmart')) {
            var btn = document.createElement('div');
            btn.id = 'backBtnSmart';
            btn.innerHTML = '<svg viewBox="0 0 24 24"><path d="M20 11H7.83l5.59-5.59L12 4l-8 8 8 8 1.41-1.41L7.83 13H20v-2z"/></svg>';
            document.body.appendChild(btn);

            btn.onclick = function(e) { e.preventDefault(); e.stopPropagation(); goBack(); };
        }

        // Watch for screen changes every 300ms
        setInterval(function() {
            pushHistory();
        }, 300);

        // Intercept hardware back button
        history.pushState({page: 'app'}, '', '');
        window.addEventListener('popstate', function() {
            goBack();
            history.pushState({page: 'app'}, '', '');
        });
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initBackButton);
    } else {
        initBackButton();
    }
})();
// END SMART BACK BTN





// UPDATE BTN
(function() {
    function initUpdateButton() {
        var now = Date.now();
        var DAY_MS = 24 * 60 * 60 * 1000;
        var HOUR_MS = 60 * 60 * 1000;

        var state = JSON.parse(localStorage.getItem('biUpdateBtnState') || '{}');
        var today = new Date().toISOString().slice(0, 10);

        // 2-day lockout still active
        if (state.lockUntil && now < state.lockUntil) {
            console.log('[UpdateBtn] Locked until', new Date(state.lockUntil).toLocaleString());
            return;
        }

        // New day → reset counter
        if (state.day !== today) {
            state.day = today;
            state.showsToday = 0;
            state.lockUntil = null;
        }

        // 3 shows done today → 2-day lock
        if (state.showsToday >= 3) {
            state.lockUntil = now + (2 * DAY_MS);
            localStorage.setItem('biUpdateBtnState', JSON.stringify(state));
            console.log('[UpdateBtn] Hit daily limit, locking for 2 days.');
            return;
        }

        // --- CSS (only once) ---
        if (!document.getElementById('updateBtnStyle')) {
            var style = document.createElement('style');
            style.id = 'updateBtnStyle';
            style.textContent = `
                #updateBtnSmart {
                    display: none;
                    position: fixed;
                    bottom: 150px;
                    right: 15px;
                    z-index: 999998;
                    background: linear-gradient(135deg, #00e0d0, #008f85);
                    color: #000;
                    border: none;
                    border-radius: 30px;
                    padding: 12px 20px;
                    font-size: 13px;
                    font-weight: bold;
                    cursor: pointer;
                    box-shadow: 0 6px 20px rgba(0, 224, 208, 0.5);
                    align-items: center;
                    gap: 8px;
                    transition: opacity 0.5s ease, transform 0.3s ease;
                    opacity: 0;
                }
                #updateBtnSmart.visible {
                    display: flex;
                    opacity: 1;
                    animation: pulseUpdate 2s infinite;
                }
                @keyframes pulseUpdate {
                    0% { transform: scale(1); }
                    50% { transform: scale(1.06); }
                    100% { transform: scale(1); }
                }
                #updateBtnSmart:active { transform: scale(0.95); }
                #updateBtnSmart svg { width: 16px; height: 16px; fill: #000; }
            `;
            document.head.appendChild(style);
        }

        // --- Create the button (hidden) ---
        if (!document.getElementById('updateBtnSmart')) {
            var btn = document.createElement('button');
            btn.id = 'updateBtnSmart';
            btn.innerHTML = '<svg viewBox="0 0 24 24"><path d="M17.65 6.35A7.958 7.958 0 0012 4c-4.42 0-7.99 3.58-7.99 8s3.57 8 7.99 8c3.73 0 6.84-2.55 7.73-6h-2.08A5.99 5.99 0 0112 18c-3.31 0-6-2.69-6-6s2.69-6 6-6c1.66 0 3.14.69 4.22 1.78L13 11h7V4l-2.35 2.35z"/></svg> Update Available';
            document.body.appendChild(btn);

            btn.onclick = function() {
                btn.innerHTML = '⏳ Updating...';
                btn.disabled = true;
                setTimeout(function() {
                    window.location.href = window.location.pathname + '?update=' + Date.now();
                }, 400);
            };
        }

        // --- Random appearance scheduler ---
        function scheduleNextShow() {
            // Random delay between 2 and 5 hours
            var minMs = 2 * HOUR_MS;
            var maxMs = 5 * HOUR_MS;
            var delay = minMs + Math.random() * (maxMs - minMs);
            var delayMinutes = Math.round(delay / 60000);

            console.log('[UpdateBtn] Next appearance in ~' + delayMinutes + ' minutes.');

            setTimeout(function() {
                // Re-check state just before showing
                var currentState = JSON.parse(localStorage.getItem('biUpdateBtnState') || '{}');
                var nowCheck = Date.now();
                var todayCheck = new Date().toISOString().slice(0, 10);

                if (currentState.lockUntil && nowCheck < currentState.lockUntil) return;
                if (currentState.day !== todayCheck) {
                    currentState.day = todayCheck;
                    currentState.showsToday = 0;
                    currentState.lockUntil = null;
                }
                if (currentState.showsToday >= 3) {
                    currentState.lockUntil = nowCheck + (2 * DAY_MS);
                    localStorage.setItem('biUpdateBtnState', JSON.stringify(currentState));
                    return;
                }

                // Show the button
                var btn = document.getElementById('updateBtnSmart');
                if (btn) {
                    btn.style.display = 'flex';
                    btn.classList.add('visible');

                    // Log this show
                    currentState.showsToday = (currentState.showsToday || 0) + 1;
                    localStorage.setItem('biUpdateBtnState', JSON.stringify(currentState));
                    console.log('[UpdateBtn] Shown ' + currentState.showsToday + '/3 today.');

                    // Hide after 60 seconds
                    setTimeout(function() {
                        btn.classList.remove('visible');
                        setTimeout(function() { btn.style.display = 'none'; }, 600);
                    }, 60000);
                }

                // Schedule the next random appearance
                scheduleNextShow();
            }, delay);
        }

        // Start the scheduler
        scheduleNextShow();
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initUpdateButton);
    } else {
        initUpdateButton();
    }
})();
// END UPDATE BTN
