from flask import Flask, request, jsonify, render_template_string
import google.generativeai as genai

genai.configure(api_key="AIzaSyCAT9fFtlkZH0ObvhUnHEqmYwCPw-EJx7E")
model = genai.GenerativeModel("gemini-3.1-flash-lite-preview")
chat = model.start_chat(history=[])

app = Flask(__name__)

HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>JARVIS - Om's AI Assistant</title>
    <style>
        body { font-family: Arial; max-width: 800px; margin: 50px auto; background: #1a1a2e; color: white; }
        h1 { color: #00d4ff; text-align: center; }
        #chat { height: 400px; overflow-y: auto; border: 1px solid #00d4ff; padding: 15px; border-radius: 10px; margin-bottom: 10px; }
        .user { color: #00d4ff; margin: 10px 0; }
        .jarvis { color: #00ff88; margin: 10px 0; }
        input { width: 75%; padding: 10px; border-radius: 5px; border: none; background: #16213e; color: white; }
        button { padding: 10px 20px; background: #00d4ff; border: none; border-radius: 5px; cursor: pointer; color: black; font-weight: bold; }
    </style>
</head>
<body>
    <h1>🤖 JARVIS - Om's AI Study Assistant</h1>
    <div id="chat"></div>
    <input id="msg" placeholder="Ask JARVIS anything..." onkeypress="if(event.key==='Enter')send()">
    <button onclick="send()">Send</button>
    <script>
        async function send() {
            const msg = document.getElementById("msg").value;
            if (!msg) return;
            document.getElementById("chat").innerHTML += "<p class='user'>You: " + msg + "</p>";
            document.getElementById("msg").value = "";
            const res = await fetch("/chat", {method:"POST", headers:{"Content-Type":"application/json"}, body:JSON.stringify({message:msg})});
            const data = await res.json();
            document.getElementById("chat").innerHTML += "<p class='jarvis'>JARVIS: " + data.reply + "</p>";
            document.getElementById("chat").scrollTop = 999999;
        }
    </script>
</body>
</html>
'''

@app.route("/")
def home():
    return render_template_string(HTML)

@app.route("/chat", methods=["POST"])
def chat_api():
    msg = request.json["message"]
    response = chat.send_message(msg)
    return jsonify({"reply": response.text})

if __name__ == "__main__":
    import os
port = int(os.environ.get("PORT", 5000))
app.run(host="0.0.0.0", port=port)
