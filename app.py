from flask import Flask, request, redirect
import random, os

app = Flask(__name__)

DB = {}

@app.route("/")
def home():
    return """
<html><head><meta name="viewport" content="width=device-width, initial-scale=1">
<style>
body{background:#000;color:#fff;font-family:Arial;padding:20px}
.box{max-width:380px;margin:40px auto;background:#111;padding:25px;border-radius:20px;border:1px solid #222}
input{width:100%;padding:14px;margin:8px 0;border-radius:10px;border:none;background:#222;color:#fff}
button{width:100%;padding:14px;border-radius:10px;border:none;background:#FE2C55;color:#fff;font-weight:bold;font-size:16px}
</style></head><body>
<div class="box">
<h1 style="text-align:center">KREST X 🔥</h1>
<p style="text-align:center;color:#888">Create Account</p>
<form action="/signup">
<input name="u" placeholder="Username e.g Raphael1234" required>
<input name="p" placeholder="Phone e.g 0911..." required>
<button>CREATE ACCOUNT</button>
</form>
<hr style="margin:20px 0;border:0;border-top:1px solid #222">
<p style="text-align:center;color:#888">Already have account?</p>
<form action="/login">
<input name="u" placeholder="Username" required>
<input name="p" placeholder="Phone" required>
<button style="background:#222">LOGIN</button>
</form>
</div></body></html>
"""

@app.route("/signup")
def signup():
    u = request.args.get("u")
    p = request.args.get("p")
    if not u or not p:
        return redirect("/")
    # Save user
    DB[p] = {"username": u, "phone": p, "followers": 0, "likes": 0, "viewers": 0, "posts": ["Welcome to KREST X!"]}
    otp = random.randint(1000,9999)
    return f"""
<html><body style="background:#000;color:#fff;font-family:Arial;padding:20px">
<div style="max-width:380px;margin:40px auto;background:#111;padding:25px;border-radius:20px;text-align:center">
<h2>OTP: {otp}</h2>
<p>For {u} - {p}</p>
<p style="color:#888">Copy OTP then tap below</p>
<a href="/me?phone={p}" style="display:block;background:#FE2C55;color:#fff;padding:14px;border-radius:10px;text-decoration:none;font-weight:bold">VERIFY & GO TO ME PAGE</a>
</div></body></html>
"""

@app.route("/login")
def login():
    u = request.args.get("u")
    p = request.args.get("p")
    # If not exist, auto-create (so login never fails)
    if p not in DB:
        DB[p] = {"username": u, "phone": p, "followers": random.randint(0,5), "likes": random.randint(0,10), "viewers": random.randint(10,50), "posts": []}
    return redirect(f"/me?phone={p}")

@app.route("/me")
def me():
    phone = request.args.get("")
    if phone not in DB:
        return redirect("/")
    d = DB[phone]
    posts_html = "".join([f"<div style='background:#222;padding:12px;margin:8px 0;border-radius:10px'>🎥 {x}</div>" for x in d["posts"]])
    return f"""
<html><head><meta name="viewport" content="width=device-width, initial-scale=1">
<style>
body{{background:#000;color:#fff;font-family:Arial;margin:0}}
.top{{padding:20px;text-align:center}}
.stats{{display:flex;justify-content:space-around;background:#111;padding:15px;margin:10px;border-radius:15px}}
.b{{font-size:22px;font-weight:bold}}.l{{color:#888;font-size:12px}}
.btn{{background:#FE2C55;color:#fff;padding:12px 25px;border-radius:20px;border:none;font-weight:bold;margin:5px}}
</style></head><body>
<div class="top">
<h2>{d['username']}</h2>
<p style="color:#888">@{d['username'].lower()} • {d['phone']}</p>
</div>
<div style="padding:0 15px">
<div class="stats">
<div><div class="b">{d['followers']}</div><div class="l">Followers</div></div>
<div><div class="b">{d['likes']}</div><div class="l">Likes</div></div>
<div><div class="b">{d['viewers']}</div><div class="l">Viewers</div></div>
</div>
<center style="margin:15px">
<button class="btn" onclick="let t=prompt('What are you posting?'); if(t) location.href='/post?phone={phone}&text='+encodeURIComponent(t)">+ POST</button>
<button class="btn" style="background:#222" onclick="location.href='/live?phone={phone}'">🔴 GO LIVE</button>
</center>
<h3>Your Posts ({len(d['posts'])})</h3>
{posts_html}
<br><a href="/" style="color:#555">Logout / Create New</a>
</div>
</body></html>
"""

@app.route("/post")
def post():
    phone = request.args.get("phone")
    text = request.args.get("text")
    if phone in DB and text:
        DB[phone]["posts"].append(text)
        DB[phone]["likes"] += random.randint(1,5)
        DB[phone]["viewers"] += random.randint(5,20)
        DB[phone]["followers"] += random.randint(0,1)
    return redirect(f"/me?phone={phone}")

@app.route("/live")
def live():
    phone = request.args.get("phone")
    if phone in DB:
        DB[phone]["viewers"] += random.randint(20,100)
    return redirect(f"/me?phone={phone}")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
