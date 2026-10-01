from flask import Flask, request, jsonify
import os

app = Flask(__name__)
msgs = []

@app.route('/')
def home():
    return """
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>KRESTCHAT - New Gen Chat</title>
<style>
*{box-sizing:border-box}
body{margin:0;font-family:system-ui;background:#0f0f13;color:white;padding-bottom:80px}
.header{background:linear-gradient(90deg,#8e2de2,#4a00e0);padding:16px;text-align:center;font-size:22px;font-weight:800;letter-spacing:1px}
.sub{font-size:11px;opacity:0.8;font-weight:400}
.feed{padding:14px;max-width:500px;margin:auto}
.card{background:#1c1c22;border-radius:18px;padding:14px;margin-bottom:12px;box-shadow:0 4px 15px #0005}
.userline{display:flex;align-items:center;gap:8px;font-weight:700}
.dot{width:8px;height:8px;background:#00ff88;border-radius:50%;box-shadow:0 0 8px #00ff88}
.bubble{background:#2a2a33;padding:10px 14px;border-radius:16px;margin-top:8px;font-size:15px;line-height:1.4}
.reply{background:#8e2de2;opacity:0.8;font-size:12px;padding:4px 8px;border-radius:8px;margin-bottom:6px}
.inputwrap{position:fixed;bottom:68px;left:0;right:0;background:#1c1c22;padding:10px;display:flex;gap:8px;max-width:500px;margin:auto;border-top:1px solid #333}
.inputwrap input{flex:1;background:#2a2a33;border:none;color:white;padding:12px 16px;border-radius:25px;outline:none}
.inputwrap button{background:linear-gradient(90deg,#8e2de2,#4a00e0);border:none;color:white;padding:12px 20px;border-radius:25px;font-weight:bold}
.bottom{position:fixed;bottom:0;left:0;right:0;background:#1c1c22;border-top:1px solid #333;display:flex;justify-content:space-around;padding:12px;max-width:500px;margin:auto}
.bottom button{background:#2a2a33;color:white;border:none;padding:8px 18px;border-radius:20px}
.bottom button.active{background:linear-gradient(90deg,#8e2de2,#4a00e0);font-weight:bold}
#repbar{position:fixed;bottom:118px;left:0;right:0;background:#ffcc00;color:black;padding:6px;text-align:center;font-size:13px;display:none;max-width:500px;margin:auto}
</style>
</head>
<body>
<div class="header">KRESTCHAT<div class="sub">⚡ Built for the new generation</div></div>
<div class="feed" id="chat"></div>
<div id="repbar" onclick="this.style.display='none'"></div>
<div class="inputwrap">
<input id="inp" placeholder="Type a message...">
<button onclick="send()">➤</button>
</div>
<div class="bottom">
<button class="active" id="u">Guest</button>
<button onclick="login()">Log In</button>
<button onclick="logout()">Log Out</button>
</div>
<script>
let replyTo=null;
let user=localStorage.getItem('krest_user')||'Guest';
document.getElementById('u').innerText=user;
function login(){let n=prompt('Your display name:'); if(n){localStorage.setItem('krest_user',n); user=n; document.getElementById('u').innerText=n}}
function logout(){localStorage.removeItem('krest_user'); user='Guest'; document.getElementById('u').innerText='Guest'}
function setR(t){replyTo=t; let r=document.getElementById('repbar'); r.style.display='block'; r.innerText='↩ Replying to: '+t+' (tap to cancel)';}
function load(){fetch('/api/m').then(r=>r.json()).then(d=>{let c=document.getElementById('chat'); c.innerHTML=''; d.forEach(m=>{c.innerHTML+=`<div class='card' onclick='setR("${m.text.replace(/"/g,'')})'><div class='userline'><div class='dot'></div>${m.user}</div>${m.reply?'<div class=reply>↩ '+m.reply+'</div>':''}<div class='bubble'>${m.text}</div></div>`}); if(d.length) window.scrollTo(0,document.body.scrollHeight);})}
function send(){let v=document.getElementById('inp').value; if(!v)return; fetch('/api/s',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({user:user,text:v,reply:replyTo})}).then(()=>{document.getElementById('inp').value=''; replyTo=null; document.getElementById('repbar').style.display='none'; load()})}
setInterval(load,2000); load();
</script>
</body>
</html>
"""
@app.route('/api/m')
def m(): return jsonify(msgs[-50:])
@app.route('/api/s', methods=['POST'])
def s():
    d=request.get_json()
    msgs.append({"user":d.get("user","Guest"),"text":d.get("text",""),"reply":d.get("reply")})
    return jsonify({"ok":True})
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT",10000))) flask import Flask
import os

app = Flask(__name__)

@app.route('/')
def home():
    return """
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>KRESTCHAT</title>
</head>
<body style="margin:0;font-family:sans-serif;background:#ece5dd">
<div style="background:#075E54;color:white;padding:12px;display:flex;justify-content:space-between;align-items:center">
  <span>🟢 KRESTCHAT</span>
  <button onclick="logout()" style="background:red;color:white;border:none;padding:6px 12px;border-radius:5px">Log Out</button>
</div>
<div style="padding:20px">
  <p>Welcome! Chat works.</p>
  <input id="msg" placeholder="Type..." style="padding:10px;width:70%">
  <button onclick="send()" style="padding:10px;background:#075E54;color:white">Send</button>
  <div id="box"></div>
</div>
<script>
function logout(){
  localStorage.clear();
  sessionStorage.clear();
  alert('Logged out');
  location.reload();
}
function send(){
  let v=document.getElementById('msg').value;
  if(!v) return;
  document.getElementById('box').innerHTML+='<p>'+v+'</p>';
  document.getElementById('msg').value='';
}
</script>
</body>
</html>
"""

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
