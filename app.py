from flask import Flask, render_template_string
import os

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>KRESTCHAT</title>
<style>
body{margin:0;font-family:sans-serif;background:#ece5dd}
.header{background:#075E54;color:white;padding:12px;display:flex;justify-content:space-between;align-items:center}
.btn-logout{background:#ff3b30;color:white;border:none;padding:6px 14px;border-radius:6px;font-weight:bold}
.chat{padding:15px}
.msg{background:white;padding:10px;border-radius:8px;margin-bottom:10px;max-width:80%}
.online{width:10px;height:10px;background:#00ff00;border-radius:50%;display:inline-block}
</style>
</head>
<body>
<div class="header">
  <span><span class="online"></span> KRESTCHAT</span>
  <button class="btn-logout" onclick="logout()">Log Out</button>
</div>
<div class="chat">
  <div class="msg">Welcome to KRESTCHAT! 🟢 Online</div>
  <div class="msg">Real Google login ready - Add your Client ID</div>
  <div id="messages"></div>
</div>
<input id="inp" placeholder="Type message..." style="position:fixed;bottom:0;width:80%;padding:12px">
<button onclick="send()" style="position:fixed;bottom:0;right:0;width:20%;padding:12px;background:#075E54;color:white;border:none">Send</button>

<script>
function logout(){
  if(confirm('Log out of KRESTCHAT?')){
    localStorage.clear();
    sessionStorage.clear();
    location.href='/';
  }
}
function send(){
  let v=document.getElementById('inp').value;
  if(!v)return;
  let d=document.createElement('div');
  d.className='msg'; d.innerText=v;
  document.getElementById('messages').appendChild(d);
  document.getElementById('inp').value='';
}
</script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
"""

**2. Then check `requirements.txt` - must be:**
