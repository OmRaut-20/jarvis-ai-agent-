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
<title>JARVIS AI</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=DM+Serif+Display:ital@0;1&display=swap" rel="stylesheet">
<script src="https://cdnjs.cloudflare.com/ajax/libs/marked/9.1.6/marked.min.js"></script>
<style>
*{margin:0;padding:0;box-sizing:border-box}
:root{
  --bg:#f8f6f2;
  --sidebar:#f1ede7;
  --surface:#ffffff;
  --surface2:#f4f1ec;
  --border:#e6e1da;
  --border2:#d9d4cc;
  --text:#1a1714;
  --text-dim:#8c877f;
  --text-light:#c0bab2;
  --accent:#5a7a4a;
  --accent2:#7a9e68;
  --accent-light:#eaf0e5;
  --user-bg:#edeae4;
  --shadow:rgba(0,0,0,0.07);
}

html,body{height:100%;overflow:hidden;}
body{background:var(--bg);color:var(--text);font-family:'Inter',sans-serif;}

/* ===== LANDING PAGE ===== */
#landing{
  position:fixed;inset:0;
  background:var(--bg);
  display:flex;flex-direction:column;
  align-items:center;justify-content:center;
  z-index:100;padding:24px;
  text-align:center;
  transition:opacity 0.6s ease, transform 0.6s ease;
}
#landing.hide{opacity:0;transform:translateY(-20px);pointer-events:none;}

.land-badge{
  display:inline-flex;align-items:center;gap:8px;
  background:var(--accent-light);border:1px solid #c8dbb8;
  border-radius:20px;padding:6px 16px;
  font-size:0.75rem;color:var(--accent);
  font-weight:500;letter-spacing:0.05em;
  margin-bottom:32px;
  animation:fadeUp 0.6s ease 0.1s both;
}
.land-dot{width:6px;height:6px;background:var(--accent2);border-radius:50%;animation:breathe 2s infinite;}
@keyframes breathe{0%,100%{opacity:0.4}50%{opacity:1}}

.land-icon{
  width:90px;height:90px;
  background:var(--accent);
  border-radius:28px;
  display:flex;align-items:center;justify-content:center;
  font-family:'DM Serif Display',serif;
  font-size:2.4rem;color:#fff;
  margin:0 auto 28px;
  box-shadow:0 12px 40px rgba(90,122,74,0.3);
  animation:fadeUp 0.6s ease 0.2s both, float 4s ease-in-out 1s infinite;
}
@keyframes float{0%,100%{transform:translateY(0)}50%{transform:translateY(-8px)}}
@keyframes fadeUp{from{opacity:0;transform:translateY(20px)}to{opacity:1;transform:translateY(0)}}

.land-title{
  font-family:'DM Serif Display',serif;
  font-size:clamp(2.2rem,6vw,3.8rem);
  color:var(--text);line-height:1.1;
  margin-bottom:16px;
  animation:fadeUp 0.6s ease 0.3s both;
}
.land-title em{font-style:italic;color:var(--accent);}

.land-sub{
  font-size:clamp(0.9rem,2.5vw,1.05rem);
  color:var(--text-dim);max-width:480px;
  line-height:1.7;margin-bottom:40px;
  animation:fadeUp 0.6s ease 0.4s both;
}

.land-cta{
  display:inline-flex;align-items:center;gap:10px;
  background:var(--accent);color:#fff;
  border:none;border-radius:14px;
  padding:16px 32px;cursor:pointer;
  font-family:'Inter',sans-serif;font-size:0.95rem;font-weight:500;
  transition:all 0.2s;
  box-shadow:0 4px 20px rgba(90,122,74,0.35);
  animation:fadeUp 0.6s ease 0.5s both;
}
.land-cta:hover{background:var(--accent2);transform:translateY(-2px);box-shadow:0 8px 28px rgba(90,122,74,0.4);}
.land-cta svg{width:18px;height:18px;fill:#fff;transition:transform 0.2s;}
.land-cta:hover svg{transform:translateX(3px);}

.land-features{
  display:flex;flex-wrap:wrap;gap:12px;
  justify-content:center;max-width:500px;
  margin-top:40px;
  animation:fadeUp 0.6s ease 0.6s both;
}
.land-feat{
  display:flex;align-items:center;gap:7px;
  background:var(--surface);border:1px solid var(--border);
  border-radius:10px;padding:9px 14px;
  font-size:0.78rem;color:var(--text-dim);
  box-shadow:0 1px 4px var(--shadow);
}
.land-feat-icon{font-size:0.9rem;}

.land-credit{
  margin-top:32px;font-size:0.72rem;
  color:var(--text-light);letter-spacing:0.05em;
  animation:fadeUp 0.6s ease 0.7s both;
}

/* ===== APP ===== */
#app{
  display:none;flex;height:100vh;
  opacity:0;transition:opacity 0.5s ease;
}
#app.show{display:flex;opacity:1;}

/* Sidebar */
.sidebar{
  width:240px;flex-shrink:0;
  background:var(--sidebar);
  border-right:1px solid var(--border);
  display:flex;flex-direction:column;
  height:100vh;
  transition:transform 0.3s ease;
}
@media(max-width:768px){
  .sidebar{position:fixed;left:0;top:0;bottom:0;z-index:50;transform:translateX(-100%);}
  .sidebar.open{transform:translateX(0);box-shadow:4px 0 20px var(--shadow);}
}
.sidebar-header{padding:20px 14px 14px;}
.logo-wrap{display:flex;align-items:center;gap:10px;margin-bottom:18px;}
.logo-icon{width:32px;height:32px;background:var(--accent);border-radius:9px;display:flex;align-items:center;justify-content:center;font-family:'DM Serif Display',serif;font-size:0.95rem;color:#fff;box-shadow:0 2px 8px rgba(90,122,74,0.3);}
.logo-text{font-family:'DM Serif Display',serif;font-size:1.1rem;color:var(--text);}
.new-btn{width:100%;background:var(--surface);border:1px solid var(--border2);color:var(--text-dim);border-radius:10px;padding:9px 14px;cursor:pointer;font-family:'Inter',sans-serif;font-size:0.81rem;transition:all 0.2s;display:flex;align-items:center;gap:8px;box-shadow:0 1px 3px var(--shadow);}
.new-btn:hover{color:var(--text);border-color:var(--accent2);background:var(--accent-light);}
.section-label{font-size:0.61rem;color:var(--text-light);letter-spacing:0.12em;text-transform:uppercase;padding:0 14px;margin:14px 0 6px;}
.chat-list{padding:0 6px;flex:1;overflow-y:auto;}
.chat-entry{padding:8px 10px;border-radius:8px;font-size:0.8rem;color:var(--text-dim);cursor:pointer;transition:all 0.15s;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;margin-bottom:1px;}
.chat-entry:hover{background:var(--surface);color:var(--text);}
.chat-entry.active{background:var(--surface);color:var(--text);}
.sidebar-footer{padding:14px;border-top:1px solid var(--border);}
.user-card{display:flex;align-items:center;gap:10px;padding:9px;border-radius:10px;cursor:pointer;transition:all 0.15s;}
.user-card:hover{background:var(--surface);}
.avatar{width:32px;height:32px;background:var(--accent);border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:0.82rem;font-weight:500;color:#fff;flex-shrink:0;}
.user-name{font-size:0.83rem;font-weight:500;}
.user-sub{font-size:0.67rem;color:var(--text-light);}

/* Main */
.main{flex:1;display:flex;flex-direction:column;height:100vh;overflow:hidden;min-width:0;}

/* Topbar */
.topbar{display:flex;align-items:center;justify-content:space-between;padding:12px 18px;border-bottom:1px solid var(--border);flex-shrink:0;background:var(--surface);}
.topbar-left{display:flex;align-items:center;gap:12px;}
.menu-btn{display:none;background:transparent;border:none;cursor:pointer;padding:6px;border-radius:8px;color:var(--text-dim);}
.menu-btn:hover{background:var(--surface2);}
@media(max-width:768px){.menu-btn{display:flex;align-items:center;justify-content:center;}}
.model-pill{display:flex;align-items:center;gap:7px;background:var(--surface2);border:1px solid var(--border);border-radius:20px;padding:5px 13px;font-size:0.78rem;color:var(--text-dim);}
.status-dot{width:6px;height:6px;background:var(--accent2);border-radius:50%;animation:breathe 3s ease-in-out infinite;}
.share-btn{background:transparent;border:1px solid var(--border2);color:var(--text-dim);border-radius:8px;padding:6px 14px;cursor:pointer;font-size:0.77rem;font-family:'Inter',sans-serif;transition:all 0.15s;}
.share-btn:hover{color:var(--text);background:var(--surface2);}

/* Chat */
.chat-area{flex:1;overflow-y:auto;scroll-behavior:smooth;}
.chat-area::-webkit-scrollbar{width:3px}
.chat-area::-webkit-scrollbar-thumb{background:var(--border2);border-radius:2px}

/* Welcome */
.welcome{display:flex;flex-direction:column;align-items:center;justify-content:center;min-height:100%;padding:40px 20px;text-align:center;}
.welcome-icon{width:64px;height:64px;background:var(--accent);border-radius:18px;display:flex;align-items:center;justify-content:center;font-family:'DM Serif Display',serif;font-size:1.8rem;color:#fff;margin-bottom:20px;box-shadow:0 6px 24px rgba(90,122,74,0.25);animation:float 4s ease-in-out infinite;}
.welcome h1{font-family:'DM Serif Display',serif;font-size:1.7rem;margin-bottom:8px;}
.welcome p{font-size:0.86rem;color:var(--text-dim);max-width:380px;line-height:1.7;margin-bottom:28px;}
.chips{display:flex;flex-wrap:wrap;gap:9px;justify-content:center;max-width:520px;}
.chip{background:var(--surface);border:1px solid var(--border);border-radius:11px;padding:10px 14px;cursor:pointer;font-size:0.8rem;color:var(--text-dim);transition:all 0.2s;text-align:left;line-height:1.5;box-shadow:0 1px 4px var(--shadow);}
.chip:hover{background:var(--accent-light);color:var(--accent);border-color:var(--accent2);transform:translateY(-2px);box-shadow:0 4px 12px rgba(90,122,74,0.15);}

/* Messages */
.msg-wrap{max-width:700px;margin:0 auto;padding:8px 18px;}
.msg-row{display:flex;gap:12px;align-items:flex-start;animation:msgIn 0.3s ease;}
@keyframes msgIn{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:translateY(0)}}
.msg-row.user{justify-content:flex-end;margin-bottom:12px;}
.msg-row.jarvis{margin-bottom:16px;}
.j-avatar{width:30px;height:30px;flex-shrink:0;background:var(--accent);border-radius:8px;display:flex;align-items:center;justify-content:center;font-family:'DM Serif Display',serif;font-size:0.8rem;color:#fff;margin-top:2px;box-shadow:0 2px 6px rgba(90,122,74,0.2);}
.user-bubble{background:var(--user-bg);border:1px solid var(--border);border-radius:14px 14px 2px 14px;padding:10px 15px;max-width:78%;font-size:0.86rem;line-height:1.7;}
.j-body{flex:1;padding-top:2px;}
.j-body p{margin:5px 0;font-size:0.86rem;line-height:1.8;color:var(--text);}
.j-body strong{font-weight:600;}
.j-body ul,.j-body ol{padding-left:20px;margin:7px 0;}
.j-body li{margin:4px 0;font-size:0.86rem;line-height:1.7;}
.j-body h1,.j-body h2,.j-body h3{font-family:'DM Serif Display',serif;font-size:1.02rem;font-weight:400;margin:12px 0 5px;}
.j-body code{background:var(--surface2);border:1px solid var(--border);border-radius:4px;padding:1px 5px;font-size:0.8rem;color:var(--accent);}
.j-body pre{background:var(--surface2);border:1px solid var(--border);border-radius:9px;padding:12px;margin:9px 0;overflow-x:auto;}

/* Typing cursor */
.typing-cursor{display:inline-block;width:2px;height:1em;background:var(--accent);margin-left:1px;animation:blink 0.7s infinite;vertical-align:text-bottom;}
@keyframes blink{0%,100%{opacity:1}50%{opacity:0}}

.thinking{display:flex;align-items:center;gap:5px;padding:6px 0;}
.t-dot{width:5px;height:5px;border-radius:50%;background:var(--border2);animation:think 1.4s ease-in-out infinite;}
.t-dot:nth-child(2){animation-delay:0.2s}.t-dot:nth-child(3){animation-delay:0.4s}
@keyframes think{0%,100%{opacity:0.3;transform:scale(1)}50%{opacity:1;transform:scale(1.3)}}

/* Input */
.input-wrap{padding:10px 18px 18px;flex-shrink:0;background:var(--surface);}
.input-box{max-width:700px;margin:0 auto;background:var(--surface);border:1px solid var(--border2);border-radius:14px;transition:all 0.2s;box-shadow:0 2px 12px var(--shadow);}
.input-box:focus-within{border-color:var(--accent2);box-shadow:0 2px 16px rgba(90,122,74,0.12);}
.input-inner{display:flex;align-items:flex-end;padding:12px 13px 10px;}
textarea{flex:1;background:transparent;border:none;outline:none;color:var(--text);font-family:'Inter',sans-serif;font-size:0.86rem;font-weight:300;resize:none;line-height:1.6;max-height:160px;min-height:24px;}
textarea::placeholder{color:var(--text-light)}
.send{width:33px;height:33px;background:var(--accent);border:none;border-radius:9px;cursor:pointer;display:flex;align-items:center;justify-content:center;flex-shrink:0;margin-left:9px;transition:all 0.15s;opacity:0.3;}
.send.on{opacity:1;box-shadow:0 2px 8px rgba(90,122,74,0.3);}
.send:hover{background:var(--accent2);}
.send svg{width:13px;height:13px;fill:#fff;}
.input-hint{text-align:center;padding:6px;font-size:0.63rem;color:var(--text-light);border-top:1px solid var(--border);}

/* Overlay for mobile sidebar */
.overlay{display:none;position:fixed;inset:0;background:rgba(0,0,0,0.3);z-index:40;}
.overlay.show{display:block;}
</style>
</head>
<body>

<!-- LANDING PAGE -->
<div id="landing">
  <div class="land-badge">
    <div class="land-dot"></div>
    AI Assistant by Om Raut
  </div>
  <div class="land-icon">J</div>
  <h1 class="land-title">Meet <em>Jarvis</em>,<br>Your Personal AI</h1>
  <p class="land-sub">An intelligent assistant that thinks, explains, and helps — built from scratch by Om Raut using Python, Flask, and Groq AI.</p>
  <button class="land-cta" onclick="startApp()">
    Start Chatting
    <svg viewBox="0 0 24 24"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
  </button>
  <div class="land-features">
    <div class="land-feat"><span class="land-feat-icon">🧠</span> Powered by Llama 3.3</div>
    <div class="land-feat"><span class="land-feat-icon">⚡</span> Fast responses</div>
    <div class="land-feat"><span class="land-feat-icon">🎨</span> Beautiful UI</div>
    <div class="land-feat"><span class="land-feat-icon">📱</span> Mobile friendly</div>
  </div>
  <div class="land-credit">Built with ❤️ by Om Raut &nbsp;·&nbsp; Deployed on Railway</div>
</div>

<!-- MAIN APP -->
<div id="app">
  <div class="overlay" id="overlay" onclick="closeSidebar()"></div>
  <div class="sidebar" id="sidebar">
    <div class="sidebar-header">
      <div class="logo-wrap">
        <div class="logo-icon">J</div>
        <div class="logo-text">Jarvis</div>
      </div>
      <button class="new-btn" onclick="newChat()">+ &nbsp; New conversation</button>
    </div>
    <div class="section-label">Recent</div>
    <div class="chat-list"><div class="chat-entry active" id="current-chat">New conversation</div></div>
    <div class="sidebar-footer">
      <div class="user-card">
        <div class="avatar">O</div>
        <div><div class="user-name">Om Raut</div><div class="user-sub">JARVIS AI</div></div>
      </div>
    </div>
  </div>

  <div class="main">
    <div class="topbar">
      <div class="topbar-left">
        <button class="menu-btn" onclick="toggleSidebar()">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="18" x2="21" y2="18"/></svg>
        </button>
        <div class="model-pill"><div class="status-dot"></div>JARVIS &mdash; Online</div>
      </div>
      <button class="share-btn" onclick="shareApp()">Share</button>
    </div>

    <div class="chat-area" id="chat">
      <div class="welcome" id="welcome">
        <div class="welcome-icon">J</div>
        <h1>Hi, I'm Jarvis</h1>
        <p>Your personal AI assistant by Om Raut. Ask me anything!</p>
        <div class="chips">
          <div class="chip" onclick="suggest('Explain AI in simple words')">💡 Explain AI simply</div>
          <div class="chip" onclick="suggest('Write a Python function for me')">🐍 Write Python code</div>
          <div class="chip" onclick="suggest('What is machine learning?')">🧠 Machine learning?</div>
          <div class="chip" onclick="suggest('Help me prepare for my exam')">📚 Exam help</div>
          <div class="chip" onclick="suggest('Who are you?')">🤖 Who are you?</div>
          <div class="chip" onclick="suggest('Give me productivity tips')">⚡ Productivity tips</div>
        </div>
      </div>
    </div>

    <div class="input-wrap">
      <div class="input-box">
        <div class="input-inner">
          <textarea id="inp" rows="1" placeholder="Message Jarvis..."
            oninput="resize(this);toggleSend(this)"
            onkeydown="if(event.key==='Enter'&&!event.shiftKey){event.preventDefault();send()}"></textarea>
          <button class="send" id="sendbtn" onclick="send()">
            <svg viewBox="0 0 24 24"><path d="M2 21l21-9L2 3v7l15 2-15 2v7z"/></svg>
          </button>
        </div>
        <div class="input-hint">Jarvis can make mistakes &nbsp;·&nbsp; Built by Om Raut</div>
      </div>
    </div>
  </div>
</div>

<script>
marked.setOptions({breaks:true,gfm:true});
var chat=document.getElementById('chat'),inp=document.getElementById('inp'),welcome=document.getElementById('welcome'),hasMsg=false;

function startApp(){
  document.getElementById('landing').classList.add('hide');
  setTimeout(function(){
    document.getElementById('app').style.display='flex';
    setTimeout(function(){document.getElementById('app').classList.add('show');},50);
  },500);
}

function toggleSidebar(){
  document.getElementById('sidebar').classList.toggle('open');
  document.getElementById('overlay').classList.toggle('show');
}
function closeSidebar(){
  document.getElementById('sidebar').classList.remove('open');
  document.getElementById('overlay').classList.remove('show');
}
function shareApp(){
  if(navigator.share){navigator.share({title:'JARVIS AI',url:window.location.href});}
  else{navigator.clipboard.writeText(window.location.href);alert('Link copied!');}
}
function resize(el){el.style.height='auto';el.style.height=Math.min(el.scrollHeight,160)+'px';}
function toggleSend(el){document.getElementById('sendbtn').classList.toggle('on',el.value.trim().length>0);}
function suggest(t){inp.value=t;toggleSend(inp);send();}
function newChat(){
  while(chat.firstChild)chat.removeChild(chat.firstChild);
  chat.appendChild(welcome);welcome.style.display='flex';
  hasMsg=false;inp.value='';document.getElementById('current-chat').textContent='New conversation';
  closeSidebar();
}

function send(){
  var msg=inp.value.trim();if(!msg)return;
  if(!hasMsg){welcome.style.display='none';hasMsg=true;}
  if(document.getElementById('current-chat').textContent==='New conversation')
    document.getElementById('current-chat').textContent=msg.substring(0,26)+'...';
  addUser(msg);inp.value='';inp.style.height='auto';
  document.getElementById('sendbtn').classList.remove('on');
  var t=addThink();
  fetch('/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message:msg})})
    .then(r=>r.json()).then(d=>{t.remove();typeJarvis(d.reply);})
    .catch(()=>{t.remove();typeJarvis('Something went wrong. Please try again.');});
}

function addUser(text){
  var w=document.createElement('div');w.className='msg-wrap';
  var r=document.createElement('div');r.className='msg-row user';
  var b=document.createElement('div');b.className='user-bubble';b.textContent=text;
  r.appendChild(b);w.appendChild(r);chat.appendChild(w);chat.scrollTop=chat.scrollHeight;
}

function typeJarvis(text){
  var w=document.createElement('div');w.className='msg-wrap';
  var r=document.createElement('div');r.className='msg-row jarvis';
  var av=document.createElement('div');av.className='j-avatar';av.textContent='J';
  var body=document.createElement('div');body.className='j-body';
  r.appendChild(av);r.appendChild(body);w.appendChild(r);chat.appendChild(w);

  // Type word by word
  var words=text.split(' ');
  var current='';
  var i=0;
  var cursor=document.createElement('span');cursor.className='typing-cursor';

  function typeNext(){
    if(i<words.length){
      current+=( i>0?' ':'')+words[i];
      body.innerHTML=marked.parse(current);
      body.appendChild(cursor);
      chat.scrollTop=chat.scrollHeight;
      i++;
      setTimeout(typeNext, 18);
    } else {
      body.innerHTML=marked.parse(current);
      chat.scrollTop=chat.scrollHeight;
    }
  }
  typeNext();
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
