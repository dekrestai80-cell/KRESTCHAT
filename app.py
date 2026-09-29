import os 
from flask import Flask, request, jsonify
from datetime import datetime
import threading

app = Flask(__name__)
# Stores messages
CHATS = {"GLOBAL GROUP": [{"user":"KREST","text":"Welcome to Global Group 🌍 Everybody talk here!","time":"20:54","me":False}]}
PRIVATE = {}
lock = threading.Lock()

HTML = """
<!DOCTYPE html>
<html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>WhatsApp</title>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
<style>
*{margin:0;padding:0;box-sizing:border-box;font-family: -apple-system, Arial}
body{background:#fff;height:100vh;overflow:hidden}
#login{position:fixed;inset:0;background:#fff;z-index:1000;display:flex;align-items:center;justify-content:center}
.card{width:90%;max-width:350px;background:#fff;border-radius:20px;box-shadow:0 10px 40px rgba(0,0,0,.15);padding:28px;text-align:center}
.pro{width:110px;height:110px;border-radius:50%;object-fit:cover;margin:0 auto 18px;display:block;border:4px solid #0ca694}
.btn-gray{width:100%;padding:14px;background:#f0f0f0;border:0;border-radius:12px;font-weight:600;margin-bottom:12px;cursor:pointer}
.inp{width:100%;padding:14px;background:#eef2ff;border:0;border-radius:12px;margin-bottom:12px;font-size:15px;outline:0}
.btn-green{width:100%;padding:15px;background:#0ca694;border:0;border-radius:12px;color:#fff;font-weight:700;font-size:16px;cursor:pointer}
#app{display:flex;flex-direction:column;height:100vh;display:none}
.header{background:#075E54;padding:12px 14px;color:#fff;display:flex;align-items:center;gap:10px}
.header b{font-size:19px}
#list{flex:1;overflow-y:auto;background:#fff}
.chat-row{display:flex;gap:12px;padding:12px 14px;border-bottom:1px solid #f0f0f0;cursor:pointer}
.chat-row img{width:52px;height:52px;border-radius:50%;object-fit:cover}
.chat-row:active{background:#f5f5f5}
#chatPage{position:fixed;inset:0;background:#ECE5DD;z-index:50;display:none;flex-direction:column}
#chatPage.show{display:flex}
#chatHeader{background:#f0f2f5;padding:10px 12px;display:flex;align-items:center;gap:10px;border-bottom:1px solid #ddd}
#messages{flex:1;overflow-y:auto;padding:12px;display:flex;flex-direction:column;gap:6px;background-image:url('https://user-images.githubusercontent.com/15075759/28719144-86dc0f70-73b1-11e7-911d-60d70fcded21.png');background-size:contain}
.bubble{max-width:75%;padding:8px 12px;border-radius:8px;font-size:14.5px;position:relative;box-shadow:0 1px 1px rgba(0,0,0,.1)}
.me{align-self:flex-end;background:#d9fdd3;border-top-right-radius:2px}
.other{align-self:flex-start;background:#fff;border-top-left-radius:2px}
.time{font-size:10px;color:#667781;float:right;margin-left:8px;margin-top:6px}
#inputBar{padding:6px 8px;background:#f0f2f5;display:flex;align-items:center;gap:6px}
#inputBar input{flex:1;padding:12px 16px;border-radius:24px;border:0;outline:0;font-size:15px}
.circle{width:44px;height:44px;border-radius:50%;border:0;background:#00a884;color:#fff;display:flex;align-items:center;justify-content:center;cursor:pointer}
#mic.rec{background:red}
</style></head><body>

<div id="login">
<div class="card">
<img id="preview" class="pro" src="https://i.pravatar.cc/150?u=krest">
<input type="file" id="file" accept="image/*" style="display:none">
<button class="btn-gray" onclick="file.click()">📷 Gallery</button>
<input id="name" class="inp" placeholder="Your name" value="KREST">
<input id="phone" class="inp" placeholder="Phone 0911..." value="09114701914">
<button class="btn-green" onclick="enterApp()">Continue</button>
</div>
</div>

<div id="app">
<div class="header"><b>WhatsApp</b><div style="margin-left:auto;display:flex;gap:18px"><i class="fa fa-search"></i><i class="fa fa-ellipsis-v"></i></div></div>
<div style="display:flex;background:#fff;border-bottom:1px solid #eee"><div style="flex:1;text-align:center;padding:12px;border-bottom:3px solid #075E54;color:#075E54;font-weight:700">CHATS</div><div style="flex:1;text-align:center;padding:12px;color:#888">GROUPS</div><div style="flex:1;text-align:center;padding:12px;color:#888">CALLS</div></div>
<div id="list"></div>
<div style="position:fixed;bottom:18px;right:18px;width:56px;height:56px;background:#00a884;border-radius:50%;display:flex;align-items:center;justify-content:center;color:#fff;font-size:22px;cursor:pointer" onclick="newPrivate()"><i class="fa fa-comment"></i></div>
</div>

<div id="chatPage">
<div id="chatHeader"><i class="fa fa-arrow-left" onclick="chatPage.classList.remove('show')" style="padding:8px;cursor:pointer"></i><img id="cImg" src="https://i.pravatar.cc/100?img=12" style="width:38px;height:38px;border-radius:50%"><div><b id="cName">GLOBAL GROUP</b><br><small id="cSub" style="color:#667781">tap here for info</small></div></div>
<div id="messages"></div>
<div id="inputBar">
<button class="circle" id="micBtn"><i class="fa fa-microphone"></i></button>
<input id="msgInput" placeholder="Message">
<button class="circle" onclick="sendMsg()" style="background:#00a884"><i class="fa fa-paper-plane"></i></button>
</div>
</div>

<script>
let myName="", myPhone="", myImg="", current="GLOBAL GROUP", isPrivate=false, recording=false, mediaRec, chunks=[];
const preview=document.getElementById('preview');
document.getElementById('file').addEventListener('change', e=>{
 let f=e.target.files[0]; if(!f) return;
 let r=new FileReader(); r.onload=ev=>{ myImg=ev.target.result; preview.src=myImg; }; r.readAsDataURL(f);
});
function enterApp(){
 myName=document.getElementById('name').value.trim()||"KREST";
 myPhone=document.getElementById('phone').value.trim()||"09114701914";
 if(!myImg) myImg=preview.src;
 localStorage.setItem('wa_name',myName); localStorage.setItem('wa_phone',myPhone); localStorage.setItem('wa_img',myImg);
 document.getElementById('login').style.display='none';
 document.getElementById('app').style.display='flex';
 start();
}
// auto login if saved
let sn=localStorage.getItem('wa_name');
if(sn){ myName=sn; myPhone=localStorage.getItem('wa_phone'); myImg=localStorage.getItem('wa_img'); preview.src=myImg; document.getElementById('login').style.display='none'; document.getElementById('app').style.display='flex'; start(); }

function newPrivate(){
 let p=prompt('Enter phone number to chat (e.g 081...)');
 if(!p) return; current=p; isPrivate=true;
 document.getElementById('cName').innerText=p; document.getElementById('cImg').src='https://i.pravatar.cc/100?u='+p;
 document.getElementById('chatPage').classList.add('show'); loadMessages();
}

function openChat(name, img, priv){
 current=name; isPrivate=priv;
 document.getElementById('cName').innerText=name;
 document.getElementById('cImg').src=img;
 document.getElementById('chatPage').classList.add('show');
 loadMessages();
}

async function loadMessages(){
 let url = isPrivate? '/api/private?chat='+encodeURIComponent(current)+'&me='+myPhone : '/api/chat?chat='+encodeURIComponent(current);
 let res = await fetch(url); let data = await res.json();
 let box=document.getElementById('messages'); box.innerHTML='';
 data.forEach(m=>{
  let d=document.createElement('div'); d.className='bubble '+(m.me?'me':'other');
  if(m.audio){ d.innerHTML=m.text+'<br><audio controls src="'+m.audio+'" style="width:160px"></audio><span class="time">'+m.time+'</span>'; }
  else{ d.innerHTML=m.text+'<span class="time">'+m.time+'</span>'; }
  box.appendChild(d);
 });
 box.scrollTop=box.scrollHeight;
 renderList(data.all||[]);
}

function renderList(extra){
 let list=document.getElementById('list');
 // Keep it simple WhatsApp look
 fetch('/api/all?me='+myPhone).then(r=>r.json()).then(all=>{
  list.innerHTML='';
  all.forEach(c=>{
   let row=document.createElement('div'); row.className='chat-row';
   row.innerHTML='<img src="'+c.img+'"><div style="flex:1"><div style="font-weight:600;display:flex;justify-content:space-between"><span>'+c.name+'</span><span style="font-size:11px;color:#667781">'+c.time+'</span></div><div style="font-size:13px;color:#667781;white-space:nowrap;overflow:hidden;text-overflow:ellipsis">'+c.last+'</div></div>';
   row.onclick=()=>openChat(c.name, c.img, c.priv);
   list.appendChild(row);
  });
 });
}

async function sendMsg(){
 let inp=document.getElementById('msgInput'); let t=inp.value.trim(); if(!t) return; inp.value='';
 let url = isPrivate?'/api/private':'/api/chat';
 await fetch(url,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({chat:current,user:myName,phone:myPhone,text:t})});
 loadMessages();
}
document.getElementById('msgInput').addEventListener('keydown', e=>{ if(e.key==='Enter') sendMsg(); });

// Mic feature 🎙
document.getElementById('micBtn').addEventListener('click', async ()=>{
 let btn=document.getElementById('micBtn');
 if(!recording){
  try{
   let stream=await navigator.mediaDevices.getUserMedia({audio:true});
   mediaRec=new MediaRecorder(stream); chunks=[];
   mediaRec.ondataavailable=e=>{ if(e.data.size>0) chunks.push(e.data); };
   mediaRec.onstop=async()=>{
    let blob=new Blob(chunks,{type:'audio/webm'});
    let reader=new FileReader();
    reader.onload=async()=>{
     let url=isPrivate?'/api/private':'/api/chat';
     await fetch(url,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({chat:current,user:myName,phone:myPhone,text:'🎙 Voice',audio:reader.result})});
     loadMessages();
    };
    reader.readAsDataURL(blob);
   };
   mediaRec.start(); recording=true; btn.classList.add('rec'); btn.innerHTML='<i class="fa fa-stop"></i>';
  }catch{ alert('Allow mic'); }
 }else{
  mediaRec.stop(); recording=false; btn.classList.remove('rec'); btn.innerHTML='<i class="fa fa-microphone"></i>';
 }
});

function start(){ loadMessages(); setInterval(()=>{ if(document.getElementById('chatPage').classList.contains('show')) loadMessages(); else renderList(); },2500); }
</script></body></html>
"""

@app.route('/')
def home():
    return HTML

@app.route('/ping')
def ping():
    return 'ok', 200

@app.route('/api/chat', methods=['GET','POST'])
def chat():
    if request.method == 'GET':
        name = request.args.get('chat','GLOBAL GROUP')
        with lock:
            msgs = CHATS.get(name, [])
            out=[]
            for m in msgs[-100:]:
                out.append({"text":m['text'],"time":m['time'],"me":False,"audio":m.get('audio')})
            return jsonify(out)
    else:
        d=request.json
        name=d.get('chat','GLOBAL GROUP')
        with lock:
            if name not in CHATS: CHATS[name]=[]
            CHATS[name].append({"user":d['user'],"text":d['text'],"time":datetime.now().strftime("%H:%M"),"audio":d.get('audio')})
        return jsonify(ok=True)

@app.route('/api/private', methods=['GET','POST'])
def private_chat():
    if request.method == 'GET':
        chat = request.args.get('chat','')
        me = request.args.get('me','')
        key = "_".join(sorted([me, chat])) if me and chat else chat
        with lock:
            msgs = PRIVATE.get(key, [])
            out=[]
            for m in msgs[-100:]:
                out.append({"text":m['text'],"time":m['time'],"me": m.get('phone')==me, "audio":m.get('audio')})
            return jsonify(out)
    else:
        d=request.json
        chat=d.get('chat','')
        me=d.get('phone','')
        key = "_".join(sorted([me, chat]))
        with lock:
            if key not in PRIVATE: PRIVATE[key]=[]
            PRIVATE[key].append({"user":d['user'],"phone":d['phone'],"text":d['text'],"time":datetime.now().strftime("%H:%M"),"audio":d.get('audio')})
        return jsonify(ok=True)

@app.route('/api/all')
def all_chats():
    me=request.args.get('me','')
    with lock:
        result=[]
        # Global always first
        if CHATS.get("GLOBAL GROUP"):
            last=CHATS["GLOBAL GROUP"][-1]
            result.append({"name":"🌍 GLOBAL GROUP","last":last['text'],"time":last['time'],"img":"https://i.pravatar.cc/100?img=12","priv":False})
        for k,v in PRIVATE.items():
            if me in k and v:
                other=k.replace(me,"").replace("_","")
                if not other: continue
                result.append({"name":other,"last":v[-1]['text'],"time":v[-1]['time'],"img":f"https://i.pravatar.cc/100?u={other}","priv":True})
        # Also global chats
        for k,v in CHATS.items():
            if k!="GLOBAL GROUP" and v:
                result.append({"name":k,"last":v[-1]['text'],"time":v[-1]['time'],"img":f"https://i.pravatar.cc/100?img={len(k)}","priv":False})
        return jsonify(result)

if __name__ == '__main__':
    port=int(os.environ.get('PORT',10000))
    app.run(host='0.0.0.0', port=port)
