import os
import random
import time
import threading
from datetime import datetime
from flask import Flask
from flask import request
from flask import jsonify

app = Flask(__name__)
CHATS = {"GLOBAL GROUP": [{"user":"KREST","text":"Welcome to KRESTCHAT","time":"16:45"}]}
PRIVATE = {}
OTP_STORE = {}
ONLINE = {}
lock = threading.Lock()

HTML = """<!DOCTYPE html>
<html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>KRESTCHAT</title>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
<style>
*{margin:0;padding:0;box-sizing:border-box;font-family:Arial}
body{background:#fff;height:100vh;overflow:hidden}
#login{position:fixed;inset:0;background:#f6f6f6;z-index:999;display:flex;align-items:center;justify-content:center;padding:16px}
.card{width:100%;max-width:360px;background:#fff;border-radius:20px;box-shadow:0 10px 40px rgba(0,0,0,.15);padding:26px;text-align:center}
.inp{width:100%;padding:14px;background:#eef2ff;border:0;border-radius:12px;margin-bottom:12px;outline:0}
.btn{width:100%;padding:14px;background:#0ca694;border:0;border-radius:12px;color:#fff;font-weight:700;cursor:pointer}
#app{display:none;flex-direction:column;height:100vh}
.header{background:#075E54;padding:14px;color:#fff}
#list{flex:1;overflow-y:auto}
.row{display:flex;gap:12px;padding:14px;border-bottom:1px solid #f0f0f0;cursor:pointer;position:relative}
.row img{width:52px;height:52px;border-radius:50%;background:#ddd}
.on-dot{position:absolute;left:48px;top:42px;width:14px;height:14px;background:#00e676;border:2px solid #fff;border-radius:50%;display:none}
.on-dot.on{display:block}
.notif{position:absolute;right:14px;top:18px;background:#25D366;color:#fff;font-size:12px;font-weight:bold;min-width:22px;height:22px;border-radius:11px;display:flex;align-items:center;justify-content:center;display:none}
.notif.show{display:flex}
#chatPage{position:fixed;inset:0;background:#ECE5DD;z-index:50;display:none;flex-direction:column}
#chatPage.show{display:flex}
#chatHeader{background:#f0f2f5;padding:10px 12px;display:flex;align-items:center;gap:10px}
#onlineText{font-size:12px}
#onlineText.online{color:#0ca694}
#messages{flex:1;overflow-y:auto;padding:12px;display:flex;flex-direction:column;gap:6px}
.bubble{max-width:75%;padding:8px 12px;border-radius:8px;font-size:14px}
.me{align-self:flex-end;background:#d9fdd3}
.other{align-self:flex-start;background:#fff}
.time{font-size:10px;color:#667781;float:right;margin-left:8px;margin-top:6px}
#inputBar{padding:6px 8px;background:#f0f2f5;display:flex;gap:6px}
#inputBar input{flex:1;padding:12px 16px;border-radius:24px;border:0;outline:0}
.circle{width:44px;height:44px;border-radius:50%;border:0;background:#00a884;color:#fff;display:flex;align-items:center;justify-content:center;cursor:pointer}
</style></head><body>
<div id="login">
<div class="card" id="s1">
<h2 style="color:#075E54">KRESTCHAT</h2>
<p style="font-size:11px;color:#666;margin:8px 0">Green dot = online | Red dot = new message</p>
<input id="name" class="inp" placeholder="Your name" value="KREST">
<input id="phone" class="inp" placeholder="Phone e.g 09114701914">
<button class="btn" onclick="sendOTP()">Send OTP</button>
<div id="e1" style="color:red;font-size:12px;margin-top:8px"></div>
</div>
<div class="card" id="s2" style="display:none">
<h3>Enter OTP</h3>
<div style="background:#eef2ff;padding:14px;border-radius:10px;margin:12px 0">OTP: <b id="showOTP" style="font-size:26px;color:#0ca694"></b></div>
<input id="otpInput" class="inp" placeholder="Enter OTP">
<button class="btn" onclick="verifyOTP()">Verify</button>
<div id="e2" style="color:red;font-size:12px;margin-top:8px"></div>
</div>
</div>
<div id="app">
<div class="header"><b>KRESTCHAT</b></div>
<div style="background:#fff;padding:10px;text-align:center;border-bottom:1px solid #eee;color:#075E54;font-weight:700">CHATS</div>
<div id="list"></div>
<div style="position:fixed;bottom:18px;right:18px;width:56px;height:56px;background:#00a884;border-radius:50%;display:flex;align-items:center;justify-content:center;color:#fff;font-size:22px;cursor:pointer" onclick="newP()"><i class="fa fa-comment"></i></div>
</div>
<div id="chatPage">
<div id="chatHeader">
<i class="fa fa-arrow-left" onclick="closeC()" style="padding:8px;cursor:pointer"></i>
<img id="cImg" src="https://i.pravatar.cc/100?img=12" style="width:38px;height:38px;border-radius:50%">
<div style="margin-left:6px"><b id="cName">GLOBAL GROUP</b><div id="onlineText" class="offline">offline</div></div>
</div>
<div id="messages"></div>
<div id="inputBar">
<input id="msgInput" placeholder="Message">
<button class="circle" onclick="sendM()"><i class="fa fa-paper-plane"></i></button>
</div>
</div>
<script>
let myName="",myPhone="",current="GLOBAL GROUP",isPrivate=false,lastCounts={},onlineMap={};
async function sendOTP(){myName=document.getElementById('name').value.trim()||"KREST";myPhone=document.getElementById('phone').value.trim();if(myPhone.length<10){document.getElementById('e1').innerText='Enter phone';return;}let r=await fetch('/api/send_otp',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({phone:myPhone})});let d=await r.json();document.getElementById('showOTP').innerText=d.otp;document.getElementById('s1').style.display='none';document.getElementById('s2').style.display='block';}
async function verifyOTP(){let c=document.getElementById('otpInput').value.trim();let r=await fetch('/api/verify_otp',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({phone:myPhone,otp:c})});let d=await r.json();if(!d.ok){document.getElementById('e2').innerText=d.error;return;}localStorage.setItem('wa_name',myName);localStorage.setItem('wa_phone',myPhone);document.getElementById('login').style.display='none';document.getElementById('app').style.display='flex';start();}
let sn=localStorage.getItem('wa_name');if(sn){myName=sn;myPhone=localStorage.getItem('wa_phone');document.getElementById('login').style.display='none';document.getElementById('app').style.display='flex';start();}
function closeC(){document.getElementById('chatPage').classList.remove('show');renderL();}
function newP(){let p=prompt('Enter phone');if(!p)return;current=p;isPrivate=true;document.getElementById('cName').innerText=p;document.getElementById('cImg').src='https://i.pravatar.cc/100?u='+p;document.getElementById('chatPage').classList.add('show');upH();loadM();}
function openC(n,i,p){current=n;isPrivate=p;document.getElementById('cName').innerText=n;document.getElementById('cImg').src=i;document.getElementById('chatPage').classList.add('show');if(lastCounts[n])lastCounts[n]=null;upH();loadM();}
function upH(){let e=document.getElementById('onlineText');if(!isPrivate){e.innerText='Everyone online';e.className='online';return;}if(onlineMap[current]){e.innerText='online';e.className='online';}else{e.innerText='offline';e.className='offline';}}
async function beat(){if(!myPhone)return;await fetch('/api/online',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({phone:myPhone})});let r=await fetch('/api/online_status');onlineMap=await r.json();upH();document.querySelectorAll('.row').forEach(row=>{let name=row.dataset.name;let dot=row.querySelector('.on-dot');if(dot){if(onlineMap[name])dot.classList.add('on');else dot.classList.remove('on');}});}
async function loadM(){let u=isPrivate?'/api/private?chat='+encodeURIComponent(current)+'&me='+myPhone:'/api/chat?chat='+encodeURIComponent(current);let r=await fetch(u);let d=await r.json();let b=document.getElementById('messages');b.innerHTML='';d.forEach(m=>{let dv=document.createElement('div');dv.className='bubble '+(m.me?'me':'other');dv.innerHTML=m.text+'<span class="time">'+m.time+'</span>';b.appendChild(dv);});b.scrollTop=b.scrollHeight;if(isPrivate)lastCounts[current]=d.length;}
async function renderL(){let r=await fetch('/api/all?me='+myPhone);let all=await r.json();let ro=await fetch('/api/online_status');onlineMap=await ro.json();let list=document.getElementById('list');list.innerHTML='';all.forEach(c=>{let unread=0;if(lastCounts[c.name]!==undefined&&lastCounts[c.name]!==null){let diff=c.count-lastCounts[c.name];if(diff>0&&c.name!==current)unread=diff;}else if(lastCounts[c.name]===undefined){lastCounts[c.name]=c.count;}let row=document.createElement('div');row.className='row';row.dataset.name=c.name;let oc=onlineMap[c.name]?'on':'';let ns=unread>0?'show':'';row.innerHTML='<div style="position:relative"><img src="'+c.img+'"><div class="on-dot '+oc+'"></div></div><div style="flex:1;overflow:hidden"><div style="font-weight:600;display:flex;justify-content:space-between"><span>'+c.name+'</span><span style="font-size:11px;color:#667781">'+c.time+'</span></div><div style="font-size:13px;color:#667781;white-space:nowrap;overflow:hidden;text-overflow:ellipsis">'+c.last+'</div></div><div class="notif '+ns+'">'+(unread>9?'9+':unread)+'</div>';row.onclick=()=>openC(c.name,c.img,c.priv);list.appendChild(row);});}
async function sendM(){let inp=document.getElementById('msgInput');let t=inp.value.trim();if(!t)return;inp.value='';let url=isPrivate?'/api/private':'/api/chat';await fetch(url,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({chat:current,user:myName,phone:myPhone,text:t})});loadM();}
document.getElementById('msgInput').addEventListener('keydown',e=>{if(e.key==='Enter')sendM();});
function start(){renderL();beat();setInterval(()=>{if(document.getElementById('chatPage').classList.contains('show'))loadM();else renderL();},2500);setInterval(beat,4000);}
</script></body></html>
"""

@app.route('/')
def home():
    return HTML

@app.route('/api/send_otp', methods=['POST'])
def send_otp():
    phone = request.json.get('phone', '').strip()
    code = str(random.randint(100000, 999999))
    with lock:
        OTP_STORE[phone] = code
    return jsonify(ok=True, otp=code)

@app.route('/api/verify_otp', methods=['POST'])
def verify_otp():
    d = request.json
    phone = d.get('phone')
    otp = d.get('otp')
    with lock:
        real = OTP_STORE.get(phone)
        if not real or real!= otp:
            return jsonify(ok=False, error="Wrong! Correct is " + str(real))
        OTP_STORE.pop(phone, None)
    return jsonify(ok=True)

@app.route('/api/online', methods=['POST'])
def online():
    phone = request.json.get('phone', '')
    with lock:
        ONLINE[phone] = time.time()
    return jsonify(ok=True)

@app.route('/api/online_status')
def online_status():
    now = time.time()
    with lock:
        result = {}
        for p, t in ONLINE.items():
            if now - t < 30:
                result[p] = True
        return jsonify(result)

@app.route('/api/chat', methods=['GET', 'POST'])
def chat():
    if request.method == 'GET':
        name = request.args.get('chat', 'GLOBAL GROUP')
        with lock:
            msgs = CHATS.get(name, [])
            data = []
            for m in msgs[-100:]:
                data.append({"text": m['text'], "time": m['time'], "me": False})
            return jsonify(data)
    else:
        d = request.json
        name = d.get('chat', 'GLOBAL GROUP')
        with lock:
            if name not in CHATS:
                CHATS[name] = []
            CHATS[name].append({"user": d['user'], "text": d['text'], "time": datetime.now().strftime("%H:%M")})
        return jsonify(ok=True)

@app.route('/api/private', methods=['GET', 'POST'])
def private_chat():
    if request.method == 'GET':
        chat = request.args.get('chat', '')
        me = request.args.get('me', '')
        key = "_".join(sorted([me, chat])) if me and chat else chat
        with lock:
            msgs = PRIVATE.get(key, [])
            data = []
            for m in msgs[-100:]:
                data.append({"text": m['text'], "time": m['time'], "me": m.get('phone') == me})
            return jsonify(data)
    else:
        d = request.json
        chat = d.get('chat', '')
        me = d.get('phone', '')
        key = "_".join(sorted([me, chat]))
        with lock:
            if key not in PRIVATE:
                PRIVATE[key] = []
            PRIVATE[key].append({"user": d['user'], "phone": d['phone'], "text": d['text'], "time": datetime.now().strftime("%H:%M")})
        return jsonify(ok=True)

@app.route('/api/all')
def all_chats():
    me = request.args.get('me', '')
    with lock:
        res = []
        if CHATS.get("GLOBAL GROUP"):
            last = CHATS["GLOBAL GROUP"][-1]
            res.append({"name": "GLOBAL GROUP", "last": last['text'], "time": last['time'], "img": "https://i.pravatar.cc/100?img=12", "priv": False, "count": len(CHATS["GLOBAL GROUP"])})
        for k, v in PRIVATE.items():
            if me in k and v:
                other = k.replace(me, "").replace("_", "")
                if other:
                    res.append({"name": other, "last": v[-1]['text'], "time": v[-1]['time'], "img": "https://i.pravatar.cc/100?u=" + other, "priv": True, "count": len(v)})
        return jsonify(res)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
