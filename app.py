from flask import Flask, request, jsonify
import os

app = Flask(__name__)
messages = []
posts = []

@app.route('/')
def home():
    return """
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>KRESTCHAT</title>
<style>
body{margin:0;font-family:Arial;background:#0a0a0a;color:#fff}
.header{background:linear-gradient(90deg,#ff00cc,#3333ff);padding:15px;text-align:center;font-size:22px;font-weight:bold}
.box{max-width:500px;margin:auto;padding:10px;padding-bottom:80px}
.card{background:#1a1a1a;padding:12px;border-radius:12px;margin-bottom:10px}
input{width:100%;padding:10px;border-radius:8px;border:none;background:#2a2a2a;color:#fff;margin:5px 0}
button{padding:10px 12px;border:none;border-radius:8px;font-weight:bold;background:linear-gradient(90deg,#ff00cc,#3333ff);color:#fff;margin-top:5px}
.msg{background:#2a2a2a;padding:8px;border-radius:8px;margin:5px 0}
.post-img{width:100%;border-radius:10px;margin-top:8px}
.video-block{background:#2a2a2a;padding:30px;text-align:center;border-radius:10px}
.switch{padding:6px 12px;background:#222;border-radius:20px;font-size:12px;cursor:pointer}
</style>
</head>
<body>
<div class="header">KRESTCHAT - Free Mode ON</div>
<div class="box">

<div class="card">
<b>Login</b><br>
<input id="myPhone" placeholder="Your phone +234...">
<input id="myName" placeholder="Your name">
<button onclick="login()">Login</button>
<span id="freeBtn" class="switch" onclick="toggleFree()">Free Mode: ON</span>
<p id="loginStatus" style="font-size:12px;color:#aaa"></p>
</div>

<div class="card">
<b>Add Number to Chat Somebody</b><br>
<input id="otherPhone" placeholder="Other phone +234...">
<input id="otherName" placeholder="Other name">
<button onclick="addContact()">Add Contact</button>
<div id="contacts"></div>
</div>

<div class="card">
<b>Create Post - Photo / Video</b><br>
<input id="postText" placeholder="What is happening?">
<input type="file" id="postFile" accept="image/*,video/*">
<button onclick="createPost()">Post Photo/Video</button>
<p style="font-size:11px;color:#aaa">Photos = FREE to see. Videos = need data (like you said)</p>
</div>

<div id="feed"></div>

<div class="card">
<b id="chatTitle">Chat - select contact</b>
<div id="chat" style="max-height:250px;overflow:auto"></div>
<input id="msgText" placeholder="Type message...">
<button onclick="sendMsg()">Send</button>
</div>

</div>
<script>
let myPhone = localStorage.getItem('phone') || '';
let myName = localStorage.getItem('name') || '';
let contacts = JSON.parse(localStorage.getItem('contacts') || '[]');
let currentChat = null;
let freeMode = localStorage.getItem('freeMode')!== 'OFF';

document.getElementById('myPhone').value = myPhone;
document.getElementById('myName').value = myName;
updateFreeBtn();

function updateFreeBtn(){
  document.getElementById('freeBtn').innerText = freeMode? 'Free Mode: ON (Chat+Photos FREE)' : 'Free Mode: OFF';
}

function toggleFree(){
  freeMode =!freeMode;
  localStorage.setItem('freeMode', freeMode? 'ON' : 'OFF');
  updateFreeBtn();
  loadFeed();
}

function login(){
  myPhone = document.getElementById('myPhone').value;
  myName = document.getElementById('myName').value;
  if(!myPhone ||!myName){alert('Enter phone and name'); return;}
  localStorage.setItem('phone', myPhone);
  localStorage.setItem('name', myName);
  document.getElementById('loginStatus').innerText = 'Logged in as ' + myName;
  renderContacts();
}

function addContact(){
  let p = document.getElementById('otherPhone').value;
  let n = document.getElementById('otherName').value;
  if(!p){alert('Enter phone'); return;}
  if(!n) n = p;
  contacts.push({phone:p, name:n});
  localStorage.setItem('contacts', JSON.stringify(contacts));
  document.getElementById('otherPhone').value = '';
  document.getElementById('otherName').value = '';
  renderContacts();
}

function renderContacts(){
  let div = document.getElementById('contacts');
  div.innerHTML = '';
  contacts.forEach(function(c){
    div.innerHTML += '<div class=msg onclick="openChat(&quot;'+c.phone+'&quot;)"><b>'+c.name+'</b> - '+c.phone+'</div>';
  });
}

function openChat(phone){
  currentChat = phone;
  document.getElementById('chatTitle').innerText = 'Chatting with ' + phone;
  loadMessages();
}

function loadMessages(){
  fetch('/api/get').then(r=>r.json()).then(function(res){
    let chatDiv = document.getElementById('chat');
    chatDiv.innerHTML = '';
    res.messages.forEach(function(m){
      if((m.from==myPhone && m.to==currentChat) || (m.from==currentChat && m.to==myPhone)){
        let who = m.from==myPhone? 'You' : m.name;
        chatDiv.innerHTML += '<div class=msg><b>'+who+':</b> '+m.text+'</div>';
      }
    });
  });
}

function sendMsg(){
  let t = document.getElementById('msgText').value;
  if(!t ||!currentChat){alert('Select contact first'); return;}
  fetch('/api/send',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({from:myPhone,to:currentChat,name:myName,text:t})}).then(function(){document.getElementById('msgText').value=''; loadMessages();});
}

function createPost(){
  let txt = document.getElementById('postText').value;
  let fileInput = document.getElementById('postFile');
  let file = fileInput.files[0];
  if(!txt &&!file){alert('Type something or add photo/video'); return;}

  if(file){
    let reader = new FileReader();
    reader.onload = function(e){
      let type = file.type.includes('video')? 'video' : 'image';
      sendPost(txt, e.target.result, type);
    };
    reader.readAsDataURL(file);
  } else {
    sendPost(txt, '', 'text');
  }
}

function sendPost(text, data, type){
  fetch('/api/post',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({name:myName, phone:myPhone, text:text, media:data, mtype:type})}).then(function(){document.getElementById('postText').value=''; document.getElementById('postFile').value=''; loadFeed();});
}

function loadFeed(){
  fetch('/api/get').then(r=>r.json()).then(function(res){
    let feed = document.getElementById('feed');
    feed.innerHTML = '';
    res.posts.slice().reverse().forEach(function(p){
      let html = '<div class=card><b>'+p.name+'</b> - '+p.phone+'<p>'+p.text+'</p>';
      if(p.mtype=='image' && p.media){
        html += '<img src="'+p.media+'" class="post-img">';
      } else if(p.mtype=='video' && p.media){
        if(freeMode){
          html += '<div class=video-block>VIDEO - Free mode hides video to save data<br><button onclick="this.parentElement.innerHTML=\\'<video src='+p.media+' controls style=width:100%><\\\\/video>\\'">Use Data to Watch Video</button></div>';
        } else {
          html += '<video src="'+p.media+'" controls style="width:100%;border-radius:10px"></video>';
        }
      }
      html += '</div>';
      feed.innerHTML += html;
    });
  });
}

renderContacts();
loadFeed();
setInterval(function(){if(currentChat) loadMessages();},2000);
setInterval(loadFeed,5000);
</script>
</body>
</html>
"""

@app.route('/api/get')
def get_data():
    return jsonify({'messages': messages[-200:], 'posts': posts[-100:]})

@app.route('/api/send', methods=['POST'])
def send_msg():
    d = request.get_json()
    messages.append({'from': d.get('from',''), 'to': d.get('to',''), 'name': d.get('name','Guest'), 'text': d.get('text','')})
    return jsonify({'ok': True})

@app.route('/api/post', methods=['POST'])
def create_post():
    d = request.get_json()
    posts.append({'name': d.get('name','Guest'), 'phone': d.get('phone',''), 'text': d.get('text',''), 'media': d.get('media',''), 'mtype': d.get('mtype','text')})
    return jsonify({'ok': True})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT',10000)))
