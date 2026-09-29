import os
from flask import Flask, request, jsonify
from datetime import datetime
import threading, random

app = Flask(__name__)

CHATS = {}
PROFILES = {}
OTP = {}
lock = threading.Lock()

HTML = """
<!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>KREST CHAT X</title><link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
<style>
*{margin:0;padding:0;box-sizing:border-box;font-family:Arial}
body{background:#0a0a0b;color:white;height:100vh;overflow:hidden}
#side{width:100%;height:100vh;display:flex;flex-direction:column}
.top{padding:18px 20px;border-bottom:1px solid #232326;display:flex;justify-content:space-between}
.top b{font-size:20px;font-weight:800}.top b span{background:white;color:black;padding:2px 8px;border-radius:8px;margin-left:4px}
.search{margin:14px 16px;padding:12px 16px;background:#141416;border:1px solid #232326;border-radius:14px;display:flex;gap:10px}
.search input{border:0;background:transparent;flex:1;outline:0;color:white}
#list{flex:1;overflow-y:auto;padding:0 8px 90px}
.row{display:flex;gap:12px;padding:12px;border-radius:16px;cursor:pointer;margin:2px 4px}
.row:hover{background:#141416}
.row img{width:48px;height:48px;border-radius:14px;object-fit:cover}
.mid{flex:1;overflow:hidden}.nRow{display:flex;justify-content:space-between}
.prev{font-size:13px;color:#8a8a90;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;margin-top:3px}
.fab{position:fixed;bottom:20px;right:16px;width:56px;height:56px;background:white;color:black;border-radius:18px;display:flex;align-items:center;justify-content:center;font-size:22px;cursor:pointer}
#main{position:fixed;inset:0;background:#0a0a0b;z-index:20;display:none;flex-direction:column}
#main.show{display:flex}
#mainHead{padding:14px 16px;background:#141416;display:flex;align-items:center;gap:12px;border-bottom:1px solid #232326}
#mainHead img{width:38px;height:38px;border-radius:12px;object-fit:cover}
#msgs{flex:1;overflow-y:auto;padding:16px;display:flex;flex-direction:column;gap:10px}
.bubble{max-width:78%;padding:11px 14px;border-radius:20px;font-size:14px;white-space:pre-wrap}
.me{align-self:flex-end;background:white;color:black;border-bottom-right-radius:8px}.other{align-self:flex-start;background:#1c1c1f;border:1px solid #232326}
#inputBar{padding:10px 12px;background:#141416;border-top:1px solid #232326;display:flex;gap:8px}
#inputBar input{flex:1;padding:13px 18px;border-radius:100px;border:1px solid #232326;background:#0a0a0b;color:white;outline:0}
#inputBar button{width:44px;height:44px;border-radius:50%;border:0;background:white;color:black}
#login{position:fixed;inset:0;background:#0a0a0b;z-index:100;display:flex;align-items:center;justify-content:center;padding:20px}
.box{background:#141416;padding:28px;border-radius:24px;width:100%;max-width:360px;text-align:center;border:1px solid #232326}
.box input{width:100%;padding:13px 16px;border-radius:12px;border:1px solid #232326;margin:8px 0;background:#0a0a0b;color:white;outline:0}
.box button{width:100%;padding:13px;background:white;border:0;border-radius:12px;color:black;font-weight:800;margin-top:10px;cursor:pointer}
.wrap{position:relative;width:90px;height:90px;margin:16px auto}
.prevImg{width:90px;height:90px;border-radius:20px;object-fit:cover;background:#1c1c1f;border:1px solid #232326}
.cam{position:absolute;bottom:-6px;right:-6px;width:30px;height:30px;background:white;color:black;border-radius:50%;display:flex;align-items:center;justify-content:center;border:3px solid #141416}
.otp{display:flex;gap:8px;justify-content:center;margin:18px 0}.otp input{width:46px;height:52px;text-align:center;font-size:20px;border-radius:12px;border:1px solid #232326;background:#0a0a0b;color:white;font-weight:700}
</style></head><body>
<div id="login">
<div class="box" id="s1">
<div style="font-size:32px">⚡</div><h2>KREST CHAT X</h2><p style="font-size:12px;color:#8a8a90;margin:6px 0 14px">Simple chat</p>
<div class="wrap" onclick="document.getElementById('pf').click()">
<img id="prev" class="prevImg" src="https://i.pravatar.cc/150?u=krest">
<div class="cam"><i class="fa fa-camera" style="font-size:12px"></i></div>
</div>
<input type="file" id="pf" accept="image/*" style="display:none">
<button onclick="document.getElementById('pf').click()" style="background:#0a0a0b;color:white;border:1px solid #232326;font-size:12px">Gallery</button>
<input id="myName" placeholder="Your Name"><input id="myNumber" placeholder="08146096232" type="tel">
<button onclick="sendOTP()">Continue</button><div id="e1" style="color:#ff5a5a;font-size:12px;margin-top:8px"></div>
</div>
<div class="box" id="s2" style="display:none">
<h3>Verify</h3><p style="font-size:12px;color:#8a8a90">Code to <b id="vNum" style="color:white"></b></p>
<div style="background:#0a0a0b;padding:14px;border-radius:14px;margin:14px 0;border:1px solid #232326">OTP: <b id="dOTP" style="font-size:24px"></b></div>
<div class="otp"><input id="o1" maxlength="1" oninput="jmp(1)"><input id="o2" maxlength="1" oninput="jmp(2)"><input id="o3" maxlength="1" oninput="jmp(3)"><input id="o4" maxlength="1" oninput="jmp(4)"><input id="o5" maxlength="1" oninput="jmp(5)"><input id="o6" maxlength="1" oninput="jmp(6)"></div>
<button onclick="verifyOTP()">Verify</button><div id="e2" style="color:#ff5a5a;font-size:12px;margin-top:8px"></div>
</div>
</div>
<div id="app">
<div id="side">
<div class="top"><b>KREST CHAT <span>X</span></b><i class="fa fa-ellipsis" style="color:#8a8a90"></i></div>
<div class="search"><i class="fa fa-search" style="color:#8a8a90"></i><input id="q" placeholder="Search..." oninput="render()"></div>
<div id="list"></div>
<div class="fab" onclick="newChat()"><i class="fa fa-plus"></i></div>
</div>
<div id="main">
<div id="mainHead"><i class="fa fa-arrow-left" onclick="closeC()" style="padding:8px;cursor:pointer;color:#8a8a90"></i><img id="cImg" src=""><div><b id="cName"></b></div></div>
<div id="msgs"></div>
<div id="inputBar"><input id="msgIn" placeholder="Type a message..." onkeydown="if(event.key==='Enter')send()"><button onclick="send()"><i class="fa fa-paper-plane"></i></button></div>
</div>
</div>
<script>
let myName="",myNumber="",pB64="",curRoom="",allChats=[];
document.getElementById('pf').addEventListener('change',e=>{
 let f=e.target.files[0];if(!f)return;
 let r=new FileReader();r.onload=ev=>{pB64=ev.target.result;document.getElementById('prev').src=pB64;};r.readAsDataURL(f);
});
function jmp(i){if(document.getElementById('o'+i).value&&i<6)document.getElementById('o'+(i+1)).focus();}
async function sendOTP(){
 myName=document.getElementById('myName').value.trim();myNumber=document.getElementById('myNumber').value.trim();
 if(!myName||myNumber.length!=11)return document.getElementById('e1').textContent="Name + 11 digits";
 if(!pB64)pB64=document.getElementById('prev').src;
 let res=await fetch('/api/send_otp',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({number:myNumber})});
 let d=await res.json();document.getElementById('vNum').textContent=myNumber;document.getElementById('dOTP').textContent=d.otp;
 document.getElementById('s1').style.display='none';document.getElementById('s2').style.display='block';
}
async function verifyOTP(){
 let code=['o1','o2','o3','o4','o5','o6'].map(id=>document.getElementById(id).value).join('');
 let res=await fetch('/api/verify_otp',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({number:myNumber,otp:code,name:myName,img:pB64})});
 let d=await res.json();if(!d.ok)return document.getElementById('e2').textContent=d.error;
 localStorage.setItem('kName',myName);localStorage.setItem('kNum',myNumber);localStorage.setItem('kImg',pB64);
 document.getElementById('login').style.display='none';start();
}
let sn=localStorage.getItem('kName'),snum=localStorage.getItem('kNum'),si=localStorage.getItem('kImg');
if(sn&&snum){myName=sn;myNumber=snum;pB64=si;document.getElementById('prev').src=pB64;document.getElementById('login').style.display='none';start();}
function getKey(a,b){let arr=[a,b].sort();return arr[0]+'_'+arr[1];}
function newChat(){let num=prompt('Enter phone e.g. 08146096232');if(!num)return;curRoom=getKey(myNumber,num);document.getElementById('cName').textContent=num;document.getElementById('cImg').src='https://i.pravatar.cc/100?u='+num;document.getElementById('main').classList.add('show');load();}
function openChat(k,name,img){curRoom=k;document.getElementById('cName').textContent=name;document.getElementById('cImg').src=img;document.getElementById('main').classList.add('show');load();}
function closeC(){document.getElementById('main').classList.remove('show');}
async function load(){
 let res=await fetch(`/api/chat?key=${curRoom}&me=${myNumber}`);let data=await res.json();
 let box=document.getElementById('msgs');box.innerHTML='';
 data.messages.forEach(m=>{
  let d=document.createElement('div');d.className='bubble '+(m.num==myNumber?'me':'other');d.textContent=m.text;box.appendChild(d);
 });
 box.scrollTop=box.scrollHeight;allChats=data.all_chats;render();
}
function render(){
 let q=document.getElementById('q').value.toLowerCase();
 let list=document.getElementById('list');list.innerHTML='';
 allChats.forEach(c=>{
  if(q&&!c.display.toLowerCase().includes(q))return;
  let row=document.createElement('div');row.className='row';
  row.innerHTML=`<img src="${c.img}"><div class="mid"><div class="nRow"><b>${c.display}</b><span class="t">${c.time}</span></div><div class="prev">${c.last}</div></div>`;
  row.onclick=()=>openChat(c.key,c.display,c.img);
  list.appendChild(row);
 });
 if(allChats.length==0){list.innerHTML=`<div style="text-align:center;padding:40px;color:#8a8a90">No chats<br><small>Tap + to start</small></div>`;}
}
async function send(){
 let t=document.getElementById('msgIn').value.trim();if(!t)return;document.getElementById('msgIn').value='';
 await fetch('/api/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({key:curRoom,user:myName,num:myNumber,text:t,img:pB64})});
 load();
}
function start(){load();setInterval(load,3000);}
</script></body></html>
"""

@app.route("/")
def home():
    return HTML

@app.route("/api/send_otp", methods=["POST"])
def send_otp():
    num = request.json.get("number","")
    otp = str(random.randint(100000,999999))
    with lock:
        OTP[num] = otp
    return jsonify({"ok":True,"otp":otp})

@app.route("/api/verify_otp", methods=["POST"])
def verify_otp():
    d = request.json
    num = d.get("number")
    with lock:
        real = OTP.get(num)
        if not real or real!= d.get("otp"):
            return jsonify({"ok":False,"error":f"Wrong! Correct is {real}"})
        PROFILES[num] = {"name": d.get("name"), "img": d.get("img")}
        OTP.pop(num,None)
    return jsonify({"ok":True})

def make_key(a,b):
    return "_".join(sorted([a,b]))

@app.route("/api/chat", methods=["GET","POST"])
def chat():
    if request.method == "GET":
        key = request.args.get("key","")
        me = request.args.get("me","")
        with lock:
            msgs = CHATS.get(key,[])
            chats = []
            for k,v in CHATS.items():
                if me and me in k and v:
                    other = k.split("_")[0] if k.split("_")[1]==me else k.split("_")[1]
                    prof = PROFILES.get(other, {"name":other,"img":f"https://i.pravatar.cc/100?u={other}"})
                    chats.append({"key":k,"display":prof["name"],"last":v[-1]["text"][:30],"img":prof["img"],"time":v[-1]["time"]})
            for num, prof in PROFILES.items():
                if num!= me and not any(num in k for k in CHATS.keys() if me in k):
                    if not any(c["display"]==prof["name"] for c in chats):
                        chats.append({"key":make_key(me,num),"display":prof["name"],"last":"Tap to chat","img":prof["img"],"time":"now"})
            return jsonify({"messages":msgs[-50:],"all_chats":chats})
    else:
        d = request.json
        key = d.get("key")
        with lock:
            if key not in CHATS:
                CHATS[key] = []
            CHATS[key].append({"user":d["user"],"num":d["num"],"text":d["text"],"time":datetime.now().strftime("%H:%M")})
        return jsonify({"ok":True})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
