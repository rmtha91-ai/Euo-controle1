from flask import Flask, render_template_string, request
import os

app = Flask(__name__)

# المتغيرات العالمية للعدادات
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
        body { background-color: #000; color: #7fdbff; font-family: sans-serif; margin: 0; display: flex; justify-content: center; align-items: center; min-height: 100vh; }
        .container { width: 90%; max-width: 450px; background-color: #0d0d0d; padding: 20px; border-radius: 15px; border: 1px solid #7fdbff; box-shadow: 0 0 10px #007bff; text-align: center; }
        h2 { color: #fff; border-bottom: 1px solid #333; padding-bottom: 10px; margin-top: 20px; font-size: 18px; }
        input, select, button { width: 100%; padding: 10px; margin: 5px 0; border-radius: 6px; border: 1px solid #333; background: #1a1a1a; color: white; box-sizing: border-box; }
        button { background: #007bff; border: none; font-weight: bold; cursor: pointer; margin-top: 10px; }
        button:hover { background: #0056b3; }
        .stats { font-size: 14px; color: #888; margin: 20px 0; background: #111; padding: 10px; border-radius: 5px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>منصة Euo</h1>
        <div class="stats">الزوار: {{ visitors }} | العمليات: {{ count }}</div>
        
        <form method="POST" action="/action_presence">
            <h2>قسم الحالة</h2>
            <input type="text" name="token" placeholder="توكن الحساب..." required>
            <select name="type"><option value="3">Watching</option><option value="0">Playing</option></select>
            <input type="text" name="text" placeholder="النص..." required>
            <button type="submit">تفعيل الحالة</button>
        </form>

        <form method="POST" action="/action_clone">
            <h2>قسم نسخ السيرفرات</h2>
            <input type="text" name="token" placeholder="توكن الحساب..." required>
            <input type="text" name="source" placeholder="آيدي السيرفر المصدر..." required>
            <input type="text" name="target" placeholder="آيدي السيرفر الهدف..." required>
            <button type="submit" style="background:#28a745;">بدء النسخ</button>
        </form>

        <form method="POST" action="/action_check">
            <h2>قسم فحص اليوزرات</h2>
            <input type="text" name="username" placeholder="اكتب اليوزر للفحص..." required>
            <button type="submit" style="background:#ffc107; color:#000;">فحص الآن</button>
        </form>
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    global visitor_counter
    visitor_counter += 1
    return render_template_string(HTML_TEMPLATE, count=usage_counter, visitors=visitor_counter)

@app.route('/action_presence', methods=['POST'])
def action_presence():
    global usage_counter
    usage_counter += 1
    return render_template_string(HTML_TEMPLATE, count=usage_counter, visitors=visitor_counter)

@app.route('/action_clone', methods=['POST'])
def action_clone():
    global usage_counter
    usage_counter += 1
    return render_template_string(HTML_TEMPLATE, count=usage_counter, visitors=visitor_counter)

@app.route('/action_check', methods=['POST'])
def action_check():
    global usage_counter
    usage_counter += 1
    return render_template_string(HTML_TEMPLATE, count=usage_counter, visitors=visitor_counter)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
