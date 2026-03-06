import os
from flask import Flask, request, jsonify, render_template_string
from groq import Groq

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>JARVIS AI Agent</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px; background: #0a0a0a; color: #00ff88; }
        h1 { text-align: center; font-size: 2.5em; }
        #chat-box { background: #111; border: 1px solid #00ff88; border-radius: 10px; padding: 20px; height: 400px; overflow-y: auto; margin-bottom: 20px; }
        .user-msg { color: #fff; margin: 10px 0; }
        .jarvis-msg { color: #00ff88; margin: 10px 0; }
        input { width: 75%; padding: 12px; border-radius: 8px; border: 1px solid #00ff88; background: #111; color: #fff; font-size: 1em; }
        button { padding: 12px 20px; background: #00ff88; color: #000; border: none; border-radius: 8px; font-size: 1em; cursor: pointer; }
    </style>
</head>
<body>
    <h1>&#9889; JARVIS</h1>
    <div id="chat-box"></div>
    <input type="text" id="user-input" placeholder="Ask JARVIS anything..." onkeypress="if(event.key==='Enter') sendMessage()" />
    <button onclick="sendMessage()">Send</button>
    <script>
        function sendMessage() {
            var input = document.getElementById('user-input');
            var msg = input.value.trim();
            if (!msg) return;
            var box = document.getElementById('chat-box');
            box.innerHTML += '<div class="user-msg">You: ' + msg + '</div>';
            input.value = '';
            fetch('/chat', { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({message: msg}) })
                .then(function(r) { return r.json(); })
                .then(function(data) {
                    box.innerHTML += '<div class="jarvis-msg">JARVIS: ' + data.reply + '</div>';
                    box.scrollTop = box.scrollHeight;
                });
        }
    </script>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML)

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")
    try:
        response = client.chat.completions.create(
            import os
from flask import Flask, request, jsonify, render_template_string
from groq import Groq

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>JARVIS AI Agent</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px; background: #0a0a0a; color: #00ff88; }
        h1 { text-align: center; font-size: 2.5em; }
        #chat-box { background: #111; border: 1px solid #00ff88; border-radius: 10px; padding: 20px; height: 400px; overflow-y: auto; margin-bottom: 20px; }
        .user-msg { color: #fff; margin: 10px 0; }
        .jarvis-msg { color: #00ff88; margin: 10px 0; }
        input { width: 75%; padding: 12px; border-radius: 8px; border: 1px solid #00ff88; background: #111; color: #fff; font-size: 1em; }
        button { padding: 12px 20px; background: #00ff88; color: #000; border: none; border-radius: 8px; font-size: 1em; cursor: pointer; }
    </style>
</head>
<body>
    <h1>&#9889; JARVIS</h1>
    <div id="chat-box"></div>
    <input type="text" id="user-input" placeholder="Ask JARVIS anything..." onkeypress="if(event.key==='Enter') sendMessage()" />
    <button onclick="sendMessage()">Send</button>
    <script>
        function sendMessage() {
            var input = document.getElementById('user-input');
            var msg = input.value.trim();
            if (!msg) return;
            var box = document.getElementById('chat-box');
            box.innerHTML += '<div class="user-msg">You: ' + msg + '</div>';
            input.value = '';
            fetch('/chat', { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({message: msg}) })
                .then(function(r) { return r.json(); })
                .then(function(data) {
                    box.innerHTML += '<div class="jarvis-msg">JARVIS: ' + data.reply + '</div>';
                    box.scrollTop = box.scrollHeight;
                });
        }
    </script>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML)

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")
    try:
        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role": "user", "content": user_message}]
        )
        return jsonify({"reply": response.choices[0].message.content})
    except Exception as e:
        return jsonify({"reply": "Error: " + str(e)})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
            messages=[{"role": "user", "content": user_message}]
        )
        return jsonify({"reply": response.choices[0].message.content})
    except Exception as e:
        return jsonify({"reply": "Error: " + str(e)})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
