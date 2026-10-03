from flask import Flask, request, redirect
import os, random

app = Flask(__name__)

# This is our database for now - simple dictionary
USERS = {}

@app.route("/")
def home():
    # This is your landing page like TikTok login
    return """
    <html>
    <head><meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
    body{background:black;color:white;font-family:Arial;text-align:center;padding-top:50px}
    input{padding:15px;width:80%;max-width:300px;border-radius:10px;border:none;margin:10px;background:#222;color:white}
    button{padding:15px;width:80%;max-width:300px;border-radius:10px;border:none;background:#FE2C55;color:white;font-weight:bold;font-size:18px}
    </style>
    </head>
    <body>
    <h1>KREST X</h1>
    <p style="color:#888">Day 0 - We Start Here</p>
    <form action="/create">
    <input name="name" placeholder="Your name e.g DE KREST" required><br>
    <input name="phone" placeholder="Your phone e.g 0913..." required><br>
    <button>CREATE MY ACCOUNT</button>
    </form>
    </body>
    </html>
    """

@app.route("/create")
def create():
    name = request.args.get("name")
    phone = request.args.get("phone")
    if not name or not phone:
        return redirect("/")

    # Save user
    USERS[phone] = {"name": name, "phone": phone, "posts": 0, "likes": 0}

    # Go to ME page
    return redirect(f"/me?phone={phone}")

@app.route("/me")
def me():
    phone = request.args.get("phone")
    if phone not in USERS:
        return redirect("/")

    user = USERS[phone]
    return f"""
    <html>
    <head><meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
    body{{background:black;color:white;font-family:Arial;padding:20px}}
   .card{{background:#111;padding:20px;border-radius:20px;text-align:center;max-width:350px;margin:0 auto}}
   .num{{font-size:28px;font-weight:bold}}.label{{color:#888;font-size:12px}}
   .row{{display:flex;justify-content:space-around;margin:20px 0}}
    </style>
    </head>
    <body>
    <div class="card">
    <h2>{user['name']}</h2>
    <p style="color:#888">@{user['name'].lower().replace(' ','') } • {user['phone']}</p>
    <div class="row">
    <div><div class="num">{user['posts']}</div><div class="label">Posts</div></div>
    <div><div class="num">{user['likes']}</div><div class="label">Likes</div></div>
    <div><div class="num">0</div><div class="label">Followers</div></div>
    </div>
    <p style="color:#0f0">✅ ACCOUNT WORKS!</p>
    <p>This is ME page. It is showing!</p>
    <br>
    <a href="/" style="color:#555">Logout</a>
    </div>
    </body>
    </html>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
