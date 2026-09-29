 import os 
from flask import Flask, request, jsonify
from datetime import datetime
import threading, random, time

app = Flask(__name__)
CHATS = {"GLOBAL GROUP": [{"user":"KREST","text":"🌍 Global Group - see who is online!","time":"21:15"}]}
PRIVATE = {}
OTP_STORE = {}
ONLINE = {}
lock = threading.Lock()

HTML = """
<!DOCTYPE html>
<html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>WhatsApp</title>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
<script src="https://accounts.google.com/gsi/client" async defer></script>
<style>
*{margin:0;padding:0;box-sizing:border-box;font-family:Arial}
body{background:#fff;height:100vh;overflow:hidden}
#login{position:fixed;inset:0;background:#f6f6f6;z-index:1000;display:flex;align-items:center;justify-content:center;padding:16px}
.card{width:100%;max-width:360px;background:#fff;border-radius:20px;box-shadow:0 10px 40px rgba(0,0,0,.15);padding:26px;text-align:center}
.inp{width:100%;padding:14px;background:#eef2ff;border:0;border-radius:12px;margin-bottom:12px;font-size:15px;outline:0}
.btn-green{width:100%;padding:14px;background:#0ca694;border:0;border-radius:12px;color:#fff;font-weight:700;font-size:16px;cursor:pointer}
#noData{position:fixed;inset:0;background:#111b21;z-index:2000;display:none;flex-direction:column;align-items:center;justify-content:center;color:#fff;text-align:center;padding:24px}
#app{display:none;flex-direction:column;height:100vh}
.header{background:#075E54;padding:14px;color:#fff;display:flex;align-items:center}
#list{flex:1;overflow-y:auto;background:#fff}
.chat-row{display:flex;gap:12px;padding:14px;border-bottom:1px solid #f0f0f0;cursor:pointer;position:relative}
.chat-row img{width:52px;height:52px;border-radius:50%;background:#ddd}
.dot-online{position:absolute;left:48px;top:42px;width:14px;height:14px;background:#00e676;border:2px solid #fff;border-radius:50%;display:none}
.dot-online.on{display:block}
.dot-notif{position:absolute;right:14px;top:18px;background:#25D366;color:#fff;font-size:12px;font-weight:bold;min-width:22px;height:22px;border-radius:11px;display:flex;align-items:center;justify-content:center;padding:0 6px;display:none}
.dot-notif.show{display:flex}
#chatPage{position:fixed;inset:0;background:#ECE5DD;z-index:50;display:none;flex-direction:column}
#chatPage.show{display:flex}
#chatHeader{background:#f0f2f5;padding:10px 12px;display:flex;align-items:center;gap:10px}
#onlineText{font-size:12px}
#onlineText.online{color:#0ca694}
#onlineText.offline{color:#888}
#messages{flex:1;overflow-y:auto;padding:12px;display:flex;flex-direction:column;gap:6px;background:#e5ddd5}
.bubble{max-width:75%;padding:8px 12px;border-radius:8px;font-size:14.5px;box-shadow:0 1px 1px rgba(0,0,0,.1)}
.me{align-self:flex-end;background:#d9fdd3}
.other{align-self:flex-start;background:#fff}
.time{font-size:10px;color:#667781;float:right;margin-left:8px;margin-top:6px}
#inputBar{padding:6px 8px;background:#f0f2f5;display:flex;gap:6px;align-items:center}
#inputBar input{flex:1;padding:12px 16px;border-radius:24px;border:0;outline:0}
.circle{width:44px;height:44px;border-radius:50%;border:0;background:#00a884;color:#fff;display:flex;align-items:center;justify-content:center;cursor:pointer}
#mic.rec{background:red}
</style></head><body>

<div id="noData">
<i class="fa fa-wifi" style="font-size:60px;color:#ff3b30;margin-bottom:16px"></i>
<h2>No Data</h2>
<p style="color:#bbb;margin:10px 0">Turn on mobile data to use app</p>
<button onclick="checkData()" style="padding:12px 24px;background:#0ca694;border:0;border-radius:20px;color:#fff;font-weight:bold;cursor:pointer">Retry</button>
</div>

<div id="login">
<div class="card" id="step1">
<h2 style="color:#075E54">WhatsApp</h2>
<p style="font-size:11px;color:#666;margin:6px 0 12px"><i class="fa fa-circle" style="color:#00e676"></i> Shows who is online</p>
<div id="g_id_onload" data-client_id="demo" data-callback="handleGoogle"></div>
<div class="g_id_signin" data-type="standard" data-size="large" data-theme="outline" data-text="signin_with" style="width:100%;margin-bottom:12px"></div>
<div style="color:#888;font-size:12px;margin:10px 0">OR</div>
<input id="name" class="inp" placeholder="Your name" value="KREST">
<input id="phone" class="inp" placeholder="Phone e.g 09114701914">
<button class="btn-green" onclick="sendOTP()">Send OTP</button>
<div id="e1" style="color:red;font-size:12px;margin-top:8px"></div>
</div>
<div class="card" id="step2" style="display:none">
<h3>Enter OTP</h3>
<p style="font-size:13px;color:#666;margin:8px 0">To <b id="vPhone"></b></p>
<div style="background:#eef2ff;padding:14px;border-radius:10px;margin:12px 0">OTP: <b id="showOTP" style="font-size:26px;color:#0ca694;letter-spacing:3px"></b></div>
<input id="otpInput" class="inp" placeholder="Enter OTP">
<button class="btn-green" onclick="verifyOTP()">Verify</button>
<div id="e2" style="color:red;font-size:12px;margin-top:8px"></div>
</div>
</div>

<div id="app">
<div class="header"><b>WhatsApp</b><span style="margin-left:8px;font-size:10px;background:#0ca694;padding:3px 8px;border-radius:10px"><i class="fa fa-circle" style="color:#00e676"></i> Online</span></div>
<div style="background:#fff;padding:10px;text-align:center;border-bottom:1px solid #eee;color:#075E54;font-weight:700">CHATS</div>
<div id="list"></div>
<div style="position:fixed;bottom:18px;right:18px;width:56px;height:56px;background:#00a884;border-radius:50%;display:flex;align-items:center;justify-content:center;color:#fff;font-size:22px;cursor:pointer" onclick="newPrivate()"><i class="fa fa-comment"></i></div>
</div>

<div id="chatPage">
<div id="chatHeader">
<i class="fa fa-arrow-left" onclick="closeChat()" style="padding:8px;cursor:pointer"></i>
<img id="cImg" src="https://i.pravatar.cc/100?img=12" style="width:38px;height:38px;border-radius:50%">
<div style="margin-left:6px"><b id="cName">GLOBAL GROUP</b><div id="onlineText" class="offline">offline</div></div>
</div>
<div id="messages"></div>
<div id="inputBar">
<button class="circle" id="micBtn"><i class="fa fa-microphone"></i></button>
<input id="msgInput" placeholder="Message">
<button class="circle" onclick="sendMsg()" style="background:#00a884"><i class="fa fa-paper-plane"></i></button>
</div>
</div>

<script>
let myName="", myPhone="", current="GLOBAL GROUP", isPrivate=false, recording=false, mediaRec, chunks=[], lastCounts={}, onlineMap={};

function checkData(){ if(!navigator.onLine){ document.getElementById('noData').style.display='flex'; return false; } document.getElementById('noData').style.display='none'; return true; }
window.addEventListener('online', checkData); window.addEventListener('offline', checkData); checkData();

function handleGoogle(r){ if(!checkData()) return; try{ let p=JSON.parse(atob(r.credential.split('.')[1])); myName=p.name; myPhone=p.email; localStorage.setItem('wa_name',myName); localStorage.setItem('wa_phone',myPhone); document.getElementById('login').style.display='none'; document.getElementById('app').style.display='flex'; start(); }catch{ alert('Use OTP'); } }
async function sendOTP(){ if(!checkData()) return; myName=document.getElementById('name').value.trim()||"KREST"; myPhone=document.getElementById('phone').value.trim(); if(myPhone.length<10){ document.getElementById('e1').innerText='Enter phone'; return; } let res=await fetch('/api/send_otp',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({phone:myPhone})}); let d=await res.json(); document.getElementById('vPhone').innerText=myPhone; document.getElementById('showOTP').innerText=d.otp; document.getElementById('step1').style.display='none'; document.getElementById('step2').style.display='block'; }
async function verifyOTP(){ let code=document.getElementById('otpInput').value.trim(); let res=await fetch('/api/verify_otp',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({phone:myPhone,otp:code})}); let d=await res.json(); if(!d.ok){ document.getElementById('e2').innerText=d.error; return; } localStorage.setItem('wa_name',myName); localStorage.setItem('wa_phone',myPhone); document.getElementById('login').style.display='none'; document.getElementById('app').style.display='flex'; start(); }
let sn=localStorage.getItem('wa_name'); if(sn){ myName=sn; myPhone=localStorage.getItem('wa_phone'); document.getElementById('login').style.display='none'; document.getElementById('app').style.display='flex'; start(); }

function closeChat(){ document.getElementById('chatPage').classList.remove('show'); renderList(); }
function newPrivate(){ if(!checkData()) return; let p=prompt('Enter phone to chat'); if(!p) return; current=p; isPrivate=true; document.getElementById('cName').innerText=p; document.getElementById('cImg').src='https://i.pravatar.cc/100?u='+p; document.getElementById('chatPage').classList.add('show'); updateHeader(); loadMessages(); }
function openChat(name,img,priv){ current=name; isPrivate=priv; document.getElementById('cName').innerText=name; document.getElementById('cImg').src=img; document.getElementById('chatPage').classList.add('show'); if(lastCounts[name]) lastCounts[name]=null; updateHeader(); loadMessages(); }

function updateHeader(){
 let el=document.getElementById('onlineText');
 if(!isPrivate){ el.innerText='Everyone can see online'; el.className='online'; return; }
 if(onlineMap[current]){ el.innerText='● online'; el.className='online'; } else { el.innerText='offline - last seen recently'; el.className='offline'; }
}
async function heartbeat(){
 if(!myPhone ||!checkData()) return;
 await fetch('/api/online',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({phone:myPhone})});
 let res=await fetch('/api/online_status'); onlineMap=await res.json(); updateHeader();
 document.querySelectorAll('.chat-row').forEach(row=>{
  let name=row.dataset.name; let dot=row.querySelector('.dot-online');
  if(dot){ if(onlineMap[name]) dot.classList.add('on'); else dot.classList.remove('on'); }
 });
}
async function loadMessages(){
 let url = isPrivate? '/api/private?chat='+encodeURIComponent(current)+'&me='+myPhone : '/api/chat?chat='+encodeURIComponent(current);
 let res=await fetch(url); let data=await res.json();
 let box=document.getElementById('messages'); box.innerHTML='';
 data.forEach(m=>{
  let d=document.createElement('div'); d.className='bubble '+(m.me?'me':'other');
  if(m.audio){ d.innerHTML=m.text+'<br><audio controls src="'+m.audio+'" style="width:160px"></audio><span class="time">'+m.time+'</span>'; }
  else{ d.innerHTML=m.text+'<span class="time">'+m.time+'</span>'; }
  box.appendChild(d);
 });
 box.scrollTop=box.scrollHeight; if(isPrivate) lastCounts[current]=data.length;
}
async function renderList(){
 let res=await fetch('/api/all?me='+myPhone); let all=await res.json();
 let resOn=await fetch('/api/online_status'); onlineMap=await resOn.json();
 let list=document.getElementById('list'); list.innerHTML='';
 all.forEach(c=>{
  let unread=0;
  if(lastCounts[c.name]!==undefined && lastCounts[c.name]!==null){ let diff=c.count - lastCounts[c.name]; if(diff>0 && c.name!==current) unread=diff; } else if(lastCounts[c.name]===undefined){ lastCounts[c.name]=c.count; }
  let row=document.createElement('div'); row.className='chat-row'; row.dataset.name=c.name;
  let onlineClass = onlineMap[c.name]? 'on' : '';
  let notifShow = unread>0? 'show' : '';
  row.innerHTML='<div style="position:relative"><img src="'+c.img+'"><div class="dot-online '+onlineClass+'"></div></div><div style="flex:1;overflow:hidden"><div style="font-weight:600;display:flex;justify-content:space-between"><span>'+c.name+'</span><span style="font-size:11px;color:#667781">'+c.time+'</span></div><div style="font-size:13px;color:#667781;white-space:nowrap;overflow:hidden;text-overflow:ellipsis">'+c.last+'</div></div><div class="dot-notif '+notifShow+'">'+(unread>9?'9+':unread)+'</div>';
  row.onclick=()=>openChat(c.name,c.img,c.priv);
  list.appendChild(row);
 });
}
async function sendMsg(){ if(!checkData()) return alert('Turn on data'); let inp=document.getElementById('msgInput'); let t=inp.value.trim(); if(!t) return; inp.value=''; let url=isPrivate?'/api/private':'/api/chat'; await fetch(url,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({chat:current,user:myName,phone:myPhone,text:t})}); loadMessages(); }
document.getElementById('msgInput').addEventListener('keydown', e=>{ if(e.key==='Enter') sendMsg(); });
document.getElementById('micBtn').addEventListener('click', async ()=>{
 if(!checkData()) return;
 let btn=document.getElementById('micBtn');
 if(!recording){ try{ let s=await navigator.mediaDevices.getUserMedia({audio:true}); mediaRec=new MediaRecorder(s); chunks=[]; mediaRec.ondataavailable=e=>{ if(e.data.size>0) chunks.push(e.data); }; mediaRec.onstop=async()=>{ let blob=new Blob(chunks,{type:'audio/webm'}); let reader=new FileReader(); reader.onload=async()=>{ let url=isPrivate?'/api/private':'/api/chat'; await fetch(url,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({chat:current,user:myName,phone:myPhone,text:'🎙 Voice',audio:reader.result})}); loadMessages(); }; reader.readAsDataURL(blob); }; mediaRec.start(); recording=true; btn.classList.add('rec'); btn.innerHTML='<i class="fa fa-stop"></i>'; }catch{ alert('Allow mic'); } } else { mediaRec.stop(); recording=false; btn.classList.remove('rec'); btn.innerHTML='<i class="fa fa-microphone"></i>'; }
});
function start(){ renderList(); heartbeat(); setInterval(()=>{ if(document.getElementById('chatPage').classList.contains('show')) loadMessages(); else renderList(); },2500); setInterval(heartbeat,4000); }
</script></body></html>
"""

@app.route('/')
def home(): return HTML
@app.route('/ping')
def ping(): return 'ok',200

@app.route('/api/send_otp', methods=['POST'])
def send_otp():
    phone=request.json.get('phone','').strip()
    code=str(random.randint(100000,999999))
    with lock: OTP_STORE[phone]=code
    return jsonify(ok=True, otp=code)

@app.route('/api/verify_otp', methods=['POST'])
def verify_otp():
    d=request.json; phone=d.get('phone'); otp=d.get('otp')
    with lock:
        real=OTP_STORE.get(phone)
        if not real or real!=otp: return jsonify(ok=False, error=f"Wrong! Correct is {real}")
        OTP_STORE.pop(phone,None)
    return jsonify(ok=True)

@app.route('/api/online', methods=['POST'])
def online():
    phone=request.json.get('phone','')
    with lock: ONLINE[phone]=time.time()
    return jsonify(ok=True)

@app.route('/api/online_status')
def online_status():
    now=time.time()
    with lock:
        result={p:True for p,t in ONLINE.items() if now-t < 30}
        return jsonify(result)

@app.route('/api/chat', methods=['GET','POST'])
def chat():
    if request.method=='GET':
        name=request.args.get('chat','GLOBAL GROUP')
        with lock:
            msgs=CHATS.get(name,[])
            return jsonify([{"text":m['text'],"time":m['time'],"me":False,"audio":m.get('audio')} for m in msgs[-100:]])
    else:
        d=request.json; name=d.get('chat','GLOBAL GROUP')
        with lock:
            if name not in CHATS: CHATS[name]=[]
            CHATS[name].append({"user":d['user'],"text":d['text'],"time":datetime.now().strftime("%H:%M"),"audio":d.get('audio')})
        return jsonify(ok=True)

@app.route('/api/private', methods=['GET','POST'])
def private_chat():
    if request.method=='GET':
        chat=request.args.get('chat',''); me=request.args.get('me','')
        key="_".join(sorted([me,chat])) if me and chat else chat
        with lock:
            msgs=PRIVATE.get(key,[])
            return jsonify([{"text":m['text'],"time":m['time'],"me":m.get('phone')==me,"audio":m.get('audio')} for m in msgs[-100:]])
    else:
        d=request.json; chat=d.get('chat',''); me=d.get('phone',''); key="_".join(sorted([me,chat]))
        with lock:
            if key not in PRIVATE: PRIVATE[key]=[]
            PRIVATE[key].append({"user":d['user'],"phone":d['phone'],"text":d['text'],"time":datetime.now().strftime("%H:%M"),"audio":d.get('audio')})
        return jsonify(ok=True)

@app.route('/api/all')
def all_chats():
    me=request.args.get('me','')
    with lock:
        res=[]
        if CHATS.get("GLOBAL GROUP"):
            last=CHATS["GLOBAL GROUP"][-1]
            res.append({"name":"GLOBAL GROUP","last":last['text'],"time":last['time'],"img":"https://i.pravatar.cc/100?img=12","priv":False,"count":len(CHATS["GLOBAL GROUP"])})
        for k,v in PRIVATE.items():
            if me in k and v:
                other=k.replace(me,"").replace("_","")
                if other: res.append({"name":other,"last":v[-1]['text'],"time":v[-1]['time'],"img":f"https://i.pravatar.cc/100?u={other}","priv":True,"count":len(v)})
        return jsonify(res)

if __name__=='__main__':
    port=int(os.environ.get('PORT',10000))
    app.run(host='0.0.0.0', port=port)
