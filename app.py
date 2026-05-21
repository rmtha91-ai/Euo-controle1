from flask import Flask, render_template_string, request
import requests
import os

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <title>EUO PLATFORM</title>
    <style>
        :root { --neon: #00d4ff; --bg: #050505; }
        body { background: var(--bg); color: #fff; font-family: 'Segoe UI', Tahoma, sans-serif; display: flex; justify-content: center; align-items: center; min-height: 100vh; margin: 0; }
        .container { width: 95%; max-width: 400px; background: #111; padding: 30px; border-radius: 20px; border: 1px solid #333; box-shadow: 0 0 20px rgba(0, 212, 255, 0.1); text-align: center; }
        h1 { color: var(--neon); margin-bottom: 30px; letter-spacing: 2px; }
        input { width: 100%; padding: 12px; margin: 10px 0; border-radius: 10px; border: 1px solid #222; background: #1a1a1a; color: #fff; box-sizing: border-box; }
        button { width: 100%; padding: 12px; margin: 10px 0; border-radius: 10px; border: none; background: linear-gradient(90deg, #007bff, #00d4ff); color: #fff; font-weight: bold; cursor: pointer; transition: 0.3s; }
        button:hover { opacity: 0.9; transform: translateY(-2px); }
        .res { padding: 15px; margin: 15px 0; border-radius: 10px; background: #000; border: 1px solid var(--neon); color: var(--neon); font-size: 14px; }
        .footer { margin-top: 25px; color: #444; font-size: 11px; letter-spacing: 1px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>EUO SYSTEM</h1>
        {% if msg %}<div class="res">{{ msg }}</div>{% endif %}
        <form method="POST" action="/process">
            <input type="text" name="token" placeholder="التوكن..." required>
            <input type="text" name="data" placeholder="النص أو كود الدعوة...">
            <button name="action" value="presence">تفعيل الحالة</button>
            <button name="action" value="join" style="background: linear-gradient(90deg, #28a745, #00ff88);">دخول سيرفر</button>
        </form>
        <div class="footer">تم البرمجة بواسطة EUO</div>
    </div>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/process', methods=['POST'])
def process():
    action = request.form.get('action')
    token = request.form.get('token')
    data = request.form.get('data')
    
    headers = {"Authorization": token, "Content-Type": "application/json"}
    
    if action == "presence":
        r = requests.patch("https://discord.com/api/v9/users/@me/settings", headers=headers, json={"custom_status": {"text": data}})
        msg = "✅ تم تحديث الحالة" if r.status_code == 200 else "❌ فشل تحديث الحالة"
    
    elif action == "join":
        invite = data.split('/')[-1]
        r = requests.post(f"https://discord.com/api/v9/invites/{invite}", headers=headers)
        msg = "✅ تم الدخول بنجاح" if r.status_code == 200 else "❌ فشل الدخول"
        
    return render_template_string(HTML_TEMPLATE, msg=msg)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
