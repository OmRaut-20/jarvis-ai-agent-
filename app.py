import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from groq import Groq

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
app = Flask(__name__)
CORS(app)

SYSTEM_PROMPT = """You are JARVIS, an advanced AI assistant created by Om Raut. Reply exactly like ChatGPT does.
- Use emojis to make responses engaging
- Use clear headings with emojis
- Use bullet points for lists
- Bold important words using **bold**
- Keep explanations simple and clear
- Never mention Llama or any other model
- You are JARVIS, created by Om Raut"""

@app.route("/")
def home():
    return """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>JARVIS</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&family=Space+Grotesk:wght@400;500;600;700&display=swap" rel="stylesheet">
<script src="https://cdnjs.cloudflare.com/ajax/libs/marked/9.1.6/marked.min.js"></script>
<style>
*{margin:0;padding:0;box-sizing:border-box}
:root{
  --bg:#080808;
  --sidebar:#0e0e0e;
  --surface:#141414;
  --surface2:#1c1c1c;
  --border:#222;
  --border2:#2a2a2a;
  --text:#f0f0f0;
  --text-dim:#666;
  --text-muted:#333;
  --accent:#00ff9d;
  --accent2:#00c97a;
  --accent-glow:rgba(0,255,157,0.15);
  --user-bg:#1a1a1a;
  --gradient:linear-gradient(135deg,#00ff9d,#00b4ff);
}
body{background:var(--bg);color:var(--text);font-family:'Inter',sans-serif;min-height:100vh;display:flex;overflow:hidden;}

/* Noise texture overlay */
body::before{
  content:'';position:fixed;top:0;left:0;right:0;bottom:0;
  background-image:url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)' opacity='0.03'/%3E%3C/svg%3E");
  pointer-events:none;z-index:0;opacity:0.4;
}

/* Sidebar */
.sidebar{
  width:240px;flex-shrink:0;
  background:var(--sidebar);
  border-right:1px solid var(--border);
  display:flex;flex-direction:column;
  padding:0;height:100vh;position:relative;z-index:1;
}
.sidebar-header{padding:20px 16px 16px;}
.logo-wrap{display:flex;align-items:center;gap:10px;margin-bottom:20px;}
.logo-icon{
  width:36px;height:36px;
  background:var(--gradient);
  border-radius:10px;
  display:flex;align-items:center;justify-content:center;
  font-family:'Space Grotesk',sans-serif;
  font-size:1rem;font-weight:700;color:#000;
  box-shadow:0 0 20px var(--accent-glow);
}
.logo-text{
  font-family:'Space Grotesk',sans-serif;
  font-size:1.1rem;font-weight:600;
  background:var(--gradient);
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;
}
.new-btn{
  width:100%;
  background:transparent;
  border:1px solid var(--border2);
  color:var(--text);border-radius:10px;
  padding:10px 14px;cursor:pointer;
  font-family:'Inter',sans-serif;font-size:0.82rem;
  font-weight:400;
  transition:all 0.2s;
  display:flex;align-items:center;gap:8px;
  letter-spacing:0.01em;
}
.new-btn:hover{background:var(--surface);border-color:#333;box-shadow:0 0 12px var(--accent-glow);}
.new-btn .plus{
  width:20px;height:20px;border-radius:6px;
  background:var(--surface2);
  display:flex;align-items:center;justify-content:center;
  font-size:1rem;line-height:1;color:var(--accent);
}
.sidebar-section-label{
  font-size:0.62rem;color:var(--text-dim);
  letter-spacing:0.12em;text-transform:uppercase;
  padding:0 16px;margin:16px 0 8px;
}
.chat-list{padding:0 8px;flex:1;overflow-y:auto;}
.chat-entry{
  padding:9px 10px;border-radius:8px;
  font-size:0.81rem;color:var(--text-dim);
  cursor:pointer;transition:all 0.15s;
  white-space:nowrap;overflow:hidden;text-overflow:ellipsis;
  margin-bottom:1px;
}
.chat-entry:hover{background:var(--surface);color:var(--text);}
.chat-entry.active{background:var(--surface2);color:var(--text);}
.sidebar-footer{
  padding:16px;
  border-top:1px solid var(--border);
  margin-top:auto;
}
.user-card{
  display:flex;align-items:center;gap:10px;
  padding:10px;border-radius:10px;
  cursor:pointer;transition:all 0.15s;
}
.user-card:hover{background:var(--surface);}
.avatar{
  width:34px;height:34px;
  background:var(--gradient);
  border-radius:50%;
  display:flex;align-items:center;justify-content:center;
  font-size:0.85rem;font-weight:600;color:#000;flex-shrink:0;
}
.user-name{font-size:0.85rem;font-weight:500;color:var(--text);}
.user-sub{font-size:0.68rem;color:var(--text-dim);}

/* Main */
.main{flex:1;display:flex;flex-direction:column;height:100vh;overflow:hidden;position:relative;z-index:1;}

/* Topbar */
.topbar{
  display:flex;align-items:center;justify-content:space-between;
  padding:12px 20px;
  border-bottom:1px solid var(--border);
  flex-shrink:0;backdrop-filter:blur(10px);
}
.model-pill{
  display:flex;align-items:center;gap:8px;
  background:var(--surface);border:1px solid var(--border2);
  border-radius:20px;padding:6px 14px;
  font-size:0.8rem;color:var(--text);cursor:pointer;
  transition:all 0.15s;
}
.model-pill:hover{border-color:#333;}
.status-dot{
  width:7px;height:7px;background:var(--accent);
  border-radius:50%;box-shadow:0 0 8px var(--accent);
  animation:pulse 2s infinite;
}
@keyframes pulse{0%,100%{opacity:1;box-shadow:0 0 8px var(--accent)}50%{opacity:0.5;box-shadow:0 0 3px var(--accent)}}
.share-btn{
  background:transparent;border:1px solid var(--border2);
  color:var(--text-dim);border-radius:8px;
  padding:7px 16px;cursor:pointer;font-size:0.78rem;
  font-family:'Inter',sans-serif;transition:all 0.15s;
}
.share-btn:hover{color:var(--text);border-color:#333;}

/* Chat */
.chat-area{flex:1;overflow-y:auto;scroll-behavior:smooth;}
.chat-area::-webkit-scrollbar{width:3px}
.chat-area::-webkit-scrollbar-thumb{background:var(--border2);border-radius:2px}

/* Welcome */
.welcome{
  display:flex;flex-direction:column;align-items:center;
  justify-content:center;min-height:100%;
  padding:60px 24px 40px;text-align:center;
}
.welcome-glow{
  width:80px;height:80px;
  background:var(--gradient);
  border-radius:24px;
  display:flex;align-items:center;justify-content:center;
  font-family:'Space Grotesk',sans-serif;
  font-size:2rem;font-weight:700;color:#000;
  margin-bottom:24px;
  box-shadow:0 0 60px var(--accent-glow), 0 0 120px rgba(0,180,255,0.1);
  animation:float 3s ease-in-out infinite;
}
@keyframes float{0%,100%{transform:translateY(0)}50%{transform:translateY(-8px)}}
.welcome h1{
  font-family:'Space Grotesk',sans-serif;
  font-size:2rem;font-weight:600;
  margin-bottom:10px;
  background:var(--gradient);
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;
}
.welcome p{font-size:0.9rem;color:var(--text-dim);max-width:420px;line-height:1.7;margin-bottom:32px;}
.chips{display:flex;flex-wrap:wrap;gap:10px;justify-content:center;max-width:600px;}
.chip{
  background:var(--surface);border:1px solid var(--border2);
  border-radius:12px;padding:12px 16px;cursor:pointer;
  font-size:0.82rem;color:var(--text-dim);
  transition:all 0.2s;text-align:left;line-height:1.5;
  max-width:180px;
}
.chip:hover{
  background:var(--surface2);color:var(--text);
  border-color:var(--accent);
  box-shadow:0 0 12px var(--accent-glow);
  transform:translateY(-2px);
}

/* Messages */
.msg-wrap{max-width:740px;margin:0 auto;padding:12px 24px;}
.msg-row{display:flex;gap:14px;align-items:flex-start;animation:msgIn 0.3s ease;}
@keyframes msgIn{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:translateY(0)}}
.msg-row.user{justify-content:flex-end;margin-bottom:16px;}
.msg-row.jarvis{margin-bottom:20px;}
.j-avatar{
  width:34px;height:34px;flex-shrink:0;
  background:var(--gradient);border-radius:10px;
  display:flex;align-items:center;justify-content:center;
  font-family:'Space Grotesk',sans-serif;
  font-size:0.8rem;font-weight:700;color:#000;
  margin-top:2px;
  box-shadow:0 0 16px var(--accent-glow);
}
.user-bubble{
  background:var(--surface2);
  border:1px solid var(--border2);
  border-radius:14px 14px 2px 14px;
  padding:12px 18px;max-width:75%;
  font-size:0.88rem;line-height:1.7;color:var(--text);
}
.j-body{flex:1;padding-top:4px;}
.j-body p{margin:6px 0;font-size:0.88rem;line-height:1.8;color:#d0d0d0;}
.j-body strong{font-weight:600;color:var(--text);}
.j-body ul,.j-body ol{padding-left:20px;margin:8px 0;}
.j-body li{margin:5px 0;font-size:0.88rem;line-height:1.7;color:#d0d0d0;}
.j-body h1,.j-body h2,.j-body h3{font-family:'Space Grotesk',sans-serif;font-size:1rem;font-weight:600;margin:14px 0 6px;color:var(--text);}
.j-body code{background:var(--surface2);border:1px solid var(--border2);border-radius:4px;padding:1px 6px;font-size:0.82rem;color:var(--accent);}
.j-body pre{background:var(--surface2);border:1px solid var(--border2);border-radius:10px;padding:14px;margin:10px 0;overflow-x:auto;}
.j-body pre code{background:transparent;border:none;padding:0;color:#d0d0d0;}

.thinking{display:flex;align-items:center;gap:5px;padding:6px 0;}
.t-dot{width:6px;height:6px;border-radius:50%;background:var(--accent);animation:think 1.4s ease-in-out infinite;box-shadow:0 0 6px var(--accent);}
.t-dot:nth-child(2){animation-delay:0.2s}.t-dot:nth-child(3){animation-delay:0.4s}
@keyframes think{0%,100%{opacity:0.2;transform:scale(1)}50%{opacity:1;transform:scale(1.3)}}

/* Input */
.input-wrap{padding:12px 24px 20px;flex-shrink:0;}
.input-box{
  max-width:740px;margin:0 auto;
  background:var(--surface);
  border:1px solid var(--border2);
  border-radius:16px;
  transition:all 0.2s;
  box-shadow:0 4px 40px rgba(0,0,0,0.3);
}
.input-box:focus-within{
  border-color:#333;
  box-shadow:0 4px 40px rgba(0,0,0,0.4), 0 0 0 1px rgba(0,255,157,0.08);
}
.input-inner{display:flex;align-items:flex-end;padding:14px 16px 12px;}
textarea{
  flex:1;background:transparent;border:none;outline:none;
  color:var(--text);font-family:'Inter',sans-serif;
  font-size:0.88rem;font-weight:300;resize:none;
  line-height:1.6;max-height:180px;min-height:26px;
}
textarea::placeholder{color:var(--text-muted)}
.send{
  width:36px;height:36px;
  background:var(--gradient);
  border:none;border-radius:10px;cursor:pointer;
  display:flex;align-items:center;justify-content:center;
  flex-shrink:0;margin-left:10px;
  transition:all 0.15s;opacity:0.3;
  box-shadow:0 0 0 transparent;
}
.send.on{opacity:1;box-shadow:0 0 16px var(--accent-glow);}
.send:hover{transform:scale(1.05);}
.send svg{width:15px;height:15px;fill:#000;}
.input-hint{
  text-align:center;padding:8px;
  font-size:0.65rem;color:var(--text-muted);letter-spacing:0.05em;
  border-top:1px solid var(--border);
}
</style>
</head>
<body>

<div class="sidebar">
  <div class="sidebar-header">
    <div class="logo-wrap">
      <div class="logo-icon">J</div>
      <div class="logo-text">JARVIS</div>
    </div>
    <button class="new-btn" onclick="newChat()">
      <div class="plus">+</div> New conversation
    </button>
  </div>
  <div class="sidebar-section-label">Recent</div>
  <div class="chat-list">
    <div class="chat-entry active" id="current-chat">New conversation</div>
  </div>
  <div class="sidebar-footer">
    <div class="user-card">
      <div class="avatar">O</div>
      <div>
        <div class="user-name">Om Raut</div>
        <div class="user-sub">JARVIS Pro</div>
      </div>
    </div>
  </div>
</div>

<div class="main">
  <div class="topbar">
    <div class="model-pill">
      <div class="status-dot"></div>
      JARVIS &mdash; Llama 3.3 70B
    </div>
    <button class="share-btn">Share</button>
  </div>

  <div class="chat-area" id="chat">
    <div class="welcome" id="welcome">
      <div class="welcome-glow">J</div>
      <h1>Hi, I'm JARVIS</h1>
      <p>Your personal AI assistant, built by Om Raut. Ask me anything — I'm here to help.</p>
      <div class="chips">
        <div class="chip" onclick="suggest('Explain AI in simple words 🤖')">💡 Explain AI in simple words</div>
        <div class="chip" onclick="suggest('Write me a Python function')">🐍 Write a Python function</div>
        <div class="chip" onclick="suggest('What is machine learning?')">🧠 What is machine learning?</div>
        <div class="chip" onclick="suggest('Help me prepare for my exam')">📚 Help me prepare for exams</div>
      </div>
    </div>
  </div>

  <div class="input-wrap">
    <div class="input-box">
      <div class="input-inner">
        <textarea id="inp" rows="1" placeholder="Message JARVIS..."
          oninput="resize(this);toggleSend(this)"
          onkeydown="if(event.key==='Enter'&&!event.shiftKey){event.preventDefault();send()}"></textarea>
        <button class="send" id="sendbtn" onclick="send()">
          <svg viewBox="0 0 24 24"><path d="M2 21l21-9L2 3v7l15 2-15 2v7z"/></svg>
        </button>
      </div>
      <div class="input-hint">JARVIS can make mistakes &nbsp;·&nbsp; Built by Om Raut</div>
    </div>
  </div>
</div>

<script>
marked.setOptions({breaks:true,gfm:true});
var chat=document.getElementById('chat'),inp=document.getElementById('inp'),welcome=document.getElementById('welcome'),hasMsg=false;

function resize(el){el.style.height='auto';el.style.height=Math.min(el.scrollHeight,180)+'px';}
function toggleSend(el){document.getElementById('sendbtn').classList.toggle('on',el.value.trim().length>0);}
function suggest(t){inp.value=t;toggleSend(inp);send();}
function newChat(){
  while(chat.firstChild)chat.removeChild(chat.firstChild);
  chat.appendChild(welcome);welcome.style.display='flex';
  hasMsg=false;inp.value='';document.getElementById('current-chat').textContent='New conversation';
}
function send(){
  var msg=inp.value.trim();if(!msg)return;
  if(!hasMsg){welcome.style.display='none';hasMsg=true;}
  if(document.getElementById('current-chat').textContent==='New conversation')
    document.getElementById('current-chat').textContent=msg.substring(0,28)+'...';
  addUser(msg);inp.value='';inp.style.height='auto';
  document.getElementById('sendbtn').classList.remove('on');
  var t=addThink();
  fetch('/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message:msg})})
    .then(r=>r.json()).then(d=>{t.remove();addJarvis(d.reply);})
    .catch(()=>{t.remove();addJarvis('Something went wrong. Please try again.');});
}
function addUser(text){
  var w=document.createElement('div');w.className='msg-wrap';
  var r=document.createElement('div');r.className='msg-row user';
  var b=document.createElement('div');b.className='user-bubble';b.textContent=text;
  r.appendChild(b);w.appendChild(r);chat.appendChild(w);chat.scrollTop=chat.scrollHeight;
}
function addJarvis(text){
  var w=document.createElement('div');w.className='msg-wrap';
  var r=document.createElement('div');r.className='msg-row jarvis';
  var av=document.createElement('div');av.className='j-avatar';av.textContent='J';
  var body=document.createElement('div');body.className='j-body';
  body.innerHTML=marked.parse(text);
  r.appendChild(av);r.appendChild(body);w.appendChild(r);chat.appendChild(w);chat.scrollTop=chat.scrollHeight;
}
function addThink(){
  var w=document.createElement('div');w.className='msg-wrap';
  var r=document.createElement('div');r.className='msg-row jarvis';
  var av=document.createElement('div');av.className='j-avatar';av.textContent='J';
  var body=document.createElement('div');body.className='j-body';
  body.innerHTML='<div class="thinking"><div class="t-dot"></div><div class="t-dot"></div><div class="t-dot"></div></div>';
  r.appendChild(av);r.appendChild(body);w.appendChild(r);chat.appendChild(w);chat.scrollTop=chat.scrollHeight;
  return w;
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
            max_tokens=600,
            temperature=0.7
        )
        reply = res.choices[0].message.content.strip()
        return jsonify({"reply": reply})
    except Exception as e:
        return jsonify({"reply": "Error: " + str(e)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

 
