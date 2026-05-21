from flask import Flask, render_template_string, request
import os

app = Flask(__name__)

visitor_counter = 0
usage_counter = 0

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>EUO PLATFORM</title>
    <style>
        body { background: #000; color: #7fdbff; font-family: 'Segoe UI', sans-serif; display: flex; justify-content: center; min-height: 100vh; padding: 20px; }
        .container { width: 100%; max-width: 500px; background: #0a0a0a; padding: 25px; border-radius: 20px; border: 1px solid #7fdbff; box-shadow: 0 0 20px rgba(0, 123, 255, 0.3); }
        h1 { color: #fff; text-align: center; }
        h2 { color: #7fdbff; font-size: 16px; margin-top: 20px; border-bottom: 1px solid #333; }
        input, select, button { width: 100%; padding: 12px; margin: 8px 0; border-radius: 10px; border: 1px solid #222; background: #111; color: #fff; box-sizing: border-box; }
        button { background: #007bff; font-weight: bold; cursor: pointer; transition: 0.3s; }
        button:hover { background: #0056b3; }
        .stats { text-align: center; color: #888; font-size: 14px; margin-bottom: 20px; }
        .result { background: #1a1a1a; padding: 15px; border-radius: 10px; color: #0f0; text-align: center; margin-top: 10px; border: 1px solid #0f0; }
    </style>
</head>
<body>
    <div class="container">
        <h1>منصة Euo</h1>
        <div class="stats">الزوار: {{ visitors }} | العمليات: {{ count }}</div>
        {% if msg %}<div class="result">{{ msg }}</div>{% endif %}
        <form method="POST" action="/process">
            <h2>1. الحالة</h2>
            <input type="text" name="token" placeholder="التوكن...">
            <select name="type"><option value="3">Watching</option><option value="0">Playing</option></select>
            <input type="text" name="text" placeholder="النص...">
            <button name="action" value="presence">تفعيل الحالة</button>
            <h2>2. نسخ السيرفرات</h2>
            <input type="text" name="token_clone" placeholder="التوكن...">
            <input type="text" name="src" placeholder="آيدي المصدر...">
            <input type="text" name="tgt" placeholder="آيدي الهدف...">
            <button name="action" value="clone" style="background:#28a745;">بدء النسخ</button>
            <h2>3. فحص اليوزرات</h2>
            <input type="text" name="user_id" placeholder="آيدي اليوزر...">
            <button name="action" value="check" style="background:#ffc107; color:#000;">فحص اليوزر</button>
        </form>
    </div>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    global visitor_counter, usage_counter
    if request.method == 'GET': visitor_counter += 1
    return render_template_string(HTML_TEMPLATE, visitors=visitor_counter, count=usage_counter, msg="")

@app.route('/process', methods=['POST'])
def process():
    global usage_counter
    usage_counter += 1
    action = request.form.get('action')
    msg = "تم استلام طلبك - جاري التنفيذ..."
    return render_template_string(HTML_TEMPLATE, visitors=visitor_counter, count=usage_counter, msg=msg)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
