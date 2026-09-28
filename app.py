from flask import Flask, request, jsonify
from datetime import datetime
import threading

app = Flask(__name__)

# DATABASES
GROUPS = {
    "world": [{"user":"KrestAI","num":"000","text":"🌍 WORLD GROUP - Everyone can chat here","time":"10:00"}]
}
PRIVATE = {} # key = 080123_080456
ONLINE = {}
lock = threading.Lock()

# HTML - WHATSAPP WITH NUMBER SYSTEM
HTML = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>KRESTCHAT - Chat By Number</title>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
<style>
*{margin:0;padding:0;box-sizing:border-box;font-family:Arial}
body{height:100vh;background:#111b21;color:white}
#app{display:flex;height:100vh}
#side{width:100%;max-width:380px;background:#111b21;border-right:1px solid #222;display:flex;flex-direction:column}
.head{padding:12px;background:#202c33;display:flex;justify-content:space-between}
.searchBox{padding:10px;background:#111b21}
.searchBox input{width:100%;padding:12px;border-radius:8px;border:0;background:#2a3942;color:white}
.searchBox button{width:100%;margin-top:8px;padding:12px;background:#00a884;border:0;border-radius:8px;color:white;font-weight:bold}
.tabs{display:flex;gap:6px;padding:8px}
.tabs button{flex:1;padding:8px;border-radius:20px;border:0;background:#2a3942;color:white}
.tabs button.active{background:#00a884}
#chatList{flex:1;overflow:auto}
.chatItem{padding:12px;display:flex;gap:10px;border-bottom:1px solid #1f2c34;cursor:pointer}
.chatItem:hover{background:#202c33}
.chatItem img{width:45px;height:45px;border-radius:50%}
#main{flex:1;display:flex;flex-direction:column;display:none}
#main.show{display:flex}
.msgHead{padding:10px;background:#202c33;display:flex;align-items:center;gap:10px}
#messages{flex:1;overflow:auto;padding:12px;display:flex;flex-direction:column;gap:6px;background:#0b141a}
.bubble{max-width:75%;padding:8px 10px;border-radius:8px;font-size:14px}
.bubble.me{align-self:flex-end;background:#005c4b}
.bubble.other{align-self:flex-start;background:#202c33}
.bubble span{font-size:10px;color:#8696a0;float:right;margin-left:8px;margin-top:4px}
#inputArea{padding:8px;background:#202c33;display:flex;gap:8px}
#inputArea input{flex:1;padding:12px;border-radius:8px;border:0;background:#2a3942;color:white}
#inputArea button{width:45px;height:45px;border-radius:50%;border:0;background:#00a884;color:white}
#login{position:fixed;inset:0;background:#111b21;z-index:100;display:flex;align-items:center;justify-content:center}
#loginBox{background:#202c33;padding:24px;border-radius:12px;width:92%;max-width:360px;text-align:center}
#loginBox input{width:100%;padding:12px;border-radius:8px;border:0;margin:6px 0;background:#2a3942;color:white}
#loginBox button{width:100%;padding:12px;background:#00a884;border:0;border-radius:8px;color:white;font-weight:bold;margin-top:10px}
</style>
</head>
<body>

<div id="login">
<div id="loginBox">
<div style="font-size:50px">📱</div>
<h2>Chat By Number</h2>
<p style="font-size:12px;color:#8696a0">Enter your number like WhatsApp</p>
<input id="myName" placeholder="Your Name e.g. DE Krest">
<input id="myNumber" placeholder="Your Number e.g. 08012345678">
<button onclick="login()">START CHATTING</button>
</div>
</div>

<div id="app">
<div id="side">
<div class="head"><b id="myDisplay">KRESTCHAT</b><span id="onlineCount">0 online</span></div>
<div class="searchBox">
<input id="searchNum" placeholder="Enter phone number to chat e.g. 080123...">
<button onclick="startPrivateChat()">💬 Chat This Number</button>
</div>
<div class="tabs">
<button class="active" onclick="filterChats('all')">All</button>
<button onclick="filterChats('private')">Private</button>
<button onclick="filterChats('group')">Groups</button>
</div>
<div id="chatList"></div>
</div>

<div id="main">
<div class="msgHead">
<i class="fa fa-arrow-left" onclick="backToList()" style="cursor:pointer"></i>
<img id="currentChatImg" src="https://i.pravatar.cc/100" style="width:35px;height:35px;border-radius:50%">
<b id="currentChatName"># world</b>
</div>
<div id="messages"></div>
<div id="inputArea">
<input id="msgInput" placeholder="Type message..." onkeydown="if(event.key==='Enter')sendMsg()">
<button onclick="sendMsg()"><i class="fa fa-paper-plane"></i></button>
</div>
</div>
</div>

<script>
let myName = "", myNumber = "", currentRoom = "world", isPrivate = false, currentFilter = "all";

function login(){
 myName = document.getElementById('myName').value.trim();
 myNumber = document.getElementById('myNumber').value.trim();
 if(!myName ||!myNumber) return alert('Enter Name and Number');
 localStorage.setItem('kName', myName);
 localStorage.setItem('kNum', myNumber);
 document.getElementById('login').style.display='none';
 document.getElementById('myDisplay').textContent = myName + " • " + myNumber;
 startApp();
}
let savedName = localStorage.getItem('kName');
let savedNum = localStorage.getItem('kNum');
if(savedName && savedNum){
 myName = savedName; myNumber = savedNum;
 document.getElementById('login').style.display='none';
 document.getElementById('myDisplay').textContent = myName + " • " + myNumber;
 startApp();
}

function getPrivateKey(a,b){ let arr=[a,b].sort(); return arr[0]+"_"+arr[1]; }

function startPrivateChat(){
 let num = document.getElementById('searchNum').value.trim();
 if(!num) return alert('Enter number');
 if(num == myNumber) return alert('That is your number');
 currentRoom = getPrivateKey(myNumber, num);
 isPrivate = true;
 document.getElementById('currentChatName').textContent = num;
 document.getElementById('currentChatImg').src = "https://i.pravatar.cc/100?u="+num;
 document.getElementById('main').classList.add('show');
 loadMessages();
}

function openChat(key, priv, displayName){
 currentRoom = key; isPrivate = priv;
 document.getElementById('currentChatName').textContent = displayName;
 document.getElementById('currentChatImg').src = "https://i.pravatar.cc/100?u="+displayName;
 document.getElementById('main').classList.add('show');
 loadMessages();
}

async function loadMessages(){
 let url = isPrivate? `/api/private?key=${currentRoom}&me=${myNumber}` : `/api/groups?room=${currentRoom}&me=${myNumber}`;
 let res = await fetch(url);
 let data = await res.json();

 // Show messages
 let box = document.getElementById('messages');
 box.innerHTML = "";
 data.messages.forEach(m=>{
   let div = document.createElement('div');
   div.className = "bubble " + (m.num == myNumber? "me" : "other");
   div.innerHTML = `<b style="font-size:11px;color:#53bdeb">${m.user}</b><br>${m.text}<span>${m.time}</span>`;
   box.appendChild(div);
 });
 box.scrollTop = box.scrollHeight;

 // Show chat list
 let list = document.getElementById('chatList');
 list.innerHTML = "";
 data.all_chats.forEach(c=>{
   if(currentFilter=='private' &&!c.isPrivate) return;
   if(currentFilter=='group' && c.isPrivate) return;
   let div = document.createElement('div');
   div.className = "chatItem";
   div.innerHTML = `<img src="https://i.pravatar.cc/100?u=${c.display}"><div><b>${c.display}</b><br><small style="color:#8696a0">${c.lastMsg}</small></div>`;
   div.onclick = ()=> openChat(c.key, c.isPrivate, c.display);
   list.appendChild(div);
 });
 document.getElementById('onlineCount').textContent = data.online + " online";
}

async function sendMsg(){
 let text = document.getElementById('msgInput').value.trim();
 if(!text) return;
 document.getElementById('msgInput').value = "";
 let endpoint = isPrivate? "/api/private" : "/api/groups";
 await fetch(endpoint, {
   method:"POST",
   headers:{"Content-Type":"application/json"},
   body: JSON.stringify({key: currentRoom, room: currentRoom, user: myName, num: myNumber, text: text})
 });
 loadMessages();
}

function filterChats(f){ currentFilter=f; document.querySelectorAll('.tabs button').forEach(b=>b.classList.remove('active')); event.target.classList.add('active'); loadMessages(); }
function backToList(){ document.getElementById('main').classList.remove('show'); }
function startApp(){ loadMessages(); setInterval(loadMessages, 2000); }
</script>
</body>
</html>
"""

@app.route("/")
def home():
    return HTML

@app.route("/api/groups", methods=["GET","POST"])
def groups():
    if request.method == "GET":
        room = request.args.get("room","world")
        me = request.args.get("me","")
        with lock:
            msgs = GROUPS.get(room, [])
            all_chats = []
            for k,v in GROUPS.items():
                last = v[-1]["text"][:25] if v else "Tap to chat"
                all_chats.append({"key":k,"display":"# "+k,"lastMsg":last,"isPrivate":False})
            for k,v in PRIVATE.items():
                if me in k and v:
                    other = k.split("_")[0] if k.split("_")[1]==me else k.split("_")[1]
                    last = v[-1]["text"][:25]
                    all_chats.append({"key":k,"display":other,"lastMsg":last,"isPrivate":True})
            return jsonify({"messages":msgs[-100:],"all_chats":all_chats,"online":len(ONLINE)})
    else:
        d = request.json
        room = d.get("room","world")
        with lock:
            if room not in GROUPS: GROUPS[room]=[]
            GROUPS[room].append({"user":d["user"],"num":d["num"],"text":d["text"],"time":datetime.now().strftime("%H:%M")})
            ONLINE[d["num"]]=True
        return jsonify({"ok":True})

@app.route("/api/private", methods=["GET","POST"])
def private_chat():
    if request.method == "GET":
        key = request.args.get("key","")
        me = request.args.get("me","")
        with lock:
            msgs = PRIVATE.get(key, [])
            all_chats = []
            for k,v in GROUPS.items():
                last = v[-1]["text"][:25] if v else "Tap to chat"
                all_chats.append({"key":k,"display":"# "+k,"lastMsg":last,"isPrivate":False})
            for k,v in PRIVATE.items():
                if me in k and v:
                    other = k.split("_")[0] if k.split("_")[1]==me else k.split("_")[1]
                    last = v[-1]["text"][:25]
                    all_chats.append({"key":k,"display":other,"lastMsg":last,"isPrivate":True})
            return jsonify({"messages":msgs[-100:],"all_chats":all_chats,"online":len(ONLINE)})
    else:
        d = request.json
        key = d.get("key")
        with lock:
            if key not in PRIVATE: PRIVATE[key]=[]
            PRIVATE[key].append({"user":d["user"],"num":d["num"],"text":d["text"],"time":datetime.now().strftime("%H:%M")})
            ONLINE[d["num"]]=True
        return jsonify({"ok":True})

if __name__ == "__main__":
    app.run()
