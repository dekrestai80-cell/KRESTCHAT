import os
from flask import Flask, request, jsonify
from datetime import datetime
import threading, random

app = Flask(__name__)

GROUPS = {"global": [{"user":"KREST ADMIN","num":"000","text":"🌍 GLOBAL GROUP - Everybody join and talk! ⚡","time":"20:00","type":"text"}]}
PRIVATE = {}
PROFILES = {}
OTP = {}
lock = threading.Lock()

HTML_PAGE = """
<!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>KREST CHAT X</title>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
<style>
*{margin:0;padding:0;box-sizing:border-box;font-family:Arial}
body{background:#fff;height:100vh;overflow:hidden}
#side{width:100%;height:100vh;display:flex;flex-direction:column}
.top{padding:14px;border-bottom:1px solid #ddd;display:flex;justify-content:space-between}
#chatList{flex:1;overflow-y:auto;padding-bottom:90px}
.row{display:flex;gap:12px;padding:12px;border-bottom:1px solid #f5f6f6;cursor:pointer}
.row img{width:48px;height:48px;border-radius:50%}
.global{background:#e7f8e8;border-left:4px solid #00a884}
#main{position:fixed;inset:0;background:#efeae2;z-index:50;display:none;flex-direction:column}
#main.show{display:flex}
#mHead{padding:10px;background:#f0f2f5;display:flex;gap:10px;align-items:center}
#msgs{flex:1;overflow-y:auto;padding:12px;display:flex;flex-direction:column;gap:8px}
.bubble{max-width:78%;padding:8px 10px;border-radius:10px;font-size:14px}
.me{align-self:flex-end;background:#d9fdd3}
.other{align-self:flex-start;background:#fff}
#inputArea{padding:8px;background:#f0f2f5;display:flex;gap:8px;align-items:center}
#inputArea input{flex:1;padding:12px;border-radius:20px;border:0;outline:0}
#inputArea button{width:44px;height:44px;border-radius:50%;border:0;background:#00a884;color:#fff;display:flex;align-items:center;justify-content:center;cursor:pointer}
#micBtn{background:#111b21}
#micBtn.rec{background:#ff3b30;animation:pulse 1s infinite}
@keyframes pulse{0%{transform:scale(1)}50%{transform:scale(1.2)}100%{transform:scale(1)}}
#login{position:fixed;inset:0;background:#fff;z-index:100;display:flex;align-items:center;justify-content:center;padding:16px}
.box{padding:20px;border-radius:16px;width:100%;max-width:360px;box-shadow:0 10px 30px rgba(0,0,0,.2);text-align:center}
.box input{width:100%;padding:12px;border-radius:8px;border:1px solid #ddd;margin:6px 0}
.box button{width:100%;padding:12px;background:#00a884;border:0;border-radius:8px;color:#fff;font-weight:bold;margin-top:8px}
.prev{width:90px;height:90px;border-radius:50%;border:3px solid #00a884;margin:0 auto 10px;display:block}
</style></head><body>
<div id="login"><div class="box" id="b1"><img id="prev" class="prev" src="https://i.pravatar.cc/150?u=krest"><input type="file" id="pf" accept="image/*" style="display:none"><button onclick="pf.click()" style="background:#f0f2f5;color:#000;border:1px solid #ddd">📷 Gallery</button><input id="myName" placeholder="Your Name"><input id="myNumber" placeholder="08146096232"><button onclick="sendOTP()">Continue</button><div id="e1" style="color:red;font-size:12px"></div></div><div class="box" id="b2" style="display:none"><h3>Verify</h3><p>To <b id="vNum"></b></p><div style="background:#f0f2f5;padding:10px;margin:10px 0">OTP: <b id="dOTP" style="font-size:24px;color:#00a884"></b></div><input id="otpIn" placeholder="Enter OTP"><button onclick="verifyOTP()">Verify</button><div id="e2" style="color:red;font-size:12px"></div></div></div>
<div id="side"><div class="top"><b>KREST CHAT X</b><span style="color:#00a884;font-size:12px">● LIVE</span></div><div id="chatList"></div><div style="position:fixed;bottom:20px;right:16px;width:56px;height:56px;background:#111b21;border-radius:16px;display:flex;align-items:center;justify-content:center;color:#fff;cursor:pointer" onclick="newChat()"><i class="fa fa-plus"></i></div></div>
<div id="main"><div id="mHead"><i class="fa fa-arrow-left" onclick="main.classList.remove('show')" style="padding:8px"></i><img id="cImg" src="https://i.pravatar.cc/100?img=12" style="width:36px;height:36px;border-radius:50%"><div><b id="cName">GLOBAL GROUP</b><br><small>Everybody can talk</small></div></div><div id="msgs"></div><div id="inputArea"><button id="micBtn" onclick="toggleMic()"><i class="fa fa-microphone"></i></button><input id="msgIn" placeholder="Message" onkeydown="if(event.key==='Enter')sendMsg()"><button onclick="sendMsg()"><i class="fa fa-paper-plane"></i></button></div></div>
<script>
let myName="",myNumber="",pB64="",curRoom="global",isPriv=false,allChats=[],mediaRec,chunks=[],recording=false;
pf.addEventListener('change',e=>{let f=e.target.files[0];if(!f)return;let r=new FileReader();r.onload=ev=>{pB64=ev.target.result;prev.src=pB64};r.readAsDataURL(f)});
async function sendOTP(){myName=myNameEl.value.trim();myNumber=myNumberEl.value.trim();if(!myName||myNumber.length!=11)return e1.textContent="Name + 11 digits";if(!pB64)pB64=prev.src;let res=await fetch('/api/send_otp',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({number:myNumber})});let d=await res.json();vNum.textContent=myNumber;dOTP.textContent=d.otp;b1.style.display='none';b2.style.display='block';}
async function verifyOTP(){let code=otpIn.value.trim();let res=await fetch('/api/verify_otp',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({number:myNumber,otp:code,name:myName,img:pB64})});let d=await res.json();if(!d.ok)return e2.textContent=d.error;localStorage.setItem('kName',myName);localStorage.setItem('kNum',myNumber);localStorage.setItem('kImg',pB64);login.style.display='none';start();}
const myNameEl=document.getElementById('myName'),myNumberEl=document.getElementById('myNumber'),otpIn=document.getElementById('otpIn'),login=document.getElementById('login'),main=document.getElementById('main'),prev=document.getElementById('prev'),pf=document.getElementById('pf');
let sn=localStorage.getItem('kName'),snum=localStorage.getItem('kNum'),si=localStorage.getItem('kImg');if(sn&&snum){myName=sn;myNumber=snum;pB64=si;prev.src=pB64;login.style.display='none';start();}
function getKey(a,b){return [a,b].sort().join('_');}
function newChat(){let num=prompt('Enter phone 081...');if(!num||num.length!=11)return;curRoom=getKey(myNumber,num);isPriv=true;cName.textContent=num;cImg.src='https://i.pravatar.cc/100?u='+num;main.classList.add('show');load();}
function openChat(k,priv,name,img){curRoom=k;isPriv=priv;cName.textContent=name;cImg.src=img;main.classList.add('show');load();}
async function toggleMic(){let btn=document.getElementById('micBtn');if(!recording){try{let s=await navigator.mediaDevices.getUserMedia({audio:true});mediaRec=new MediaRecorder(s);chunks=[];mediaRec.ondataavailable=e=>{if(e.data.size>0)chunks.push(e.data)};mediaRec.onstop=async()=>{let blob=new Blob(chunks,{type:'audio/webm'});let r=new FileReader();r.onload=async()=>{await fetch(isPriv?'/api/private':'/api/groups',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({key:curRoom,room:curRoom,user:myName,num:myNumber,text:'Voice note',audio:r.result,type:'audio'})});load();};r.readAsDataURL(blob);};mediaRec.start();recording=true;btn.classList.add('rec');btn.innerHTML='<i class="fa fa-stop"></i>';}catch{alert('Allow mic');}}else{mediaRec.stop();recording=false;btn.classList.remove('rec');btn.innerHTML='<i class="fa fa-microphone"></i>';}}
async function load(){let url=isPriv?'/api/private?key='+curRoom+'&me='+myNumber:'/api/groups?room='+curRoom+'&me='+myNumber;let res=await fetch(url);let data=await res.json();msgs.innerHTML='';data.messages.forEach(m=>{let d=document.createElement('div');d.className='bubble '+(m.num==myNumber?'me':'other');if(m.type=='audio'){d.innerHTML='<b style="font-size:11px">'+m.user+'</b><br><audio controls src="'+m.audio+'" style="width:180px"></audio><div style="font-size:10px;float:right">'+m.time+'</div>';}else{d.innerHTML='<b style="font-size:11px">'+m.user+'</b><br>'+m.text+'<div style="font-size:10px;float:right">'+m.time+'</div>';}msgs.appendChild(d);});msgs.scrollTop=msgs.scrollHeight;allChats=data.all_chats;render();}
function render(){chatList.innerHTML='';let g=allChats.find(c=>c.key=='global')||{key:'global',display:'GLOBAL GROUP',last:'Everybody can join!',img:'https://i.pravatar.cc/100?img=12',time:'Live'};let row=document.createElement('div');row.className='row global';row.innerHTML='<img src="'+g.img+'"><div><b>🌍 '+g.display+'</b><div style="font-size:13px;color:#555">'+g.last+'</div></div>';row.onclick=()=>openChat('global',false,'GLOBAL GROUP','https://i.pravatar.cc/100?img=12');chatList.appendChild(row);allChats.forEach(c=>{if(c.key=='global')return;let r=document.createElement('div');r.className='row';r.innerHTML='<img src="'+c.img+'"><div><b>'+c.display+'</b><div style="font-size:13px;color:#555">'+c.last+'</div></div>';r.onclick=()=>openChat(c.key,true,c.display,c.img);chatList.appendChild(r);});}
async function sendMsg(){let t=msgIn.value.trim();if(!t)return;msgIn.value='';await fetch(isPriv?'/api/private':'/api/groups',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({key:curRoom,room:curRoom,user:myName,num:myNumber,text:t,type:'text'})});load();}
function start(){load();setInterval(load,3000);setInterval(()=>fetch('/ping'),60000);}
</script></body></html>
"""

@app.route('/')
def home():
    return HTML_PAGE

@app.route('/ping')
def ping():
    return 'alive - KREST CHAT X no sleep', 200

@app.route('/api/send_otp', methods=['POST'])
def send_otp():
    num = request.json.get('number','').strip()
    code = str(random.randint(100000,999999))
    with lock:
        OTP[num] = code
    return jsonify(ok=True, otp=code)

@app.route('/api/verify_otp', methods=['POST'])
def verify_otp():
    d = request.json
    num = d.get('number')
    with lock:
        real = OTP.get(num)
        if not real or real!= d.get('otp'):
            return jsonify(ok=False, error=f"Wrong code! Correct is {real}")
        PROFILES[num] = {"name": d.get('name'), "img": d.get('img')}
        OTP.pop(num, None)
    return jsonify(ok=True)

@app.route('/api/groups', methods=['GET','POST'])
def groups_api():
    if request.method == 'GET':
        with lock:
            room = request.args.get('room','global')
            msgs = GROUPS.get(room, [])
            me = request.args.get('me','')
            chats = [{"key":"global","display":"GLOBAL GROUP","last":msgs[-1]['text'][:40] if msgs else "Everybody join and talk!","img":"https://i.pravatar.cc/100?img=12","time":msgs[-1]['time'] if msgs else "Live"}]
            for k,v in PRIVATE.items():
                if me in k and v:
                    other = k.split('_')[0] if k.split('_')[1]==me else k.split('_')[1]
                    prof = PROFILES.get(other, {"name":other,"img":f"https://i.pravatar.cc/100?u={other}"})
                    chats.append({"key":k,"display":prof['name'],"last":v[-1]['text'][:35],"img":prof['img'],"time":v[-1]['time']})
            return jsonify(messages=msgs[-100:], all_chats=chats)
    else:
        d = request.json
        room = d.get('room','global')
        with lock:
            if room not in GROUPS: GROUPS[room]=[]
            GROUPS[room].append({"user":d['user'],"num":d['num'],"text":d['text'],"time":datetime.now().strftime("%H:%M"),"type":d.get('type','text'),"audio":d.get('audio')})
        return jsonify(ok=True)

@app.route('/api/private', methods=['GET','POST'])
def private_api():
    if request.method == 'GET':
        with lock:
            key = request.args.get('key','')
            me = request.args.get('me','')
            msgs = PRIVATE.get(key, [])
            chats = [{"key":"global","display":"GLOBAL GROUP","last":GROUPS['global'][-1]['text'][:40],"img":"https://i.pravatar.cc/100?img=12","time":GROUPS['global'][-1]['time']}]
            for k,v in PRIVATE.items():
                if me in k and v:
                    other = k.split('_')[0] if k.split('_')[1]==me else k.split('_')[1]
                    prof = PROFILES.get(other, {"name":other,"img":f"https://i.pravatar.cc/100?u={other}"})
                    chats.append({"key":k,"display":prof['name'],"last":v[-1]['text'][:35],"img":prof['img'],"time":v[-1]['time']})
            return jsonify(messages=msgs[-100:], all_chats=chats)
    else:
        d = request.json
        key = d.get('key')
        with lock:
            if key not in PRIVATE: PRIVATE[key]=[]
            PRIVATE[key].append({"user":d['user'],"num":d['num'],"text":d['text'],"time":datetime.now().strftime("%H:%M"),"type":d.get('type','text'),"audio":d.get('audio')})
        return jsonify(ok=True)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
