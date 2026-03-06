import os
from flask import Flask, request, jsonify
from groq import Groq

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
app = Flask(__name__)

@app.route("/")
def home():
    return open("index.html").read() if os.path.exists("index.html") else """
<html><body style="background:#0a0a0a;color:#00ff88;font-family:Arial;max-width:800px;margin:50px auto;padding:20px">
<h1 style="text-align:center">JARVIS</h1>
<div id="box" style="background:#111;border:1px solid #00ff88;border-radius:10px;padding:20px;height:400px;overflow-y:auto;margin-bottom:20px"></div>
<input id="inp" style="width:75%;padding:12px;border-radius:8px;border:1px solid #00ff88;background:#111;color:#fff;font-size:1em" placeholder="Ask JARVIS anything..." onkeypress="if(event.key==='Enter')send()"/>
<button onclick="send()" style="padding:12px 20px;background:#00ff88;color:#000;border:none;border-radius:8px;font-size:1em;cursor:pointer">Send</button>
<script>
function send(){
var i=document.getElementById('inp'),b=document.getElementById('box'),m=i.value.trim();
if(!m)return;
b.innerHTML+='<p style="color:#fff">You: '+m+'</p>';
i.value='';
fetch('/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message:m})})
.then(function(r){return r.json()})
.then(function(d){b.innerHTML+='<p style="color:#00ff88">JARVIS: '+d.reply+'</p>';b.scrollTop=b.scrollHeight});
}
</script></body></html>"""

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    msg = data.get("message", "")
    try:
        res = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": msg}]
        )
        return jsonify({"reply": res.choices[0].message.content})
    except Exception as e:
        return jsonify({"reply": "Error: " + str(e)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
