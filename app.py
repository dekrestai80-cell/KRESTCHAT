from flask import Flask, request, jsonify
from datetime import datetime
import threading, random, re
app = Flask(__name__)

GROUPS = {"world": [{"user":"System","num":"000","text":"Welcome! Tap + to add chat, tap KrestAI for AI","time":"00:51","img":"https://i.pravatar.cc/100?img=12"}]}
PRIVATE = {}
AI_CHATS = {}
OTP_STORE = {}
PROFILES = {}
lock = threading.Lock()

def ai_brain(q, name=""):
    ql = q.lower()
    if "who are you" in ql: return f"I'm KrestAI 🤖 built by {name or 'DE Krest'} inside your WhatsApp clone! I answer ANY question."
    if any(x in ql for x in ["code","python","html","app","build"]): return f"For '{q}' - Tell me exactly what app you want and I'll write FULL CODE now! Example: 'build calculator'"
    if re.search(r'\d+.*[\+\-\*\/].*\d+', q):
        try: return f"{q} = {eval(re.findall(r'[\d\+\-\*\/\(\)\.\s]+', q)[0])} ✅"
        except: pass
    if "aba" in ql or "business" in ql: return "Aba business: Post shoes/clothes online, charge 500 for AD, you are middleman without shop! Want plan?"
    if "hello" in ql or "xup" in ql: return f"Xup {name}! I'm online ✅ Ask me anything!"
    return f"You asked: '{q}'\n\nAnswer: {q} works by understanding it step by step. Tell me more details and I give exact code/plan."

HTML = """
<!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1">
<title>WhatsApp</title><link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
<style>
*{margin:0;padding:0;box-sizing:border-box;font-family:Arial}
html,body{height:100%;overflow:hidden;background:white;color:#111b21}
#app{height:100vh;display:flex}
#side{width:100%;background:white;display:flex;flex-direction:column}
.top{padding:14px 16px;display:flex;justify-content:space-between;align-items:center}
.top b{font-size:28px;font-weight:800}
.search{margin:8px 16px;background:#f0f2f5;padding:12px 16px;border-radius:24px;display:flex;gap:12px;align-items:center}
.search input{border:0;background:transparent;flex:1;font-size:16px;outline:0}
.filters{display:flex;gap:8px;padding:10px 16px;overflow-x:auto;white-space:nowrap}
.filters button{padding:8px 14px;border-radius:20px;border:1px solid #e9edef;background:white;font-size:13px;display:flex;gap:6px;white-space:nowrap;cursor:pointer}
.filters button.active{background:#e7f8e8;border-color:#00a884}
.dotR{width:10px;height:10px;background:#f15c6d;border-radius:50%}.dotG{width:10px;height:10px;background:#00a884;border-radius:50%}
#chatList{flex:1;overflow-y:auto;padding-bottom:90px}
.row{display:flex;gap:12px;padding:12px 16px;cursor:pointer;align-items:center;border-bottom:1px solid #f5f6f6}
.row:hover{background:#f5f6f6}.row.aiRow{background:#f0faf0;border-left:4px solid #00a884}
.row img{width:50px;height:50px;border-radius:50%;object-fit:cover;flex-shrink:0}
.mid{flex:1;overflow:hidden}.nameLine{display:flex;justify-content:space-between}
.nameLine b{font-size:16px;font-weight:500}.nameLine span.t{font-size:12px;color:#667781}
.prevLine{font-size:14px;color:#667781;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;display:flex;gap:4px;margin-top:2px}
.badge{background:#00a884;color:white;font-size:12px;font-weight:bold;min-width:22px;height:22px;border-radius:11px;display:flex;align-items:center;justify-content:center}
.bottom{position:fixed;bottom:0;left:0;right:0;background:white;border-top:1px solid #e9edef;display:flex;justify-content:space-around;padding:8px 0 14px;z-index:10}
.nav{flex:1;text-align:center;position:relative}.nav i{font-size:22px;color:#667781}.nav.active i{color:#111b21}.nav b{font-size:12px;display:block;margin-top:2px;color:#667781}.nav.active b{color:#111b21;font-weight:700}
.noti{position:absolute;top:-6px;right:28px;background:#00a884;color:white;font-size:10px;min-width:18px;height:18px;border-radius:9px;display:flex;align-items:center;justify-content:center}
.fab{position:fixed;bottom:88px;right:16px;width:56px;height:56px;background:#111b21;border-radius:16px;display:flex;align-items:center;justify-content:center;color:white;font-size:22px;z-index:11;box-shadow:0 4px 10px rgba(0,0,0,0.3);cursor:pointer}
#main{position:fixed;inset:0;background:#efeae2;z-index:20;display:none;flex-direction:column}
#main.show{display:flex}
#mainHeader{padding:10px 12px;background:#f0f2f5;display:flex;align-items:center;gap:10px}
#mainHeader img{width:36px;height:36px;border-radius:50%}
#messages{flex:1;overflow-y:auto;padding:12px;display:flex;flex-direction:column;gap:8px}
.bubble{max-width:78%;padding:8px 10px;border-radius:8px;font-size:14.5px;white-space:pre-wrap;box-shadow:0 1px 0.5px rgba(0,0,0,0.13)}
.me{align-self:flex-end;background:#d9fdd3}.other{align-self:flex-start;background:white}.aiB{align-self:flex-start;background:#e7f8e8;border:1px solid #c0e6c0}
#inputBar{padding:8px;background:#f0f2f5;display:flex;gap:8px;align-items:center}
#inputBar input{flex:1;padding:12px 16px;border-radius:24px;border:0;outline:0;font-size:15px}
#inputBar button{width:44px;height:44px;border-radius:50%;border:0;background:#00a884;color:white}
#typing{font-size:12px;color:#00a884;padding:2px 16px;display:none}
#login{position:fixed;inset:0;background:white;z-index:100;display:flex;align-items:center;justify-content:center;padding:16px;overflow-y:auto}
.box{background:white;padding:24px;border-radius:16px;width:100%;max-width:380px;box-shadow:0 8px 30px rgba(0,0,0,0.15);text-align:center;border:1px solid #e9edef}
.box input{width:100%;padding:12px;border-radius:8px;border:1px solid #ddd;margin:7px 0;font-size:15px}
.box button{width:100%;padding:12px;background:#00a884;border:0;border-radius:8px;color:white;font-weight:bold;margin-top:8px;font-size:15px}
.prevWrap{position:relative;width:110px;height:110px;margin:10px auto}
.prevImg{width:110px;height:110px;border-radius:50%;object-fit:cover;border:4px solid #00a884;background:#f0f2f5;display:block}
.editBadge{position:absolute;bottom:2px;right:2px;width:32px;height:32px;background:#00a884;border-radius:50%;display:flex;align-items:center;justify-content:center;color:white;border:2px solid white;cursor:pointer}
.galleryBtns{display:flex;gap:8px;margin:8px 0}
.galleryBtns button{flex:1;padding:10px;background:#f0f2f5;color:#111b21;border:1px solid #ddd;font-size:12px}
.otpRow{display:flex;gap:8px;justify-content:center;margin:14px 0}.otpRow input{width:44px;height:50px;text-align:center;font-size:20px;border-radius:10px;border:1px solid #ddd;font-weight:bold}
</style></head><body>

<div id="login">
<div class="box" id="step1">
<h2 style="margin-bottom:6px">KRESTCHAT</h2><p style="font-size:12px;color:#667781;margin-bottom:10px">Choose profile from gallery - Like WhatsApp</p>

<!-- GALLERY PROFILE PICKER - BLUETOOTH/GALLERY ACCESS -->
<div class="prevWrap" onclick="openGallery()">
<img id="prev" class="prevImg" src="https://i.pravatar.cc/150?u=krest">
<div class="editBadge"><i class="fa fa-camera"></i></div>
</div>

<input type="file" id="pf" accept="image/*" style="display:none" capture="user">
<div class="galleryBtns">
<button onclick="openGallery()"><i class="fa fa-images"></i> Gallery</button>
<button onclick="openCamera()"><i class="fa fa-camera"></i> Camera</button>
</div>
<small style="font-size:11px;color:#00a884">Tap photo or Gallery button to choose ANY photo from your phone</small>

<input id="myName" placeholder="Your Name e.g. DE Krest" style="margin-top:12px">
<input id="myNumber" placeholder="Phone e.g. 08146096232" type="tel">
<small style="color:#667781;font-size:11px">11 digits - OTP verification like WhatsApp</small>
<button onclick="sendOTP()">Send OTP Code</button>
<div id="e1" style="color:#f15c6d;font-size:12px;margin-top:8px"></div>
</div>

<div class="box" id="step2" style="display:none">
<div style="font-size:36px">🔐</div><h3>Verify Number</h3>
<p style="font-size:12px;color:#667781">Code sent to <b id="vNum"></b></p>
<div style="background:#f0f2f5;padding:12px;border-radius:10px;margin:10px 0">
Demo OTP: <b id="dOTP" style="color:#00a884;font-size:20px">------</b><br><small style="color:#667781">Real app via SMS - demo shows here</small>
</div>
<div class="otpRow">
<input id="o1" maxlength="1" oninput="jump(1)"><input id="o2" maxlength="1" oninput="jump(2)"><input id="o3" maxlength="1" oninput="jump(3)">
<input id="o4" maxlength="1" oninput="jump(4)"><input id="o5" maxlength="1" oninput="jump(5)"><input id="o6" maxlength="1" oninput="jump(6)">
</div>
<button onclick="verifyOTP()">Verify & Enter</button>
<button onclick="back1()" style="background:#eee;color:#111b21">Change Number</button>
<div id="e2" style="color:#f15c6d;font-size:12px;margin-top:8px"></div>
</div>
</div>

<div id="app">
<div id="side">
<div class="top"><b>WhatsApp</b><div><i class="fa fa-camera"></i><i class="fa fa-ellipsis-v"></i></div></div>
<div class="search"><i class="fa fa-search" style="color:#667781"></i><input id="q" placeholder="Search..." oninput="renderList()"></div>
<div class="filters">
<button class="active" id="f-all" onclick="setF('all')">All</button>
<button id="f-private" onclick="setF('private')"><span class="dotR"></span> AI handoff</button>
<button id="f-ai" onclick="setF('ai')"><span class="dotG"></span> AI responding</button>
<button id="f-unread" onclick="setF('unread')">Unread 1</button>
</div>
<div id="chatList"></div>
<div class="fab" onclick="addChat()"><i class="fa-solid fa-plus"></i></div>
<div class="bottom">
<div class="nav active"><i class="fa-solid fa-message"></i><span class="noti">1</span><b>Chats</b></div>
<div class="nav"><i class="fa fa-phone"></i><b>Calls</b></div>
<div class="nav"><i class="fa-solid fa-circle-notch"></i><span class="noti" style="width:10px;height:10px;right:32px"></span><b>Updates</b></div>
<div class="nav"><i class="fa fa-store"></i><b>Tools</b></div>
</div>
</div>

<div id="main">
<div id="mainHeader"><i class="fa fa-arrow-left" onclick="closeChat()" style="padding:8px;cursor:pointer"></i><img id="cImg" src=""><div><b id="cName"></b><br><small id="cStatus" style="color:#667781">tap here for contact info</small></div><div style="margin-left:auto;display:flex;gap:18px"><i class="fa fa-video"></i><i class="fa fa-phone"></i><i class="fa fa-ellipsis-v"></i></div></div>
<div id="messages"></div>
<div id="typing">KrestAI is typing...</div>
<div id="inputBar"><input id="msgIn" placeholder="Message" onkeydown="if(event.key==='Enter')sendMsg()"><button onclick="sendMsg()"><i class="fa fa-paper-plane"></i></button></div>
</div>
</div>

<script>
let myName="",myNumber="",pB64="",curRoom="world",isPriv=false,isAI=false,filter="all",allChats=[];

function openGallery(){
 document.getElementById('pf').removeAttribute('capture');
 document.getElementById('pf').click();
}
function openCamera(){
 document.getElementById('pf').setAttribute('capture','user');
 document.getElementById('pf').click();
}
document.getElementById('pf').addEventListener('change',e=>{
 let f=e.target.files[0];if(!f)return;
 // Check if image
 if(!f.type.startsWith('image/')){alert('Please choose image from gallery');return;}
 let r=new FileReader();
 r.onload=ev=>{
  pB64=ev.target.result;
  document.getElementById('prev').src=pB64;
  // Save instantly
  if(myNumber) localStorage.setItem('kImg',pB64);
 };
 r.readAsDataURL(f);
});

function jump(i){if(document.getElementById('o'+i).value&&i<6)document.getElementById('o'+(i+1)).focus();}
async function sendOTP(){
 myName=document.getElementById('myName').value.trim();
 myNumber=document.getElementById('myNumber').value.trim().replace(/\\s/g,'');
 if(!myName)return document.getElementById('e1').textContent="Enter name";
 if(!/^(0[789][01]\\d{8})$/.test(myNumber))return document.getElementById('e1').textContent="Invalid! Use 11 digits e.g. 08146096232";
 if(!pB64)pB64=document.getElementById('prev').src;
 let res=await fetch('/api/send_otp',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({number:myNumber})});
 let d=await res.json();
 document.getElementById('vNum').textContent=myNumber;
 document.getElementById('dOTP').textContent=d.otp;
 document.getElementById('step1').style.display='none';
 document.getElementById('step2').style.display='block';
}
function back1(){document.getElementById('step1').style.display='block';document.getElementById('step2').style.display='none';}
async function verifyOTP(){
 let code=['o1','o2','o3','o4','o5','o6'].map(id=>document.getElementById(id).value).join('');
 if(code.length!=6)return document.getElementById('e2').textContent="Enter 6 digits";
 let res=await fetch('/api/verify_otp',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({number:myNumber,otp:code,name:myName,img:pB64})});
 let d=await res.json();if(!d.ok)return document.getElementById('e2').textContent=d.error;
 localStorage.setItem('kName',myName);localStorage.setItem('kNum',myNumber);localStorage.setItem('kImg',pB64);
 document.getElementById('login').style.display='none';start();
}
let sn=localStorage.getItem('kName'),snum=localStorage.getItem('kNum'),si=localStorage.getItem('kImg');
if(sn&&snum){myName=sn;myNumber=snum;pB64=si;document.getElementById('prev').src=pB64;document.getElementById('login').style.display='none';start();}

function getKey(a,b){let arr=[a,b].sort();return arr[0]+'_'+arr[1];}
function addChat(){
 let num=prompt('Enter phone number e.g. 08146096232');
 if(!num)return;num=num.replace(/\\s/g,'');
 if(!/^(0[789][01]\\d{8})$/.test(num))return alert('Invalid 11 digit number');
 if(num==myNumber)return alert('Your own number');
 curRoom=getKey(myNumber,num);isPriv=true;isAI=false;
 document.getElementById('cName').textContent=num;document.getElementById('cImg').src='https://i.pravatar.cc/100?u='+num;
 document.getElementById('main').classList.add('show');loadChat();
}
function openChat(key,priv,name,img,ai){
 curRoom=key;isPriv=priv;isAI=ai||false;
 document.getElementById('cName').textContent=name;
 document.getElementById('cImg').src=img;
 document.getElementById('cStatus').textContent=ai?'● AI responding - ask anything':'● tap here for contact info';
 document.getElementById('main').classList.add('show');
 loadChat();
}
function closeChat(){document.getElementById('main').classList.remove('show');}

async function loadChat(){
 let url=isAI?`/api/ai_chat?user=${myNumber}`:(isPriv?`/api/private?key=${curRoom}&me=${myNumber}`:`/api/groups?room=${curRoom}&me=${myNumber}`);
 let res=await fetch(url);let data=await res.json();
 let box=document.getElementById('messages');box.innerHTML='';
 data.messages.forEach(m=>{
  let d=document.createElement('div');
  d.className='bubble '+(m.isAI?'aiB':(m.num==myNumber?'me':'other'));
  d.textContent=m.text;
  let time=document.createElement('div');
  time.style.cssText='font-size:10px;color:#667781;float:right;margin-left:8px;margin-top:4px';
  time.textContent=m.time+(m.num==myNumber?' ✓✓':'');
  d.appendChild(time);
  box.appendChild(d);
 });
 box.scrollTop=box.scrollHeight;
 allChats=data.all_chats;
 renderList();
}
function renderList(){
 let q=document.getElementById('q').value.toLowerCase();
 let list=document.getElementById('chatList');list.innerHTML='';
 let aiRow=document.createElement('div');aiRow.className='row aiRow';
 aiRow.innerHTML=`<img src="https://i.pravatar.cc/100?img=32"><div class="mid"><div class="nameLine"><b>KrestAI 🤖</b><span class="t">now</span></div><div class="prevLine">Ask me anything - I answer instantly!</div></div><div class="right"><span style="background:#00a884;color:white;font-size:10px;padding:4px 8px;border-radius:10px">AI</span></div>`;
 aiRow.onclick=()=>openChat('ai',true,'KrestAI 🤖','https://i.pravatar.cc/100?img=32',true);
 list.appendChild(aiRow);

 allChats.forEach(c=>{
  if(filter=='private'&&!c.isPrivate)return;
  if(filter=='ai'&&c.key!='ai'&&!c.isPrivate)return;
  if(filter=='unread'&&c.unread==0)return;
  if(q&&!c.display.toLowerCase().includes(q)&&!c.last.toLowerCase().includes(q))return;
  let row=document.createElement('div');row.className='row';
  row.innerHTML=`<img src="${c.img}"><div class="mid"><div class="nameLine"><b>${c.display}</b><span class="t">${c.time||'00:51'}</span></div><div class="prevLine"><span style="color:#53bdeb">✓✓</span> ${c.last}</div></div><div class="right">${c.unread>0?`<span class="badge">${c.unread}</span>`:''}</div>`;
  row.onclick=()=>openChat(c.key,c.isPrivate,c.display,c.img,false);
  list.appendChild(row);
 });
}
function setF(f){
 filter=f;
 document.querySelectorAll('.filters button').forEach(b=>b.classList.remove('active'));
 document.getElementById('f-'+f).classList.add('active');
 renderList();
}
async function sendMsg(){
 let t=document.getElementById('msgIn').value.trim();if(!t)return;
 document.getElementById('msgIn').value='';
 if(isAI){
  await fetch('/api/ai_chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({user:myNumber,name:myName,text:t,img:pB64})});
  document.getElementById('typing').style.display='block';
  setTimeout(()=>{document.getElementById('typing').style.display='none';loadChat();},800);
 }else{
  let ep=isPriv?'/api/private':'/api/groups';
  await fetch(ep,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({key:curRoom,room:curRoom,user:myName,num:myNumber,text:t,img:pB64})});
 }
 loadChat();
}
function start(){loadChat();setInterval(()=>{if(!document.getElementById('main').classList.contains('show')||!isAI)loadChat();},3000);}
</script></body></html>
"""

@app.route("/")
def home(): return HTML

@app.route("/api/send_otp", methods=["POST"])
def send_otp():
    num=request.json.get("number","").strip()
    if not num or len(num)!=11: return jsonify({"ok":False,"otp":"000000"})
    otp=str(random.randint(100000,999999))
    with lock: OTP_STORE[num]=otp
    return jsonify({"ok":True,"otp":otp})

@app.route("/api/verify_otp", methods=["POST"])
def verify_otp():
    d=request.json; num=d.get("number"); otp=d.get("otp")
    with lock:
        real=OTP_STORE.get(num)
        if not real: return jsonify({"ok":False,"error":"No OTP sent"})
        if real!=otp: return jsonify({"ok":False,"error":f"Wrong! Correct is {real}"})
        PROFILES[num]={"name":d.get("name"),"img":d.get("img")}
        OTP_STORE.pop(num,None)
    return jsonify({"ok":True})

@app.route("/api/ai_chat", methods=["GET","POST"])
def ai_chat():
    user=request.args.get("user") if request.method=="GET" else request.json.get("user")
    if request.method=="GET":
        with lock:
            msgs=AI_CHATS.get(user,[{"user":"KrestAI","text":"Hello! I'm KrestAI 🤖\nI answer ANY question:\n• Code\n• Math\n• Business\n• School\n\nAsk me now!","time":datetime.now().strftime("%H:%M"),"isAI":True}])
            chats=[]
            for k,v in GROUPS.items(): chats.append({"key":k,"display":"# "+k,"last":v[-1]["text"][:35] if v else "Tap","isPrivate":False,"img":"https://i.pravatar.cc/100?u="+k,"time":v[-1]["time"] if v else "00:51","unread":0})
            for k,v in PRIVATE.items():
                if user in k and v:
                    other=k.split("_")[0] if k.split("_")[1]==user else k.split("_")[1]
                    prof=PROFILES.get(other,{"name":other,"img":"https://i.pravatar.cc/100?u="+other})
                    chats.append({"key":k,"display":prof["name"],"last":v[-1]["text"][:35],"isPrivate":True,"img":prof["img"],"time":v[-1]["time"],"unread":1})
            return jsonify({"messages":msgs[-100:],"all_chats":chats})
    else:
        d=request.json; q=d.get("text",""); name=d.get("name","")
        with lock:
            if user not in AI_CHATS: AI_CHATS[user]=[]
            AI_CHATS[user].append({"user":name,"num":user,"text":q,"time":datetime.now().strftime("%H:%M"),"img":d.get("img"),"isAI":False})
            AI_CHATS[user].append({"user":"KrestAI","text":ai_brain(q,name),"time":datetime.now().strftime("%H:%M"),"isAI":True,"img":"https://i.pravatar.cc/100?img=32"})
        return jsonify({"ok":True})

@app.route("/api/groups", methods=["GET","POST"])
def groups():
    if request.method=="GET":
        with lock:
            room=request.args.get("room","world"); msgs=GROUPS.get(room,[])
            chats=[]
            for k,v in GROUPS.items(): chats.append({"key":k,"display":"# "+k,"last":v[-1]["text"][:35] if v else "Tap","isPrivate":False,"img":"https://i.pravatar.cc/100?u="+k,"time":v[-1]["time"] if v else "00:51","unread":0})
            for k,v in PRIVATE.items():
                if request.args.get("me","") in k and v:
                    other=k.split("_")[0] if k.split("_")[1]==request.args.get("me","") else k.split("_")[1]
                    prof=PROFILES.get(other,{"name":other,"img":"https://i.pravatar.cc/100?u="+other})
                    chats.append({"key":k,"display":prof["name"],"last":v[-1]["text"][:35],"isPrivate":True,"img":prof["img"],"time":v[-1]["time"],"unread":2})
            return jsonify({"messages":msgs[-100:],"all_chats":chats})
    else:
        d=request.json; room=d.get("room","world")
        with lock:
            if room not in GROUPS: GROUPS[room]=[]
            GROUPS[room].append({"user":d["user"],"num":d["num"],"text":d["text"],"time":datetime.now().strftime("%H:%M"),"img":d.get("img")})
        return jsonify({"ok":True})

@app.route("/api/private", methods=["GET","POST"])
def private_chat():
    if request.method=="GET":
        key=request.args.get("key",""); me=request.args.get("me","")
        with lock:
            msgs=PRIVATE.get(key,[]); chats=[]
            for k,v in GROUPS.items(): chats.append({"key":k,"display":"# "+k,"last":v[-1]["text"][:35] if v else "","isPrivate":False,"img":"https://i.pravatar.cc/100?u="+k,"time":v[-1]["time"] if v else "","unread":0})
            for k,v in PRIVATE.items():
                if me in k and v:
                    other=k.split("_")[0] if k.split("_")[1]==me else k.split("_")[1]
                    prof=PROFILES.get(other,{"name":other,"img":"https://i.pravatar.cc/100?u="+other})
                    chats.append({"key":k,"display":prof["name"],"last":v[-1]["text"][:35],"isPrivate":True,"img":prof["img"],"time":v[-1]["time"],"unread":0 if k==key else 1})
            return jsonify({"messages":msgs[-100:],"all_chats":chats})
    else:
        d=request.json; key=d.get("key")
        with lock:
            if key not in PRIVATE: PRIVATE[key]=[]
            PRIVATE[key].append({"user":d["user"],"num":d["num"],"text":d["text"],"time":datetime.now().strftime("%H:%M"),"img":d.get("img")})
        return jsonify({"ok":True})

if __name__=="__main__": app.run(host="0.0.0.0", port=10000)
