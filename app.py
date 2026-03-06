import os
from flask import Flask, request, jsonify
from groq import Groq

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
app = Flask(__name__)

HTML = open("templates/index.html").read() if os.path.exists("templates/index.html") else ""

@app.route("/")
def home():
    return """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>JARVIS</title>
<link href="https://fonts.googleapis.com/css2?family=DM+Mono:wght@300;400;500&family=Syne:wght@400;600;700;800&display=swap" rel="stylesheet">
<style>
*{margin:0;padding:0;box-sizing:border-box}
:root{
  --bg:#080808;
  --surface:#0f0f0f;
  --border:#1a1a1a;
  --border-light:#242424;
  --text:#e8e8e8;
  --text-dim:#666;
  --accent:#e8e8e8;
  --green:#4ade80;
  --green-dim:#1a3a25;
}
body{
  background:var(--bg);
  color:var(--text);
  font-family:'DM Mono',monospace;
  min-height:100vh;
  display:flex;
  flex-direction:column;
  align-items:center;
  justify-content:center;
  padding:24px;
  position:relative;
  overflow:hidden;
}
body::before{
  content:'';
  position:fixed;
  top:0;left:0;right:0;bottom:0;
  background:radial-gradient(ellipse 80% 50% at 50% -20%, #1a1a1a 0%, transparent 60%);
  pointer-events:none;
}
.grid-bg{
  position:fixed;
  top:0;left:0;right:0;bottom:0;
  background-image:linear-gradient(rgba(255,255,255,0.02) 1px, transparent 1px),
                   linear-gradient(90deg, rgba(255,255,255,0.02) 1px, transparent 1px);
  background-size:48px 48px;
  pointer-events:none;
}
.container{
  width:100%;
  max-width:720px;
  position:relative;
  z-index:1;
}
header{
  margin-bottom:40px;
  display:flex;
  align-items:flex-end;
  justify-content:space-between;
}
.logo{
  font-family:'Syne',sans-serif;
  font-weight:800;
  font-size:2.8rem;
  letter-spacing:-0.03em;
  color:var(--text);
  line-height:1;
}
.logo span{
  color:var(--green);
}
.status{
  display:flex;
  align-items:center;
  gap:8px;
  font-size:0.7rem;
  color:var(--text-dim);
  letter-spacing:0.1em;
  text-transform:uppercase;
  padding-bottom:4px;
}
.status-dot{
  width:6px;height:6px;
  border-radius:50%;
  background:var(--green);
  box-shadow:0 0 8px var(--green);
  animation:pulse 2s infinite;
}
@keyframes pulse{
  0%,100%{opacity:1}
  50%{opacity:0.4}
}
.chat-window{
  background:var(--surface);
  border:1px solid var(--border);
  border-radius:4px;
  height:460px;
  overflow-y:auto;
  padding:24px;
  margin-bottom:2px;
  scroll-behavior:smooth;
}
.chat-window::-webkit-scrollbar{width:3px}
.chat-window::-webkit-scrollbar-track{background:transparent}
.chat-window::-webkit-scrollbar-thumb{background:var(--border-light)}
.empty-state{
  height:100%;
  display:flex;
  flex-direction:column;
  align-items:center;
  justify-content:center;
  gap:12px;
  color:var(--text-dim);
}
.empty-state .big-text{
  font-family:'Syne',sans-serif;
  font-size:4rem;
  font-weight:800;
  color:#1a1a1a;
  letter-spacing:-0.05em;
}
.empty-state .hint{
  font-size:0.75rem;
  letter-spacing:0.08em;
  text-transform:uppercase;
}
.message{
  margin-bottom:20px;
  animation:fadeUp 0.3s ease;
}
@keyframes fadeUp{
  from{opacity:0;transform:translateY(8px)}
  to{opacity:1;transform:translateY(0)}
}
.message-meta{
  font-size:0.65rem;
  letter-spacing:0.1em;
  text-transform:uppercase;
  margin-bottom:6px;
}
.message.user .message-meta{color:var(--text-dim)}
.message.jarvis .message-meta{color:var(--green)}
.message-text{
  font-size:0.875rem;
  line-height:1.7;
  color:var(--text);
  padding:12px 16px;
  border-left:2px solid var(--border-light);
}
.message.jarvis .message-text{
  border-left-color:var(--green);
  background:var(--green-dim);
  border-radius:0 4px 4px 0;
}
.message.user .message-text{
  border-left-color:var(--border-light);
}
.input-area{
  border:1px solid var(--border);
  border-top:none;
  background:var(--surface);
  border-radius:0 0 4px 4px;
  display:flex;
  align-items:center;
  gap:0;
  overflow:hidden;
}
.prompt-symbol{
  padding:0 16px;
  color:var(--green);
  font-size:0.9rem;
  flex-shrink:0;
}
input{
  flex:1;
  background:transparent;
  border:none;
  outline:none;
  color:var(--text);
  font-family:'DM Mono',monospace;
  font-size:0.875rem;
  padding:16px 0;
  letter-spacing:0.02em;
}
input::placeholder{color:var(--text-dim)}
button{
  background:transparent;
  border:none;
  border-left:1px solid var(--border);
  color:var(--text-dim);
  font-family:'DM Mono',monospace;
  font-size:0.7rem;
  letter-spacing:0.1em;
  text-transform:uppercase;
  padding:16px 20px;
  cursor:pointer;
  transition:all 0.15s;
  white-space:nowrap;
}
button:hover{
  color:var(--text);
  background:var(--border);
}
.thinking{
  display:flex;
  align-items:center;
  gap:6px;
  padding:8px 0;
}
.thinking-dot{
  width:4px;height:4px;
  border-radius:50%;
  background:var(--green);
  animation:think 1.2s infinite;
}
.thinking-dot:nth-child(2){animation-delay:0.2s}
.thinking-dot:nth-child(3){animation-delay:0.4s}
@keyframes think{
  0%,100%{opacity:0.2;transform:scale(1)}
  50%{opacity:1;transform:scale(1.3)}
}
footer{
  margin-top:20px;
  display:flex;
  justify-content:space-between;
  align-items:center;
  font-size:0.65rem;
  color:var(--text-dim);
  letter-spacing:0.08em;
  text-transform:uppercase;
}
</style>
</head>
<body>
<div class="grid-bg"></div>
<div class="container">
  <header>
    <div class="logo">JAR<span>V</span>IS</div>
    <div class="status"><div class="status-dot"></div>System Online</div>
  </header>
  <div class="chat-window" id="chat">
    <div class="empty-state" id="empty">
      <div class="big-text">J.</div>
      <div class="hint">Begin your query</div>
    </div>
  </div>
  <div class="input-area">
    <div class="prompt-symbol">&#62;</div>
    <input type="text" id="inp" placeholder="Ask me anything..." onkeypress="if(event.key==='Enter')send()" autofocus/>
    <button onclick="send()">Execute</button>
  </div>
  <footer>
    <span>JARVIS AI &mdash; Powered by Llama 3.3</span>
    <span>Built by Om Raut</span>
  </footer>
</div>
<script>
var empty = document.getElementById('empty');
var chat = document.getElementById('chat');
var inp = document.getElementById('inp');
var hasMessages = false;

function send(){
  var msg = inp.value.trim();
  if(!msg) return;
  if(!hasMessages){ empty.style.display='none'; hasMessages=true; }
  addMessage('user', msg);
  inp.value = '';
  var thinking = addThinking();
  fetch('/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message:msg})})
    .then(function(r){return r.json()})
    .then(function(d){
      thinking.remove();
      addMessage('jarvis', d.reply);
    })
    .catch(function(){
      thinking.remove();
      addMessage('jarvis','Connection error. Please try again.');
    });
}

function addMessage(role, text){
  var div = document.createElement('div');
  div.className = 'message ' + role;
  var meta = role === 'user' ? 'You' : 'JARVIS';
  div.innerHTML = '<div class="message-meta">'+meta+'</div><div class="message-text">'+text+'</div>';
  chat.appendChild(div);
  chat.scrollTop = chat.scrollHeight;
  return div;
}

function addThinking(){
  var div = document.createElement('div');
  div.className = 'message jarvis';
  div.innerHTML = '<div class="message-meta">JARVIS</div><div class="message-text"><div class="thinking"><div class="thinking-dot"></div><div class="thinking-dot"></div><div class="thinking-dot"></div></div></div>';
  chat.appendChild(div);
  chat.scrollTop = chat.scrollHeight;
  return div;
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
            messages=[{"role": "user", "content": msg}]
        )
        return jsonify({"reply": res.choices[0].message.content})
    except Exception as e:
        return jsonify({"reply": "Error: " + str(e)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
