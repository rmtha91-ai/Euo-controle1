from flask import Flask, render_template_string, request
import requests
import os

app = Flask(__name__)

# التصميم الاحترافي مع "المحرك" الحقيقي
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <title>EUO SYSTEM</title>
    <style>
        :root { --neon: #00d4ff; --bg: #050505; }
        body { background: var(--bg); color: #fff; font-family: sans-serif; display: flex; justify-content: center; padding: 20px; }
        .container { width: 100%; max-width: 400px; background: #111; padding: 25px; border-radius: 20px; border: 1px solid #333; box-shadow: 0 0 15px rgba(0, 212, 255, 0.2); }
        h1 { color: var(--neon); text-align: center; }
        h3 { color: #888; font-size: 14px; margin-top: 20px; }
        input { width: 100%; padding: 12px; margin: 8px 0; border-radius: 10px; border: 1px solid #222; background: #1a1a1a; color: white; box-sizing: border-box; }
        button { width: 100%; padding: 12px; margin: 10px 0; border-radius: 10px; border: none; background: linear-gradient(90deg, #007bff, #00d4ff); color: white; font-weight: bold; cursor: pointer; }
        .res { padding: 12px; border-radius: 10px; text-align: center; border: 1px solid var(--neon); color: var(--neon); margin: 15px 0; }
    </style>
</head>
<body>
    <div class="container">
        <h1>EUO SYSTEM</h1>
        {% if msg %}<div class="res">{{ msg }}</div>{% endif %}
        
        <form method="POST" action="/process">
            <h3>تفعيل الحالة</h3>
            <input type="text" name="token" placeholder="التوكن..." required>
            <input type="text" name="status" placeholder="النص المطلوب...">
            <button name="action" value="presence">تفعيل الحالة الآن</button>
            
            <h3>دخول سيرفر</h3>
            <input type="text" name="token_join" placeholder="التوكن...">
            <input type="text" name="invite" placeholder="كود الدعوة (مثال: discord.gg/xyz)...">
            <button name="action" value="join" style="background: linear-gradient(90deg, #28a745, #00ff88);">دخول السيرفر</button>
        </form>
        <p style="text-align:center; font-size:10px; color:#444; margin-top:20px;">تم البرمجة بواسطة EUO</p>
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
    msg = "خطأ غير متوقع"
    
    if action == "presence":
        token = request.form.get('token')
        status = request.form.get('status')
        headers = {"Authorization": token, "Content-Type": "application/json"}
        r = requests.patch("https://discord.com/api/v9/users/@me/settings", headers=headers, json={"custom_status": {"text": status}})
        msg = "✅ تم تفعيل الحالة بنجاح" if r.status_code == 200 else f"❌ فشل التفعيل (كود: {r.status_code})"
        
    elif action == "join":
        token = request.form.get('token_join')
        invite = request.form.get('invite').split('/')[-1]
        headers = {"Authorization": token}
        r = requests.post(f"https://discord.com/api/v9/invites/{invite}", headers=headers)
        msg = "✅ تم الدخول للسيرفر" if r.status_code == 200 else f"❌ فشل الدخول (كود: {r.status_code})"
        
    return render_template_string(HTML_TEMPLATE, msg=msg)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
