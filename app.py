from flask import Flask, request, jsonify
import os

app = Flask(__name__)
msgs = []

@app.route('/')
def home():
    html = '''
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>KRESTCHAT</title>
<style>
body{margin:0;font-family:sans-serif;background:#0f0f13;color:#fff;padding-bottom:90px}
.top{background:linear-gradient(90deg,#ff00cc,#3333ff);padding:18px;text-align:center;font-size:22px;font-weight:900}
.chat{max-width:500px;margin:auto;padding:12px}
.card{background:#1e1e26;padding:12px;border-radius:16px;margin-bottom:10px}
.bubble{background:#2d2d38;padding:10px;border-radius:12px;margin-top:6px}
.bottom{position:fixed;bottom:0;left:0;right:0;background:#1e1e26;display:flex;justify-content:space-around;padding:12px;border-top:1px solid #333}
.bottom button{border:none;padding:8px 16px;border-radius:20px;font-weight:bold}
#inputbar{position:fixed;bottom:58px;left:0;right:0;display:flex;padding:8px;background:#1e1e26;max-width:500px;margin:auto}
#inputbar input{flex:1;padding:12px;border-radius:20px;border:none;background:#2d2d38;color:white}
#inputbar button{background:linear-gradient(90deg,#ff00cc,#3333ff);border:none;color:white;padding:12px 18px;border-radius:20px;margin-left:6px}
</style>
</head>
<body>
<div class="top">KRESTCHAT - For People</div>
<div class="chat" id="chat"></div>
<div id="inputbar">
<input id="inp" placeholder="Type message...">
<button onclick="sendMsg()">Send</button>
</div>
<div class="bottom">
<button onclick="doLogin()" style="background:white;color:#3333ff">Log In</button>
<button id="userBtn" style="background:linear-gradient(90deg,#ff00cc,#3333ff);color:white">Guest</button>
<button onclick="doLogout()" style="background:#ff4444;color:white">Log Out</button>
</div>
<script>
let replyTo=null;
let user=localStorage.getItem('krest_user')||'Guest';
document.getElementById('userBtn').innerText=user;
function doLogin(){let n=prompt('Enter your name'); if(n){localStorage.setItem('krest_user',n); user=n; document.getElementById('userBtn').innerText=n;}}
function doLogout(){localStorage.removeItem('krest_user'); user='Guest'; document.getElementById('userBtn').innerText='Guest';}
function loadMsgs(){fetch('/api/get').then(r=>r.json()).then(data=>{let c=document.getElementById('chat'); c.innerHTML=''; data.forEach(m=>{c.innerHTML+='<div class=card><b>'+m.user+'</b><div class=bubble>'+m.text+'</div></div>';})})}
function sendMsg(){let v=document.getElementById('inp').value; if(!v)return; fetch('/api/send',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({user:user,text:v})}).then(()=>{document.getElementById('inp').value=''; loadMsgs();})}
setInterval(loadMsgs,2000); loadMsgs();
</script>
</body>
</html>
'''
    return html

@app.route('/api/get')
def get_msgs():
    return jsonify(msgs[-50:])

@app.route('/api/send', methods=['POST'])
def send_msg():
    data = request.get_json()
    msgs.append({'user': data.get('user','Guest'), 'text': data.get('text','')})
    return jsonify({'ok': True})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
