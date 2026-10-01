from flask import Flask
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
