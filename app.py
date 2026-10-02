from flask import Flask, request, jsonify, render_template_string
import requests

app = Flask(__name__)

# --- KREST X FOREVER KEYS ---
SUPABASE_URL = "https://vbbfhsafshqjjnkogsro.supabase.co"
SUPABASE_KEY = "sb_publishable_Y0uv406ne10zTrtLakbeAA_lMVrh8EQ"
# ---------------------------

HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=representation"
}

HTML = """
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>KREST X</title>
<style>
body{background:#000;color:#fff;font-family:system-ui;margin:0}
.top{padding:14px;text-align:center;font-weight:900;font-size:24px;border-bottom:1px solid #222;position:sticky;top:0;background:#000;z-index:10;letter-spacing:1px}
.feed{max-width:420px;margin:0 auto}
.card{border-bottom:1px solid #222;padding:14px}
video{width:100%;border-radius:14px;background:#111;max-height:72vh}
.actions{display:flex;gap:12px;margin-top:10px}
.btn{background:#111;border:1px solid #333;color:#fff;padding:7px 14px;border-radius:20px;font-weight:700}
.post-box{padding:14px;border:1px solid #333;margin:14px;border-radius:14px;background:#0a0a0a}
input,textarea{width:100%;background:#111;color:#fff;border:1px solid #333;padding:11px;border-radius:10px;margin:7px 0;box-sizing:border-box}
.postBtn{width:100%;background:#fff;color:#000;font-weight:900;padding:13px;border-radius:30px;border:none;margin-top:8px}
small{color:#777}
</style>
</head>
<body>
<div class="top">KREST X ✨</div>
<div class="feed">
  <div class="post-box">
    <small>POST A SPARK - Lives forever</small>
    <input id="name" placeholder="Your name - DE KREST" value="DE KREST">
    <input id="country" placeholder="Country - Nigeria" value="Nigeria">
    <textarea id="caption" placeholder="What's happening?"></textarea>
    <input id="video_url" placeholder="Video URL (mp4 link or leave empty)">
    <button class="postBtn" onclick="postSpark()">POST SPARK 🔥</button>
  </div>
  <div id="feed">Loading sparks...</div>
</div>
<script>
async function load(){
 let r = await fetch('/api/sparks');
 let data = await r.json();
 if(!Array.isArray(data)){document.getElementById('feed').innerHTML='Error loading';return;}
 let html='';
 data.reverse().forEach(s=>{
  html+=`<div class="card">
    ${s.video_url?`<video src="${s.video_url}" controls playsinline loop></video>`:''}
    <div style="margin-top:8px"><b>${s.name||'Anon'}</b> • ${s.country||''}</div>
    <div style="margin:4px 0">${s.caption||''}</div>
    <div class="actions">
     <button class="btn" onclick="like(${s.id},${s.likes||0})">❤️ ${s.likes||0}</button>
     <button class="btn">👁️ ${s.views||0}</button>
    </div>
  </div>`;
 });
 document.getElementById('feed').innerHTML=html||'<p style="text-align:center;color:#555">No sparks yet. Be first!</p>';
}
async function postSpark(){
 let caption = document.getElementById('caption').value;
 if(!caption && !document.getElementById('video_url').value){alert('Add caption or video');return;}
 let body={
  name:document.getElementById('name').value||'DE KREST',
  country:document.getElementById('country').value||'Nigeria',
  caption:caption,
  video_url:document.getElementById('video_url').value
 };
 let btn=document.querySelector('.postBtn'); btn.innerText='Posting...';
 await fetch('/api/sparks',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)});
 document.getElementById('caption').value=''; document.getElementById('video_url').value='';
 btn.innerText='POST SPARK 🔥';
 load();
}
async function like(id,likes){
 await fetch(`/api/like/${id}`,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({likes:likes+1})});
 load();
}
load();
</script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML)

@app.route('/api/sparks')
def get_sparks():
    r = requests.get(f"{SUPABASE_URL}/rest/v1/sparks?select=*&order=id.desc", headers=HEADERS)
    return jsonify(r.json())

@app.route('/api/sparks', methods=['POST'])
def add_spark():
    data = request.json
    r = requests.post(f"{SUPABASE_URL}/rest/v1/sparks", headers=HEADERS, json=data)
    return jsonify(r.json()), r.status_code

@app.route('/api/like/<int:sid>', methods=['POST'])
def like_spark(sid):
    likes = request.json.get('likes',0)
    r = requests.patch(f"{SUPABASE_URL}/rest/v1/sparks?id=eq.{sid}", headers=HEADERS, json={"likes":likes})
    return jsonify({"ok":True})

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
