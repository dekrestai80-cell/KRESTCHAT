from flask import Flask, request, jsonify
import os
app = Flask(__name__)

users = {}  # phone: name
contacts = {} # phone: [ {phone, name} ]
messages = [] # {from, to, text}

@app.route('/')
def home():
    return '''
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>KRESTCHAT</title>
<style>
body{margin:0;background:#0f0f0f;color:#fff;font-family:Arial}
.top{background:linear-gradient(90deg,#ff00cc,#3333ff);padding:15px;text-align:center;font-weight:bold;font-size:22px}
.box{max-width:480px;margin:auto;padding:15px}
.card{background:#1e1e1e;padding:15px;border-radius:12px;margin-bottom:12px}
input{width:100%;padding:12px;border:none;border-radius:8px;background:#2a2a2a;color:#fff;margin:6px 0;box-sizing:border-box}
button{width:100%;padding:12px;border:none;border-radius:8px;background:linear-gradient(90deg,#ff00cc,#3333ff);color:#fff;font-weight:bold;margin-top:6px}
.hide{display:none}
.msg{background:#2a2a2a;padding:8px;border-radius:8px;margin:5px 0}
.small{font-size:11px;color:#888}
</style>
</head>
<body>
<div class="top">KRESTCHAT</div>
<div class="box">

<div id="loginBox" class="card">
<h3>Login Required</h3>
<p class="small">You must login before you can add people and chat</p>
<input id="phone" placeholder="Your phone e.g +2348012345678">
<input id="name" placeholder="Your name">
<button onclick="doLogin()">Login / Create Account</button>
</div>

<div id="mainBox" class="hide">
<div class="card">
<p>Welcome <b id="myNameShow"></b> - <span id="myPhoneShow"></span> <button onclick="doLogout()" style="width:auto;padding:5px 10px;background:#ff3333">Logout</button></p>
</div>

<div class="card">
<h3>Add People</h3>
<p class="small">Add phone number to chat with them</p>
<input id="addPhone" placeholder="Person phone +234...">
<input id="addName" placeholder="Person name">
<button onclick="addPerson()">Add Person</button>
<div id="contactList"></div>
</div>

<div class="card">
<h3 id="chatTitle">Select a person to chat</h3>
<div id="chatArea" style="max-height:250px;overflow:auto;background:#111;padding:8px;border-radius:8px"></div>
<input id="msgInput" placeholder="Type message...">
<button onclick="sendChat()">Send Message</button>
</div>
</div>

</div>
<script>
let myPhone = localStorage.getItem('krest_phone');
let myName = localStorage.getItem('krest_name');
let myContacts = JSON.parse(localStorage.getItem('krest_contacts')||'[]');
let chatWith = null;

function checkLogin(){
  if(myPhone && myName){
    document.getElementById('loginBox').className='card hide';
    document.getElementById('mainBox').className='';
    document.getElementById('myNameShow').innerText=myName;
    document.getElementById('myPhoneShow').innerText=myPhone;
    renderContacts();
  } else {
    document.getElementById('loginBox').className='card';
    document.getElementById('mainBox').className='hide';
  }
}

function doLogin(){
  let p=document.getElementById('phone').value;
  let n=document.getElementById('name').value;
  if(!p || !n){alert('Enter phone and name');return;}
  fetch('/api/login',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({phone:p,name:n})})
  .then(r=>r.json()).then(d=>{
    myPhone=p; myName=n;
    localStorage.setItem('krest_phone',p);
    localStorage.setItem('krest_name',n);
    checkLogin();
  });
}

function doLogout(){
  localStorage.clear();
  myPhone=null; myName=null; chatWith=null;
  location.reload();
}

function addPerson(){
  if(!myPhone){alert('Login first!');return;}
  let p=document.getElementById('addPhone').value;
  let n=document.getElementById('addName').value;
  if(!p){alert('Enter phone');return;}
  if(!n) n=p;
  myContacts.push({phone:p,name:n});
  localStorage.setItem('krest_contacts',JSON.stringify(myContacts));
  document.getElementById('addPhone').value='';
  document.getElementById('addName').value='';
  renderContacts();
}

function renderContacts(){
  let div=document.getElementById('contactList');
  div.innerHTML='';
  myContacts.forEach(c=>{
    div.innerHTML += '<div class=msg onclick="openChat(\\''+c.phone+'\\')"><b>'+c.name+'</b> - '+c.phone+' (tap to chat)</div>';
  });
}

function openChat(phone){
  if(!myPhone){alert('Login first!');return;}
  chatWith=phone;
  document.getElementById('chatTitle').innerText='Chatting with '+phone;
  loadChat();
}

function loadChat(){
  if(!chatWith) return;
  fetch('/api/get').then(r=>r.json()).then(data=>{
    let area=document.getElementById('chatArea');
    area.innerHTML='';
    data.forEach(m=>{
      if((m.from==myPhone && m.to==chatWith) || (m.from==chatWith && m.to==myPhone)){
        let who = m.from==myPhone ? 'You' : m.from;
        area.innerHTML += '<div class=msg><b>'+who+':</b> '+m.text+'</div>';
      }
    });
  });
}

function sendChat(){
  if(!myPhone){alert('You must login first!');return;}
  if(!chatWith){alert('Select a person to chat first');return;}
  let t=document.getElementById('msgInput').value;
  if(!t) return;
  fetch('/api/send',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({from:myPhone,to:chatWith,text:t})})
  .then(r=>r.json()).then(d=>{
    document.getElementById('msgInput').value='';
    loadChat();
  });
}

checkLogin();
setInterval(()=>{if(chatWith) loadChat();},2000);
</script>
</body>
</html>
'''

@app.route('/api/login', methods=['POST'])
def login():
    d=request.get_json()
    users[d['phone']] = d['name']
    if d['phone'] not in contacts:
        contacts[d['phone']] = []
    return jsonify({'ok':True})

@app.route('/api/get')
def get_msg():
    return jsonify(messages[-200:])

@app.route('/api/send', methods=['POST'])
def send():
    d=request.get_json()
    if not d.get('from') or not d.get('to'):
        return jsonify({'error':'login required'}), 400
    messages.append({'from':d['from'],'to':d['to'],'text':d.get('text','')})
    return jsonify({'ok':True})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT',10000)))
