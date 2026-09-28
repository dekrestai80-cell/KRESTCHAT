from flask import Flask
app = Flask(__name__)

HTML = """<!DOCTYPE html>
<html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>KRESTCHAT WORLD - 10K</title>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
<style>
*{margin:0;padding:0;box-sizing:border-box;font-family:Arial}
body{height:100vh;background:#111b21;display:flex}
#app{display:flex;width:100%;height:100vh}
#sidebar{width:380px;background:#111b21;border-right:1px solid #222}
.sH{background:#202c33;padding:10px 14px;display:flex;justify-content:space-between;align-items:center}
.sH img{width:40px;height:40px;border-radius:50%}
.sH div{display:flex;gap:18px;color:#aebac1;font-size:20px}
.search{padding:8px 12px}.sBox{background:#202c33;border-radius:8px;display:flex;align-items:center;padding:8px}
.sBox input{flex:1;background:0;border:0;padding:6px;color:#fff;outline:0}
#list{flex:1;overflow-y:auto}
.item{display:flex;gap:12px;padding:12px;cursor:pointer;border-bottom:1px solid #222}
.item:hover,.item.active{background:#2a3942}
.item img{width:48px;height:48px;border-radius:50%}
.item b{color:#e9edef}.item p{color:#8696a0;font-size:13px}
#main{flex:1;display:flex;flex-direction:column;background:#0b141a}
.mH{background:#202c33;padding:10px;display:flex;align-items:center;gap:10px;color:#fff}
.mH img{width:40px;height:40px;border-radius:50%}
#msgs{flex:1;overflow-y:auto;padding:16px;display:flex;flex-direction:column;gap:8px;background:#0b141a}
.msg{max-width:65%;padding:8px 10px;border-radius:8px;font-size:14px}
.me{align-self:flex-end;background:#005c4b;color:#fff}
.other{align-self:flex-start;background:#202c33;color:#fff}
#inputBar{background:#202c33;padding:8px;display:flex;gap:8px;align-items:center}
#inputBar input{flex:1;padding:12px;border-radius:8px;border:0;outline:0;background:#2a3942;color:#fff}
#send{background:#00a884;width:44px;height:44px;border-radius:50%;border:0;color:#fff;font-size:18px}
#gate{position:fixed;inset:0;background:#111b21;display:flex;align-items:center;justify-content:center;z-index:99}
#gateBox{background:#202c33;padding:28px;border-radius:12px;width:90%;max-width:360px;text-align:center}
#gateBox input{width:100%;padding:12px;border-radius:8px;border:0;margin:10px 0;background:#2a3942;color:#fff}
#gateBox button{width:100%;padding:12px;background:#00a884;border:0;border-radius:8px;color:#fff;font-weight:bold}
@media(max-width:700px){#sidebar{width:100%}}
</style></head><body>
<div id="gate"><div id="gateBox">
<div style="font-size:50px">🌍</div><h2 style="color:#fff;margin:10px 0">KRESTCHAT WORLD</h2>
<p style="font-size:12px;color:#8696a0;margin-bottom:12px">For 10,000 People - No Download</p>
<input id="gateName" placeholder="Your name"><button onclick="enterApp()">ENTER WORLD CHAT</button>
</div></div>
<div id="app"><div id="sidebar"><div class="sH"><img src="https://i.pravatar.cc/100"><div><i class="fa-solid fa-message"></i><i class="fa-solid fa-ellipsis-vertical"></i></div></div>
<div class="search"><div class="sBox"><i class="fa-solid fa-search" style="color:#aebac1"></i><input id="searchInp" placeholder="Search world chat" oninput="render(this.value)"></div></div>
<div id="list"></div></div>
<div id="main"><div class="mH"><img id="mImg" src=""><div><b id="mName"></b><p style="font-size:11px;color:#8696a0">World Online • 10K users</p></div></div>
<div id="msgs"></div>
<div id="inputBar"><input id="msgInp" placeholder="Type message to world"><button id="send" onclick="send()"><i class="fa-solid fa-paper-plane"></i></button></div>
</div></div>
<script>
function enterApp(){let n=document.getElementById('gateName').value.trim();if(!n)return alert('Enter name');localStorage.setItem('kWorldName',n);document.getElementById('gate').style.display='none';init()}
let me=localStorage.getItem('kWorldName')||'';
let chats=JSON.parse(localStorage.getItem('kWorldChats')||'null')||[{id:0,name:'KrestAI World Group',phone:'WORLD AI',img:'https://i.pravatar.cc/100?img=12',msgs:[{t:'Welcome to KRESTCHAT WORLD 🌍',m:1}]}];
let cur=null;
function save(){localStorage.setItem('kWorldChats',JSON.stringify(chats))}
function render(f=''){let l=document.getElementById('list');l.innerHTML='';chats.filter(c=>c.name.toLowerCase().includes(f.toLowerCase())).forEach(c=>{let d=document.createElement('div');d.className='item'+(cur==c.id?' active':'');d.innerHTML=`<img src="${c.img}"><div><b>${c.name}</b><p>${c.msgs[c.msgs.length-1]?.t||''}</p></div>`;d.onclick=()=>openC(c.id);l.appendChild(d)})}
function openC(id){cur=id;let c=chats.find(x=>x.id==id);document.getElementById('mName').textContent=c.name;document.getElementById('mImg').src=c.img;render();show()}
function show(){let c=chats.find(x=>x.id==cur);if(!c)return;let m=document.getElementById('msgs');m.innerHTML='';c.msgs.forEach(x=>{let d=document.createElement('div');d.className='msg '+(x.m?'me':'other');d.textContent=x.t;m.appendChild(d)});m.scrollTop=m.scrollHeight}
function send(){let inp=document.getElementById('msgInp');let t=inp.value.trim();if(!t||cur==null)return;let c=chats.find(x=>x.id==cur);c.msgs.push({t:t,m:1});save();inp.value='';show();setTimeout(()=>{c.msgs.push({t:'World received: '+t,m:0});save();show()},800)}
function init(){if(localStorage.getItem('kWorldName'))document.getElementById('gate').style.display='none';cur=0;render();openC(0)}
init();
document.getElementById('msgInp').addEventListener('keydown',e=>{if(e.key==='Enter')send()})
</script></body></html>"""

@app.route("/")
def home():
    return HTML

if __name__ == "__main__":
    app.run()
