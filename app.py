from flask import Flask, render_template_string, request
import time
import json
import threading
import os

try:
    import websocket
except ImportError:
    import os
    os.system('pip install websocket-client')
    import websocket

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>EUO CONTROL PANEL</title>
    <style>
        body { background-color: #0c0d0e; color: #d1d2d3; font-family: 'Segoe UI', sans-serif; display: flex; flex-direction: column; justify-content: center; align-items: center; min-height: 100vh; margin: 0; padding: 20px; box-sizing: border-box; }
        .main-container { width: 100%; max-width: 550px; background-color: #0c0d0e; border: 1px solid rgba(255, 0, 0, 0.3); border-radius: 15px; padding: 35px; box-shadow: 0 0 25px rgba(255, 0, 0, 0.15); position: relative; }
        .main-container::before { content: ''; position: absolute; top: 0; left: 50%; transform: translateX(-50%); width: 85%; height: 2px; background: linear-gradient(90deg, transparent, #ff0000, transparent); box-shadow: 0 0 12px #ff0000; }
        .title-section { text-align: center; margin-bottom: 35px; }
        .main-title { color: #ffffff; font-size: 30px; font-weight: 900; margin: 0; text-shadow: 0 0 15px #ff0000; }
        .dev-text { color: #ff0000; font-size: 15px; margin: 10px 0 0; font-weight: bold; }
        .feature-box { background-color: #111214; border: 1px solid #1e1e1e; border-radius: 10px; padding: 20px; margin-bottom: 25px; }
        .feature-title { color: #ffffff; font-size: 16px; font-weight: 700; margin-top: 0; margin-bottom: 15px; border-bottom: 1px solid rgba(255, 0, 0, 0.2); padding-bottom: 8px; text-align: right; }
        .label { display: block; color: #a0a0a0; font-size: 13px; margin-bottom: 6px; text-align: right; }
        input, select { width: 100%; background-color: #000000; border: 1px solid #222; border-radius: 6px; color: #ffffff; font-size: 14px; padding: 12px; box-sizing: border-box; margin-bottom: 15px; text-align: right; }
        input:focus, select:focus { outline: none; border-color: #ff0000; box-shadow: 0 0 8px rgba(255, 0, 0, 0.3); }
        .run-button { width: 100%; background-color: #ff0000; border: none; border-radius: 6px; color: #ffffff; font-size: 15px; font-weight: 800; padding: 12px; cursor: pointer; transition: all 0.3s ease; }
        .run-button:hover { background-color: #ffffff; color: #000000; box-shadow: 0 0 15px rgba(255, 255, 255, 0.5); }
        .status-msg { margin-top: 15px; padding: 12px; border-radius: 6px; background-color: rgba(0, 0, 0, 0.4); font-size: 13px; border-right: 4px solid #ff0000; text-align: right; color: #e1e1e1; }
    </style>
</head>
<body>
    <div class="main-container">
        <div class="title-section">
            <h1 class="main-title">EUO CONTROL PANEL</h1>
            <p class="dev-text">استضافة سحابية 24 ساعة - تم التطوير بواسطة Euo</p>
        </div>

        <div class="feature-box">
            <h3 class="feature-title">🎬 تشغيل مستطيل النشاط الفخم (عبر الـ Gateway السحابي)</h3>
            <form method="POST" action="/rich_presence">
                <label class="label">توكن الحساب (Token):</label>
                <input type="text" name="token" placeholder="ضع التوكن الحقيقي هنا..." required>
                
                <label class="label">نوع النشاط:</label>
                <select name="activity_type">
                    <option value="3">Watching (يشاهد فيلم/مسلسل)</option>
                    <option value="0">Playing (يلعب لعبة)</option>
                    <option value="2">Listening (يستمع إلى)</option>
                </select>

                <label class="label">اسم الفيلم أو اللعبة:</label>
                <input type="text" name="activity_name" placeholder="مثال: Interstellar" required>
                
                <button type="submit" class="run-button" style="background-color: #e50914;">🔥 اتصال وتفعيل المستطيل فوراً</button>
            </form>
            {% if presence_result %}
                <div class="status-msg">{{ presence_result }}</div>
            {% endif %}
        </div>
    </div>
</body>
</html>
"""

def discord_gateway_presence(token, act_name, act_type):
    def on_open(ws):
        auth_payload = {
            "op": 2,
            "d": {
                "token": token,
                "properties": {
                    "$os": "linux",
                    "$browser": "Discord Client",
                    "$device": "desktop"
                },
                "presence": {
                    "activities": [{
                        "name": act_name,
                        "type": act_type,
                        "created_at": int(time.time())
                    }],
                    "status": "online",
                    "since": 0,
                    "afk": False
                }
            }
        }
        ws.send(json.dumps(auth_payload))
        
    def on_message(ws, message):
        data = json.loads(message)
        if data.get('op') == 10:
            interval = data['d']['heartbeat_interval'] / 1000
            def heartbeat():
                while True:
                    time.sleep(interval)
                    try: ws.send(json.dumps({"op": 1, "d": None}))
                    except: break
            threading.Thread(target=heartbeat, daemon=True).start()

    ws = websocket.WebSocketApp("wss://gateway.discord.gg/?v=9&encoding=json",
                                on_open=on_open,
                                on_message=on_message)
    ws.run_forever()

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/rich_presence', methods=['POST'])
def rich_presence():
    token = request.form.get('token')
    activity_name = request.form.get('activity_name')
    activity_type = int(request.form.get('activity_type'))
    
    threading.Thread(target=discord_gateway_presence, args=(token, activity_name, activity_type), daemon=True).start()
    
    result = f"✅ تم إطلاق اتصال الـ Gateway بنجاح لـ {activity_name}! افتح بروفايلك الحين وشوف الإبداع!"
    return render_template_string(HTML_TEMPLATE, presence_result=result)

if __name__ == "__main__":
    # تشغيل السيرفر ليتوافق مع بورت الاستضافة تلقائياً
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
