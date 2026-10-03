from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return """
    <h1>KREST X IS BACK ONLINE! 🚀</h1>
    <h2>LOGIN</h2>
    <input id='user' placeholder='Username'><br><br>
    <input id='pass' type='password' placeholder='Password'><br><br>
    <button onclick="alert('Login will check Supabase here')">LOGIN (Old User)</button>
    <button onclick="alert('Signup will create account here')">SIGN UP (New User)</button>
    <p>Followers: 0 | Likes: 0 | Viewers: 0 - will show after login</p>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
