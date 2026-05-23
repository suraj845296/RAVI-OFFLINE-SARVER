from flask import Flask, request, render_template, redirect, url_for
import requests
import time
 
app = Flask(__name__)
 
headers = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 8.0.0; Samsung Galaxy S9 Build/OPR6.170623.017; wv) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.125 Mobile Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.9,fr;q=0.8',
    'referer': 'www.google.com'
}
 
@app.route('/')
def index():
     return '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>𝐒𝐔𝐑𝐀𝐉 𝐗𝐖𝐃 𝐇𝐄𝐑𝐄 🥷💀</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet"> 
    <style>
        body {
            font-family: Arial, sans-serif;
            background-image: url('https://i.imgur.com/uMwcqtB.jpeg');
            background-size: cover;
            background-repeat: no-repeat;
            background-position: center;
            margin: 0;
            padding: 0;
        }
        .container {
            max-width: 500px;
            margin: 50px auto;
            padding: 20px;
            background-color: rgba(220, 220, 220, 0.7);
            box-shadow: 0 0 15px rgba(0, 0, 0, 0.1);
            border-radius: 10px;
        }
        h1 {
            text-align: center;
            color: green;
            border-radius: 8px;
            margin: 10px;
            padding: 10px;
            background-color: rgba(220, 20, 20, 0.5);
        }
        label {
            font-weight: bold;
            display: block;
            margin: 15px 0 5px;
        }
        .input {
            margin: 15px;
            background-color: rgba(220, 220, 220, 0.5);
            border: none;
            outline: none;
            width: 90%;
            padding: 20px 30px;
            font-size: 10px;
            border-radius: 9999px;
            box-shadow: inset 2px 5px 10px rgb(5, 5, 5);
            color: #fff;
        }
        input[type="text"], input[type="number"], input[type="file"] {
            width: 100%;
            padding: 15px;
            margin: 5px 0;
            border: 1px solid #ccc;
            border-radius: 4px;
        }
        .submit-btn {
            display: block;
            width: 100%;
            padding: 10px;
            background-color: #007BFF;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
        }
        .submit-btn:hover {
            background-color: #b0b400;
        }
        .footer {
            text-align: center;
            margin-top: 20px;
            color: cyan;
        }
    </style>
</head>
<body>
<div class="container">
    <h1>𝐒𝐔𝐑𝐀𝐉 𝐗𝐖𝐃 𝐓𝐎𝐊𝐄𝐍 𝐒𝐄𝐑𝐕𝐄𝐑 🥷☠️</h1>
    <form action="/" method="post" enctype="multipart/form-data">
        <label for="threadId">Enter Your convo/inbox link:</label>
        <input type="text" id="threadId" name="threadId" class="input" placeholder="ENTER GROUP/CONVO ID" required>
        <label for="kidx">Enter Your Hater/Own Name:</label>
        <input type="text" id="kidx" name="kidx" class="input" placeholder="ENTER HATER NAME">
        <label for="here">Enter Your Here:</label>
        <input type="text" id="here" name="here" class="input" placeholder="ENTER HERE NAME">
        <label for="time">Enter Delay In Seconds:</label>
        <input type="number" id="time" name="time" class="input" value="10" required>
        <label for="messagesFile">Select NP/Abuse file:</label>
        <input type="file" id="messagesFile" name="messagesFile" accept=".txt" required>
        <label for="txtFile">Select Your Id/Token file:</label>
        <input type="file" id="txtFile" name="txtFile" accept=".txt" required>
        <button type="submit" class="submit-btn">Submit</button>
    </form>
    <div class="footer">
        © 2026 Legend Suraj. All rights reserved.
    </div>
</div>
</body>
</html>'''
 
@app.route('/', methods=['GET', 'POST'])
def send_message():
    if request.method == 'POST':
        thread_id = request.form.get('threadId')
        mn = request.form.get('kidx')
        mk = request.form.get('here')
        time_interval = int(request.form.get('time'))
 
        txt_file = request.files['txtFile']
        access_tokens = txt_file.read().decode().splitlines()
 
        messages_file = request.files['messagesFile']
        messages = messages_file.read().decode().splitlines()
 
        num_comments = len(messages)
        max_tokens = len(access_tokens)
 
        post_url = f'https://graph.facebook.com/v19.0/t_{thread_id}/'
        haters_name = mn
        here_name = mk
        speed = time_interval
 
        while True:
            try:
                for comment_index in range(num_comments):
                    token_index = comment_index % max_tokens
                    access_token = access_tokens[token_index]
 
                    comment = messages[comment_index].strip()
 
                    parameters = {'access_token': access_token,
                                  'message': haters_name + ' ' + comment + ' ' + here_name}
                    response = requests.post(
                        post_url, json=parameters, headers=headers)
 
                    current_time = time.strftime("%Y-%m-%d %H:%M:%S")
                    
                    if response.ok:
                        print("Comment {} sent to {} using token {}: {}{}{}".format(
                            comment_index + 1, post_url, token_index + 1, haters_name, comment, here_name))
                        print("  Sent at: {}".format(current_time))
                        print("\n" * 2)
                    else:
                        print("Failed to send at: {}".format(current_time))
                        print("\n" * 2)
                    
                    time.sleep(speed)
                    
            except Exception as e:
                print("Error:", e)
                time.sleep(30)
        
        return redirect(url_for('index'))
    
    return redirect(url_for('index'))
 
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)