from flask import Flask, render_template_string, request
import time, json, threading, os
import websocket

app = Flask(__name__)

# قاعدة بيانات بسيطة في الذاكرة
active_sessions = {}
usage_counter = 0

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <title>EUO BLUE PLATFORM</title>
    <style>
        body { background: #001f3f; color: #7fdbff; font-family: 'Segoe UI', sans-serif; padding: 20px; text-align: center; }
        .container { max-width: 600px; margin: auto; background: #003366; padding: 25px; border-radius: 15px; border: 2px solid #7fdbff; box-shadow: 0 0 20px #0074d9; }
        h1 { color: #7fdbff; text-shadow: 0 0 10px #7fdbff; }
        .dev-info { font-size: 14px; color: #ffffff; margin-bottom: 20px; }
        .privacy { font-size: 12px; color: #ffdc00; margin-bottom: 20px; }
        input, select, button { width: 100%; padding: 12px; margin: 10px 0; border-radius: 8px; border: 1px solid #7fdbff; background: #001f3f; color: white; box-sizing: border-box; }
        button { background: #0074d9; color: white; font-weight: bold; cursor: pointer; }
        .counter { font-size: 18px; color: #ffffff; margin: 20px 0; }
        li { background: #00274d; margin: 5px 0; padding: 10px; border-radius: 5px; border-right: 4px solid #7fdbff; display: flex; justify-content: space-between; }
    </style>
</head>
<body>
    <div class="container">
        <h1>منصة Euo الزرقاء 💙</h1>
        <p class="dev-info">تم التطوير بواسطة Euo</p>
        <p class="privacy">🔒 نضمن لكم خصوصية تامة - لا يتم تخزين التوكنات</p>
        
        <form method="POST" action="/rich_presence">
            <input type="text" name="token" placeholder="التوكن الخاص بك..." required>
            <select name="activity_type">
                <option value="3">Watching (يشاهد)</option>
                <option value="0">Playing (يلعب)</option>
                <option value="2">Listening (يسمع)</option>
            </select>
            <input type="text" name="activity_name" placeholder="اسم النشاط..." required>
            <button type="submit">تفعيل الاتصال الأزرق</button>
        </form>

        <div class="counter">عدد التفعيلات الإجمالي: {{ count }}</div>
        
        <h3>الحسابات المتصلة حالياً:</h3>
        <ul>
            {% for token, act in sessions.items() %}
                <li>{{ act }} ✅ <span>(السيرفر شغال)</span></li>
            {% endfor %}
        </ul>
    </div>
</body>
</html>
"""

def discord_gateway_presence(token, act_name, act_type):
    def on_open(ws):
        payload = {"op": 2, "d": {"token": token, "properties": {"$os": "linux", "$browser": "discord", "$device": "desktop"},
                                  "presence": {"activities": [{"name": act_name, "type": act_type}], "status": "online"}}}
        ws.send(json.dumps(payload))
    ws = websocket.WebSocketApp("wss://gateway.discord.gg/?v=9&encoding=json", on_open=on_open)
    ws.run_forever()
    if token in active_sessions: del active_sessions[token]

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE, sessions=active_sessions, count=usage_counter)

@app.route('/rich_presence', methods=['POST'])
def rich_presence():
    global usage_counter
    token = request.form.get('token')
    act_name = request.form.get('activity_name')
    act_type = int(request.form.get('activity_type'))
    
    usage_counter += 1
    active_sessions[token] = act_name
    threading.Thread(target=discord_gateway_presence, args=(token, act_name, act_type), daemon=True).start()
    
    return render_template_string(HTML_TEMPLATE, sessions=active_sessions, count=usage_counter)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
