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
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0">
<title>JARVIS — AI Assistant</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&family=Lora:ital,wght@0,400;0,500;1,400&display=swap" rel="stylesheet">
<script src="https://cdnjs.cloudflare.com/ajax/libs/marked/9.1.6/marked.min.js"></script>
<style>
*{margin:0;padding:0;box-sizing:border-box;-webkit-tap-highlight-color:transparent;}
:root{
  --bg:#ffffff;
  --bg2:#f9f9f8;
  --sidebar:#f7f6f3;
  --border:#e9e9e7;
  --border2:#d9d9d6;
  --text:#1a1a18;
  --text-dim:#9b9a97;
  --text-light:#d3d2ce;
  --accent:#2f6f3f;
  --accent-soft:#ebf3ed;
  --accent-border:#c3ddc9;
  --user-bg:#f1f0ec;
  --shadow-sm:0 1px 3px rgba(0,0,0,0.06);
  --shadow-md:0 4px 16px rgba(0,0,0,0.08);
  --shadow-lg:0 12px 40px rgba(0,0,0,0.1);
  --radius:10px;
  --radius-lg:16px;
}
html,body{height:100%;overflow:hidden;}
body{background:var(--bg);color:var(--text);font-family:'Inter',sans-serif;font-size:15px;}

/* ======== LANDING ======== */
#landing{
  position:fixed;inset:0;background:var(--bg);
  display:flex;flex-direction:column;align-items:center;justify-content:center;
  z-index:200;padding:24px;text-align:center;
  transition:opacity 0.5s ease,transform 0.5s ease;
}
#landing.out{opacity:0;transform:scale(0.98);pointer-events:none;}

.land-nav{
  position:absolute;top:0;left:0;right:0;
  padding:18px 28px;
  display:flex;align-items:center;justify-content:space-between;
  border-bottom:1px solid var(--border);
}
.land-nav-logo{display:flex;align-items:center;gap:9px;}
.nav-icon{width:28px;height:28px;background:var(--accent);border-radius:7px;display:flex;align-items:center;justify-content:center;font-family:'Lora',serif;font-size:0.85rem;color:#fff;}
.nav-name{font-size:0.9rem;font-weight:500;color:var(--text);}
.nav-tag{font-size:0.72rem;color:var(--text-dim);background:var(--bg2);border:1px solid var(--border);border-radius:6px;padding:3px 9px;}

.land-body{max-width:540px;width:100%;}
.land-eyebrow{
  display:inline-flex;align-items:center;gap:7px;
  font-size:0.72rem;font-weight:500;
  color:var(--accent);letter-spacing:0.08em;text-transform:uppercase;
  background:var(--accent-soft);border:1px solid var(--accent-border);
  border-radius:20px;padding:5px 14px;margin-bottom:28px;
}
.eye-dot{width:5px;height:5px;background:var(--accent);border-radius:50%;animation:blink2 2s infinite;}
@keyframes blink2{0%,100%{opacity:0.4}50%{opacity:1}}

.land-h{
  font-family:'Lora',serif;
  font-size:clamp(2rem,5.5vw,3.2rem);
  line-height:1.15;color:var(--text);
  margin-bottom:18px;letter-spacing:-0.01em;
}
.land-h em{font-style:italic;color:var(--accent);}

.land-p{
  font-size:clamp(0.88rem,2vw,1rem);
  color:var(--text-dim);line-height:1.75;
  margin-bottom:36px;
}

.land-actions{display:flex;align-items:center;justify-content:center;gap:12px;flex-wrap:wrap;margin-bottom:48px;}
.btn-primary{
  display:inline-flex;align-items:center;gap:9px;
  background:var(--accent);color:#fff;
  border:none;border-radius:var(--radius);
  padding:13px 26px;cursor:pointer;
  font-family:'Inter',sans-serif;font-size:0.9rem;font-weight:500;
  box-shadow:0 2px 12px rgba(47,111,63,0.3);
  transition:all 0.2s;
}
.btn-primary:hover{background:#266035;transform:translateY(-1px);box-shadow:0 4px 18px rgba(47,111,63,0.4);}
.btn-primary svg{width:16px;height:16px;fill:none;stroke:#fff;stroke-width:2;transition:transform 0.2s;}
.btn-primary:hover svg{transform:translateX(3px);}
.btn-secondary{
  display:inline-flex;align-items:center;gap:7px;
  background:transparent;color:var(--text-dim);
  border:1px solid var(--border2);border-radius:var(--radius);
  padding:13px 22px;cursor:pointer;
  font-family:'Inter',sans-serif;font-size:0.9rem;font-weight:400;
  transition:all 0.2s;
}
.btn-secondary:hover{color:var(--text);border-color:var(--border2);background:var(--bg2);}

.land-cards{display:flex;gap:12px;justify-content:center;flex-wrap:wrap;}
.land-card{
  background:var(--bg2);border:1px solid var(--border);
  border-radius:var(--radius);padding:14px 18px;
  text-align:left;max-width:160px;
  box-shadow:var(--shadow-sm);
}
.card-icon{font-size:1.2rem;margin-bottom:8px;}
.card-title{font-size:0.78rem;font-weight:500;color:var(--text);margin-bottom:3px;}
.card-desc{font-size:0.71rem;color:var(--text-dim);line-height:1.5;}

.land-foot{
  position:absolute;bottom:0;left:0;right:0;
  padding:14px;text-align:center;
  font-size:0.68rem;color:var(--text-light);
  border-top:1px solid var(--border);
}

/* ======== APP ======== */
#app{display:none;height:100vh;flex-direction:column;}
#app.show{display:flex;}

/* Topbar */
.topbar{
  display:flex;align-items:center;justify-content:space-between;
  padding:0 18px;height:52px;
  border-bottom:1px solid var(--border);
  background:var(--bg);flex-shrink:0;
}
.tb-left{display:flex;align-items:center;gap:12px;}
.tb-logo{display:flex;align-items:center;gap:8px;}
.tb-icon{width:26px;height:26px;background:var(--accent);border-radius:7px;display:flex;align-items:center;justify-content:center;font-family:'Lora',serif;font-size:0.8rem;color:#fff;}
.tb-name{font-size:0.9rem;font-weight:500;}
.tb-divider{width:1px;height:18px;background:var(--border2);}
.tb-model{font-size:0.75rem;color:var(--text-dim);display:flex;align-items:center;gap:6px;}
.online-dot{width:5px;height:5px;background:#4caf76;border-radius:50%;animation:blink2 3s infinite;}
.tb-right{display:flex;align-items:center;gap:8px;}
.tb-btn{background:transparent;border:1px solid var(--border);color:var(--text-dim);border-radius:7px;padding:5px 13px;cursor:pointer;font-size:0.75rem;font-family:'Inter',sans-serif;transition:all 0.15s;}
.tb-btn:hover{color:var(--text);background:var(--bg2);}
.new-chat-tb{display:flex;align-items:center;gap:6px;background:var(--bg2);border:1px solid var(--border);color:var(--text-dim);border-radius:7px;padding:5px 12px;cursor:pointer;font-size:0.75rem;font-family:'Inter',sans-serif;transition:all 0.15s;}
.new-chat-tb:hover{color:var(--text);border-color:var(--border2);}

/* Chat */
.chat-area{flex:1;overflow-y:auto;scroll-behavior:smooth;}
.chat-area::-webkit-scrollbar{width:4px}
.chat-area::-webkit-scrollbar-thumb{background:var(--border);border-radius:2px}

/* Welcome screen */
.welcome{
  max-width:580px;margin:0 auto;
  padding:56px 24px 32px;
}
.wel-greeting{
  font-family:'Lora',serif;
  font-size:clamp(1.5rem,4vw,2rem);
  color:var(--text);margin-bottom:8px;
}
.wel-greeting em{font-style:italic;color:var(--accent);}
.wel-sub{font-size:0.88rem;color:var(--text-dim);line-height:1.7;margin-bottom:32px;}

.wel-section{font-size:0.68rem;font-weight:500;color:var(--text-dim);letter-spacing:0.1em;text-transform:uppercase;margin-bottom:10px;}
.wel-chips{display:flex;flex-direction:column;gap:8px;margin-bottom:32px;}
.wel-chip{
  display:flex;align-items:center;gap:12px;
  background:var(--bg);border:1px solid var(--border);
  border-radius:var(--radius);padding:12px 16px;
  cursor:pointer;transition:all 0.18s;
  box-shadow:var(--shadow-sm);
}
.wel-chip:hover{border-color:var(--accent-border);background:var(--accent-soft);transform:translateX(4px);}
.wel-chip-icon{font-size:1rem;flex-shrink:0;}
.wel-chip-text{font-size:0.84rem;color:var(--text-dim);}
.wel-chip:hover .wel-chip-text{color:var(--accent);}
.wel-chip-arr{margin-left:auto;color:var(--text-light);font-size:0.8rem;transition:transform 0.18s;}
.wel-chip:hover .wel-chip-arr{transform:translateX(3px);color:var(--accent);}

/* Messages */
.msg-page{max-width:680px;margin:0 auto;padding:20px 24px;}
.msg-group{margin-bottom:28px;animation:msgIn 0.3s ease;}
@keyframes msgIn{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:translateY(0)}}

.msg-user{
  display:flex;justify-content:flex-end;
  margin-bottom:6px;
}
.user-bubble{
  background:var(--user-bg);
  border:1px solid var(--border);
  border-radius:var(--radius-lg) var(--radius-lg) 4px var(--radius-lg);
  padding:11px 16px;max-width:80%;
  font-size:0.88rem;line-height:1.7;
}

.msg-jarvis{display:flex;gap:12px;align-items:flex-start;}
.j-av{
  width:28px;height:28px;flex-shrink:0;
  background:var(--accent);border-radius:7px;
  display:flex;align-items:center;justify-content:center;
  font-family:'Lora',serif;font-size:0.78rem;color:#fff;
  margin-top:3px;
}
.j-content{flex:1;min-width:0;}
.j-name{font-size:0.68rem;font-weight:500;color:var(--text-dim);letter-spacing:0.05em;text-transform:uppercase;margin-bottom:6px;}
.j-body{font-size:0.88rem;line-height:1.85;color:var(--text);}
.j-body p{margin:6px 0;}
.j-body strong{font-weight:600;}
.j-body ul,.j-body ol{padding-left:20px;margin:8px 0;}
.j-body li{margin:5px 0;line-height:1.75;}
.j-body h1,.j-body h2,.j-body h3{font-family:'Lora',serif;font-size:1rem;font-weight:500;margin:14px 0 6px;}
.j-body code{background:var(--bg2);border:1px solid var(--border);border-radius:5px;padding:1px 6px;font-size:0.81rem;color:var(--accent);}
.j-body pre{background:var(--bg2);border:1px solid var(--border);border-radius:var(--radius);padding:14px;margin:10px 0;overflow-x:auto;}
.j-body blockquote{border-left:3px solid var(--accent-border);padding-left:14px;color:var(--text-dim);margin:10px 0;}

.typing-cursor{display:inline-block;width:2px;height:0.9em;background:var(--accent);margin-left:1px;animation:cur 0.7s infinite;vertical-align:text-bottom;}
@keyframes cur{0%,100%{opacity:1}50%{opacity:0}}

.thinking{display:flex;align-items:center;gap:4px;padding:4px 0;}
.t-dot{width:5px;height:5px;border-radius:50%;background:var(--border2);animation:tdot 1.4s ease-in-out infinite;}
.t-dot:nth-child(2){animation-delay:0.2s}.t-dot:nth-child(3){animation-delay:0.4s}
@keyframes tdot{0%,100%{opacity:0.3;transform:scale(1)}50%{opacity:1;transform:scale(1.3)}}

/* Input */
.input-area{
  border-top:1px solid var(--border);
  padding:14px 24px 20px;
  background:var(--bg);flex-shrink:0;
}
.input-inner{
  max-width:680px;margin:0 auto;
  background:var(--bg2);
  border:1px solid var(--border2);
  border-radius:var(--radius-lg);
  transition:all 0.2s;
  box-shadow:var(--shadow-sm);
}
.input-inner:focus-within{
  background:var(--bg);
  border-color:var(--accent-border);
  box-shadow:0 0 0 3px var(--accent-soft),var(--shadow-sm);
}
.input-row{display:flex;align-items:flex-end;padding:12px 14px 10px;}
textarea{
  flex:1;background:transparent;border:none;outline:none;
  color:var(--text);font-family:'Inter',sans-serif;
  font-size:0.88rem;font-weight:300;resize:none;
  line-height:1.65;max-height:160px;min-height:24px;
}
textarea::placeholder{color:var(--text-light)}
.send-btn{
  width:32px;height:32px;background:var(--accent);
  border:none;border-radius:8px;cursor:pointer;
  display:flex;align-items:center;justify-content:center;
  flex-shrink:0;margin-left:9px;opacity:0.25;
  transition:all 0.15s;
}
.send-btn.on{opacity:1;box-shadow:0 2px 8px rgba(47,111,63,0.25);}
.send-btn svg{width:13px;height:13px;fill:#fff;}
.input-foot{
  display:flex;align-items:center;justify-content:center;
  padding:7px 14px;border-top:1px solid var(--border);
  font-size:0.63rem;color:var(--text-light);gap:6px;
}
.input-foot span{display:flex;align-items:center;gap:4px;}
</style>
</head>
<body>

<!-- LANDING -->
<div id="landing">
  <nav class="land-nav">
    <div class="land-nav-logo">
      <div class="nav-icon">J</div>
      <span class="nav-name">Jarvis</span>
    </div>
    <span class="nav-tag">Built by Om Raut</span>
  </nav>

  <div class="land-body">
    <div class="land-eyebrow"><div class="eye-dot"></div>AI Assistant &mdash; Live Now</div>
    <h1 class="land-h">Think it.<br><em>Ask Jarvis.</em><br>Get answers.</h1>
    <p class="land-p">A personal AI assistant built from scratch using Python, Flask & Groq. Ask anything — from coding help to exam prep to creative writing.</p>
    <div class="land-actions">
      <button class="btn-primary" onclick="startApp()">
        Start chatting
        <svg viewBox="0 0 24 24"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
      </button>
      <button class="btn-secondary" onclick="startApp()">See a demo</button>
    </div>
    <div class="land-cards">
      <div class="land-card"><div class="card-icon">⚡</div><div class="card-title">Fast</div><div class="card-desc">Powered by Llama 3.3 70B</div></div>
      <div class="land-card"><div class="card-icon">🧠</div><div class="card-title">Smart</div><div class="card-desc">Understands context deeply</div></div>
      <div class="land-card"><div class="card-icon">📱</div><div class="card-title">Mobile</div><div class="card-desc">Works great on any device</div></div>
      <div class="land-card"><div class="card-icon">🎨</div><div class="card-title">Beautiful</div><div class="card-desc">Notion-inspired clean UI</div></div>
    </div>
  </div>
  <div class="land-foot">© 2025 Om Raut &nbsp;·&nbsp; JARVIS AI &nbsp;·&nbsp; Deployed on Railway</div>
</div>

<!-- APP -->
<div id="app">
  <div class="topbar">
    <div class="tb-left">
      <div class="tb-logo">
        <div class="tb-icon">J</div>
        <span class="tb-name">Jarvis</span>
      </div>
      <div class="tb-divider"></div>
      <div class="tb-model"><div class="online-dot"></div>Online</div>
    </div>
    <div class="tb-right">
      <button class="new-chat-tb" onclick="newChat()">+ New chat</button>
      <button class="tb-btn" onclick="shareApp()">Share</button>
    </div>
  </div>

  <div class="chat-area" id="chat">
    <div class="welcome" id="welcome">
      <div class="wel-greeting">Good day! I'm <em>Jarvis</em>.</div>
      <p class="wel-sub">Your personal AI assistant by Om Raut. I can help you learn, code, write, and think. What's on your mind?</p>
      <div class="wel-section">Suggested prompts</div>
      <div class="wel-chips">
        <div class="wel-chip" onclick="suggest('Explain artificial intelligence simply')"><span class="wel-chip-icon">💡</span><span class="wel-chip-text">Explain artificial intelligence simply</span><span class="wel-chip-arr">→</span></div>
        <div class="wel-chip" onclick="suggest('Write a Python function to sort a list')"><span class="wel-chip-icon">🐍</span><span class="wel-chip-text">Write a Python function to sort a list</span><span class="wel-chip-arr">→</span></div>
        <div class="wel-chip" onclick="suggest('Help me understand machine learning')"><span class="wel-chip-icon">🧠</span><span class="wel-chip-text">Help me understand machine learning</span><span class="wel-chip-arr">→</span></div>
        <div class="wel-chip" onclick="suggest('Give me 5 productivity tips for students')"><span class="wel-chip-icon">📚</span><span class="wel-chip-text">Give me 5 productivity tips for students</span><span class="wel-chip-arr">→</span></div>
        <div class="wel-chip" onclick="suggest('Who are you and what can you do?')"><span class="wel-chip-icon">🤖</span><span class="wel-chip-text">Who are you and what can you do?</span><span class="wel-chip-arr">→</span></div>
      </div>
    </div>
  </div>

  <div class="input-area">
    <div class="input-inner">
      <div class="input-row">
        <textarea id="inp" rows="1" placeholder="Ask Jarvis anything..."
          oninput="resize(this);toggleSend(this)"
          onkeydown="if(event.key==='Enter'&&!event.shiftKey){event.preventDefault();send()}"></textarea>
        <button class="send-btn" id="sendbtn" onclick="send()">
          <svg viewBox="0 0 24 24"><path d="M2 21l21-9L2 3v7l15 2-15 2v7z"/></svg>
        </button>
      </div>
      <div class="input-foot">
        <span>↵ Enter to send</span>
        <span>·</span>
        <span>Shift + Enter for new line</span>
        <span>·</span>
        <span>Built by Om Raut</span>
      </div>
    </div>
  </div>
</div>

<script>
marked.setOptions({breaks:true,gfm:true});
var chat=document.getElementById('chat'),inp=document.getElementById('inp'),welcome=document.getElementById('welcome'),hasMsg=false;

function startApp(){
  document.getElementById('landing').classList.add('out');
  setTimeout(function(){
    document.getElementById('landing').style.display='none';
    var app=document.getElementById('app');
    app.classList.add('show');
    inp.focus();
  },480);
}

function shareApp(){
  if(navigator.share){navigator.share({title:'JARVIS AI by Om Raut',url:window.location.href});}
  else{navigator.clipboard.writeText(window.location.href).then(function(){alert('Link copied to clipboard!');});}
}

function resize(el){el.style.height='auto';el.style.height=Math.min(el.scrollHeight,160)+'px';}
function toggleSend(el){document.getElementById('sendbtn').classList.toggle('on',el.value.trim().length>0);}
function suggest(t){inp.value=t;toggleSend(inp);send();}

function newChat(){
  while(chat.firstChild)chat.removeChild(chat.firstChild);
  chat.appendChild(welcome);
  welcome.style.display='block';
  hasMsg=false;inp.value='';inp.style.height='auto';
}

function send(){
  var msg=inp.value.trim();if(!msg)return;
  if(!hasMsg){welcome.style.display='none';hasMsg=true;}
  addUser(msg);
  inp.value='';inp.style.height='auto';
  document.getElementById('sendbtn').classList.remove('on');
  var t=addThink();
  fetch('/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message:msg})})
    .then(r=>r.json()).then(d=>{t.remove();typeJarvis(d.reply);})
    .catch(()=>{t.remove();typeJarvis('Something went wrong. Please try again.');});
}

function addUser(text){
  var pg=document.createElement('div');pg.className='msg-page';
  var g=document.createElement('div');g.className='msg-group';
  var u=document.createElement('div');u.className='msg-user';
  var b=document.createElement('div');b.className='user-bubble';b.textContent=text;
  u.appendChild(b);g.appendChild(u);pg.appendChild(g);
  chat.appendChild(pg);chat.scrollTop=chat.scrollHeight;
}

function typeJarvis(text){
  var pg=document.createElement('div');pg.className='msg-page';
  var g=document.createElement('div');g.className='msg-group';
  var j=document.createElement('div');j.className='msg-jarvis';
  var av=document.createElement('div');av.className='j-av';av.textContent='J';
  var con=document.createElement('div');con.className='j-content';
  var nm=document.createElement('div');nm.className='j-name';nm.textContent='Jarvis';
  var body=document.createElement('div');body.className='j-body';
  con.appendChild(nm);con.appendChild(body);
  j.appendChild(av);j.appendChild(con);g.appendChild(j);pg.appendChild(g);
  chat.appendChild(pg);

  var words=text.split(' ');var current='';var i=0;
  var cursor=document.createElement('span');cursor.className='typing-cursor';

  function next(){
    if(i<words.length){
      current+=(i>0?' ':'')+words[i];
      body.innerHTML=marked.parse(current);
      body.appendChild(cursor);
      chat.scrollTop=chat.scrollHeight;
      i++;setTimeout(next,16);
    } else {
      body.innerHTML=marked.parse(current);
      chat.scrollTop=chat.scrollHeight;
    }
  }
  next();
}

function addThink(){
  var pg=document.createElement('div');pg.className='msg-page';
  var g=document.createElement('div');g.className='msg-group';
  var j=document.createElement('div');j.className='msg-jarvis';
  var av=document.createElement('div');av.className='j-av';av.textContent='J';
  var con=document.createElement('div');con.className='j-content';
  var nm=document.createElement('div');nm.className='j-name';nm.textContent='Jarvis';
  var body=document.createElement('div');body.className='j-body';
  body.innerHTML='<div class="thinking"><div class="t-dot"></div><div class="t-dot"></div><div class="t-dot"></div></div>';
  con.appendChild(nm);con.appendChild(body);
  j.appendChild(av);j.appendChild(con);g.appendChild(j);pg.appendChild(g);
  chat.appendChild(pg);chat.scrollTop=chat.scrollHeight;
  return pg;
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
