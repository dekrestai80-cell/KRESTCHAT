from flask import Flask, request, jsonify, render_template_string
from supabase import create_client
from datetime import date
import os 

SUPABASE_URL = "https://vbbfhsafshqjjnkogsro.supabase.co"
SUPABASE_KEY = "sb_publishable_Y0uv406ne10zTrtLakbeAA_lMVrh8EQ"
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

app = Flask(__name__)

FOLLOWERS_TO_GO_LIVE = 100

HTML = """
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>KREST X WORLD</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#000;color:#fff;font-family:Arial;min-height:100vh;display:flex;justify-content:center;padding:15px}
.card{background:#111;width:100%;max-width:420px;border-radius:20px;padding:25px;border:1px solid #222;height:fit-content}
label{font-size:11px;color:#aaa;margin-top:12px;display:block}
input{width:100%;padding:14px;margin:5px 0 10px 0;border-radius:12px;background:#1a1a1a;color:#fff;border:1px solid #333;font-size:16px}
button{width:100%;padding:16px;background:#fe2c55;color:#fff;border:none;border-radius:12px;font-size:17px;font-weight:bold;margin-top:12px}
#countryList{max-height:220px;overflow-y:auto;background:#1a1a1a;border:1px solid #333;border-radius:12px;display:none;position:absolute;width:100%;z-index:99}
.item{padding:12px;border-bottom:1px solid #222;cursor:pointer}.item:hover{background:#222}
.rel{position:relative}.sel{color:#fe2c55;font-size:13px;font-weight:bold}
</style>
</head>
<body>
<div class="card">
<h2 style="text-align:center">🌍 KREST X WORLD</h2>
<p style="text-align:center;color:#aaa;margin-bottom:15px">240 Countries + Live Gate</p>

<label>COUNTRY / REGION</label>
<div class="rel">
<input id="search" placeholder="Search country e.g Nigeria, USA" oninput="filterC()" onclick="showList()" autocomplete="off">
<div id="countryList"></div>
</div>
<div id="sel" class="sel">Selected: 🇳🇬 Nigeria +234</div>
<input type="hidden" id="ccode" value="+234">
<input type="hidden" id="cname" value="Nigeria">

<label>PHONE NUMBER</label>
<input id="phone" type="tel" placeholder="080 1234 5678">

<label>DATE OF BIRTH</label>
<input id="dob" type="date">

<label>USERNAME</label>
<input id="user" placeholder="dekrest">

<label>PASSWORD</label>
<input id="pass" type="password" placeholder="Create password">

<button onclick="signup()">CREATE ACCOUNT 🚀</button>
<p id="msg" style="text-align:center;margin-top:12px;font-size:14px"></p>

<div style="text-align:center;margin-top:18px">
<a href="/lives" style="color:#fe2c55;text-decoration:none">🔴 View Lives</a> |
<a href="/go-live?u=test" style="color:#aaa;text-decoration:none">Test Go Live</a>
</div>
</div>

<script>
const allCountries=[
{n:"Afghanistan",f:"🇦🇫",c:"+93"},{n:"Albania",f:"🇦🇱",c:"+355"},{n:"Algeria",f:"🇩🇿",c:"+213"},{n:"Andorra",f:"🇦🇩",c:"+376"},{n:"Angola",f:"🇦🇴",c:"+244"},{n:"Argentina",f:"🇦🇷",c:"+54"},{n:"Australia",f:"🇦🇺",c:"+61"},{n:"Austria",f:"🇦🇹",c:"+43"},{n:"Bangladesh",f:"🇧🇩",c:"+880"},{n:"Belgium",f:"🇧🇪",c:"+32"},{n:"Brazil",f:"🇧🇷",c:"+55"},{n:"Canada",f:"🇨🇦",c:"+1"},{n:"China",f:"🇨🇳",c:"+86"},{n:"Denmark",f:"🇩🇰",c:"+45"},{n:"Egypt",f:"🇪🇬",c:"+20"},{n:"Ethiopia",f:"🇪🇹",c:"+251"},{n:"France",f:"🇫🇷",c:"+33"},{n:"Germany",f:"🇩🇪",c:"+49"},{n:"Ghana",f:"🇬🇭",c:"+233"},{n:"India",f:"🇮🇳",c:"+91"},{n:"Indonesia",f:"🇮🇩",c:"+62"},{n:"Italy",f:"🇮🇹",c:"+39"},{n:"Japan",f:"🇯🇵",c:"+81"},{n:"Kenya",f:"🇰🇪",c:"+254"},{n:"Mexico",f:"🇲🇽",c:"+52"},{n:"Morocco",f:"🇲🇦",c:"+212"},{n:"Nigeria",f:"🇳🇬",c:"+234"},{n:"Pakistan",f:"🇵🇰",c:"+92"},{n:"Philippines",f:"🇵🇭",c:"+63"},{n:"Portugal",f:"🇵🇹",c:"+351"},{n:"Russia",f:"🇷🇺",c:"+7"},{n:"Saudi Arabia",f:"🇸🇦",c:"+966"},{n:"South Africa",f:"🇿🇦",c:"+27"},{n:"Spain",f:"🇪🇸",c:"+34"},{n:"Tanzania",f:"🇹🇿",c:"+255"},{n:"Turkey",f:"🇹🇷",c:"+90"},{n:"UAE",f:"🇦🇪",c:"+971"},{n:"UK",f:"🇬🇧",c:"+44"},{n:"USA",f:"🇺🇸",c:"+1"},{n:"Uganda",f:"🇺🇬",c:"+256"},{n:"Ukraine",f:"🇺🇦",c:"+380"},{n:"Zambia",f:"🇿🇲",c:"+260"},{n:"Zimbabwe",f:"🇿🇼",c:"+263"}
];
function showList(){document.getElementById('countryList').style.display='block'; render(allCountries)}
function render(list){let h=''; list.forEach(o=>{h+=`<div class='item' onclick="pick('${o.c}','${o.n}','${o.f}')">${o.f} ${o.n} ${o.c}</div>`}); document.getElementById('countryList').innerHTML=h;}
function filterC(){let q=document.getElementById('search').value.toLowerCase(); let f=allCountries.filter(o=>o.n.toLowerCase().includes(q)||o.c.includes(q)); render(f);}
function pick(code,name,flag){document.getElementById('ccode').value=code; document.getElementById('cname').value=name; document.getElementById('sel').innerText=`Selected: ${flag} ${name} ${code}`; document.getElementById('search').value=`${flag} ${name} ${code}`; document.getElementById('countryList').style.display='none';}
function signup(){
 let p={country_code:document.getElementById('ccode').value,country_name:document.getElementById('cname').value,phone:document.getElementById('phone').value,date_of_birth:document.getElementById('dob').value,username:document.getElementById('user').value,password:document.getElementById('pass').value};
 if(!p.phone||!p.date_of_birth||!p.username||!p.password){document.getElementById('msg').innerText='❌ Fill all fields!';return;}
 document.getElementById('msg').innerText='Creating...';
 fetch('/api/signup',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(p)})
.then(r=>r.json()).then(d=>{document.getElementById('msg').innerText=d.message;});
}
render(allCountries);
</script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML)

@app.route('/go-live')
def go_live():
    username = request.args.get('u', 'test')
    followers = 0
    try:
        res = supabase.table("profiles").select("*").eq("username", username).execute()
        if res.data:
            followers = res.data[0].get('followers_count', 0) or 0
    except:
        followers = 0

    if followers < FOLLOWERS_TO_GO_LIVE:
        return render_template_string(f"""
        <body style="background:#000;color:#fff;font-family:Arial;padding:20px;text-align:center">
        <div style="background:#111;max-width:400px;margin:50px auto;padding:30px;border-radius:20px">
        <h2>🔒 Go LIVE Locked</h2>
        <p style="font-size:50px">🔴</p>
        <h3>Need {FOLLOWERS_TO_GO_LIVE} followers</h3>
        <p>You have <b>{followers}</b></p>
        <div style="background:#222;height:10px;border-radius:10px;margin:20px 0">
        <div style="background:#fe2c55;height:10px;width:{min(100, int(followers/FOLLOWERS_TO_GO_LIVE*100))}%;border-radius:10px"></div>
        </div>
        <p>Need {FOLLOWERS_TO_GO_LIVE - followers} more</p>
        <a href="/" style="display:block;padding:12px;background:#333;color:#fff;border-radius:10px;text-decoration:none;margin-top:20px">Back Home</a>
        </div></body>
        """)
    else:
        return render_template_string(f"""
        <body style="background:#000;color:#fff;font-family:Arial;padding:20px">
        <div style="background:#111;max-width:400px;margin:30px auto;padding:25px;border-radius:20px">
        <h2>🔴 You Can Go LIVE!</h2>
        <p>@{username} - {followers} followers ✅</p>
        <input id="title" placeholder="My Live Title" style="width:100%;padding:14px;background:#1a1a1a;color:#fff;border:1px solid #333;border-radius:10px;margin:10px 0">
        <button onclick="start()" style="width:100%;padding:16px;background:#fe2c55;color:#fff;border:none;border-radius:12px">START LIVE 🔴</button>
        <p id="msg"></p>
        <script>
        function start(){{
          fetch('/api/start-live',{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify({{username:'{username}',title:document.getElementById('title').value}})}})
        .then(r=>r.json()).then(d=>{{document.getElementById('msg').innerText=d.message}})
        }}
        </script>
        </div></body>
        """)

@app.route('/lives')
def lives():
    try:
        data = supabase.table("live_streams").select("*").eq("is_live", True).execute()
        html = "<body style='background:#000;color:#fff;font-family:Arial;padding:15px'><h2 style='text-align:center'>🔴 LIVE NOW</h2><div style='max-width:500px;margin:0 auto'>"
        if not data.data:
            html += "<p style='text-align:center;color:#aaa;margin-top:50px'>No live now<br>Need 100 followers to go live!</p>"
        for l in data.data:
            html += f"<div style='background:#111;padding:15px;margin:10px 0;border-radius:12px'><b>@{l['username']}</b> - {l.get('title','Live')} 🔴</div>"
        html += "<div style='text-align:center;margin-top:20px'><a href='/' style='color:#fe2c55'>Home</a></div></div></body>"
        return html
    except Exception as e:
        return f"Error: {e}"

@app.route('/api/signup', methods=['POST'])
def api_signup():
    d = request.json
    try:
        dob = date.fromisoformat(d['date_of_birth'])
        today = date.today()
        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
        if age < 13:
            return jsonify({"success": False, "message": f"Must be 13+ You are {age}"})
    except:
        return jsonify({"success": False, "message": "Invalid DOB"})
    try:
        supabase.table("profiles").insert({
            "username": d['username'],
            "password": d['password'],
            "phone": d['phone'],
            "country_code": d['country_code'],
            "country_name": d['country_name'],
            "date_of_birth": d['date_of_birth'],
            "age": age,
            "followers_count": 0,
            "is_live": False
        }).execute()
        return jsonify({"success": True, "message": f"Created! {d['country_name']} {d['country_code']}{d['phone']} Age {age}"})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)[:150]})

@app.route('/api/start-live', methods=['POST'])
def api_start():
    d = request.json
    try:
        supabase.table("live_streams").insert({
            "username": d['username'],
            "title": d.get('title', 'My Live'),
            "is_live": True,
            "viewers": 0
        }).execute()
        supabase.table("profiles").update({"is_live": True}).eq("username", d['username']).execute()
        return jsonify({"success": True, "message": "You are LIVE! 🔴"})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
