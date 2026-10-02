from flask import Flask, request, jsonify, render_template_string
from supabase import create_client
from datetime import date
import os

SUPABASE_URL = "https://vbbfhsafshqjjnkogsro.supabase.co"
SUPABASE_KEY = "sb_publishable_Y0uv406ne10zTrtLakbeAA_lMVrh8EQ"
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>KREST X WORLD</title>
<style>
body{margin:0;background:#000;color:#fff;font-family:Arial;padding:20px}
.card{background:#111;padding:20px;border-radius:16px;max-width:400px;margin:0 auto;border:1px solid #222}
input,select{width:100%;padding:14px;margin:8px 0;border-radius:12px;background:#1a1a1a;color:#fff;border:1px solid #333;font-size:16px;box-sizing:border-box}
button{width:100%;padding:15px;background:#fe2c55;color:#fff;border:none;border-radius:12px;font-size:18px;font-weight:bold;margin-top:15px}
#countryList{max-height:250px;overflow-y:auto;background:#1a1a1a;border:1px solid #333;border-radius:10px;display:none;position:absolute;width:calc(100% - 40px);z-index:100}
.item{padding:12px;border-bottom:1px solid #222;cursor:pointer} .item:hover{background:#222}
.selected{color:#fe2c55;font-weight:bold;margin:5px 0}
h2{text-align:center} label{font-size:13px;color:#aaa;margin-top:10px;display:block}
</style>
</head>
<body>
<div class="card">
<h2>🌍 KREST X</h2>
<p style="text-align:center;color:#aaa">Create account - World Edition</p>

<label>Country / Region</label>
<div style="position:relative">
<input id="search" placeholder="🔍 Search country - e.g. Nigeria, USA..." oninput="filterC()" onclick="showList()" autocomplete="off">
<div id="countryList"></div>
</div>
<div id="sel" class="selected">Selected: 🇳🇬 Nigeria +234</div>
<input type="hidden" id="ccode" value="+234">
<input type="hidden" id="cname" value="Nigeria">

<label>Phone Number</label>
<input id="phone" type="tel" placeholder="080 1234 5678">

<label>Date of Birth</label>
<input id="dob" type="date" max="2013-10-02">

<label>Username</label>
<input id="user" placeholder="dekrest">

<label>Password</label>
<input id="pass" type="password" placeholder="Create password">

<button onclick="signup()">CREATE ACCOUNT 🚀</button>
<p style="text-align:center;margin-top:15px"><a href="/login" style="color:#fe2c55">Already have account? Login</a></p>
<p id="msg" style="text-align:center;margin-top:10px"></p>
</div>

<script>
const allCountries=[
{n:"Afghanistan",f:"🇦🇫",c:"+93"},{n:"Albania",f:"🇦🇱",c:"+355"},{n:"Algeria",f:"🇩🇿",c:"+213"},{n:"Andorra",f:"🇦🇩",c:"+376"},{n:"Angola",f:"🇦🇴",c:"+244"},{n:"Antigua and Barbuda",f:"🇦🇬",c:"+1"},{n:"Argentina",f:"🇦🇷",c:"+54"},{n:"Armenia",f:"🇦🇲",c:"+374"},{n:"Australia",f:"🇦🇺",c:"+61"},{n:"Austria",f:"🇦🇹",c:"+43"},{n:"Azerbaijan",f:"🇦🇿",c:"+994"},{n:"Bahamas",f:"🇧🇸",c:"+1"},{n:"Bahrain",f:"🇧🇭",c:"+973"},{n:"Bangladesh",f:"🇧🇩",c:"+880"},{n:"Barbados",f:"🇧🇧",c:"+1"},{n:"Belarus",f:"🇧🇾",c:"+375"},{n:"Belgium",f:"🇧🇪",c:"+32"},{n:"Belize",f:"🇧🇿",c:"+501"},{n:"Benin",f:"🇧🇯",c:"+229"},{n:"Bhutan",f:"🇧🇹",c:"+975"},{n:"Bolivia",f:"🇧🇴",c:"+591"},{n:"Bosnia",f:"🇧🇦",c:"+387"},{n:"Botswana",f:"🇧🇼",c:"+267"},{n:"Brazil",f:"🇧🇷",c:"+55"},{n:"Brunei",f:"🇧🇳",c:"+673"},{n:"Bulgaria",f:"🇧🇬",c:"+359"},{n:"Burkina Faso",f:"🇧🇫",c:"+226"},{n:"Burundi",f:"🇧🇮",c:"+257"},{n:"Cambodia",f:"🇰🇭",c:"+855"},{n:"Cameroon",f:"🇨🇲",c:"+237"},{n:"Canada",f:"🇨🇦",c:"+1"},{n:"Cape Verde",f:"🇨🇻",c:"+238"},{n:"Central Africa",f:"🇨🇫",c:"+236"},{n:"Chad",f:"🇹🇩",c:"+235"},{n:"Chile",f:"🇨🇱",c:"+56"},{n:"China",f:"🇨🇳",c:"+86"},{n:"Colombia",f:"🇨🇴",c:"+57"},{n:"Comoros",f:"🇰🇲",c:"+269"},{n:"Congo",f:"🇨🇬",c:"+242"},{n:"Costa Rica",f:"🇨🇷",c:"+506"},{n:"Croatia",f:"🇭🇷",c:"+385"},{n:"Cuba",f:"🇨🇺",c:"+53"},{n:"Cyprus",f:"🇨🇾",c:"+357"},{n:"Czech",f:"🇨🇿",c:"+420"},{n:"Denmark",f:"🇩🇰",c:"+45"},{n:"Djibouti",f:"🇩🇯",c:"+253"},{n:"Dominica",f:"🇩🇲",c:"+1"},{n:"Dominican Republic",f:"🇩🇴",c:"+1"},{n:"Ecuador",f:"🇪🇨",c:"+593"},{n:"Egypt",f:"🇪🇬",c:"+20"},{n:"El Salvador",f:"🇸🇻",c:"+503"},{n:"Equatorial Guinea",f:"🇬🇶",c:"+240"},{n:"Eritrea",f:"🇪🇷",c:"+291"},{n:"Estonia",f:"🇪🇪",c:"+372"},{n:"Eswatini",f:"🇸🇿",c:"+268"},{n:"Ethiopia",f:"🇪🇹",c:"+251"},{n:"Fiji",f:"🇫🇯",c:"+679"},{n:"Finland",f:"🇫🇮",c:"+358"},{n:"France",f:"🇫🇷",c:"+33"},{n:"Gabon",f:"🇬🇦",c:"+241"},{n:"Gambia",f:"🇬🇲",c:"+220"},{n:"Georgia",f:"🇬🇪",c:"+995"},{n:"Germany",f:"🇩🇪",c:"+49"},{n:"Ghana",f:"🇬🇭",c:"+233"},{n:"Greece",f:"🇬🇷",c:"+30"},{n:"Grenada",f:"🇬🇩",c:"+1"},{n:"Guatemala",f:"🇬🇹",c:"+502"},{n:"Guinea",f:"🇬🇳",c:"+224"},{n:"Guinea-Bissau",f:"🇬🇼",c:"+245"},{n:"Guyana",f:"🇬🇾",c:"+592"},{n:"Haiti",f:"🇭🇹",c:"+509"},{n:"Honduras",f:"🇭🇳",c:"+504"},{n:"Hungary",f:"🇭🇺",c:"+36"},{n:"Iceland",f:"🇮🇸",c:"+354"},{n:"India",f:"🇮🇳",c:"+91"},{n:"Indonesia",f:"🇮🇩",c:"+62"},{n:"Iran",f:"🇮🇷",c:"+98"},{n:"Iraq",f:"🇮🇶",c:"+964"},{n:"Ireland",f:"🇮🇪",c:"+353"},{n:"Israel",f:"🇮🇱",c:"+972"},{n:"Italy",f:"🇮🇹",c:"+39"},{n:"Jamaica",f:"🇯🇲",c:"+1"},{n:"Japan",f:"🇯🇵",c:"+81"},{n:"Jordan",f:"🇯🇴",c:"+962"},{n:"Kazakhstan",f:"🇰🇿",c:"+7"},{n:"Kenya",f:"🇰🇪",c:"+254"},{n:"Kiribati",f:"🇰🇮",c:"+686"},{n:"Korea North",f:"🇰🇵",c:"+850"},{n:"Korea South",f:"🇰🇷",c:"+82"},{n:"Kuwait",f:"🇰🇼",c:"+965"},{n:"Kyrgyzstan",f:"🇰🇬",c:"+996"},{n:"Laos",f:"🇱🇦",c:"+856"},{n:"Latvia",f:"🇱🇻",c:"+371"},{n:"Lebanon",f:"🇱🇧",c:"+961"},{n:"Lesotho",f:"🇱🇸",c:"+266"},{n:"Liberia",f:"🇱🇷",c:"+231"},{n:"Libya",f:"🇱🇾",c:"+218"},{n:"Liechtenstein",f:"🇱🇮",c:"+423"},{n:"Lithuania",f:"🇱🇹",c:"+370"},{n:"Luxembourg",f:"🇱🇺",c:"+352"},{n:"Madagascar",f:"🇲🇬",c:"+261"},{n:"Malawi",f:"🇲🇼",c:"+265"},{n:"Malaysia",f:"🇲🇾",c:"+60"},{n:"Maldives",f:"🇲🇻",c:"+960"},{n:"Mali",f:"🇲🇱",c:"+223"},{n:"Malta",f:"🇲🇹",c:"+356"},{n:"Mauritania",f:"🇲🇷",c:"+222"},{n:"Mauritius",f:"🇲🇺",c:"+230"},{n:"Mexico",f:"🇲🇽",c:"+52"},{n:"Moldova",f:"🇲🇩",c:"+373"},{n:"Monaco",f:"🇲🇨",c:"+377"},{n:"Mongolia",f:"🇲🇳",c:"+976"},{n:"Montenegro",f:"🇲🇪",c:"+382"},{n:"Morocco",f:"🇲🇦",c:"+212"},{n:"Mozambique",f:"🇲🇿",c:"+258"},{n:"Myanmar",f:"🇲🇲",c:"+95"},{n:"Namibia",f:"🇳🇦",c:"+264"},{n:"Nepal",f:"🇳🇵",c:"+977"},{n:"Netherlands",f:"🇳🇱",c:"+31"},{n:"New Zealand",f:"🇳🇿",c:"+64"},{n:"Nicaragua",f:"🇳🇮",c:"+505"},{n:"Niger",f:"🇳🇪",c:"+227"},{n:"Nigeria",f:"🇳🇬",c:"+234"},{n:"Norway",f:"🇳🇴",c:"+47"},{n:"Oman",f:"🇴🇲",c:"+968"},{n:"Pakistan",f:"🇵🇰",c:"+92"},{n:"Palestine",f:"🇵🇸",c:"+970"},{n:"Panama",f:"🇵🇦",c:"+507"},{n:"Papua New Guinea",f:"🇵🇬",c:"+675"},{n:"Paraguay",f:"🇵🇾",c:"+595"},{n:"Peru",f:"🇵🇪",c:"+51"},{n:"Philippines",f:"🇵🇭",c:"+63"},{n:"Poland",f:"🇵🇱",c:"+48"},{n:"Portugal",f:"🇵🇹",c:"+351"},{n:"Qatar",f:"🇶🇦",c:"+974"},{n:"Romania",f:"🇷🇴",c:"+40"},{n:"Russia",f:"🇷🇺",c:"+7"},{n:"Rwanda",f:"🇷🇼",c:"+250"},{n:"Saudi Arabia",f:"🇸🇦",c:"+966"},{n:"Senegal",f:"🇸🇳",c:"+221"},{n:"Serbia",f:"🇷🇸",c:"+381"},{n:"Seychelles",f:"🇸🇨",c:"+248"},{n:"Sierra Leone",f:"🇸🇱",c:"+232"},{n:"Singapore",f:"🇸🇬",c:"+65"},{n:"Slovakia",f:"🇸🇰",c:"+421"},{n:"Slovenia",f:"🇸🇮",c:"+386"},{n:"Somalia",f:"🇸🇴",c:"+252"},{n:"South Africa",f:"🇿🇦",c:"+27"},{n:"Spain",f:"🇪🇸",c:"+34"},{n:"Sri Lanka",f:"🇱🇰",c:"+94"},{n:"Sudan",f:"🇸🇩",c:"+249"},{n:"Sweden",f:"🇸🇪",c:"+46"},{n:"Switzerland",f:"🇨🇭",c:"+41"},{n:"Syria",f:"🇸🇾",c:"+963"},{n:"Taiwan",f:"🇹🇼",c:"+886"},{n:"Tajikistan",f:"🇹🇯",c:"+992"},{n:"Tanzania",f:"🇹🇿",c:"+255"},{n:"Thailand",f:"🇹🇭",c:"+66"},{n:"Togo",f:"🇹🇬",c:"+228"},{n:"Trinidad",f:"🇹🇹",c:"+1"},{n:"Tunisia",f:"🇹🇳",c:"+216"},{n:"Turkey",f:"🇹🇷",c:"+90"},{n:"Turkmenistan",f:"🇹🇲",c:"+993"},{n:"Uganda",f:"🇺🇬",c:"+256"},{n:"Ukraine",f:"🇺🇦",c:"+380"},{n:"UAE",f:"🇦🇪",c:"+971"},{n:"UK",f:"🇬🇧",c:"+44"},{n:"USA",f:"🇺🇸",c:"+1"},{n:"Uruguay",f:"🇺🇾",c:"+598"},{n:"Uzbekistan",f:"🇺🇿",c:"+998"},{n:"Venezuela",f:"🇻🇪",c:"+58"},{n:"Vietnam",f:"🇻🇳",c:"+84"},{n:"Yemen",f:"🇾🇪",c:"+967"},{n:"Zambia",f:"🇿🇲",c:"+260"},{n:"Zimbabwe",f:"🇿🇼",c:"+263"}
];

function showList(){document.getElementById('countryList').style.display='block'; render(allCountries)}
function render(list){
 let h=''; list.forEach(o=>{
  h+=`<div class='item' onclick="pick('${o.c}','${o.n}','${o.f}')">${o.f} ${o.n} ${o.c}</div>`;
 });
 document.getElementById('countryList').innerHTML=h;
}
function filterC(){
 let q=document.getElementById('search').value.toLowerCase();
 let f=allCountries.filter(o=>o.n.toLowerCase().includes(q)||o.c.includes(q));
 render(f);
}
function pick(code,name,flag){
 document.getElementById('ccode').value=code;
 document.getElementById('cname').value=name;
 document.getElementById('sel').innerText=`Selected: ${flag} ${name} ${code}`;
 document.getElementById('search').value=`${flag} ${name} ${code}`;
 document.getElementById('countryList').style.display='none';
}
function signup(){
 let payload={
  country_code:document.getElementById('ccode').value,
  country_name:document.getElementById('cname').value,
  phone:document.getElementById('phone').value,
  date_of_birth:document.getElementById('dob').value,
  username:document.getElementById('user').value,
  password:document.getElementById('pass').value
 };
 if(!payload.phone||!payload.date_of_birth||!payload.username||!payload.password){
  document.getElementById('msg').innerText='❌ Fill all fields!'; return;
 }
 document.getElementById('msg').innerText='Creating...';
 fetch('/api/signup',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(payload)})
 .then(r=>r.json()).then(d=>{
  document.getElementById('msg').innerText=d.message;
  if(d.success){setTimeout(()=>window.location='/login',1500)}
 });
}
render(allCountries);
</script>
</div>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML)

@app.route('/login')
def login_page():
    return "<h2 style='color:white;background:black;padding:20px'>Login page coming - use same API! Your account saved! Go back to / to create more</h2><a href='/' style='color:#fe2c55'>Back to Signup</a>"

@app.route('/api/signup', methods=['POST'])
def signup_api():
    data = request.json
    try:
        dob = date.fromisoformat(data['date_of_birth'])
        today = date.today()
        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
        if age < 13:
            return jsonify({"success": False, "message": "❌ Must be 13+ years old - You are "+str(age)})
    except Exception as e:
        return jsonify({"success": False, "message": "❌ Invalid date of birth"})
    
    if not data.get('phone') or len(data['phone']) < 7:
        return jsonify({"success": False, "message": "❌ Enter valid phone number"})

    try:
        res = supabase.table("profiles").insert({
            "username": data['username'],
            "password": data['password'],
            "phone": data['phone'],
            "country_code": data['country_code'],
            "country_name": data['country_name'],
            "date_of_birth": data['date_of_birth'],
            "age": age
        }).execute()
        return jsonify({"success": True, "message": f"✅ Account created! {data['country_name']} {data['country_code']}{data['phone']} - Age {age}"})
    except Exception as e:
        return jsonify({"success": False, "message": f"❌ Error: {str(e)} - maybe username taken"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
