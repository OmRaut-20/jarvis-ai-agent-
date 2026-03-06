import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from groq import Groq

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
app = Flask(__name__)
CORS(app)

SYSTEM_PROMPT = """You are JARVIS, a friendly AI assistant made by Om Raut.

STRICT RULES - always follow these:
- Reply in 1-3 short sentences only
- NEVER use bullet points or numbered lists
- NEVER use asterisks or symbols
- Talk like a smart friend texting you
- Be casual, warm and direct
- If someone asks for a list, describe it naturally in one sentence instead

Example:
User: What is AI?
JARVIS: AI is basically teaching computers to think and learn like humans. It powers things like voice assistants, recommendations, and self-driving cars!"""

@app.route("/")
def home():
    return """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>JARVIS</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500&family=Playfair+Display:wght@400;500&display=swap" rel="stylesheet">
<style>
*{margin:0;padding:0;box-sizing:border-box}
:root{--bg:#f5f4f0;--surface:#ffffff;--border:#e8e6e0;--text:#1a1916;--text-dim:#9a9690;--text-light:#c4c2bc;--green:#2d6a4f;}
body{background:var(--bg);color:var(--text);font-family:'Inter',sans-serif;min-height:100vh;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:32px 24px;}
.container{width:100%;max-width:680px;}
header{text-align:center;margin-bottom:48px;}
.logo{font-family:'Playfair Display',serif;font-weight:400;font-size:2.2rem;color:var(--text);letter-spacing:0.08em;margin-bottom:8px;}
.tagline{font-size:0.75rem;color:var(--text-dim);letter-spacing:0.15em;text-transform:uppercase;font-weight:300;}
.status-bar{display:flex;align-items:center;justify-content:center;gap:6px;margin-top:14px;}
.dot{width:5px;height:5px;border-radius:50%;background:var(--green);animation:breathe 3s ease-in-out infinite;}
@keyframes breathe{0%,100%{opacity:0.4;transform:scale(1)}50%{opacity:1;transform:scale(1.2)}}
.status-text{font-size:0.68rem;color:var(--text-dim);letter-spacing:0.1em;text-transform:uppercase;}
.chat-window{background:var(--surface);border:1px solid var(--border);border-radius:16px;height:440px;overflow-y:auto;padding:28px;margin-bottom:12px;scroll-behavior:smooth;box-shadow:0 2px 40px rgba(0,0,0,0.04),0 1px 3px rgba(0,0,0,0.06);}
.chat-window::-webkit-scrollbar{width:3px}
.chat-window::-webkit-scrollbar-thumb{background:var(--border);border-radius:2px}
.empty-state{height:100%;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:10px;}
.empty-icon{font-family:'Playfair Display',serif;font-size:3.5rem;color:var(--text-light);}
.empty-hint{font-size:0.72rem;color:var(--text-light);letter-spacing:0.12em;text-transform:uppercase;}
.message{margin-bottom:24px;animation:appear 0.4s ease;}
@keyframes appear{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:translateY(0)}}
.message-label{font-size:0.62rem;letter-spacing:0.14em;text-transform:uppercase;font-weight:500;margin-bottom:7px;color:var(--text-dim);}
.message.jarvis .message-label{color:var(--green);}
.message-bubble{font-size:0.9rem;line-height:1.75;color:var(--text);font-weight:300;}
.message.user .message-bubble{color:var(--text-dim);}
.divider{height:1px;background:var(--border);margin:20px 0;}
.input-area{background:var(--surface);border:1px solid var(--border);border-radius:12px;display:flex;align-items:center;padding:4px 4px 4px 20px;box-shadow:0 2px 20px rgba(0,0,0,0.04);transition:border-color 0.2s,box-shadow 0.2s;}
.input-area:focus-within{border-color:#c4c2bc;box-shadow:0 2px 20px rgba(0,0,0,0.08);}
input{flex:1;background:transparent;border:none;outline:none;color:var(--text);font-family:'Inter',sans-serif;font-size:0.875rem;font-weight:300;padding:12px 0;}
input::placeholder{color:var(--text-light)}
button{background:var(--text);border:none;color:#f5f4f0;font-family:'Inter',sans-serif;font-size:0.72rem;font-weight:500;letter-spacing:0.08em;text-transform:uppercase;padding:11px 20px;border-radius:8px;cursor:pointer;transition:all 0.2s;white-space:nowrap;flex-shrink:0;}
button:hover{background:#333;transform:translateY(-1px);}
.thinking{display:flex;align-items:center;gap:5px;padding:4px 0;}
.t-dot{width:5px;height:5px;border-radius:50%;background:var(--text-light);animation:think 1.4s ease-in-out infinite;}
.t-dot:nth-child(2){animation-delay:0.2s}.t-dot:nth-child(3){animation-delay:0.4s}
@keyframes think{0%,100%{opacity:0.3;transform:translateY(0)}50%{opacity:1;transform:translateY(-3px)}}
footer{margin-top:16px;text-align:center;font-size:0.65rem;color:var(--text-light);letter-spacing:0.1em;text-transform:uppercase;}
</style>
</head>
<body>
<div class="container">
  <header>
    <div class="logo">Jarvis</div>
    <div class="tagline">Your personal AI assistant</div>
    <div class="status-bar"><div class="dot"></div><span class="status-text">Online &mdash; Ready</span></div>
  </header>
  <div class="chat-window" id="chat">
    <div class="empty-state" id="empty">
      <div class="empty-icon">J.</div>
      <div class="empty-hint">How can I help you today?</div>
    </div>
  </div>
  <div class="input-area">
    <input type="text" id="inp" placeholder="Ask Jarvis anything..." onkeypress="if(event.key==='Enter')send()" autofocus/>
    <button onclick="send()">Send</button>
  </div>
  <footer>Built by Om Raut &nbsp;&middot;&nbsp; Powered by JARVIS AI</footer>
</div>
<script>
var empty=document.getElementById('empty'),chat=document.getElementById('chat'),inp=document.getElementById('inp'),hasMessages=false;
function send(){
  var msg=inp.value.trim();if(!msg)return;
  if(!hasMessages){empty.style.display='none';hasMessages=true;}else{addDivider();}
  addMessage('user',msg);inp.value='';
  var t=addThinking();
  fetch('/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message:msg})})
    .then(function(r){return r.json()})
    .then(function(d){t.remove();addDivider();addMessage('jarvis',d.reply)})
    .catch(function(){t.remove();addDivider();addMessage('jarvis','Something went wrong. Please try again.');});
}
function addMessage(role,text){
  var div=document.createElement('div');div.className='message '+role;
  div.innerHTML='<div class="message-label">'+(role==='user'?'You':'Jarvis')+'</div><div class="message-bubble">'+text+'</div>';
  chat.appendChild(div);chat.scrollTop=chat.scrollHeight;return div;
}
function addDivider(){var d=document.createElement('div');d.className='divider';chat.appendChild(d);}
function addThinking(){
  var div=document.createElement('div');div.className='message jarvis';
  div.innerHTML='<div class="message-label">Jarvis</div><div class="message-bubble"><div class="thinking"><div class="t-dot"></div><div class="t-dot"></div><div class="t-dot"></div></div></div>';
  chat.appendChild(div);chat.scrollTop=chat.scrollHeight;return div;
}
</script>
</body>
</html>"""

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    msg = data.get("message", "")
    try:
        res = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": msg}
            ],
            max_tokens=150,
            temperature=0.7
        )
        return jsonify({"reply": res.choices[0].message.content})
    except Exception as e:
        return jsonify({"reply": "Error: " + str(e)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
       
