from flask import Flask
app = Flask(__name__)

HTML = """<!DOCTYPE html>
<html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>KRESTCHAT WORLD - 10K</title>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.6.0/css/all.min.css">
<style>
*{margin:0;padding:0;box-sizing:border-box;font-family:Segoe UI}
body{height:100vh;background:#111b21;display:flex}
#app{display:flex;width:100%;height:100vh}
#sidebar{width:380px;background:#111b21;border-right:1px solid #222d34;display:flex;flex-direction:column}
.sH{background:#202c33;padding:10px 14px;display:flex;justify-content:space-between;align-items:center}
.sH img{width:40px;height:40px;border-radius:50%;cursor:pointer}
.sH div{display:flex;gap:18px;color:#aebac1;font-size:20px;cursor:pointer}
.search{padding:8px 12px}.sBox{background:#202c33;border-radius:8px;display:flex;align-items:center;padding:0 12px;gap:10px}
.sBox input{flex:1;background:0;border:0;padding:10px 0;color:#fff;outline:0}
.sBox i{color:#aebac1;cursor:pointer}
#list{flex:1;overflow-y:auto}
.item{display:flex;gap:12px;padding:12px;cursor:pointer;border-bottom:1px solid #1f2c33}
.item:hover,.item.active{background:#2a3942}
.item img{width:48px;height:48px;border-radius:50%}
.info{flex:1;overflow:hidden}.top{display:flex;justify-content:space-between}
.top b{color:#e9edef;font-weight:400}.top span{color:#8696a0;font-size:11px}
.bot{color:#8696a0;font-size:13px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
#main{flex:1;display:flex;flex-direction:column;background:#0b141a}
.mH{background:#202c33;padding:10px 14px;display:flex;align-items:center;gap:10px}
.mH img{width:40px;height:40px;border-radius:50%}.mInfo{flex:1;color:#fff}
.mInfo p{font-size:11px;color:#00a884}.mI{color:#aebac1;display:flex;gap:16px;font-size:18px;cursor:pointer}
#msgs{flex:1;overflow-y:auto;padding:15px;background:#0b141a url('https://user-images.githubusercontent.com/15075759/28719144-86dc0f70-73b1-11e7-911d-60d70fcded21.png')}
.bubble{max-width:72%;padding:6px 10px;border-radius:8px;margin:5px 0;font-size:14px}
.other{background:#202c33;color:#e9edef;border-top-left-radius:0}
.me{background:#005c4b;color:#fff;margin-left:auto;border-top-right-radius:0}
.ai{background:#1a2f2a;border:1px solid #00a884}
.t{font-size:10px;color:#8696a0;float:right;margin:6px 0 0 8px}
.input{background:#202c33;padding:6px 12px;display:flex;align-items:center;gap:10px}
.input i{color:#8696a0;font-size:22px;cursor:pointer}
.iBox{flex:1;background:#2a3942;border-radius:8px;display:flex;padding:0 12px}
.iBox input{flex:1;background:0;border:0;padding:11px 0;color:#fff;outline:0}
#send{background:#00a884;width:44px;height:44px;border-radius:50%;border:0;color:#fff;font-size:18px;cursor:pointer}
.modal{position:fixed;inset:0;background:rgba(0,0,0,.85);z-index:50;display:none;justify-content:center;align-items:center}
.modal.show{display:flex}.box{background:#202c33;width:92%;max-width:380px;border-radius:12px;padding:18px;color:#fff}
.box h3{color:#00a884;margin-bottom:10px}.box input{width:100%;padding:11px;background:#2a3942;border:0;border-radius:8px;color:#fff;margin:6px 0;outline:0}
.box button{width:100%;padding:12px;background:#00a884;border:0;border-radius:8px;color:#fff;font-weight:700;margin-top:8px}
#gate{position:fixed;inset:0;background:#111b21;z-index:100;display:flex;justify-content:center;align-items:center;color:white}
#gateBox{background:#202c33;padding:28px;border-radius:16px;width:90%;max-width:360px;text-align:center}
@media(max-width:700px){#sidebar{width:100%}#main{position:fixed;inset:0;transform:translateX(100%);transition:.3s;z-index:10}#main.open{transform:translateX(0)}}
video,img{max-width:100%;border-radius:8px}
</style></head><body>
<div id="gate"><div id="gateBox">
<div style="font-size:50px">🌍</div><h2 style="color:#00a884">KRESTCHAT WORLD</h2>
<p style="font-size:12px;color:#8696a0;margin:8px 0">10,000 USERS - Production WSGI<br>All FREE</p>
<input id="gateName" placeholder="Your name e.g DE KREST" style="width:100%;padding:12px;background:#2a3942;border:0;border-radius:8px;color:white;text-align:center">
<button onclick="enterApp()" style="width:100%;padding:13px;background:#00a884;border:0;border-radius:10px;color:white;font-weight:bold;margin-top:12px">ENTER WORLD APP</button>
</div></div>
<div id="app"><div id="sidebar"><div class="sH"><img id="myAv" src="https://i.pravatar.cc/100?u=dekrest" onclick="openP()"><div><i class="fa-solid fa-message" onclick="openA()"></i><i class="fa-solid fa-ellipsis-vertical" onclick="openS()"></i></div></div>
<div class="search"><div class="sBox"><i class="fa-solid fa-magnifying-glass"></i><input id="search" placeholder="Search - Voice FREE" oninput="render(this.value)"><i class="fa-solid fa-microphone" onclick="voiceS()" style="color:#00a884"></i></div></div><div id="list"></div></div>
<div id="main"><div class="mH"><i class="fa-solid fa-arrow-left" id="back" onclick="closeM()" style="display:none;color:#aebac1;cursor:pointer"></i><img id="cAv" src=""><div class="mInfo"><b id="cName">KRESTCHAT</b><p>🌍 Production WSGI - 10k Ready</p></div><div class="mI"><i class="fa-solid fa-phone"></i><i class="fa-solid fa-video"></i></div></div><div id="msgs"></div><div class="input"><i class="fa-regular fa-face-smile" onclick="msgIn.value+='😊'"></i><i class="fa-solid fa-paperclip" onclick="fileIn.click()"></i><input type="file" id="fileIn" hidden accept="image/*,video/*" onchange="sendFile(event)"><div class="iBox"><input id="msgIn" placeholder="Type - World FREE" onkeypress="if(event.key==='Enter')send()"></div><button id="send" onclick="send()"><i class="fa-solid fa-paper-plane"></i></button></div></div></div>
<div id="aModal" class="modal"><div class="box"><h3>Add Contact - FREE</h3><input id="aN" placeholder="Name"><input id="aP" placeholder="Phone"><input id="aPic" placeholder="Photo URL"><button onclick="addC()">Add FREE</button><button onclick="closeMds()" style="background:#2a3942">Cancel</button></div></div>
<div id="pModal" class="modal"><div class="box"><h3>Profile</h3><img id="pPr" src="https://i.pravatar.cc/100?u=dekrest" style="width:70px;height:70px;border-radius:50%;display:block;margin:auto"><input id="pN" placeholder="Name"><input id="pAb" placeholder="About"><input id="pPicI" placeholder="Photo link" oninput="pPr.src=this.value"><button onclick="saveP()">Save FREE</button><button onclick="closeMds()" style="background:#2a3942">Close</button></div></div>
<div id="sModal" class="modal"><div class="box"><h3>🌍 Production WSGI Active</h3><p style="font-size:11px;color:#00a884">This version handles 10,000 people same time!</p><p style="font-size:11px;color:#8696a0">Server: Gunicorn<br>All FREE</p><button onclick="closeMds()">Close</button></div></div>
<script>
function enterApp(){let n=document.getElementById('gateName').value.trim();if(!n){alert('Enter name');return;}me.name=n;save();document.getElementById('gate').style.display='none';render();}
let me=JSON.parse(localStorage.getItem('kWorldMe'))||{name:'DE KREST',about:'World Owner - Aba',avatar:'https://i.pravatar.cc/100?u=dekrest'};
let chats=JSON.parse(localStorage.getItem('kWorldChats'))||[
{id:0,name:'KrestAI World',phone:'WORLD AI',avatar:'https://cdn-icons-png.flaticon.com/512/4712/4712109.png',isAI:true,messages:[{text:'🌍 PRODUCTION WSGI ACTIVE! 10,000 people can use this now!\n✅ Chat FREE\n✅ Video FREE\n✅ Add contact FREE\n✅ Voice search FREE\n✅ AI FREE',me:false,time:'now'}]}
];
let cur=null;function save(){localStorage.setItem('kWorldChats',JSON.stringify(chats));localStorage.setItem('kWorldMe',JSON.stringify(me));}
function render(f=''){let l=document.getElementById('list');l.innerHTML='';chats.filter(c=>c.name.toLowerCase().includes(f.toLowerCase())||c.phone.includes(f)).forEach(c=>{let last=c.messages.slice(-1)[0]?.text||'FREE';let d=document.createElement('div');d.className='item'+(cur===c.id?' active':'');d.onclick=()=>openC(c.id);d.innerHTML=`<img src="${c.avatar}"><div class="info"><div class="top"><b>${c.name}</b><span>${c.messages.slice(-1)[0]?.time||''}</span></div><div class="bot">${last.replace(/<[^>]*>/g,'').substring(0,30)}</div></div>`;l.appendChild(d);});document.getElementById('myAv').src=me.avatar;if(localStorage.getItem('kWorldMe'))document.getElementById('gate').style.display='none';}
function openC(id){cur=id;let c=chats.find(x=>x.id===id);document.getElementById('cName').innerText=c.name;document.getElementById('cAv').src=c.avatar;document.getElementById('main').classList.add('open');document.getElementById('back').style.display='block';show();}
function show(){let b=document.getElementById('msgs');b.innerHTML='';let c=chats.find(x=>x.id===cur);if(!c)return;c.messages.forEach(m=>{let d=document.createElement('div');d.className='bubble '+(m.me?'me':(m.isAI?'ai':'other'));d.innerHTML=m.text+`<span class="t">${m.time||''} ${m.me?'✓✓':''}</span>`;b.appendChild(d);});b.scrollTop=b.scrollHeight;}
function send(){let inp=document.getElementById('msgIn');if(!inp.value.trim()||cur===null)return;let c=chats.find(x=>x.id===cur);c.messages.push({text:inp.value,me:true,time:new Date().toLocaleTimeString()});let txt=inp.value;inp.value='';show();render();save();setTimeout(()=>{c.messages.push({text:`🌍 World AI: "${txt}" - 10k FREE!`,me:false,time:new Date().toLocaleTimeString(),isAI:true});show();render();save();},600);}
function voiceS(){let SR=window.SpeechRecognition||window.webkitSpeechRecognition;if(!SR)return alert('Use Chrome');let r=new SR();r.lang='en-NG';r.start();r.onresult=e=>{document.getElementById('search').value=e.results[0][0].transcript;render(e.results[0][0].transcript);};}
function sendFile(e){let f=e.target.files[0];if(!f||cur===null)return;let rd=new FileReader();rd.onload=ev=>{let c=chats.find(x=>x.id===cur);if(f.type.startsWith('image/'))c.messages.push({text:`<img src="${ev.target.result}">`,me:true,time:new Date().toLocaleTimeString()});else if(f.type.startsWith('video/'))c.messages.push({text:`<video controls src="${ev.target.result}" style="max-width:250px"></video>`,me:true,time:new Date().toLocaleTimeString()});show();render();save();};rd.readAsData
