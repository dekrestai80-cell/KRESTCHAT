from flask import Flask, request, jsonify, render_template
from supabase import create_client
import os

app = Flask(__name__)

# Your Supabase keys - put them here
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.route("/")
def home():
    return render_template("index.html")

# LOGIN for OLD users like Raphael1234
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    user = supabase.table("profiles").select("*").eq("username", data["username"]).eq("password", data["password"]).execute()
    if user.data:
        return jsonify({"success": True, "user": user.data[0]})
    else:
        return jsonify({"success": False, "message": "Wrong username or password"})

# SIGN UP for NEW users
@app.route("/signup", methods=["POST"])
def signup():
    data = request.json
    try:
        new_user = supabase.table("profiles").insert({
            "username": data["username"],
            "phone": data.get("phone"),
            "password": data.get("password"),
            "followers_count": 0,
            "following_count": 0,
            "likes_count": 0,
            "is_live": False
        }).execute()
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
