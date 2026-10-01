from flask import Flask, request, jsonify
import os, random app = Flask(__name__)
users = {}
msgs = []
posts = []

@app.route('/')
def home():
    return '''
<!DOCTYPE html>
<
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>KRESTCHAT</title>
<style>
*{box-sizing:border-box} body{margin:0;font-family:sans-serif;background:#080a12;color:white}
#splash{position:fixed;inset:0;background:linear-gradient(135deg,#ff00cc,#3333ff,#00ffcc);display:flex;flex-direction:column;align-items:center;justify-content:center;z-index:9999}
.page{max-width:500px;margin:auto;padding:14px;padding-bottom:90px;display:none}
.page.active{display:block}
.card{background:#151826;border-radius:16px;padding:14px;margin-bottom:12px}
input,textarea{width:100%;padding:12px;border-radius:12px;border:none;background:#1f2336;color:white;margin:6px 0}
button{width:100%;padding:12px;border:none;border-radius:12px;font-weight:bold;background:linear-gradient(90deg,#ff00cc,#3333ff);color:white;margin-top:8px}
.small{font-size:12px;color:#aaa}
.top{position:sticky;top:0;background:#080a12;padding:12px;display:flex;justify-content:space-between;align-items:center;border-bottom:1px solid #222;z-index:10}
.msg{background:#1f2336;padding:10px;border-radius:12px;margin:6px 0}
.btm{position:fixed;bottom:0;left:0;right:0;background:#101221;border-top:1px solid #222;display:flex;justify-content:space-around;padding:10px;max-width:500px;margin:auto}
.btm div{text-align:center;font-size:12px;color:#aaa}
.btm div.active{color:#ff00cc}
</style>
</head>
<body>
<div id="splash" onclick="this.style.display='none'">
<h1 style="font-size:40px;margin:0">KRESTCHAT</h1>
<p>⚡ KREST CHAT</p>
<p class="small" style="margin-top:20px">Tap to enter... Fast, Free & Modern</p>
</div>

<div id="auth" class="page active">
<div class="top"><b>KRESTCHAT</b><span>KREST</span></div>
<div class="card">
<h3>Welcome to KRESTCHAT</h3>
<p class="small">Mark style room, but KREST edition</p>
<input id="phone" placeholder="Your WhatsApp Number e.g +234...">
<input id="name" placeholder="Your Full Name">
<button onclick="sendOTP()">Create Account / Log In - OTP via WhatsApp</button>
<div id="otpbox" style="display:none">
<input id="otp" placeholder="Enter OTP">
<button onclick="verifyOTP()">Verify & Enter</button>
<p id="otpshow" class="small"></p>
</div>
</div>
</div>

<div id="feed" class="page">
<div class="top"><b>Feed</b><span id="uname2">Guest</span></div>
<div class="card">
<textarea id="posttext" placeholder="Post photo, video, thoughts..."></textarea>
<input type="file" id="file" accept="image/*,video/*">
<button onclick="makePost()">Post</button>
<p class="small">Chat + Pictures = FREE. Video needs data</p>
</div>
<div id="posts"></div>
<div class="card"><b>💬 KREST Chat - Modern (TikTok x WhatsApp)</b>
<div id="chat"></div>
<div style="display:flex;gap:6px;margin-top:8px"><input id="msginp" placeholder="Type free chat..."><button onclick="sendMsg()" style="width:80px">Send</button></div>
</div>
</div>

<div id="profile" class="page">
<div class="top"><b>My Profile</b><span onclick="showPage('settings')">Settings</span></div>
<div class="card">
<div style="width:80px;height:80px;background:linear-gradient(90deg,#ff00cc,#3333ff);border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:30px">K</div>
<h3 id="pname">Guest</h3>
<p class="small">My Profile [ edit ]</p>
<p>Name: <span id="pname2">Guest</span></p>
<p>Status: Online 🟢</p>
<p>Phone: <span id="pphone">-</span></p>
<p>Concentration: KREST Chat</p>
<p>My Friends: 1</p>
<p>My Groups: KREST Lovers</p>
<p>My Messages: Free</p>
<p>My Account: Verified by WhatsApp OTP</p>
<p>My Privacy: Free Mode ON</p>
<button onclick="editProfile()">Edit Profile</button>
</div>
</div>

<div id="settings" class="page">
<div class="top"><b>Settings</b><span onclick="showPage('profile')">Back</span></div>
<div class="card">
<input id="sname" placeholder="Change Name">
<button onclick="saveSettings()">Save</button>
<button onclick="logout()" style="background:#ff3333">Log Out</button>
</div>
</div>

<div class="btm">
<div onclick="showPage('feed')" id="bfeed" class="active">Home</div>
<div onclick="showPage('profile')" id="bprof">Profile</div>
<div onclick="showPage('settings')" id="bset">Settings</div>
<div onclick="logout()">Log Out</div>
</div>

<script>
let currentUser=null, phoneNum=null, realOTP=null;
function showPage(p){document.querySelectorAll('.page').forEach(x=>x.classList.remove('active')); document.getElementById(p).classList.add('active');}
function sendOTP(){let ph=document.getElementById('phone').value; let nm=document.getElementById('name').value; if(!ph||!nm){alert('Enter phone and name'); return;} phoneNum=ph; realOTP=Math.floor(100000+Math.random()*900000); document.getElementById('otpbox').style.display='block'; document.getElementById('otpshow').innerText='DEMO OTP (Real app sends to WhatsApp): '+realOTP; fetch('/api/request_otp',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({phone:ph,name:nm,otp:realOTP})});}
function verifyOTP(){let o=document.getElementById('otp').value; if(o==realOTP){currentUser=document.getElementById('name').value; localStorage.setItem('krest_user',currentUser); localStorage.setItem('krest_phone',phoneNum); document.getElementById('uname2').innerText=currentUser; document.getElementById('pname').innerText=currentUser; document.getElementById('pname2').innerText=currentUser; document.getElementById('pphone').innerText=phoneNum; showPage('feed'); loadAll();} else alert('Wrong OTP');}
function loadAll(){fetch('/api/get').then(r=>r.json()).then(d=>{let c=document.getElementById('chat'); c.innerHTML=''; d.msgs.slice(-20).forEach(m=>{c.innerHTML+='<div class=msg><b>'+m.user+':</b> '+m.text+'</div>';}); let p=document.getElementById('posts'); p.innerHTML=''; d.posts.slice(-20).forEach(po=>{p.innerHTML+='<div class=card><b>'+po.user+'</b><p>'+po.text+'</p></div>';});});}
function sendMsg(){let v=document.getElementById('msginp').value; if(!v)return; fetch('/api/send',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({user:currentUser,text:v})}).then(()=>{document.getElementById('msginp').value=''; loadAll();});}
function makePost(){let t=document.getElementById('posttext').value; fetch('/api/post',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({user:currentUser,text:t})}).then(()=>{document.getElementById('posttext').value=''; loadAll();});}
function editProfile(){let n=prompt('New name'); if(n){currentUser=n; localStorage.setItem('krest_user',n); document.getElementById('pname').innerText=n; document.getElementById('pname2').innerText=n; document.getElementById('uname2').innerText=n;}}
function saveSettings(){let n=document.getElementById('sname').value; if(n) editProfile(); alert('Saved'); showPage('profile');}
function logout(){localStorage.clear(); location.reload();}
let saved=localStorage.getItem('krest_user'); if(saved){currentUser=saved; phoneNum=localStorage.getItem('krest_phone')||''; document.getElementById('uname2').innerText=saved; document.getElementById('pname').innerText=saved; document.getElementById('pname2').innerText=saved; document.getElementById('pphone').innerText=phoneNum; document.getElementById('splash').style.display='none'; showPage('feed');}
setInterval(loadAll,3000);
</script>
</body>
</html>
'''
@app.route('/api/request_otp', methods=['POST'])
def req_otp():
    d=request.get_json()
    users[d['phone']] = {'name': d['name'], 'otp': d['otp']}
    return jsonify({'ok': True})
@app.route('/api/get')
def get_all(): return jsonify({'msgs': msgs[-50:], 'posts': posts[-50:]})
@app.route('/api/send', methods=['POST'])
def send():
    d=request.get_json()
    msgs.append({'user': d.get('user','Guest'), 'text': d.get('text','')})
    return jsonify({'ok': True})
@app.route('/api/post', methods=['POST'])
def post():
    d=request.get_json()
    posts.append({'user': d.get('user','Guest'), 'text': d.get('text','')})
    return jsonify({'ok': True})
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT',10000)))
