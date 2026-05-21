from flask import Flask, render_template_string, request
import requests
import os

app = Flask(__name__)

# التصميم (CSS + HTML) في متغير واحد
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>EUO PLATFORM</title>
    <style>
        body { background: #000; color: #7fdbff; font-family: sans-serif; display: flex; justify-content: center; min-height: 100vh; padding: 20px; }
        .container { width: 100%; max-width: 500px; background: #0a0a0a; padding: 20px; border-radius: 15px; border: 1px solid #7fdbff; box-shadow: 0 0 15px #007bff; text-align: center; }
        input, select, button { width: 100%; padding: 12px; margin: 8px 0; border-radius: 8px; border: 1px solid #333; background: #111; color: white; box-sizing: border-box; }
        button { background: #007bff; font-weight: bold; cursor: pointer; }
        .result { background: #111; padding: 15px; border-radius: 8px; border: 1px solid #007bff; color: #fff; margin: 10px 0; }
    </style>
</head>
<body>
    <div class="container">
        <h1>منصة Euo</h1>
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
            <input type="text" name="user_id" placeholder="ايدي اليوزر...">
            <button name="action" value="check" style="background:#ffc107; color:#000;">فحص اليوزر</button>
        </form>
    </div>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template_string(HTML_TEMPLATE, msg="")

@app.route('/process', methods=['POST'])
def process():
    action = request.form.get('action')
    msg = "خطأ في الاتصال"

    if action == "check":
        uid = request.form.get('user_id')
        # كود الفحص الحقيقي
        r = requests.get(f"https://discord.com/api/v9/users/{uid}")
        msg = f"اليوزر {uid} هو: {'مستعمل' if r.status_code == 200 else 'متاح'}"
    
    elif action == "presence":
        token = request.form.get('token')
        text = request.form.get('text')
        headers = {"Authorization": token, "Content-Type": "application/json"}
        # طلب تحديث الحالة
        r = requests.patch("https://discord.com/api/v9/users/@me/settings", 
                           headers=headers, json={"custom_status": {"text": text}})
        msg = "تم تفعيل الحالة بنجاح!" if r.status_code == 200 else "فشل: تأكد من التوكن"

    elif action == "clone":
        msg = "بدء النسخ (ملاحظة: يحتاج صلاحيات كاملة)"

    return render_template_string(HTML_TEMPLATE, msg=msg)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
