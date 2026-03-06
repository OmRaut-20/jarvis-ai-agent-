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
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet">
<script src="https://cdnjs.cloudflare.com/ajax/libs/marked/9.1.6/marked.min.js"></script>
<style>
*{margin:0;padding:0;box-sizing:border-box}
:root{
  --bg:#0d0d0d;
  --sidebar:#141414;
  --surface:#1a1a1a;
  --border:#2a2a2a;
  --text:#ececec;
  --text-dim:#888;
  --text-light:#444;
  --accent:#10a37f;
  --accent-dim:#0d8a6c;
  --user-bg:#2a2a2a;
}
body{background:var(--bg);color:var(--text);font-family:'Inter',sans-serif;min-height:100vh;display:flex;overflow:hidden;}

/* Sidebar */
.sidebar{
  width:260px;flex-shrink:0;
  background:var(--sidebar);
  border-right:1px solid var(--border);
  display:flex;flex-direction:column;
  padding:16px;
  height:100vh;
}
.sidebar-logo{
  display:flex;align-items:center;gap:10px;
  padding:12px 8px;margin-bottom:8px;
}
.logo-icon{
  width:32px;height:32px;
  background:var(--accent);
  border-radius:8px;
  display:flex;align-items:center;justify-content:center;
  font-size:1rem;font-weight:700;color:#fff;
}
.logo-text{font-size:1rem;font-weight:600;color:var(--text);}
.new-chat-btn{
  display:flex;align-items:center;gap:8px;
  background:transparent;border:1px solid var(--border);
  color:var(--text);border-radius:8px;
  padding:10px 14px;cursor:pointer;
  font-family:'Inter',sans-serif;font-size:0.85rem;
  transition:all 0.15s;margin-bottom:20px;
  width:100%;
}
.new-chat-btn:hover{background:var(--surface);}
.new-chat-btn span{font-size:1.1rem;}
.sidebar-section{font-size:0.68rem;color:var(--text-dim);letter-spacing:0.1em;text-transform:uppercase;padding:0 8px;margin-bottom:8px;}
.chat-item{
  padding:10px 12px;border-radius:8px;
  font-size:0.82rem;color:var(--text-dim);
  cursor:pointer;transition:all 0.15s;
  white-space:nowrap;overflow:hidden;text-overflow:ellipsis;
  margin-bottom:2px;
}
.chat-item:hover{background:var(--surface);color:var(--text);}
.chat-item.active{background:var(--surface);color:var(--text);}
.sidebar-bottom{margin-top:auto;border-top:1px solid var(--border);padding-top:16px;}
.user-info{display:flex;align-items:center;gap:10px;padding:8px;border-radius:8px;cursor:pointer;transition:all 0.15s;}
.user-info:hover{background:var(--surface);}
.avatar{width:32px;height:32px;background:linear-gradient(135deg,#667eea,#764ba2);border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:0.8rem;font-weight:600;color:#fff;flex-shrink:0;}
.user-name{font-size:0.85rem;font-weight:500;}
.user-plan{font-size:0.7rem;color:var(--text-dim);}

/* Main */
.main{flex:1;display:flex;flex-direction:column;height:100vh;overflow:hidden;}

/* Top bar */
.topbar{
  display:flex;align-items:center;justify-content:space-between;
  padding:14px 24px;border-bottom:1px solid var(--border);
  flex-shrink:0;
}
.model-selector{
  display:flex;align-items:center;gap:8px;
  background:var(--surface);border:1px solid var(--border);
  border-radius:8px;padding:8px 14px;cursor:pointer;
  font-size:0.85rem;color:var(--text);
}
.model-dot{width:8px;height:8px;background:var(--accent);border-radius:50%;}
.topbar-actions{display:flex;gap:8px;}
.topbar-btn{
  background:transparent;border:1px solid var(--border);
  color:var(--text-dim);border-radius:8px;
  padding:8px 14px;cursor:pointer;font-size:0.8rem;
  font-family:'Inter',sans-serif;transition:all 0.15s;
}
.topbar-btn:hover{background:var(--surface);color:var(--text);}

/* Chat area */
.chat-area{flex:1;overflow-y:auto;padding:32px 0;}
.chat-area::-webkit-scrollbar{width:4px}
.chat-area::-webkit-scrollbar-thumb{background:var(--border);border-radius:2px}

.welcome{
  display:flex;flex-direction:column;align-items:center;
  justify-content:center;height:100%;gap:16px;
  padding:40px;text-align:center;
}
.welcome-icon{
  width:56px;height:56px;background:var(--accent);
  border-radius:16px;display:flex;align-items:center;
  justify-content:center;font-size:1.5rem;font-weight:700;color:#fff;
  margin-bottom:8px;
}
.welcome h1{font-size:1.8rem;font-weight:600;color:var(--text);}
.welcome p{font-size:0.95rem;color:var(--text-dim);max-width:400px;line-height:1.6;}
.suggestions{display:flex;flex-wrap:wrap;gap:10px;justify-content:center;margin-top:16px;}
.suggestion{
  background:var(--surface);border:1px solid var(--border);
  border-radius:10px;padding:12px 16px;cursor:pointer;
  font-size:0.82rem;color:var(--text-dim);transition:all 0.15s;
  max-width:200px;text-align:left;line-height:1.5;
}
.suggestion:hover{background:var(--border);color:var(--text);}

.message-row{
  max-width:720px;margin:0 auto;padding:8px 24px;
  animation:fadeIn 0.3s ease;
}
@keyframes fadeIn{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:translateY(0)}}
.message-row.user{display:flex;justify-content:flex-end;}
.message-row.jarvis{display:flex;justify-content:flex-start;gap:12px;align-items:flex-start;}

.jarvis-avatar{
  width:32px;height:32px;background:var(--accent);
  border-radius:8px;display:flex;align-items:center;
  justify-content:center;font-size:0.75rem;font-weight:700;
  color:#fff;flex-shrink:0;margin-top:2px;
}
.user-bubble{
  background:var(--user-bg);border-radius:12px 12px 2px 12px;
  padding:12px 16px;max-width:80%;font-size:0.9rem;
  line-height:1.7;color:var(--text);
}
.jarvis-content{
  flex:1;font-size:0.9rem;line-height:1.8;color:var(--text);
  font-weight:300;padding-top:4px;
}
.jarvis-content p{margin:6px 0;}
.jarvis-content strong{font-weight:600;color:#fff;}
.jarvis-content ul,.jarvis-content ol{padding-left:20px;margin:8px 0;}
.jarvis-content li{margin:5px 0;}
.jarvis-content h1,.jarvis-content h2,.jarvis-content h3{font-size:1rem;font-weight:600;margin:12px 0 6px;color:#fff;}

.thinking{display:flex;align-items:center;gap:5px;padding:8px 0;}
.t-dot{width:6px;height:6px;border-radius:50%;background:var(--accent);animation:think 1.4s ease-in-out infinite;}
.t-dot:nth-child(2){animation-delay:0.2s}.t-dot:nth-child(3){animation-delay:0.4s}
@keyframes think{0%,100%{opacity:0.3;transform:translateY(0)}50%{opacity:1;transform:translateY(-3px)}}

/* Input */
.input-container{
  padding:16px 24px 24px;flex-shrink:0;
}
.input-box{
  max-width:720px;margin:0 auto;
  background:var(--surface);border:1px solid var(--border);
  border-radius:14px;overflow:hidden;
  transition:border-color 0.2s,box-shadow 0.2s;
  box-shadow:0 0 0 0 transparent;
}
.input-box:focus-within{
  border-color:#404040;
  box-shadow:0 0 0 3px rgba(16,163,127,0.1);
}
.input-top{display:flex;align-items:flex-end;padding:12px 16px;}
textarea{
  flex:1;background:transparent;border:none;outline:none;
  color:var(--text);font-family:'Inter',sans-serif;
  font-size:0.9rem;font-weight:300;resize:none;
  line-height:1.6;max-height:200px;min-height:24px;
  padding:0;
}
textarea::placeholder{color:var(--text-light)}
.send-btn{
  width:34px;height:34px;background:var(--accent);
  border:none;border-radius:8px;cursor:pointer;
  display:flex;align-items:center;justify-content:center;
  flex-shrink:0;margin-left:8px;transition:all 0.15s;
  opacity:0.5;
}
.send-btn.active{opacity:1;}
.send-btn:hover{background:var(--accent-dim);}
.send-btn svg{width:16px;height:16px;fill:#fff;}
.input-footer{
  display:flex;align-items:center;justify-content:center;
  padding:8px 16px;border-top:1px solid var(--border);
}
.input-footer span{font-size:0.68rem;color:var(--text-light);letter-spacing:0.05em;}
</style>
</head>
<body>

<!-- Sidebar -->
<div class="sidebar">
  <div class="sidebar-logo">
    <div class="logo-icon">J</div>
    <div class="logo-text">JARVIS</div>
  </div>
  <button class="new-chat-btn" onclick="newChat()">
    <span>+</span> New chat
  </button>
  <div class="sidebar-section">Recent</div>
  <div class="chat-item active" id="current-chat">New conversation</div>
  <div class="sidebar-bottom">
    <div class="user-info">
      <div class="avatar">O</div>
      <div>
        <div class="user-name">Om Raut</div>
        <div class="user-plan">JARVIS AI</div>
      </div>
    </div>
  </div>
</div>

<!-- Main -->
<div class="main">
  <div class="topbar">
    <div class="model-selector">
      <div class="model-dot"></div>
      JARVIS — Llama 3.3
    </div>
    <div class="topbar-actions">
      <button class="topbar-btn">Share</button>
    </div>
  </div>

  <div class="chat-area" id="chat">
    <div class="welcome" id="welcome">
      <div class="welcome-icon">J</div>
      <h1>What can I help with?</h1>
      <p>Ask me anything — I'm JARVIS, your personal AI assistant built by Om Raut.</p>
      <div class="suggestions">
        <div class="suggestion" onclick="suggest('Explain AI in simple words')">💡 Explain AI in simple words</div>
        <div class="suggestion" onclick="suggest('Write a Python function')">🐍 Write a Python function</div>
        <div class="suggestion" onclick="suggest('What is machine learning?')">🤖 What is machine learning?</div>
        <div class="suggestion" onclick="suggest('Help me study for exams')">📚 Help me study for exams</div>
      </div>
    </div>
  </div>

  <div class="input-container">
    <div class="input-box">
      <div class="input-top">
        <textarea id="inp" rows="1" placeholder="Ask JARVIS anything..."
          oninput="autoResize(this);toggleSend(this)"
          onkeydown="if(event.key==='Enter'&&!event.shiftKey){event.preventDefault();send()}"></textarea>
        <button class="send-btn" id="send-btn" onclick="send()">
          <svg viewBox="0 0 24 24"><path d="M2 21l21-9L2 3v7l15 2-15 2v7z"/></svg>
        </button>
      </div>
      <div class="input-footer">
        <span>JARVIS can make mistakes. Built by Om Raut.</span>
      </div>
    </div>
  </div>
</div>

<script>
marked.setOptions({breaks:true,gfm:true});
var chat=document.getElementById('chat');
var inp=document.getElementById('inp');
var welcome=document.getElementById('welcome');
var hasMessages=false;
var msgCount=0;

function autoResize(el){el.style.height='auto';el.style.height=Math.min(el.scrollHeight,200)+'px';}
function toggleSend(el){document.getElementById('send-btn').classList.toggle('active',el.value.trim().length>0);}

function suggest(text){inp.value=text;toggleSend(inp);send();}

function newChat(){
  chat.innerHTML='';
  chat.appendChild(welcome);
  welcome.style.display='flex';
  hasMessages=false;
  inp.value='';
  document.getElementById('current-chat').textContent='New conversation';
}

function send(){
  var msg=inp.value.trim();if(!msg)return;
  if(!hasMessages){welcome.style.display='none';hasMessages=true;}
  if(msgCount===0) document.getElementById('current-chat').textContent=msg.substring(0,30)+'...';
  msgCount++;
  addUserMsg(msg);
  inp.value='';inp.style.height='auto';
  document.getElementById('send-btn').classList.remove('active');
  var t=addThinking();
  fetch('/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message:msg})})
    .then(function(r){return r.json()})
    .then(function(d){t.remove();addJarvisMsg(d.reply);})
    .catch(function(){t.remove();addJarvisMsg('Something went wrong. Please try again.');});
}

function addUserMsg(text){
  var row=document.createElement('div');row.className='message-row user';
  var bubble=document.createElement('div');bubble.className='user-bubble';
  bubble.textContent=text;
  row.appendChild(bubble);
  chat.appendChild(row);
  chat.scrollTop=chat.scrollHeight;
}

function addJarvisMsg(text){
  var row=document.createElement('div');row.className='message-row jarvis';
  var av=document.createElement('div');av.className='jarvis-avatar';av.textContent='J';
  var content=document.createElement('div');content.className='jarvis-content';
  content.innerHTML=marked.parse(text);
  row.appendChild(av);row.appendChild(content);
  chat.appendChild(row);
  chat.scrollTop=chat.scrollHeight;
}

function addThinking(){
  var row=document.createElement('div');row.className='message-row jarvis';
  var av=document.createElement('div');av.className='jarvis-avatar';av.textContent='J';
  var content=document.createElement('div');content.className='jarvis-content';
  content.innerHTML='<div class="thinking"><div class="t-dot"></div><div class="t-dot"></div><div class="t-dot"></div></div>';
  row.appendChild(av);row.appendChild(content);
  chat.appendChild(row);chat.scrollTop=chat.scrollHeight;
  return row;
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
