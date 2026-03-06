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
<title>JARVIS — AI</title>
<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;600;700;900&family=Inter:wght@300;400;500&display=swap" rel="stylesheet">
<script src="https://cdnjs.cloudflare.com/ajax/libs/marked/9.1.6/marked.min.js"></script>
<style>
*{margin:0;padding:0;box-sizing:border-box;-webkit-tap-highlight-color:transparent;}
:root{
  --bg:#020408;
  --bg2:#040810;
  --surface:#080f1a;
  --border:#0a1628;
  --border2:#0f2040;
  --text:#e0f0ff;
  --text-dim:#4a7090;
  --text-light:#1a3050;
  --cyan:#00d4ff;
  --cyan2:#00aacc;
  --red:#ff2244;
  --orange:#ff6600;
  --glow-cyan:rgba(0,212,255,0.2);
  --glow-red:rgba(255,34,68,0.2);
  --user-bg:#040d1a;
}
html,body{height:100%;overflow:hidden;}
body{background:var(--bg);color:var(--text);font-family:'Inter',sans-serif;}

/* Scanline overlay */
body::after{
  content:'';position:fixed;inset:0;
  background:repeating-linear-gradient(0deg,transparent,transparent 2px,rgba(0,212,255,0.015) 2px,rgba(0,212,255,0.015) 4px);
  pointer-events:none;z-index:999;
}

/* ======== LANDING ======== */
#landing{
  position:fixed;inset:0;
  display:flex;flex-direction:column;align-items:center;justify-content:center;
  z-index:200;padding:24px;text-align:center;
  transition:opacity 0.6s ease,transform 0.6s ease;
  overflow:hidden;
}
#landing.out{opacity:0;transform:scale(1.02);pointer-events:none;}

#canvas3d{position:absolute;inset:0;width:100%;height:100%;z-index:0;}

/* Grid floor effect */
.grid-floor{
  position:absolute;bottom:0;left:0;right:0;height:50%;
  background:
    linear-gradient(rgba(0,212,255,0.05) 1px, transparent 1px),
    linear-gradient(90deg, rgba(0,212,255,0.05) 1px, transparent 1px);
  background-size:60px 60px;
  transform:perspective(400px) rotateX(60deg);
  transform-origin:bottom;
  z-index:0;
  mask-image:linear-gradient(to top, rgba(0,0,0,0.4), transparent);
}

.land-content{position:relative;z-index:1;max-width:600px;width:100%;}

.land-nav{
  position:absolute;top:0;left:0;right:0;
  padding:16px 28px;z-index:2;
  display:flex;align-items:center;justify-content:space-between;
  border-bottom:1px solid rgba(0,212,255,0.1);
}
.nav-logo{display:flex;align-items:center;gap:10px;}
.nav-icon{
  width:32px;height:32px;
  background:transparent;
  border:1px solid var(--cyan);
  border-radius:6px;
  display:flex;align-items:center;justify-content:center;
  font-family:'Orbitron',monospace;font-size:0.85rem;font-weight:700;
  color:var(--cyan);
  box-shadow:0 0 12px var(--cyan),inset 0 0 8px rgba(0,212,255,0.1);
}
.nav-name{font-family:'Orbitron',monospace;font-size:0.9rem;font-weight:600;color:var(--cyan);letter-spacing:0.15em;text-shadow:0 0 10px var(--cyan);}
.nav-badge{
  font-size:0.68rem;color:var(--cyan2);
  border:1px solid rgba(0,212,255,0.3);
  border-radius:4px;padding:3px 10px;
  font-family:'Orbitron',monospace;letter-spacing:0.1em;
}

/* Glitch animation */
@keyframes glitch{
  0%,90%,100%{transform:translate(0);text-shadow:0 0 20px var(--cyan),0 0 40px var(--cyan);}
  91%{transform:translate(-2px,1px);text-shadow:-2px 0 var(--red),2px 0 var(--cyan);}
  93%{transform:translate(2px,-1px);text-shadow:2px 0 var(--red),-2px 0 var(--cyan);}
  95%{transform:translate(-1px,2px);text-shadow:-1px 0 var(--red),1px 0 var(--cyan);}
  97%{transform:translate(0);text-shadow:0 0 20px var(--cyan);}
}
@keyframes fadeUp{from{opacity:0;transform:translateY(20px)}to{opacity:1;transform:translateY(0)}}
@keyframes blink{0%,100%{opacity:0.3}50%{opacity:1}}

.land-eyebrow{
  display:inline-flex;align-items:center;gap:8px;
  font-family:'Orbitron',monospace;
  font-size:0.65rem;font-weight:600;color:var(--red);
  letter-spacing:0.2em;text-transform:uppercase;
  border:1px solid rgba(255,34,68,0.4);
  border-radius:3px;padding:5px 14px;margin-bottom:20px;
  animation:fadeUp 0.7s ease 0.1s both;
  box-shadow:0 0 8px var(--glow-red);
}
.eye-dot{width:6px;height:6px;background:var(--red);border-radius:50%;animation:blink 1s infinite;box-shadow:0 0 6px var(--red);}

.land-h{
  font-family:'Orbitron',monospace;
  font-size:clamp(2rem,5.5vw,3.5rem);
  font-weight:900;
  line-height:1.1;
  color:var(--cyan);
  margin-bottom:8px;
  letter-spacing:0.05em;
  animation:glitch 4s infinite, fadeUp 0.7s ease 0.2s both;
  text-shadow:0 0 20px var(--cyan),0 0 40px var(--cyan);
}
.land-sub-h{
  font-family:'Orbitron',monospace;
  font-size:clamp(0.8rem,2vw,1rem);
  color:var(--orange);
  letter-spacing:0.2em;
  margin-bottom:20px;
  animation:fadeUp 0.7s ease 0.3s both;
  text-shadow:0 0 10px var(--orange);
}
.land-p{
  font-size:0.88rem;color:var(--text-dim);
  line-height:1.75;margin-bottom:36px;
  animation:fadeUp 0.7s ease 0.4s both;
}

.land-btns{
  display:flex;align-items:center;justify-content:center;
  gap:14px;flex-wrap:wrap;margin-bottom:48px;
  animation:fadeUp 0.7s ease 0.5s both;
}
.btn-primary{
  display:inline-flex;align-items:center;gap:10px;
  background:transparent;color:var(--cyan);
  border:1px solid var(--cyan);
  border-radius:4px;padding:13px 28px;cursor:pointer;
  font-family:'Orbitron',monospace;font-size:0.8rem;font-weight:700;
  letter-spacing:0.15em;text-transform:uppercase;
  box-shadow:0 0 16px var(--glow-cyan),inset 0 0 16px rgba(0,212,255,0.05);
  transition:all 0.2s;clip-path:polygon(8px 0%, 100% 0%, calc(100% - 8px) 100%, 0% 100%);
}
.btn-primary:hover{background:rgba(0,212,255,0.1);box-shadow:0 0 28px var(--cyan),inset 0 0 20px rgba(0,212,255,0.1);transform:translateY(-2px);}
.btn-primary svg{width:15px;height:15px;fill:none;stroke:var(--cyan);stroke-width:2;}
.btn-secondary{
  display:inline-flex;align-items:center;
  background:transparent;color:var(--text-dim);
  border:1px solid var(--border2);
  border-radius:4px;padding:13px 22px;cursor:pointer;
  font-family:'Orbitron',monospace;font-size:0.75rem;
  letter-spacing:0.1em;text-transform:uppercase;
  transition:all 0.2s;
}
.btn-secondary:hover{color:var(--text);border-color:var(--text-dim);}

.land-stats{
  display:flex;gap:0;justify-content:center;
  border:1px solid rgba(0,212,255,0.15);
  border-radius:4px;overflow:hidden;
  animation:fadeUp 0.7s ease 0.6s both;
  max-width:420px;margin:0 auto;
}
.stat{
  flex:1;padding:14px;text-align:center;
  border-right:1px solid rgba(0,212,255,0.15);
}
.stat:last-child{border-right:none;}
.stat-num{font-family:'Orbitron',monospace;font-size:1.3rem;font-weight:700;color:var(--cyan);display:block;text-shadow:0 0 8px var(--cyan);}
.stat-label{font-size:0.64rem;color:var(--text-dim);letter-spacing:0.08em;text-transform:uppercase;}

.land-foot{
  position:absolute;bottom:0;left:0;right:0;z-index:2;
  padding:10px;text-align:center;
  font-family:'Orbitron',monospace;
  font-size:0.58rem;color:var(--text-light);
  letter-spacing:0.1em;
  border-top:1px solid rgba(0,212,255,0.05);
}

/* Corner decorations */
.corner{position:absolute;width:20px;height:20px;z-index:2;}
.corner-tl{top:60px;left:20px;border-top:2px solid var(--cyan);border-left:2px solid var(--cyan);}
.corner-tr{top:60px;right:20px;border-top:2px solid var(--cyan);border-right:2px solid var(--cyan);}
.corner-bl{bottom:30px;left:20px;border-bottom:2px solid var(--cyan);border-left:2px solid var(--cyan);}
.corner-br{bottom:30px;right:20px;border-bottom:2px solid var(--cyan);border-right:2px solid var(--cyan);}

/* ======== APP ======== */
#app{display:none;height:100vh;flex-direction:column;background:var(--bg);}
#app.show{display:flex;}

.topbar{
  display:flex;align-items:center;justify-content:space-between;
  padding:0 20px;height:52px;
  border-bottom:1px solid rgba(0,212,255,0.15);
  background:var(--bg2);flex-shrink:0;
  box-shadow:0 2px 20px rgba(0,212,255,0.05);
}
.tb-l{display:flex;align-items:center;gap:14px;}
.tb-logo{display:flex;align-items:center;gap:9px;}
.tb-icon{width:26px;height:26px;border:1px solid var(--cyan);border-radius:5px;display:flex;align-items:center;justify-content:center;font-family:'Orbitron',monospace;font-size:0.75rem;font-weight:700;color:var(--cyan);box-shadow:0 0 8px var(--glow-cyan);}
.tb-name{font-family:'Orbitron',monospace;font-size:0.85rem;font-weight:700;color:var(--cyan);letter-spacing:0.15em;text-shadow:0 0 8px var(--cyan);}
.tb-sep{width:1px;height:16px;background:rgba(0,212,255,0.2);}
.tb-status{font-size:0.72rem;color:var(--text-dim);display:flex;align-items:center;gap:6px;font-family:'Orbitron',monospace;letter-spacing:0.05em;}
.online{width:6px;height:6px;background:#00ff88;border-radius:50%;box-shadow:0 0 8px #00ff88;animation:blink 2s infinite;}
.tb-r{display:flex;gap:8px;}
.tb-btn{
  background:transparent;border:1px solid rgba(0,212,255,0.2);
  color:var(--text-dim);border-radius:4px;
  padding:5px 14px;cursor:pointer;
  font-family:'Orbitron',monospace;font-size:0.65rem;
  letter-spacing:0.1em;text-transform:uppercase;
  transition:all 0.15s;
}
.tb-btn:hover{color:var(--cyan);border-color:var(--cyan);box-shadow:0 0 8px var(--glow-cyan);}

.chat-area{flex:1;overflow-y:auto;scroll-behavior:smooth;}
.chat-area::-webkit-scrollbar{width:3px}
.chat-area::-webkit-scrollbar-thumb{background:rgba(0,212,255,0.2);border-radius:2px}

.welcome{max-width:640px;margin:0 auto;padding:44px 24px 28px;}
.wel-h{
  font-family:'Orbitron',monospace;
  font-size:clamp(1.2rem,3vw,1.6rem);
  font-weight:700;color:var(--cyan);
  margin-bottom:8px;letter-spacing:0.1em;
  text-shadow:0 0 12px var(--cyan);
}
.wel-sub{font-size:0.85rem;color:var(--text-dim);line-height:1.75;margin-bottom:26px;}
.wel-label{
  font-family:'Orbitron',monospace;
  font-size:0.6rem;color:var(--text-dim);
  letter-spacing:0.2em;text-transform:uppercase;
  margin-bottom:10px;
}
.wel-chips{display:flex;flex-direction:column;gap:7px;}
.wel-chip{
  display:flex;align-items:center;gap:12px;
  background:var(--surface);
  border:1px solid rgba(0,212,255,0.1);
  border-left:2px solid var(--cyan);
  border-radius:4px;padding:11px 16px;
  cursor:pointer;transition:all 0.18s;
}
.wel-chip:hover{background:rgba(0,212,255,0.05);border-color:var(--cyan);box-shadow:0 0 12px var(--glow-cyan);transform:translateX(4px);}
.wel-chip-ico{font-size:0.95rem;flex-shrink:0;}
.wel-chip-txt{font-size:0.82rem;color:var(--text-dim);}
.wel-chip:hover .wel-chip-txt{color:var(--cyan);}
.wel-chip-arr{margin-left:auto;color:var(--text-light);font-size:0.78rem;font-family:'Orbitron',monospace;transition:transform 0.18s;}
.wel-chip:hover .wel-chip-arr{transform:translateX(3px);color:var(--cyan);}

.msg-page{max-width:700px;margin:0 auto;padding:14px 24px;}
.msg-group{margin-bottom:20px;animation:msgIn 0.3s ease;}
@keyframes msgIn{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:translateY(0)}}
.msg-user{display:flex;justify-content:flex-end;margin-bottom:6px;}
.user-bubble{
  background:var(--user-bg);
  border:1px solid rgba(0,212,255,0.15);
  border-right:2px solid var(--cyan);
  border-radius:8px 4px 4px 8px;
  padding:11px 16px;max-width:80%;
  font-size:0.86rem;line-height:1.7;
}
.msg-jarvis{display:flex;gap:11px;align-items:flex-start;}
.j-av{
  width:30px;height:30px;flex-shrink:0;
  border:1px solid var(--cyan);border-radius:5px;
  display:flex;align-items:center;justify-content:center;
  font-family:'Orbitron',monospace;font-size:0.75rem;font-weight:700;
  color:var(--cyan);margin-top:3px;
  box-shadow:0 0 10px var(--glow-cyan);
  background:rgba(0,212,255,0.05);
}
.j-con{flex:1;min-width:0;}
.j-name{
  font-family:'Orbitron',monospace;
  font-size:0.6rem;font-weight:600;
  color:var(--cyan);letter-spacing:0.15em;
  text-transform:uppercase;margin-bottom:5px;
  text-shadow:0 0 6px var(--cyan);
}
.j-body{font-size:0.86rem;line-height:1.85;color:var(--text);}
.j-body p{margin:5px 0;}
.j-body strong{font-weight:600;color:var(--cyan);}
.j-body ul,.j-body ol{padding-left:20px;margin:7px 0;}
.j-body li{margin:4px 0;line-height:1.75;}
.j-body h1,.j-body h2,.j-body h3{font-family:'Orbitron',monospace;font-size:0.9rem;font-weight:700;margin:12px 0 5px;color:var(--cyan);letter-spacing:0.1em;text-shadow:0 0 6px var(--cyan);}
.j-body code{background:var(--surface);border:1px solid rgba(0,212,255,0.2);border-radius:3px;padding:1px 6px;font-size:0.8rem;color:var(--orange);}
.j-body pre{background:var(--surface);border:1px solid rgba(0,212,255,0.15);border-left:2px solid var(--cyan);border-radius:5px;padding:14px;margin:10px 0;overflow-x:auto;}

.typing-cursor{display:inline-block;width:8px;height:2px;background:var(--cyan);margin-left:2px;animation:cur 0.6s infinite;vertical-align:middle;box-shadow:0 0 6px var(--cyan);}
@keyframes cur{0%,100%{opacity:1}50%{opacity:0}}

.thinking{display:flex;align-items:center;gap:6px;padding:6px 0;}
.t-dot{width:6px;height:6px;border-radius:1px;background:var(--cyan);animation:tdot 1.2s ease-in-out infinite;box-shadow:0 0 4px var(--cyan);}
.t-dot:nth-child(2){animation-delay:0.2s}.t-dot:nth-child(3){animation-delay:0.4s}
@keyframes tdot{0%,100%{opacity:0.2;transform:scaleY(1)}50%{opacity:1;transform:scaleY(1.8)}}

.input-area{
  border-top:1px solid rgba(0,212,255,0.1);
  padding:12px 20px 18px;
  background:var(--bg2);flex-shrink:0;
}
.input-box{
  max-width:700px;margin:0 auto;
  background:var(--surface);
  border:1px solid rgba(0,212,255,0.15);
  border-radius:5px;transition:all 0.2s;
  clip-path:polygon(6px 0%, 100% 0%, calc(100% - 6px) 100%, 0% 100%);
}
.input-box:focus-within{
  border-color:var(--cyan);
  box-shadow:0 0 20px var(--glow-cyan);
}
.input-row{display:flex;align-items:flex-end;padding:12px 14px 10px;}
textarea{
  flex:1;background:transparent;border:none;outline:none;
  color:var(--text);font-family:'Inter',sans-serif;
  font-size:0.86rem;font-weight:300;resize:none;
  line-height:1.65;max-height:160px;min-height:24px;
}
textarea::placeholder{color:var(--text-light)}
.send-btn{
  width:34px;height:34px;
  background:transparent;border:1px solid var(--cyan);
  border-radius:4px;cursor:pointer;
  display:flex;align-items:center;justify-content:center;
  flex-shrink:0;margin-left:10px;opacity:0.3;
  transition:all 0.15s;
}
.send-btn.on{opacity:1;box-shadow:0 0 12px var(--glow-cyan);}
.send-btn svg{width:13px;height:13px;fill:var(--cyan);}
.input-foot{
  text-align:center;padding:6px;
  font-family:'Orbitron',monospace;
  font-size:0.56rem;color:var(--text-light);
  letter-spacing:0.1em;border-top:1px solid rgba(0,212,255,0.08);
}
</style>
</head>
<body>

<!-- LANDING -->
<div id="landing">
  <canvas id="canvas3d"></canvas>
  <div class="grid-floor"></div>
  <div class="corner corner-tl"></div>
  <div class="corner corner-tr"></div>
  <div class="corner corner-bl"></div>
  <div class="corner corner-br"></div>
  <nav class="land-nav">
    <div class="nav-logo">
      <div class="nav-icon">J</div>
      <span class="nav-name">JARVIS</span>
    </div>
    <span class="nav-badge">BY OM RAUT</span>
  </nav>
  <div class="land-content">
    <div class="land-eyebrow"><div class="eye-dot"></div>System Online &mdash; Ready</div>
    <h1 class="land-h">JARVIS</h1>
    <div class="land-sub-h">ADVANCED AI SYSTEM v2.0</div>
    <p class="land-p">Next-generation AI assistant built by Om Raut.<br>Powered by Llama 3.3 70B — ask anything, get instant answers.</p>
    <div class="land-btns">
      <button class="btn-primary" onclick="startApp()">
        Initialize System
        <svg viewBox="0 0 24 24"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
      </button>
      <button class="btn-secondary" onclick="startApp()">View Demo</button>
    </div>
    <div class="land-stats">
      <div class="stat"><span class="stat-num">70B</span><span class="stat-label">Parameters</span></div>
      <div class="stat"><span class="stat-num">&lt;1s</span><span class="stat-label">Response</span></div>
      <div class="stat"><span class="stat-num">∞</span><span class="stat-label">Knowledge</span></div>
    </div>
  </div>
  <div class="land-foot">[ JARVIS AI SYSTEM &nbsp;·&nbsp; BUILT BY OM RAUT &nbsp;·&nbsp; DEPLOYED ON RAILWAY ]</div>
</div>

<!-- APP -->
<div id="app">
  <div class="topbar">
    <div class="tb-l">
      <div class="tb-logo"><div class="tb-icon">J</div><span class="tb-name">JARVIS</span></div>
      <div class="tb-sep"></div>
      <div class="tb-status"><div class="online"></div>ONLINE</div>
    </div>
    <div class="tb-r">
      <button class="tb-btn" onclick="newChat()">[ NEW ]</button>
      <button class="tb-btn" onclick="shareApp()">[ SHARE ]</button>
    </div>
  </div>
  <div class="chat-area" id="chat">
    <div class="welcome" id="welcome">
      <div class="wel-h">&gt; SYSTEM READY_</div>
      <p class="wel-sub">JARVIS AI online. Built by Om Raut. Enter your query below.</p>
      <div class="wel-label">// suggested queries</div>
      <div class="wel-chips">
        <div class="wel-chip" onclick="suggest('Explain AI in simple words')"><span class="wel-chip-ico">⚡</span><span class="wel-chip-txt">Explain AI in simple words</span><span class="wel-chip-arr">▶</span></div>
        <div class="wel-chip" onclick="suggest('Write a Python sorting function')"><span class="wel-chip-ico">🐍</span><span class="wel-chip-txt">Write a Python sorting function</span><span class="wel-chip-arr">▶</span></div>
        <div class="wel-chip" onclick="suggest('What is machine learning?')"><span class="wel-chip-ico">🧠</span><span class="wel-chip-txt">What is machine learning?</span><span class="wel-chip-arr">▶</span></div>
        <div class="wel-chip" onclick="suggest('Give me 5 study tips for exams')"><span class="wel-chip-ico">📡</span><span class="wel-chip-txt">Give me 5 study tips for exams</span><span class="wel-chip-arr">▶</span></div>
        <div class="wel-chip" onclick="suggest('Who are you?')"><span class="wel-chip-ico">🤖</span><span class="wel-chip-txt">Who are you?</span><span class="wel-chip-arr">▶</span></div>
      </div>
    </div>
  </div>
  <div class="input-area">
    <div class="input-box">
      <div class="input-row">
        <textarea id="inp" rows="1" placeholder="> Enter query..."
          oninput="resize(this);toggleSend(this)"
          onkeydown="if(event.key==='Enter'&&!event.shiftKey){event.preventDefault();send()}"></textarea>
        <button class="send-btn" id="sendbtn" onclick="send()">
          <svg viewBox="0 0 24 24"><path d="M2 21l21-9L2 3v7l15 2-15 2v7z"/></svg>
        </button>
      </div>
      <div class="input-foot">[ ENTER TO SEND &nbsp;·&nbsp; JARVIS AI &nbsp;·&nbsp; BY OM RAUT ]</div>
    </div>
  </div>
</div>

<script>
// ===== 3D PARTICLE SPHERE =====
(function(){
  var canvas=document.getElementById('canvas3d');
  var ctx=canvas.getContext('2d');
  var W,H,cx,cy;
  var particles=[];
  var mouse={x:0,y:0};
  var N=1000;

  function resize(){W=canvas.width=window.innerWidth;H=canvas.height=window.innerHeight;cx=W/2;cy=H/2;}
  resize();
  window.addEventListener('resize',resize);
  window.addEventListener('mousemove',function(e){mouse.x=e.clientX-cx;mouse.y=e.clientY-cy;});

  function Particle(i,total){
    this.phi=Math.acos(-1+2*i/total);
    this.theta=Math.sqrt(total*Math.PI)*this.phi;
    this.r=Math.min(W,H)*0.25;
    this.ox=this.r*Math.sin(this.phi)*Math.cos(this.theta);
    this.oy=this.r*Math.sin(this.phi)*Math.sin(this.theta);
    this.oz=this.r*Math.cos(this.phi);
    this.size=Math.random()*2+0.5;
    this.base=Math.random();
    // Color: mostly cyan, some orange/red
    var r=Math.random();
    if(r>0.85) this.color='255,102,0';
    else if(r>0.7) this.color='255,34,68';
    else this.color='0,212,255';
  }
  for(var i=0;i<N;i++) particles.push(new Particle(i,N));

  var angle=0,tiltX=0,tiltY=0;

  function draw(){
    ctx.clearRect(0,0,W,H);

    // Background glow
    var g=ctx.createRadialGradient(cx,cy,0,cx,cy,Math.min(W,H)*0.35);
    g.addColorStop(0,'rgba(0,212,255,0.04)');
    g.addColorStop(1,'transparent');
    ctx.fillStyle=g;
    ctx.fillRect(0,0,W,H);

    angle+=0.004;
    tiltX+=(mouse.y*0.00015-tiltX)*0.04;
    tiltY+=(mouse.x*0.00015-tiltY)*0.04;

    var sorted=particles.map(function(p){
      var cosA=Math.cos(angle),sinA=Math.sin(angle);
      var x1=p.ox*cosA+p.oz*sinA;var y1=p.oy;var z1=-p.ox*sinA+p.oz*cosA;
      var cosTX=Math.cos(tiltX),sinTX=Math.sin(tiltX);
      var x2=x1;var y2=y1*cosTX-z1*sinTX;var z2=y1*sinTX+z1*cosTX;
      var cosTY=Math.cos(tiltY),sinTY=Math.sin(tiltY);
      var x3=x2*cosTY+z2*sinTY;var z3=-x2*sinTY+z2*cosTY;
      var scale=0.5+0.5*(1+z3/p.r);
      return{x:cx+x3,y:cy+y2,z:z3,scale:scale,p:p};
    });
    sorted.sort(function(a,b){return a.z-b.z;});

    // Lines
    for(var i=0;i<sorted.length;i+=5){
      for(var j=i+1;j<Math.min(i+10,sorted.length);j++){
        var dx=sorted[i].x-sorted[j].x,dy=sorted[i].y-sorted[j].y;
        var dist=Math.sqrt(dx*dx+dy*dy);
        if(dist<30){
          ctx.beginPath();ctx.moveTo(sorted[i].x,sorted[i].y);ctx.lineTo(sorted[j].x,sorted[j].y);
          ctx.strokeStyle='rgba(0,212,255,'+(0.12*(1-dist/30))+')';
          ctx.lineWidth=0.4;ctx.stroke();
        }
      }
    }

    // Dots
    sorted.forEach(function(d){
      var alpha=(0.2+0.8*d.scale)*0.8;
      var size=d.p.size*Math.max(0.3,d.scale);
      ctx.beginPath();ctx.arc(d.x,d.y,size,0,Math.PI*2);
      ctx.fillStyle='rgba('+d.p.color+','+alpha+')';
      ctx.fill();
      // Glow for bright particles
      if(d.scale>0.8){
        ctx.beginPath();ctx.arc(d.x,d.y,size*2.5,0,Math.PI*2);
        ctx.fillStyle='rgba('+d.p.color+','+0.04+')';
        ctx.fill();
      }
    });
    requestAnimationFrame(draw);
  }
  draw();
})();

// ===== APP =====
marked.setOptions({breaks:true,gfm:true});
var chat=document.getElementById('chat'),inp=document.getElementById('inp'),welcome=document.getElementById('welcome'),hasMsg=false;

function startApp(){
  document.getElementById('landing').classList.add('out');
  setTimeout(function(){
    document.getElementById('landing').style.display='none';
    var app=document.getElementById('app');app.classList.add('show');inp.focus();
  },550);
}
function shareApp(){
  if(navigator.share){navigator.share({title:'JARVIS AI',url:window.location.href});}
  else{navigator.clipboard.writeText(window.location.href).then(function(){alert('Link copied!');});}
}
function resize(el){el.style.height='auto';el.style.height=Math.min(el.scrollHeight,160)+'px';}
function toggleSend(el){document.getElementById('sendbtn').classList.toggle('on',el.value.trim().length>0);}
function suggest(t){inp.value=t;toggleSend(inp);send();}
function newChat(){
  while(chat.firstChild)chat.removeChild(chat.firstChild);
  chat.appendChild(welcome);welcome.style.display='block';
  hasMsg=false;inp.value='';inp.style.height='auto';
}
function send(){
  var msg=inp.value.trim();if(!msg)return;
  if(!hasMsg){welcome.style.display='none';hasMsg=true;}
  addUser(msg);inp.value='';inp.style.height='auto';
  document.getElementById('sendbtn').classList.remove('on');
  var t=addThink();
  fetch('/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message:msg})})
    .then(r=>r.json()).then(d=>{t.remove();typeJarvis(d.reply);})
    .catch(()=>{t.remove();typeJarvis('System error. Please retry.');});
}
function addUser(text){
  var pg=document.createElement('div');pg.className='msg-page';
  var g=document.createElement('div');g.className='msg-group';
  var u=document.createElement('div');u.className='msg-user';
  var b=document.createElement('div');b.className='user-bubble';b.textContent=text;
  u.appendChild(b);g.appendChild(u);pg.appendChild(g);chat.appendChild(pg);chat.scrollTop=chat.scrollHeight;
}
function typeJarvis(text){
  var pg=document.createElement('div');pg.className='msg-page';
  var g=document.createElement('div');g.className='msg-group';
  var j=document.createElement('div');j.className='msg-jarvis';
  var av=document.createElement('div');av.className='j-av';av.textContent='J';
  var con=document.createElement('div');con.className='j-con';
  var nm=document.createElement('div');nm.className='j-name';nm.textContent='// JARVIS OUTPUT';
  var body=document.createElement('div');body.className='j-body';
  con.appendChild(nm);con.appendChild(body);j.appendChild(av);j.appendChild(con);g.appendChild(j);pg.appendChild(g);chat.appendChild(pg);
  var words=text.split(' ');var current='';var i=0;
  var cursor=document.createElement('span');cursor.className='typing-cursor';
  function next(){
    if(i<words.length){
      current+=(i>0?' ':'')+words[i];
      body.innerHTML=marked.parse(current);body.appendChild(cursor);
      chat.scrollTop=chat.scrollHeight;i++;setTimeout(next,15);
    } else {body.innerHTML=marked.parse(current);chat.scrollTop=chat.scrollHeight;}
  }
  next();
}
function addThink(){
  var pg=document.createElement('div');pg.className='msg-page';
  var g=document.createElement('div');g.className='msg-group';
  var j=document.createElement('div');j.className='msg-jarvis';
  var av=document.createElement('div');av.className='j-av';av.textContent='J';
  var con=document.createElement('div');con.className='j-con';
  var nm=document.createElement('div');nm.className='j-name';nm.textContent='// PROCESSING';
  var body=document.createElement('div');body.className='j-body';
  body.innerHTML='<div class="thinking"><div class="t-dot"></div><div class="t-dot"></div><div class="t-dot"></div></div>';
  con.appendChild(nm);con.appendChild(body);j.appendChild(av);j.appendChild(con);g.appendChild(j);pg.appendChild(g);
  chat.appendChild(pg);chat.scrollTop=chat.scrollHeight;return pg;
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
