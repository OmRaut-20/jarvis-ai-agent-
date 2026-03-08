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
<title>JARVIS — AI Assistant by Om Raut</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&family=Lora:ital,wght@0,400;0,500;1,400&display=swap" rel="stylesheet">
<script src="https://cdnjs.cloudflare.com/ajax/libs/marked/9.1.6/marked.min.js"></script>
<style>
*{margin:0;padding:0;box-sizing:border-box;-webkit-tap-highlight-color:transparent;}
:root{
  --bg:#07070f;--bg2:#0d0d1a;--surface:#111120;--border:#1a1a2e;--border2:#222235;
  --text:#e8e8f5;--text-dim:#6060a0;--text-light:#2a2a50;
  --accent:#8b7cf7;--accent2:#a99ff8;--accent-soft:rgba(139,124,247,0.1);--accent-border:rgba(139,124,247,0.25);
  --user-bg:#0f0f1e;--shadow:rgba(0,0,0,0.5);
}
html,body{height:100%;overflow:hidden;}
body{background:var(--bg);color:var(--text);font-family:'Inter',sans-serif;}

/* LANDING */
#landing{position:fixed;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;z-index:200;padding:24px;text-align:center;overflow:hidden;transition:opacity 0.6s ease,transform 0.6s ease;}
#landing.out{opacity:0;transform:scale(0.97);pointer-events:none;}
#canvas{position:absolute;inset:0;width:100%;height:100%;z-index:0;}

.land-nav{position:absolute;top:0;left:0;right:0;padding:18px 28px;z-index:2;display:flex;align-items:center;justify-content:space-between;border-bottom:1px solid var(--border);}
.nav-logo{display:flex;align-items:center;gap:10px;}
.nav-icon{width:30px;height:30px;background:var(--accent);border-radius:8px;display:flex;align-items:center;justify-content:center;font-family:'Lora',serif;font-size:0.9rem;color:#fff;box-shadow:0 0 20px rgba(139,124,247,0.5);}
.nav-name{font-family:'Lora',serif;font-size:1rem;color:var(--text);}
.nav-tag{font-size:0.7rem;color:var(--text-dim);border:1px solid var(--border2);border-radius:20px;padding:3px 12px;}

.land-content{position:relative;z-index:1;max-width:560px;width:100%;}

.badge{display:inline-flex;align-items:center;gap:7px;font-size:0.7rem;color:var(--accent2);letter-spacing:0.1em;text-transform:uppercase;background:var(--accent-soft);border:1px solid var(--accent-border);border-radius:20px;padding:5px 14px;margin-bottom:24px;animation:up 0.7s ease 0.1s both;}
.badge-dot{width:5px;height:5px;background:var(--accent2);border-radius:50%;animation:pulse 2s infinite;box-shadow:0 0 6px var(--accent2);}
@keyframes pulse{0%,100%{opacity:0.3}50%{opacity:1}}
@keyframes up{from{opacity:0;transform:translateY(16px)}to{opacity:1;transform:translateY(0)}}

.land-h{font-family:'Lora',serif;font-size:clamp(2.2rem,5.5vw,3.4rem);line-height:1.15;color:var(--text);margin-bottom:14px;letter-spacing:-0.01em;animation:up 0.7s ease 0.2s both;}
.land-h em{font-style:italic;color:var(--accent2);}
.land-p{font-size:0.9rem;color:var(--text-dim);line-height:1.75;margin-bottom:36px;animation:up 0.7s ease 0.3s both;}

.land-btns{display:flex;align-items:center;justify-content:center;gap:12px;flex-wrap:wrap;margin-bottom:44px;animation:up 0.7s ease 0.4s both;}
.btn-main{display:inline-flex;align-items:center;gap:9px;background:var(--accent);color:#fff;border:none;border-radius:10px;padding:14px 28px;cursor:pointer;font-family:'Inter',sans-serif;font-size:0.9rem;font-weight:500;box-shadow:0 4px 24px rgba(139,124,247,0.4);transition:all 0.2s;}
.btn-main:hover{background:var(--accent2);transform:translateY(-2px);box-shadow:0 6px 30px rgba(139,124,247,0.5);}
.btn-main svg{width:15px;height:15px;fill:none;stroke:#fff;stroke-width:2;transition:transform 0.2s;}
.btn-main:hover svg{transform:translateX(3px);}
.btn-ghost{display:inline-flex;background:var(--surface);color:var(--text-dim);border:1px solid var(--border2);border-radius:10px;padding:14px 22px;cursor:pointer;font-family:'Inter',sans-serif;font-size:0.9rem;transition:all 0.2s;}
.btn-ghost:hover{color:var(--text);border-color:var(--border2);}

.land-features{display:flex;gap:10px;justify-content:center;flex-wrap:wrap;animation:up 0.7s ease 0.5s both;}
.feat{background:var(--surface);border:1px solid var(--border);border-radius:10px;padding:12px 16px;text-align:left;max-width:150px;box-shadow:0 2px 12px var(--shadow);}
.feat-ico{font-size:1.1rem;margin-bottom:6px;}
.feat-t{font-size:0.77rem;font-weight:500;color:var(--text);margin-bottom:2px;}
.feat-d{font-size:0.68rem;color:var(--text-dim);line-height:1.4;}

.land-foot{position:absolute;bottom:0;left:0;right:0;z-index:2;padding:12px;text-align:center;font-size:0.64rem;color:var(--text-light);border-top:1px solid var(--border);}

/* APP */
#app{display:none;height:100vh;flex-direction:column;}
#app.show{display:flex;}

.topbar{display:flex;align-items:center;justify-content:space-between;padding:0 20px;height:52px;border-bottom:1px solid var(--border);background:var(--bg2);flex-shrink:0;}
.tb-l{display:flex;align-items:center;gap:12px;}
.tb-logo{display:flex;align-items:center;gap:8px;}
.tb-icon{width:26px;height:26px;background:var(--accent);border-radius:7px;display:flex;align-items:center;justify-content:center;font-family:'Lora',serif;font-size:0.8rem;color:#fff;box-shadow:0 0 10px rgba(139,124,247,0.4);}
.tb-name{font-family:'Lora',serif;font-size:0.95rem;color:var(--text);}
.tb-sep{width:1px;height:16px;background:var(--border2);}
.tb-status{font-size:0.73rem;color:var(--text-dim);display:flex;align-items:center;gap:6px;}
.online{width:5px;height:5px;background:#4cdd7a;border-radius:50%;box-shadow:0 0 6px #4cdd7a;animation:pulse 3s infinite;}
.tb-r{display:flex;gap:8px;}
.tb-btn{background:transparent;border:1px solid var(--border);color:var(--text-dim);border-radius:7px;padding:5px 14px;cursor:pointer;font-size:0.74rem;font-family:'Inter',sans-serif;transition:all 0.15s;}
.tb-btn:hover{color:var(--text);background:var(--surface);}

.chat-area{flex:1;overflow-y:auto;scroll-behavior:smooth;}
.chat-area::-webkit-scrollbar{width:3px}
.chat-area::-webkit-scrollbar-thumb{background:var(--border2);border-radius:2px}

.welcome{max-width:620px;margin:0 auto;padding:48px 24px 28px;}
.wel-h{font-family:'Lora',serif;font-size:clamp(1.5rem,3.5vw,2rem);color:var(--text);margin-bottom:8px;}
.wel-h em{font-style:italic;color:var(--accent2);}
.wel-sub{font-size:0.87rem;color:var(--text-dim);line-height:1.75;margin-bottom:28px;}
.wel-label{font-size:0.63rem;font-weight:500;color:var(--text-light);letter-spacing:0.12em;text-transform:uppercase;margin-bottom:10px;}
.wel-chips{display:flex;flex-direction:column;gap:7px;}
.wel-chip{display:flex;align-items:center;gap:12px;background:var(--surface);border:1px solid var(--border);border-radius:10px;padding:11px 16px;cursor:pointer;transition:all 0.18s;}
.wel-chip:hover{border-color:var(--accent-border);background:var(--accent-soft);transform:translateX(4px);}
.wel-chip-ico{font-size:0.95rem;flex-shrink:0;}
.wel-chip-txt{font-size:0.83rem;color:var(--text-dim);}
.wel-chip:hover .wel-chip-txt{color:var(--accent2);}
.wel-chip-arr{margin-left:auto;color:var(--text-light);font-size:0.78rem;transition:transform 0.18s;}
.wel-chip:hover .wel-chip-arr{transform:translateX(3px);color:var(--accent2);}

.msg-page{max-width:700px;margin:0 auto;padding:14px 24px;}
.msg-group{margin-bottom:22px;animation:msgIn 0.3s ease;}
@keyframes msgIn{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:translateY(0)}}
.msg-user{display:flex;justify-content:flex-end;margin-bottom:6px;}
.user-bubble{background:var(--user-bg);border:1px solid var(--border);border-radius:14px 14px 4px 14px;padding:11px 16px;max-width:80%;font-size:0.87rem;line-height:1.7;}
.msg-jarvis{display:flex;gap:11px;align-items:flex-start;}
.j-av{width:28px;height:28px;flex-shrink:0;background:var(--accent);border-radius:7px;display:flex;align-items:center;justify-content:center;font-family:'Lora',serif;font-size:0.78rem;color:#fff;margin-top:3px;box-shadow:0 0 10px rgba(139,124,247,0.3);}
.j-con{flex:1;min-width:0;}
.j-name{font-size:0.63rem;font-weight:500;color:var(--text-dim);letter-spacing:0.08em;text-transform:uppercase;margin-bottom:5px;}
.j-body{font-size:0.87rem;line-height:1.85;color:var(--text);}
.j-body p{margin:5px 0;}
.j-body strong{font-weight:600;color:#fff;}
.j-body ul,.j-body ol{padding-left:20px;margin:7px 0;}
.j-body li{margin:4px 0;line-height:1.75;}
.j-body h1,.j-body h2,.j-body h3{font-family:'Lora',serif;font-size:1rem;font-weight:500;margin:12px 0 5px;color:#fff;}
.j-body code{background:var(--surface);border:1px solid var(--border2);border-radius:4px;padding:1px 6px;font-size:0.8rem;color:var(--accent2);}
.j-body pre{background:var(--surface);border:1px solid var(--border2);border-radius:9px;padding:13px;margin:9px 0;overflow-x:auto;}

.typing-cursor{display:inline-block;width:2px;height:0.9em;background:var(--accent2);margin-left:1px;animation:cur 0.7s infinite;vertical-align:text-bottom;}
@keyframes cur{0%,100%{opacity:1}50%{opacity:0}}
.thinking{display:flex;align-items:center;gap:4px;padding:4px 0;}
.t-dot{width:5px;height:5px;border-radius:50%;background:var(--accent);animation:tdot 1.4s ease-in-out infinite;box-shadow:0 0 4px var(--accent);}
.t-dot:nth-child(2){animation-delay:0.2s}.t-dot:nth-child(3){animation-delay:0.4s}
@keyframes tdot{0%,100%{opacity:0.2;transform:scale(1)}50%{opacity:1;transform:scale(1.3)}}

.input-area{border-top:1px solid var(--border);padding:12px 20px 18px;background:var(--bg2);flex-shrink:0;}
.input-box{max-width:700px;margin:0 auto;background:var(--surface);border:1px solid var(--border2);border-radius:14px;transition:all 0.2s;}
.input-box:focus-within{border-color:var(--accent-border);box-shadow:0 0 0 3px var(--accent-soft);}
.input-row{display:flex;align-items:flex-end;padding:12px 13px 10px;}
textarea{flex:1;background:transparent;border:none;outline:none;color:var(--text);font-family:'Inter',sans-serif;font-size:0.87rem;font-weight:300;resize:none;line-height:1.65;max-height:160px;min-height:24px;}
textarea::placeholder{color:var(--text-light)}
.send-btn{width:32px;height:32px;background:var(--accent);border:none;border-radius:8px;cursor:pointer;display:flex;align-items:center;justify-content:center;flex-shrink:0;margin-left:9px;opacity:0.25;transition:all 0.15s;}
.send-btn.on{opacity:1;box-shadow:0 2px 12px rgba(139,124,247,0.4);}
.send-btn svg{width:13px;height:13px;fill:#fff;}
.input-foot{text-align:center;padding:7px;font-size:0.62rem;color:var(--text-light);border-top:1px solid var(--border);}
</style>
</head>
<body>

<!-- LANDING -->
<div id="landing">
  <canvas id="canvas"></canvas>
  <nav class="land-nav">
    <div class="nav-logo">
      <div class="nav-icon">J</div>
      <span class="nav-name">Jarvis</span>
    </div>
    <span class="nav-tag">Built by Om Raut</span>
  </nav>
  <div class="land-content">
    <div class="badge"><div class="badge-dot"></div>AI Assistant — Live Now</div>
    <h1 class="land-h">Your personal<br><em>AI companion</em><br>is here.</h1>
    <p class="land-p">Built from scratch with Python, Flask & Groq AI by Om Raut.<br>Ask anything. Get smart answers instantly.</p>
    <div class="land-btns">
      <button class="btn-main" onclick="startApp()">
        Start Chatting
        <svg viewBox="0 0 24 24"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
      </button>
      <button class="btn-ghost" onclick="startApp()">See Demo</button>
    </div>
    <div class="land-features">
      <div class="feat"><div class="feat-ico">⚡</div><div class="feat-t">Fast</div><div class="feat-d">Llama 3.3 70B</div></div>
      <div class="feat"><div class="feat-ico">🧠</div><div class="feat-t">Smart</div><div class="feat-d">Deep context understanding</div></div>
      <div class="feat"><div class="feat-ico">📱</div><div class="feat-t">Mobile</div><div class="feat-d">Works on any device</div></div>
      <div class="feat"><div class="feat-ico">🎨</div><div class="feat-t">Beautiful</div><div class="feat-d">Minimal clean design</div></div>
    </div>
  </div>
  <div class="land-foot">Built with ❤️ by Om Raut &nbsp;·&nbsp; Deployed on Railway &nbsp;·&nbsp; Powered by Groq AI</div>
</div>

<!-- APP -->
<div id="app">
  <div class="topbar">
    <div class="tb-l">
      <div class="tb-logo"><div class="tb-icon">J</div><span class="tb-name">Jarvis</span></div>
      <div class="tb-sep"></div>
      <div class="tb-status"><div class="online"></div>Online</div>
    </div>
    <div class="tb-r">
      <button class="tb-btn" onclick="newChat()">+ New</button>
      <button class="tb-btn" onclick="shareApp()">Share</button>
    </div>
  </div>
  <div class="chat-area" id="chat">
    <div class="welcome" id="welcome">
      <div class="wel-h">Hello! I'm <em>Jarvis</em>.</div>
      <p class="wel-sub">Your personal AI by Om Raut. Ask me anything — coding, learning, writing, and more.</p>
      <div class="wel-label">Try asking</div>
      <div class="wel-chips">
        <div class="wel-chip" onclick="suggest('Explain AI in simple words')"><span class="wel-chip-ico">💡</span><span class="wel-chip-txt">Explain AI in simple words</span><span class="wel-chip-arr">→</span></div>
        <div class="wel-chip" onclick="suggest('Write a Python sorting function')"><span class="wel-chip-ico">🐍</span><span class="wel-chip-txt">Write a Python sorting function</span><span class="wel-chip-arr">→</span></div>
        <div class="wel-chip" onclick="suggest('What is machine learning?')"><span class="wel-chip-ico">🧠</span><span class="wel-chip-txt">What is machine learning?</span><span class="wel-chip-arr">→</span></div>
        <div class="wel-chip" onclick="suggest('Give me 5 study tips for exams')"><span class="wel-chip-ico">📚</span><span class="wel-chip-txt">Give me 5 study tips for exams</span><span class="wel-chip-arr">→</span></div>
        <div class="wel-chip" onclick="suggest('Who are you?')"><span class="wel-chip-ico">🤖</span><span class="wel-chip-txt">Who are you?</span><span class="wel-chip-arr">→</span></div>
      </div>
    </div>
  </div>
  <div class="input-area">
    <div class="input-box">
      <div class="input-row">
        <textarea id="inp" rows="1" placeholder="Ask Jarvis anything..."
          oninput="resize(this);toggleSend(this)"
          onkeydown="if(event.key==='Enter'&&!event.shiftKey){event.preventDefault();send()}"></textarea>
        <button class="send-btn" id="sendbtn" onclick="send()">
          <svg viewBox="0 0 24 24"><path d="M2 21l21-9L2 3v7l15 2-15 2v7z"/></svg>
        </button>
      </div>
      <div class="input-foot">Jarvis can make mistakes &nbsp;·&nbsp; Built by Om Raut</div>
    </div>
  </div>
</div>

<script>
// PARTICLE SPHERE
(function(){
  var c=document.getElementById('canvas'),ctx=c.getContext('2d');
  var W,H,cx,cy,pts=[],N=900,angle=0,tx=0,ty=0;
  var mouse={x:0,y:0};
  function resize(){W=c.width=window.innerWidth;H=c.height=window.innerHeight;cx=W/2;cy=H/2;}
  resize();
  window.addEventListener('resize',resize);
  window.addEventListener('mousemove',function(e){mouse.x=e.clientX-cx;mouse.y=e.clientY-cy;});
  function P(i,n){
    this.phi=Math.acos(-1+2*i/n);
    this.theta=Math.sqrt(n*Math.PI)*this.phi;
    this.r=Math.min(W,H)*0.26;
    this.x=this.r*Math.sin(this.phi)*Math.cos(this.theta);
    this.y=this.r*Math.sin(this.phi)*Math.sin(this.theta);
    this.z=this.r*Math.cos(this.phi);
    this.size=Math.random()*1.8+0.4;
    this.op=Math.random()*0.5+0.2;
    var r=Math.random();
    this.col=r>0.7?'157,143,255':r>0.4?'139,124,247':'100,90,200';
  }
  for(var i=0;i<N;i++)pts.push(new P(i,N));
  function draw(){
    ctx.clearRect(0,0,W,H);
    // bg glow
    var g=ctx.createRadialGradient(cx,cy,0,cx,cy,Math.min(W,H)*0.3);
    g.addColorStop(0,'rgba(139,124,247,0.06)');g.addColorStop(1,'transparent');
    ctx.fillStyle=g;ctx.fillRect(0,0,W,H);
    angle+=0.003;
    tx+=(mouse.y*0.00012-tx)*0.04;
    ty+=(mouse.x*0.00012-ty)*0.04;
    var cosA=Math.cos(angle),sinA=Math.sin(angle);
    var cosTX=Math.cos(tx),sinTX=Math.sin(tx);
    var cosTY=Math.cos(ty),sinTY=Math.sin(ty);
    var sorted=pts.map(function(p){
      var x1=p.x*cosA+p.z*sinA,y1=p.y,z1=-p.x*sinA+p.z*cosA;
      var x2=x1,y2=y1*cosTX-z1*sinTX,z2=y1*sinTX+z1*cosTX;
      var x3=x2*cosTY+z2*sinTY,z3=-x2*sinTY+z2*cosTY;
      var sc=0.4+0.6*(1+z3/p.r)*0.5;
      return{x:cx+x3,y:cy+y2,z:z3,sc:sc,p:p};
    });
    sorted.sort(function(a,b){return a.z-b.z;});
    // lines
    for(var i=0;i<sorted.length;i+=4){
      for(var j=i+1;j<Math.min(i+8,sorted.length);j++){
        var dx=sorted[i].x-sorted[j].x,dy=sorted[i].y-sorted[j].y,d=Math.sqrt(dx*dx+dy*dy);
        if(d<32){ctx.beginPath();ctx.moveTo(sorted[i].x,sorted[i].y);ctx.lineTo(sorted[j].x,sorted[j].y);ctx.strokeStyle='rgba(139,124,247,'+(0.1*(1-d/32))+')';ctx.lineWidth=0.4;ctx.stroke();}
      }
    }
    // dots
    sorted.forEach(function(d){
      var a=d.p.op*(0.2+0.8*d.sc);
      ctx.beginPath();ctx.arc(d.x,d.y,d.p.size*Math.max(0.3,d.sc),0,Math.PI*2);
      ctx.fillStyle='rgba('+d.p.col+','+a+')';ctx.fill();
    });
    requestAnimationFrame(draw);
  }
  draw();
})();

// APP
marked.setOptions({breaks:true,gfm:true});
var chat=document.getElementById('chat'),inp=document.getElementById('inp'),welcome=document.getElementById('welcome'),hasMsg=false;

function startApp(){
  document.getElementById('landing').classList.add('out');
  setTimeout(function(){
    document.getElementById('landing').style.display='none';
    var a=document.getElementById('app');a.classList.add('show');inp.focus();
  },550);
}
function shareApp(){
  if(navigator.share)navigator.share({title:'JARVIS AI by Om Raut',url:window.location.href});
  else navigator.clipboard.writeText(window.location.href).then(function(){alert('Link copied!');});
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
    .catch(()=>{t.remove();typeJarvis('Something went wrong. Please try again.');});
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
  var nm=document.createElement('div');nm.className='j-name';nm.textContent='Jarvis';
  var body=document.createElement('div');body.className='j-body';
  con.appendChild(nm);con.appendChild(body);j.appendChild(av);j.appendChild(con);g.appendChild(j);pg.appendChild(g);chat.appendChild(pg);
  var words=text.split(' '),current='',i=0;
  var cursor=document.createElement('span');cursor.className='typing-cursor';
  function next(){
    if(i<words.length){
      current+=(i>0?' ':'')+words[i];
      body.innerHTML=marked.parse(current);body.appendChild(cursor);
      chat.scrollTop=chat.scrollHeight;i++;setTimeout(next,16);
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
  var nm=document.createElement('div');nm.className='j-name';nm.textContent='Jarvis';
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
