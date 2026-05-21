from flask import Flask, render_template_string, request
import time, threading, os

app = Flask(__name__)

# بيانات الموقع
usage_counter = 0
visitor_counter = 0
active_sessions = {}

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>EUO PLATFORM</title>
    <style>
        body { background-color: #000; color: #7fdbff; font-family: sans-serif; margin: 0; display: flex; justify-content: center; align-items: center; min-height: 100vh; }
        .container { width: 90%; max-width: 450px; background-color: #0d0d0d; padding: 25px; border-radius: 15px; border: 1px solid #7fdbff; box-shadow: 0 0 15px #007bff; text-align: center; }
        h1 { color: #fff; margin-bottom: 5px; }
        .dev-info { font-size: 13px; color: #555; margin-bottom: 20px; }
        input, select, button { width: 100%; padding: 12px; margin: 8px 0; border-radius: 8px; border: 1px solid #333; background: #1a1a1a; color: white; box-sizing: border-box; }
        button { background: #007bff; border: none; font-weight: bold; cursor: pointer; }
        button:hover { background: #0056b3; }
        .stats { font-size: 14px; color: #888; margin: 15px 0; }
        li { background: #111; margin: 5px 0; padding: 10px; border-radius: 5px; border-right: 3px solid #007bff; text-align: right; font-size: 13px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>منصة Euo</h1>
        <p class="dev-info">تم التطوير بواسطة Euo</p>
        
        <form method="POST" action="/process">
            <input type="text" name="token" placeholder="التوكن..." required>
            <input type="text" name="input_data" placeholder="ايدي سيرفر / يوزر للفحص...">
            <select name="action">
                <option value="presence">تفعيل نشاط</option>
                <option value="clone">نسخ سيرفر</option>
                <option value="check_user">فحص يوزرات</option>
            </select>
            <button type="submit">تفعيل</button>
        </form>

        <div class="stats">الزوار: {{ visitors }} | العمليات: {{ count }}</div>
        
        <h3>العمليات النشطة:</h3>
        <ul>
            {% for token, act in sessions.items() %}
                <li>{{ act }} ✅</li>
            {% endfor %}
        </ul>
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    global visitor_counter
    visitor_counter += 1
    return render_template_string(HTML_TEMPLATE, sessions=active_sessions, count=usage_counter, visitors=visitor_counter)

@app.route('/process', methods=['POST'])
def process():
    global usage_counter
    token = request.form.get('token')
    data = request.form.get('input_data')
    action = request.form.get('action')
    
    usage_counter += 1
    active_sessions[token] = f"{action.upper()}: {data}"
    
    return render_template_string(HTML_TEMPLATE, sessions=active_sessions, count=usage_counter, visitors=visitor_counter)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
