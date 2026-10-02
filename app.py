from flask import Flask, request, jsonify
import os, time

app = Flask(__name__)
messages = []
users = {}
sparks = []

@app.route('/')
def home():
    return '''
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>KRESTCHAT V5 FINAL</title>
<style>
body{margin:0;background:#000;color:#fff;font-family:Arial}
.top{background:linear-gradient(90deg,#ff00cc,#3366ff);padding:12px;text-align:center;font-size:20px;font-weight:bold;position:sticky;top:0;z-index:10}
.tabs{display:flex;background:#111;position:sticky;top:46px;z-index:9}
.tab{flex:1;padding:12px;text-align:center;cursor:pointer;border-bottom:3px solid transparent}
.tab.on{border-bottom:3px solid #ff00cc;color:#ff00cc}
.card{background:#1e1e1e;padding:12px;margin:8px;border-radius:12px}
input{width:100%;padding:10px;margin:5px 0;border:none;border-radius:8px;background:#2a2a2a;color:#fff;box-sizing:border-box}
button{padding:10px 15px;border:none;border-radius:8px;background:#ff00cc;color:#fff;font-weight:bold;cursor:pointer}
.hide{display:none}
.person{display:flex;align-items:center;gap:10px;background:#2a2a2a;padding:8px;border-radius:8px;margin:5px 0;cursor:pointer}
.dot{width:10px;height:10px;border-radius:50%;background:gray}
.dot.on{background:#00ff00;box-shadow:0 0 5px #00ff00}
.img{width:38px;height:38px;border-radius:50%;object-fit:cover;background:#444}
.m{padding:8px;margin:5px 0;border-radius:10px;background:#2a2a2a}
.v{width:100%;background:#111;border-radius:12px;overflow:hidden;margin:12px 0;border:1px solid #222}
.v video{width:100%;max-height:68vh;display:block;background:#000}
.vfoot{padding:10px;display:flex;justify-content:space-between;align-items:center}
.small{font-size:11px;color:#aaa}
.ad{background:linear-gradient(90deg,#ffcc00,#ff8800);color:#000;padding:10px;margin:8px;border-radius:10px;text-align:center;font-weight:bold}
</style>
</head>
<body>
<div class="top">KRESTCHAT V5 - SPARKS 🔥</div>
<div class="tabs">
<div id="tab1" class="tab on" onclick="showTab(1)">Chat</div>
<div id="tab2" class="tab" onclick="showTab(2)">Sparks 🔥</div>
</div>
<div class="box">

<div id="pageLogin" class="card">
<h3>Login to KRESTCHAT</h3>
<input id="p" placeholder="Phone e.g. 080...">
<input id="n" placeholder="Your Name">
<input id="ph" placeholder="Photo URL - leave empty">
<button onclick="login()" style="width:100%">Enter KRESTCHAT</button>
<p class="small">Built by DE KREST - Aba</p>
</div>

<div id="pageMain" class="hide">

<div id="pChat">
<div class="card"><div style="display:flex;gap:10px;align-items:center"><img id="myImg" class="img" src=""><b id="u"></b> <span class="dot on"></span> <button onclick="logout()" style="background:#f33">Out</button></div><div id="viewers" class="small"></div></div>
<div class="ad">📢 Advertise Your Shop Here - Chat DE KREST on WhatsApp: 0XX... Your Business Go Blow!</div>
<div class="card"><h3>People Online</h3><div id="list"></div></div>
<div class="card"><h3 id="ct">Select a person to chat</h3><div id="chat" style="height:260px;overflow:auto;background:#000;padding:8px;border-radius:10px"></div><input id="t" placeholder="Type message..."><button onclick="send()" style="width:100%;margin-top:6px">Send Message</button></div>
</div>

<div id="pSparks" class="hide">
<div class="ad">🔥 SPARKS - Our own TikTok! Post dance, comedy, football. If e blow, you blow!</div>
<div class="card">
<h3>Post a Spark - 15 sec max</h3>
<input type="file" id="vidFile" accept="video/*">
<input id="vidCap" placeholder="Caption: dance, funny, football, school...">
<button onclick="uploadSpark()" style="width:100%">Post Spark 🔥</button>
<p class="small">Write correct caption - if you like dance, app go show you more dance</p>
</div>
<div id="feed"></div>
</div>

</div>
</div>

<script>
let mePhone = localStorage.getItem("kp");
let meName = localStorage.getItem("kn");
let mePhoto = localStorage.getItem("kph");
let withP = null;
let curTab = 1;
let watched = JSON.parse(localStorage.getItem("watched") || "[]");
let likedKeys = JSON.parse(localStorage.getItem("likedKeys") || "[]");

function showTab(t){curTab=t;document.getElementById("tab1").className=t==1?"tab on":"tab";document.getElementById("tab2").className=t==2?"tab on":"tab";document.getElementById("pChat").className=t==1?"":"hide";document.getElementById("pSparks").className=t==2?"":"hide";if(t==2)loadSparks();}
function check(){if(mePhone){document.getElementById("pageLogin").className="card hide";document.getElementById("pageMain").className="";let crown=meName=="DE KREST"?" 👑 CEO":"";document.getElementById("u").innerText=meName+crown;document.getElementById("myImg").src=mePhoto||"https://via.placeholder.com/100";ping();}else{document.getElementById("pageLogin").className="card";document.getElementById("pageMain").className="hide";}}
function login(){let p=document.getElementById("p").value.trim();let n=document.getElementById("n").value.trim();let ph=document.getElementById("ph").value.trim();if(!p||!n){alert("Enter phone and name");return;}if(!ph)ph="https://via.placeholder.com/150/ff00cc/fff?text="+n[0];localStorage.setItem("kp",p);localStorage.setItem("kn",n);localStorage.setItem("kph",ph);mePhone=p;meName=n;mePhoto=ph;check();}
function logout(){localStorage.clear();location.reload();}
function ping(){fetch("/api/online",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({phone:mePhone,name:meName,photo:mePhoto})});}
function loadUsers(){fetch("/api/users").then(r=>r.json()).then(j=>{let d=document.getElementById("list");d.innerHTML="";for(let phone in j){if(phone==mePhone)continue;let u=j[phone];let on=(Date.now()/1000-u.last<40);let dot=on?"dot on":"dot";let crown=u.name=="DE KREST"?" 👑":"";d.innerHTML+="<div class=person onclick=openC('"+phone+"')><img class=img src='"+u.photo+"'><div><b>"+u.name+crown+"</b><br><span class=small>"+phone+"</span></div><span class='"+dot+"'></span></div>";}if(j[mePhone]&&j[mePhone].viewers){document.getElementById("viewers").innerHTML="👀 Viewed by: "+j[mePhone].viewers.join(", ");}});}
function openC(p){withP=p;document.getElementById("ct").innerText="Chat with "+p;fetch("/api/view",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({viewer:mePhone,viewed:p})});loadChat();}
function loadChat(){if(!withP)return;fetch("/api/get").then(r=>r.json()).then(j=>{let ch=document.getElementById("chat");ch.innerHTML="";for(let i=0;i<j.length;i++){let m=j[i];if((m.from==mePhone&&m.to==withP)||(m.from==withP&&m.to==mePhone)){let who=m.from==mePhone?"You 🔥":m.from;let tim=new Date(m.time*1000).toLocaleTimeString();ch.innerHTML+="<div class=m><b>"+who+":</b> "+m.text+"<br><span class=small>"+tim+"</span></div>";}}ch.scrollTop=ch.scrollHeight;});}
function send(){let tx=document.getElementById("t").value;if(!withP){alert("Select person");return;}if(!tx)return;fetch("/api/send",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({from:mePhone,to:withP,text:tx})}).then(()=>{document.getElementById("t").value="";loadChat();});}

function uploadSpark(){
 let f=document.getElementById("vidFile").files[0];
 let cap=document.getElementById("vidCap").value.toLowerCase();
 if(!f){alert("Select video");return;}
 if(f.size>15*1024*1024){alert("Video too big - pick <15MB");return;}
 let reader=new FileReader();
 reader.onload=function(e){
  fetch("/api/spark",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({phone:mePhone,name:meName,photo:mePhoto,caption:cap,video:e.target.result})}).then(()=>{alert("Spark posted! 🔥 Go to Sparks tab");document.getElementById("vidCap").value="";loadSparks();});
 };
 reader.readAsDataURL(f);
}

function loadSparks(){
 fetch("/api/sparks").then(r=>r.json()).then(j=>{
  let fd=document.getElementById("feed");fd.innerHTML="";
  let scored=j.map(s=>{
   let base=s.views + s.likes*5;
   let boost=0;
   for(let k of likedKeys){if(k && s.caption.includes(k)) boost+=60;}
   if(watched.includes(s.id)) base-=15;
   return {...s, _score: base+boost};
  }).sort((a,b)=>b._score-a._score);
  scored.forEach(s=>{
   let crown=s.name=="DE KREST"?" 👑":"";
   fd.innerHTML+="<div class=v><video src='"+s.video+"' controls loop playsinline onended=nextSpark()></video><div class=vfoot><div style=display:flex;gap:8px;align-items:center><img class=img src='"+s.photo+"'><div><b>"+s.name+crown+"</b><br><span class=small>"+s.caption+"</span><br><span class=small>Score: "+s._score+" | "+s.views+" views</span></div></div><div style=text-align:center><button onclick=likeSpark("+s.id+",'"+s.caption.replace(/'/g,"")+"')>❤️ "+s.likes+"</button><br><button onclick=delSpark("+s.id+") style=background:#333;margin-top:4px>🗑️</button></div></div></div>";
   fetch("/api/viewSpark",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({id:s.id})});
   if(!watched.includes(s.id)){watched.push(s.id);localStorage.setItem("watched",JSON.stringify(watched));}
  });
 });
}

function likeSpark(id,caption){
 let words=caption.split(" ");
 words.forEach(w=>{if(w.length>2 &&!likedKeys.includes(w)){likedKeys.push(w);}});
 localStorage.setItem("likedKeys",JSON.stringify(likedKeys));
 fetch("/api/like",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({id:id})}).then(()=>loadSparks());
}
function delSpark(id){if(!confirm("Delete this spark?"))return;fetch("/api/delSpark",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({id:id})}).then(()=>loadSparks());}
function nextSpark(){window.scrollBy(0,400);}

check();
setInterval(()=>{ping();loadUsers();},3000);
setInterval(()=>{if(curTab==1&&withP)loadChat();},2000);
</script>
</body>
</html>
'''

@app.route('/api/online', methods=['POST'])
def online():
    d=request.get_json()
    phone=d.get('phone')
    if phone:
        if phone not in users:
            users[phone]={'viewers':[]}
        users[phone]['name']=d.get('name')
        users[phone]['photo']=d.get('photo')
        users[phone]['last']=time.time()
        if 'viewers' not in users[phone]:
            users[phone]['viewers']=[]
    return jsonify({'ok':True})

@app.route('/api/users')
def get_users():
    return jsonify(users)

@app.route('/api/view', methods=['POST'])
def view():
    d=request.get_json()
    viewer=d.get('viewer'); viewed=d.get('viewed')
    if viewed in users and viewer!=viewed:
        if viewer not in users[viewed]['viewers']:
            users[viewed]['viewers'].append(viewer)
    return jsonify({'ok':True})

@app.route('/api/get')
def get_data():
    return jsonify(messages[-300:])

@app.route('/api/send', methods=['POST'])
def send_msg():
    d=request.get_json()
    messages.append({'from':d.get('from'),'to':d.get('to'),'text':d.get('text'),'time':time.time()})
    return jsonify({'ok':True})

@app.route('/api/spark', methods=['POST'])
def add_spark():
    d=request.get_json()
    sparks.append({'id':len(sparks),'phone':d.get('phone'),'name':d.get('name'),'photo':d.get('photo'),'caption':d.get('caption','').lower(),'video':d.get('video'),'likes':0,'views':0,'time':time.time()})
    if len(sparks)>100:
        sparks.pop(0)
    return jsonify({'ok':True})

@app.route('/api/sparks')
def get_sparks():
    def score(s):
        return s['views'] + s['likes']*5
    return jsonify(sorted(sparks, key=score, reverse=True))

@app.route('/api/viewSpark', methods=['POST'])
def view_spark():
    d=request.get_json()
    sid=d.get('id')
    for s in sparks:
        if s['id']==sid:
            s['views']+=1
    return jsonify({'ok':True})

@app.route('/api/like', methods=['POST'])
def like():
    d=request.get_json()
    sid=d.get('id')
    for s in sparks:
        if s['id']==sid:
            s['likes']+=1
    return jsonify({'ok':True})

@app.route('/api/delSpark', methods=['POST'])
def del_spark():
    d=request.get_json()
    sid=d.get('id')
    global sparks
    sparks = [s for s in sparks if s['id']!=sid]
    return jsonify({'ok':True})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 10000)))
