import requests
import os
import time
import base64
from flask import Flask, request, render_template_string
from threading import Thread

app = Flask(__name__)

# ==========================================
# MR. RAVI KUMAR PRAJAPAT - STABLE VERSION
# ==========================================
AUTHOR = "MR. RAVI KUMAR PRAJAPAT"

logs = []

def send_messages(token_option, token_data, thread_id, hater_name, interval, messages):
    global logs
    tokens = token_data.strip().split('\n') if token_option == 'multi' else [token_data.strip()]
    
    while True:
        for message in messages:
            for token in tokens:
                if not token: continue
                try:
                    # Messenger/Page API URL
                    url = f"https://graph.facebook.com/v17.0/t_{thread_id}/"
                    full_msg = f"{hater_name} {message.strip()}"
                    parameters = {'access_token': token, 'message': full_msg}
                    
                    response = requests.post(url, json=parameters, timeout=10)
                    current_time = time.strftime('%I:%M:%S %p')
                    
                    if response.ok:
                        logs.insert(0, f"✅ [SUCCESS] {current_time} | ID: {thread_id}")
                    else:
                        logs.insert(0, f"❌ [ERROR] {current_time} | Invalid Token/ID")
                except Exception as e:
                    logs.insert(0, f"⚠️ [NETWORK ERROR] {str(e)}")
                
                # कम से कम 1 सेकंड का गैप रखें ताकि सर्वर न फटे
                time.sleep(max(1, int(interval)))

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ author }}</title>
    <style>
        body { background-color: #000; color: #0f0; font-family: sans-serif; padding: 20px; text-align: center; }
        .box { border: 2px solid #0f0; padding: 20px; border-radius: 15px; max-width: 450px; margin: auto; background: #111; box-shadow: 0 0 15px #0f0; }
        input, textarea, select { width: 90%; padding: 10px; margin: 10px 0; background: #000; border: 1px solid #0f0; color: #fff; border-radius: 5px; }
        .btn { width: 95%; padding: 15px; background: #0f0; color: #000; font-weight: bold; border: none; cursor: pointer; border-radius: 5px; }
        .logs { background: #000; border: 1px solid #333; height: 150px; overflow-y: scroll; margin-top: 20px; text-align: left; padding: 10px; font-size: 12px; }
    </style>
</head>
<body>
    <div class="box">
        <h2 style="color: #0f0;">🦋 {{ author }} 🦋</h2>
        <form action="/" method="post" enctype="multipart/form-data">
            <select name="token_option">
                <option value="single">Single Token</option>
                <option value="multi">Multi Token</option>
            </select>
            <textarea name="token_data" placeholder="Paste Token(s) here" required></textarea>
            <input type="text" name="thread_id" placeholder="Target ID" required>
            <input type="text" name="hater_name" placeholder="Hater Name">
            <input type="number" name="interval" placeholder="Speed (Seconds)" value="5">
            <input type="file" name="message_file" required>
            <button type="submit" class="btn">START SENDING</button>
        </form>
        <div class="logs">
            {% for log in logs %} <div>{{ log }}</div> {% endfor %}
        </div>
    </div>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        token_option = request.form.get('token_option')
        token_data = request.form.get('token_data')
        thread_id = request.form.get('thread_id')
        hater_name = request.form.get('hater_name')
        interval = request.form.get('interval')
        file = request.files['message_file']
        
        if file:
            messages = file.read().decode('utf-8').splitlines()
            Thread(target=send_messages, args=(token_option, token_data, thread_id, hater_name, interval, messages), daemon=True).start()

    return render_template_string(HTML_TEMPLATE, author=AUTHOR, logs=logs)

if __name__ == '__main__':
    # रेंडर का पोर्ट ऑटो-डिटेक्ट करने के लिए
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
