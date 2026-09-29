from flask import Flask, request, jsonify
from datetime import datetime
import threading, random, re
app = Flask(__name__)

GROUPS = {"lounge": [{"user":"Krest","num":"000","text":"Welcome to KREST CHAT X ⚡","time":"12:00","img":"https://i.pravatar.cc/100?img=12"}]}
PRIVATE = {}
AI_CHATS = {}
OTP_STORE = {}
PROFILES = {}
STATUS = {}
lock = threading.Lock()

def ai_brain(q, name=""):
    ql=q.lower()
    if "who are you" in ql: return f"I'm X-AI in KREST CHAT X by {name or 'DE Krest'}! Ask anything."
    if re.search(r'\d+.*[\+\-\*\/].*\d+', q):
        try: return f"{q} = {eval(re.findall(r'[\d\+\-\*\/\(\)\.\s]+', q)[0])} ✅"
        except: pass
    return f"You asked: '{q}'\n\nAnswer: Here's clear explanation about {q}. Tell me more details and I give exact steps/code/plan."

HTML = """
<!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>KREST CHAT X</title><link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
<style>
:root{--bg:#0a0a0b;--card:#141416;--card2:#1c1c1f;--border:#232326;--text:#fff;--muted:#8a8a90;--accent:#fff;--green:#00d084}
*{margin:0;padding:0;box-sizing:border-box;font-family:-apple-system,BlinkMacSystemFont,'SF Pro',Inter,Arial}
body{background:var(--bg);color:var(--text);height:100vh;overflow:hidden;-webkit-font-smoothing:antialiased}
#app{height:100vh;display:flex}
#side{width:100%;background:var(--bg);display:flex;flex-direction:column}
.top{padding:18px 20px;display:flex;justify-content:space-between;align-items:center;background:var(--bg);border-bottom:1px solid var(--border)}
.top b{font-size:22px;font-weight:800;letter-spacing:-0.5px}.top b span{background:var(--text);color:var(--bg);padding:2px 8px;border-radius:8px;margin-left:4px}
.top.icons i{font-size:18px;color:var(--muted);margin-left:18px;cursor:pointer}
.searchWrap{padding:14px 16px}
.search{padding:12px 16px;background:var(--card);border:1px solid var(--border);border-radius:14px;display:flex;gap:10px;align-items:center}
.search i{color:var(--muted)}.search input{border:0;background:transparent;flex:1;outline:0;color:white;font-size:14px}
.search input::placeholder{color:var(--muted)}
.tabs{padding:8px 16px 14px;display:flex;gap:8px;overflow-x:auto;scrollbar-width:none}
.tabs::-webkit-scrollbar{display:none}
.tabs button{padding:8px 16px;border-radius:100px;border:1px solid var(--border);background:var(--card);color:var(--muted);font-size:13px;font-weight:600;white-space:nowrap;cursor:pointer;transition:0.2s}
.tabs button.active{background:var(--text);color:var(--bg);border-color:var(--text)}
#list{flex:1;overflow-y:auto;padding:0 8px 110px}
.row{display:flex;gap:12px;padding:12px 12px;border-radius:16px;cursor:pointer;align-items:center;transition:0.2s;margin:2px 4px}
.row:hover{background:var(--card)}.row.aiRow{background:linear-gradient(135deg,#111f16,#141416);border:1px solid #1e3a2a}
.row img{width:48px;height:48px;border-radius:14px;object-fit:cover;flex-shrink:0}
.mid{flex:1;overflow:hidden}.nRow{display:flex;justify-content:space-between;align-items:center}
.nRow b{font-size:15px;font-weight:600;letter-spacing:-0.2px}.nRow span.t{font-size:11px;color:var(--muted);font-weight:500}
.prev{font-size:13px;color:var(--muted);white-space:nowrap;overflow:hidden;text-overflow:ellipsis;margin-top:3px;font-weight:400}
.statusRing{position:relative;padding:2.5px;background:linear-gradient(135deg,var(--green),#7cffb0);border-radius:16px}
.statusRing img{border:2.5px solid var(--bg)}
.badge{background:var(--text);color:var(--bg);font-size:11px;min-width:20px;height:20px;border-radius:10px;display:flex;align-items:center;justify-content:center;font-weight:800;padding:0 6px}
.badgeAI{background:var(--green);color:black;font-size:10px;padding:4px 8px;border-radius:100px;font-weight:800;letter-spacing:0.3px}
.bottom{position:fixed;bottom:0;left:0;right:0;background:rgba(20,20,22,0.9);backdrop-filter:blur(20px);border-top:1px solid var(--border);display:flex;justify-content:space-around;padding:10px 0 20px;z-index:10}
.nav{flex:1;text-align:center;cursor:pointer;opacity:0.5;transition:0.2s}.nav.active{opacity:1}
.nav i{font-size:20px}.nav b{font-size:9px;display:block;margin-top:5px;letter-spacing:0.8px;font-weight:700}
.fab{position:fixed;bottom:92px;right:16px;width:56px;height:56px;background:var(--text);color:var(--bg);border-radius:18px;display:flex;align-items:center;justify-content:center;font-size:22px;z-index:11;box-shadow:0 10px 30px rgba(0,0,0,0.5);cursor:pointer;transition:0.2s}
.fab:active{transform:scale(0.95)}
#main{position:fixed;inset:0;background:var(--bg);z-index:20;display:none;flex-direction:column}
#main.show{display:flex}
#mainHead{padding:14px 16px;background:var(--card);display:flex;align-items:center;gap:12px;border-bottom:1px solid var(--border)}
#mainHead img{width:38px;height:38px;border-radius:12px;object-fit:cover}
#msgs{flex:1;overflow-y:auto;padding:16px;display:flex;flex-direction:column;gap:10px}
.bubble{max-width:78%;padding:11px 14px;border-radius:20px;font-size:14.5px;line-height:1.4;white-space:pre-wrap;animation:pop 0.25s ease}
@keyframes pop{from{transform:scale(0.9);opacity:0}to{transform:scale(1);opacity:1}}
.me{align-self:flex-end;background:var(--text);color:var(--bg);border-bottom-right-radius:8px}.other{align-self:flex-start;background:var(--card2);border:1px solid var(--border);border-bottom-left-radius:8px}.aiB{align-self:flex-start;background:#111f16;border:1px solid #1e3a2a;color:#9effc0}
#inputBar{padding:10px 12px;background:var(--card);border-top:1px solid var(--border);display:flex;gap:8px;align-items:center}
#inputBar input{flex:1;padding:13px 18px;border-radius:100px;border:1px solid var(--border);background:var(--bg);color:white;outline:0;font-size:14px}
#inputBar button{width:44px;height:44px;border-radius:50%;border:0;background:var(--text);color:var(--bg);cursor:pointer}
#login{position:fixed;inset:0;background:var(--bg);z-index:100;display:flex;align-items:center;justify-content:center;padding:20px;overflow-y:auto}
.box{background:var(--card);padding:28px;border-radius:24px;width:100%;max-width:380px;text-align:center;border:1px solid var(--border);box-shadow:0 20px 60px rgba(0,0,0,0.6)}
.box input{width:100%;padding:13px 16px;border-radius:12px;border:1px solid var(--border);margin:8px 0;background:var(--bg);color:white;font-size:14px;outline:0}
.box input:focus{border-color:var(--text)}
.box button{width:100%;padding:13px;background:var(--text);border:0;border-radius:12px;color:var(--bg);font-weight:800;margin-top:10px;cursor:pointer;font-size:14px;transition:0.2s}
.box button:active{transform:scale(0.98)}
.wrap{position:relative;width:100px;height:100px;margin:16px auto}
.prevImg{width:100px;height:100px;border-radius:24px;object-fit:cover;border:1px solid var(--border);background:var(--card2)}
.cam{position:absolute;bottom:-6px;right:-6px;width:34px;height:34px;background:var(--text);color:var(--bg);border-radius:50%;display:flex;align-items:center;justify-content:center;border:3px solid var(--card);cursor:pointer;box-shadow:0 4px 12px rgba(0,0,0,0.4)}
.gBtns{display:flex;gap:8px;margin:14px 0}.gBtns button{flex:1;padding:10px;background:var(--bg);color:var(--text);border:1px solid var(--border);font-size:12px;border-radius:12px;font-weight:600}
.otp{display:flex;gap:8px;justify-content:center;margin:18px 0}.otp input{width:46px;height:52px;text-align:center;font-size:20px;border-radius:12px;border:1px solid var(--border);background:var(--bg);color:white;font-weight:700}
#statusPage{position:fixed;inset:0;background:var(--bg);z-index:25;display:none;flex-direction:column}
#statusPage.show{display:flex}
.statusItem{display:flex;gap:12px;padding:14px 16px;border-bottom:1px solid var(--border);align-items:center;cursor:pointer}
.statusItem:hover{background:var(--card)}
.statusItem img{width:48px;height:48px;border-radius:14px;object-fit:cover}
#statusModal{position:fixed;inset:0;background:rgba(0,0,0,0.92);z-index:110;display:none;align-items:center;justify-content:center;padding:20px}
#statusModal.show{display:flex}
.statusView{width:100%;max-width:360px;background:var(--card);border-radius:24px;overflow:hidden;border:1px solid var(--border)}
.statusView img{width:100%;max-height:420px;object-fit:cover}
#typing{font-size:12px;color:var(--green);padding:6px 20px;display:none;font-weight:600}
</style></head><body>

<div id="login">
<div class="box" id="s1">
<div style="font-size:36px;margin-bottom:8px">⚡</div><h2 style="letter-spacing:-0.5px">KREST CHAT X</h2><p style="font-size:12px;color:var(--muted);margin:6px 0 14px">Neat • Fast • Your Brand</p>
<div class="wrap" onclick="openGal()">
<img id="prev" class="prevImg" src="https://i.pravatar.cc/150?u=krestx">
<div class="cam"><i class="fa fa-camera" style="font-size:14px"></i></div>
</div>
<input type="file" id="pf" accept="image/*" style="display:none">
<input type="file" id="sf" accept="image/*" style="display:none">
<div class="gBtns">
<button onclick="openGal()"><i class="fa fa-images"></i> Gallery</button>
<button onclick="openCam()"><i class="fa fa-camera"></i> Camera</button>
<button onclick="openGal()"><i class="fa-brands fa-bluetooth"></i> Files</button>
</div>
<input id="myName" placeholder="Your X Name">
<input id="myNumber" placeholder="08146096232" type="tel">
<button onclick="sendOTP()">Continue →</button>
<div id="e1" style="color:#ff5a5a;font-size:12px;margin-top:8px"></div>
<small style="color:var(--muted);font-size:11px;display:block;margin-top:10px">Profile visible to all phones • Status sharing included</small>
</div>

<div class="box" id="s2" style="display:none">
<div style="font-size:32px">🔑</div><h3 style="margin-top:8px">Verify</h3>
<p style="font-size:12px;color:var(--muted)">Code sent to <b id="vNum" style="color:white"></b></p>
<div style="background:var(--bg);padding:14px;border-radius:14px;margin:14px 0;border:1px solid var(--border)">
<span style="font-size:12px;color:var(--muted)">DEMO OTP</span><br><b id="dOTP" style="font-size:24px;letter-spacing:2px"></b>
</div>
<div class="otp">
<input id="o1" maxlength="1" oninput="jmp(1)"><input id="o2" maxlength="1" oninput="jmp(2)"><input id="o3" maxlength="1" oninput="jmp(3)">
<input id="o4" maxlength="1" oninput="jmp(4)"><input id="o5" maxlength="1" oninput="jmp(5)"><input id="o6" maxlength="1" oninput="jmp(6)">
</div>
<button onclick="verifyOTP()">Verify</button>
<button onclick="back1()" style="background:var(--bg);color:white;border:1px solid var(--border)">Back</button>
<div id="e2" style="color:#ff5a5a;font-size:12px;margin-top:8px"></div>
</div>
</div>

<div id="statusPage">
<div class="top"><div style="display:flex;align-items:center;gap:12px"><i class="fa fa-arrow-left" onclick="closeStatus()" style="cursor:pointer;color:var(--muted)"></i><b>STATUS</b></div><i class="fa fa-ellipsis" style="color:var(--muted)"></i></div>
<div style="padding:16px;display:flex;gap:12px;align-items:center;border-bottom:1px solid var(--border);cursor:pointer" onclick="postStatus()">
<div style="position:relative"><img id="myStatusImg" src="https://i.pravatar.cc/100" style="width:52px;height:52px;border-radius:16px;object-fit:cover"><div style="position:absolute;bottom:-4px;right:-4px;background:var(--text);color:var(--bg);width:20px;height:20px;border-radius:50%;display:flex;align-items:center;justify-content:center;border:2px solid var(--bg)"><i class="fa fa-plus" style="font-size:10px"></i></div></div>
<div><b style="font-size:15px">My Status</b><br><small style="color:var(--muted)">Tap to add status update</small></div>
</div>
<div id="statusList" style="flex:1;overflow-y:auto"></div>
</div>

<div id="statusModal">
<div class="statusView">
<div style="padding:14px 16px;display:flex;justify-content:space-between;align-items:center"><b id="statusViewName" style="font-size:15px"></b><i class="fa fa-times" onclick="closeStatusView()" style="cursor:pointer;color:var(--muted)"></i></div>
<img id="statusViewImg" src="">
<div style="padding:14px"><p id="statusViewText" style="font-size:14px;line-height:1.4"></p><small id="statusViewTime" style="color:var(--muted)"></small></div>
</div>
</div>

<div id="app">
<div id="side">
<div class="top"><b>KREST CHAT <span>X</span></b><div class="icons"><i class="fa fa-magnifying-glass" onclick="document.getElementById('q').focus()"></i><i class="fa fa-ellipsis"></i></div></div>
<div class="searchWrap"><div class="search"><i class="fa fa-search"></i><input id="q" placeholder="Search Krest Chat X..." oninput="render()"></div></div>
<div class="tabs">
<button class="active" id="f-all" onclick="setF('all')">All</button>
<button id="f-friends" onclick="setF('friends')">Friends</button>
<button id="f-groups" onclick="setF('groups')">Groups</button>
<button id="f-status" onclick="openStatusPage()">Status</button>
</div>
<div id="list"></div>
<div class="fab" id="fabChat" onclick="newChat()"><i class="fa fa-plus"></i></div>
<div class="fab" id="fabStatus" style="display:none;background:var(--green)" onclick="postStatus()"><i class="fa fa-camera"></i></div>
<div class="bottom">
<div class="nav active" id="nav-home" onclick="showHome()"><i class="fa-solid fa-house"></i><b>HOME</b></div>
<div class="nav" id="nav-calls" onclick="alert('Calls soon')"><i class="fa-solid fa-phone"></i><b>CALLS</b></div>
<div class="nav" id="nav-ai" onclick="openAI()"><i class="fa-solid fa-bolt"></i><b>X-AI</b></div>
<div class="nav" id="nav-status" onclick="openStatusPage()"><i class="fa-solid fa-circle-notch"></i><b>STATUS</b></div>
</div>
</div>

<div id="main">
<div id="mainHead"><i class="fa fa-arrow-left" onclick="closeC()" style="padding:8px;cursor:pointer;color:var(--muted)"></i><img id="cImg" src=""><div><b id="cName" style="font-size:15px"></b><br><small id="cStat" style="color:var(--muted);font-size:11px">Krest Chat X</small></div><div style="margin-left:auto;display:flex;gap:18px;color:var(--muted)"><i class="fa fa-video"></i><i class="fa fa-phone"></i></div></div>
<div id="msgs"></div>
<div id="typing">● X-AI thinking...</div>
<div id="inputBar"><input id="msgIn" placeholder="Message..." onkeydown="if(event.key==='Enter')send()"><button onclick="send()"><i class="fa fa-paper-plane" style="font-size:14px"></i></button></div>
</div>
</div>

<script>
let myName="",myNumber="",pB64="",curRoom="lounge",isPriv=false,isAI=false,filter="all",allChats=[];
function openGal(){document.getElementById('pf').removeAttribute('capture');document.getElementById('pf').click();}
function openCam(){document.getElementById('pf').setAttribute('capture','user');document.getElementById('pf').click();}
document.getElementById('pf').addEventListener('change',e=>{
 let f=e.target.files[0];if(!f)return;
 let r=new FileReader();r.onload=ev=>{pB64=ev.target.result;document.getElementById('prev').src=pB64;document.getElementById('myStatusImg').src=pB64;};r.readAsDataURL(f);
});
function jmp(i){if(document.getElementById('o'+i).value&&i<6)document.getElementById('o'+(i+1)).focus();}
async function sendOTP(){
 myName=document.getElementById('myName').value.trim();
 myNumber=document.getElementById('myNumber').value.trim().replace(/\\s/g,'');
 if(!myName)return document.getElementById('e1').textContent="Enter name";
 if(!/^(0[789][01]\\d{8})$/.test(myNumber))return document.getElementById('e1').textContent="11 digits e.g. 08146096232";
 if(!pB64)pB64=document.getElementById('prev').src;
 let res=await fetch('/api/send_otp',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({number:myNumber})});
 let d=await res.json();document.getElementById('vNum').textContent=myNumber;document.getElementById('dOTP').textContent=d.otp;
 document.getElementById('s1').style.display='none';document.getElementById('s2').style.display='block';
}
function back1(){document.getElementById('s1').style.display='block';document.getElementById('s2').style.display='none';}
async function verifyOTP(){
 let code=['o1','o2','o3','o4','o5','o6'].map(id=>document.getElementById(id).value).join('');
 if(code.length!=6)return document.getElementById('e2').textContent="6 digits";
 let res=await fetch('/api/verify_otp',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({number:myNumber,otp:code,name:myName,img:pB64})});
 let d=await res.json();if(!d.ok)return document.getElementById('e2').textContent=d.error;
 localStorage.setItem('kName',myName);localStorage.setItem('kNum',myNumber);localStorage.setItem('kImg',pB64);
 document.getElementById('login').style.display='none';document.getElementById('myStatusImg').src=pB64;start();
}
let sn=localStorage.getItem('kName'),snum=localStorage.getItem('kNum'),si=localStorage.getItem('kImg');
if(sn&&snum){myName=sn;myNumber=snum;pB64=si;document.getElementById('prev').src=pB64;document.getElementById('myStatusImg').src=pB64;document.getElementById('login').style.display='none';start();}
function getKey(a,b){let arr=[a,b].sort();return arr[0]+'_'+arr[1];}
function newChat(){let num=prompt('Enter phone e.g. 08146096232');if(!num)return;num=num.replace(/\\s/g,'');if(!/^(0[789][01]\\d{8})$/.test(num))return alert('11 digits');curRoom=getKey(myNumber,num);isPriv=true;isAI=false;document.getElementById('cName').textContent=num;document.getElementById('cImg').src='https://i.pravatar.cc/100?u='+num;document.getElementById('main').classList.add('show');load();}
function openChat(k,priv,name,img,ai){curRoom=k;isPriv=priv;isAI=ai||false;document.getElementById('cName').textContent=name;document.getElementById('cImg').src=img;document.getElementById('cStat').textContent=ai?'X-AI Online':'Profile visible to all phones ⚡';document.getElementById('main').classList.add('show');load();}
function closeC(){document.getElementById('main').classList.remove('show');}
function showHome(){closeStatus();document.getElementById('main').classList.remove('show');document.querySelectorAll('.nav').forEach(n=>n.classList.remove('active'));document.getElementById('nav-home').classList.add('active');document.getElementById('fabChat').style.display='flex';document.getElementById('fabStatus').style.display='none';}
function openAI(){openChat('ai',true,'X-AI Assistant','https://i.pravatar.cc/100?img=32',true);}
function openStatusPage(){
 document.getElementById('statusPage').classList.add('show');
 document.querySelectorAll('.nav').forEach(n=>n.classList.remove('active'));
 document.getElementById('nav-status').classList.add('active');
 document.getElementById('fabChat').style.display='none';
 document.getElementById('fabStatus').style.display='flex';
 loadStatus();
}
function closeStatus(){document.getElementById('statusPage').classList.remove('show');showHome();}
async function loadStatus(){
 let res=await fetch(`/api/status?me=${myNumber}`);let data=await res.json();
 let list=document.getElementById('statusList');list.innerHTML='';
 data.statuses.forEach(s=>{
  let div=document.createElement('div');div.className='statusItem';
  div.innerHTML=`<div class="statusRing"><img src="${s.img}" style="border:2.5px solid var(--bg);width:48px;height:48px;border-radius:14px"></div><div style="flex:1"><b style="font-size:14px">${s.name}</b><br><small style="color:var(--muted)">${s.time} • ${s.text? s.text.substring(0,28) : 'Photo'}</small></div>`;
  div.onclick=()=>viewStatus(s);
  list.appendChild(div);
 });
}
function viewStatus(s){
 document.getElementById('statusViewName').textContent=s.name;
 document.getElementById('statusViewImg').src=s.imgStatus||s.img;
 document.getElementById('statusViewText').textContent=s.text||'';
 document.getElementById('statusViewTime').textContent=s.time;
 document.getElementById('statusModal').classList.add('show');
}
function closeStatusView(){document.getElementById('statusModal').classList.remove('show');}
function postStatus(){
 let text=prompt('Status text:');
 document.getElementById('sf').click();
 document.getElementById('sf').onchange=e=>{
  let f=e.target.files[0];
  if(f){
   let r=new FileReader();r.onload=ev=>{uploadStatus(text, ev.target.result);};r.readAsDataURL(f);
  }else if(text){
   uploadStatus(text,"");
  }
 };
 setTimeout(()=>{if(text &&!document.getElementById('sf').files.length) uploadStatus(text,"");},1500);
}
async function uploadStatus(text, img){
 await fetch('/api/status',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({number:myNumber,name:myName,img:pB64,text:text||'',imgStatus:img})});
 alert('Status posted ⚡ All phones will see it');
 loadStatus();
}
async function load(){
 let url=isAI?`/api/ai_chat?user=${myNumber}`:(isPriv?`/api/private?key=${curRoom}&me=${myNumber}`:`/api/groups?room=${curRoom}&me=${myNumber}`);
 let res=await fetch(url);let data=await res.json();
 let box=document.getElementById('msgs');box.innerHTML='';
 data.messages.forEach(m=>{
  let d=document.createElement('div');d.className='bubble '+(m.isAI?'aiB':(m.num==myNumber?'me':'other'));d.textContent=m.text;
  let t=document.createElement('span');t.style.cssText='font-size:10px;opacity:0.5;float:right;margin-left:8px;margin-top:4px';t.textContent=m.time;d.appendChild(t);box.appendChild(d);
 });
 box.scrollTop=box.scrollHeight;allChats=data.all_chats;render();
}
function render(){
 let q=document.getElementById('q').value.toLowerCase();
 let list=document.getElementById('list');list.innerHTML='';
 let aiR=document.createElement('div');aiR.className='row aiRow';
 aiR.innerHTML=`<img src="https://i.pravatar.cc/100?img=32"><div class="mid"><div class="nRow"><b>X-AI Assistant</b><span class="t">now</span></div><div class="prev">⚡ Real AI - ask anything</div></div><div><span class="badgeAI">AI</span></div>`;
 aiR.onclick=()=>openChat('ai',true,'X-AI Assistant','https://i.pravatar.cc/100?img=32',true);
 list.appendChild(aiR);
 allChats.forEach(c=>{
  if(filter=='friends'&&!c.isPrivate)return;if(filter=='groups'&&c.isPrivate)return;
  if(q&&!c.display.toLowerCase().includes(q)&&!c.last.toLowerCase().includes(q))return;
  let ring=c.hasStatus?'class="statusRing"':'';
  let row=document.createElement('div');row.className='row';
  row.innerHTML=`<div ${ring}><img src="${c.img}" style="${c.hasStatus?'border:2.5px solid var(--bg)':''}"></div><div class="mid"><div class="nRow"><b>${c.display}</b><span class="t">${c.time||'now'}</span></div><div class="prev">${c.last}</div></div><div>${c.unread>0?`<span class="badge">${c.unread}</span>`:''}</div>`;
  row.onclick=()=>openChat(c.key,c.isPrivate,c.display,c.img,false);
  list.appendChild(row);
 });
}
function setF(f){filter=f;document.querySelectorAll('.tabs button').forEach(b=>b.classList.remove('active'));document.getElementById('f-'+f).classList.add('active');render();}
async function send(){
 let t=document.getElementById('msgIn').value.trim();if(!t)return;document.getElementById('msgIn').value='';
 if(isAI){
  await fetch('/api/ai_chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({user:myNumber,name:myName,text:t,img:pB64})});
  document.getElementById('typing').style.display='block';setTimeout(()=>{document.getElementById('typing').style.display='none';load();},700);
 }else{
  let ep=isPriv?'/api/private':'/api/groups';
  await fetch(ep,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({key:curRoom,room:curRoom,user:myName,num:myNumber,text:t,img:pB64})});
 }
 load();
}
function start(){load();setInterval(()=>{if(!isAI||!document.getElementById('main').classList.contains('show')){load();}},3000);}
</script></body></html>
"""

@app.route("/")
def home(): return HTML

@app.route("/api/send_otp", methods=["POST"])
def send_otp():
    otp=str(random.randint(100000,999999))
    with lock: OTP_STORE[request.json.get("number","").strip()]=otp
    return jsonify({"ok":True,"otp":otp})

@app.route("/api/verify_otp", methods=["POST"])
def verify_otp():
    d=request.json; num=d.get("number"); otp=d.get("otp")
    with lock:
        real=OTP_STORE.get(num)
        if not real or real!=otp: return jsonify({"ok":False,"error":f"Wrong! Correct is {real}"})
        PROFILES[num]={"name":d.get("name"),"img":d.get("img")}
        OTP_STORE.pop(num,None)
    return jsonify({"ok":True})

@app.route("/api/status", methods=["GET","POST"])
def status_api():
    if request.method=="GET":
        with lock:
            all_status=[]
            for num, sts in STATUS.items():
                prof=PROFILES.get(num,{"name":num,"img":f"https://i.pravatar.cc/100?u={num}"})
                for s in sts[-5:]:
                    all_status.append({"number":num,"name":prof["name"],"img":prof["img"],"text":s["text"],"imgStatus":s.get("imgStatus"),"time":s["time"]})
            return jsonify({"statuses":all_status[::-1]})
    else:
        d=request.json; num=d.get("number")
        with lock:
            if num not in STATUS: STATUS[num]=[]
            STATUS[num].append({"text":d.get("text",""),"imgStatus":d.get("imgStatus",""),"time":datetime.now().strftime("%H:%M")})
        return jsonify({"ok":True})

def get_key(a,b): return "_".join(sorted([a,b]))

@app.route("/api/ai_chat", methods=["GET","POST"])
def ai_chat():
    user=request.args.get("user") if request.method=="GET" else request.json.get("user")
    if request.method=="GET":
        with lock:
            msgs=AI_CHATS.get(user,[{"user":"X-AI","text":"Welcome to KREST CHAT X ⚡\nI'm X-AI - Ask anything!","time":datetime.now().strftime("%H:%M"),"isAI":True}])
            chats=[{"key":"lounge","display":"Krest Lounge","last":"Welcome","isPrivate":False,"img":"https://i.pravatar.cc/100?img=12","time":"now","unread":0,"hasStatus":False}]
            for num, prof in PROFILES.items():
                if num!=user:
                    hasStatus=num in STATUS
                    chats.append({"key":get_key(user,num),"display":prof["name"],"last":"Tap to chat • profile visible","isPrivate":True,"img":prof["img"],"time":"now","unread":0,"hasStatus":hasStatus})
            for k,v in PRIVATE.items():
                if user in k and v:
                    other=k.split("_")[0] if k.split("_")[1]==user else k.split("_")[1]
                    prof=PROFILES.get(other,{"name":other,"img":f"https://i.pravatar.cc/100?u={other}"})
                    if not any(c["display"]==prof["name"] for c in chats):
                        chats.append({"key":k,"display":prof["name"],"last":v[-1]["text"][:35],"isPrivate":True,"img":prof["img"],"time":v[-1]["time"],"unread":1,"hasStatus":other in STATUS})
            return jsonify({"messages":msgs[-100:],"all_chats":chats})
    else:
        d=request.json; q=d.get("text",""); name=d.get("name","")
        with lock:
            if user not in AI_CHATS: AI_CHATS[user]=[]
            AI_CHATS[user].append({"user":name,"num":user,"text":q,"time":datetime.now().strftime("%H:%M"),"isAI":False})
            AI_CHATS[user].append({"user":"X-AI","text":ai_brain(q,name),"time":datetime.now().strftime("%H:%M"),"isAI":True})
        return jsonify({"ok":True})

@app.route("/api/groups", methods=["GET","POST"])
def groups():
    if request.method=="GET":
        with lock:
            msgs=GROUPS.get("lounge",[])
            return jsonify({"messages":msgs[-100:],"all_chats":[]})
    else:
        d=request.json
        with lock:
            if "lounge" not in GROUPS: GROUPS["lounge"]=[]
            GROUPS["lounge"].append({"user":d["user"],"num":d["num"],"text":d["text"],"time":datetime.now().strftime("%H:%M"),"img":d.get("img")})
        return jsonify({"ok":True})

@app.route("/api/private", methods=["GET","POST"])
def private_chat():
    if request.method=="GET":
        with lock:
            msgs=PRIVATE.get(request.args.get("key",""),[])
            return jsonify({"messages":msgs[-100:],"all_chats":[]})
    else:
        d=request.json; key=d.get("key")
        with lock:
            if key not in PRIVATE: PRIVATE[key]=[]
            PRIVATE[key].append({"user":d["user"],"num":d["num"],"text":d["text"],"time":datetime.now().strftime("%H:%M"),"img":d.get("img")})
        return jsonify({"ok":True})

if __name__=="__main__": app.run(host="0.0.0.0", port=10000) flask import Flask, request, jsonify
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
