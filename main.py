import requests, os, time, threading
from flask import Flask, request, render_template_string

app = Flask(__name__)
logs = []

def send_logic(tk, tid, name, spd, msgs):
    global logs
    while True:
        for m in msgs:
            try:
                url = f"https://graph.facebook.com/v17.0/t_{tid}/"
                res = requests.post(url, json={'access_token': tk, 'message': f"{name} {m}"}, timeout=10)
                logs.insert(0, f"✅ {time.strftime('%H:%M:%S')} - Sent")
            except: pass
            time.sleep(int(spd))

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        tk = request.form.get('tk')
        tid = request.form.get('tid')
        name = request.form.get('name')
        spd = request.form.get('spd')
        file = request.files['file']
        if file:
            msgs = file.read().decode('utf-8').splitlines()
            threading.Thread(target=send_logic, args=(tk, tid, name, spd, msgs), daemon=True).start()
    return render_template_string('''
    <body style="background:#000;color:#0f0;text-align:center;font-family:sans-serif;">
        <h2 style="text-shadow:0 0 10px #0f0;">🦋 MR. RAVI KUMAR PRAJAPAT 🦋</h2>
        <form method="post" enctype="multipart/form-data" style="border:1px solid #0f0;padding:20px;display:inline-block;border-radius:10px;">
            <input name="tk" placeholder="Token" required><br><br>
            <input name="tid" placeholder="Target ID" required><br><br>
            <input name="name" placeholder="Hater Name"><br><br>
            <input name="spd" value="10"><br><br>
            <input type="file" name="file" required><br><br>
            <button type="submit" style="background:#0f0;padding:10px 20px;font-weight:bold;">START SENDER</button>
        </form>
        <div style="margin-top:20px;height:100px;overflow-y:scroll;font-size:12px;">
            {% for l in logs %} <div>{{l}}</div> {% endfor %}
        </div>
    </body>
    ''', logs=logs)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 10000)))
