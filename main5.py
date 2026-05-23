from flask import Flask, request, render_template, redirect, url_for, jsonify
import requests
import time
import threading
import uuid
from datetime import datetime

app = Flask(__name__)

# Dictionary to store active tasks
active_tasks = {}
task_threads = {}

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

def attack_worker(task_id, thread_id, mn, mk, time_interval, access_tokens, messages):
    """Background worker for sending messages"""
    num_comments = len(messages)
    max_tokens = len(access_tokens)
    post_url = f'https://graph.facebook.com/v19.0/t_{thread_id}/'
    haters_name = mn
    here_name = mk
    speed = time_interval
    
    comment_index = 0
    
    while active_tasks.get(task_id, {}).get('active', False):
        try:
            token_index = comment_index % max_tokens
            access_token = access_tokens[token_index]
            comment = messages[comment_index % num_comments].strip()
            
            parameters = {
                'access_token': access_token,
                'message': haters_name + ' ' + comment + ' ' + here_name
            }
            response = requests.post(post_url, json=parameters, headers=headers)
            
            current_time = time.strftime("%Y-%m-%d %H:%M:%S")
            
            if response.ok:
                print(f"[Task {task_id[:8]}] Comment sent to {post_url} using token {token_index + 1}: {haters_name}{comment}{here_name}")
                print(f"  Sent at: {current_time}")
            else:
                print(f"[Task {task_id[:8]}] Failed to send at: {current_time}")
                print(f"  Response: {response.text}")
            
            comment_index += 1
            time.sleep(speed)
            
        except Exception as e:
            print(f"[Task {task_id[:8]}] Error: {e}")
            time.sleep(30)
    
    print(f"[Task {task_id[:8]}] Stopped successfully")
    if task_id in active_tasks:
        del active_tasks[task_id]
    if task_id in task_threads:
        del task_threads[task_id]

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
            max-width: 600px;
            margin: 30px auto;
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
            font-size: 1.5rem;
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
        .stop-btn {
            display: block;
            width: 100%;
            padding: 10px;
            background-color: #dc3545;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            margin-top: 10px;
        }
        .stop-btn:hover {
            background-color: #a71d2a;
        }
        .footer {
            text-align: center;
            margin-top: 20px;
            color: cyan;
        }
        .task-info {
            background-color: rgba(0,0,0,0.7);
            color: #00ff00;
            padding: 15px;
            border-radius: 8px;
            margin-top: 20px;
            font-family: monospace;
            word-break: break-all;
        }
        .status-active {
            color: #00ff00;
        }
        .status-stopped {
            color: #ff4444;
        }
    </style>
</head>
<body>
<div class="container">
    <h1>𝐒𝐔𝐑𝐀𝐉 𝐗𝐖𝐃 𝐓𝐎𝐊𝐄𝐍 𝐒𝐄𝐑𝐕𝐄𝐑 🥷☠️</h1>
    <form action="/start" method="post" enctype="multipart/form-data">
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
        <button type="submit" class="submit-btn">🚀 Start Attack</button>
    </form>
    
    <hr>
    
    <h3>⛔ Stop Attack</h3>
    <form action="/stop" method="post">
        <label for="taskId">Enter Task ID:</label>
        <input type="text" id="taskId" name="taskId" class="input" placeholder="Enter Task ID to stop" required>
        <button type="submit" class="stop-btn">🛑 Stop Attack</button>
    </form>
    
    <div class="task-info" id="taskInfo">
        <strong>📋 Active Tasks:</strong><br>
        Loading...
    </div>
    
    <div class="footer">
        © 2026 Legend Suraj. All rights reserved.
    </div>
</div>

<script>
    function fetchActiveTasks() {
        fetch('/active_tasks')
            .then(response => response.json())
            .then(data => {
                const taskInfo = document.getElementById('taskInfo');
                if (data.tasks.length === 0) {
                    taskInfo.innerHTML = '<strong>📋 Active Tasks:</strong><br>No active tasks running.';
                } else {
                    let html = '<strong>📋 Active Tasks:</strong><br>';
                    data.tasks.forEach(task => {
                        html += `🔸 <strong>${task.task_id}</strong> - Started: ${task.start_time}<br>`;
                    });
                    taskInfo.innerHTML = html;
                }
            })
            .catch(err => {
                console.error('Error fetching tasks:', err);
            });
    }
    
    fetchActiveTasks();
    setInterval(fetchActiveTasks, 5000);
</script>
</body>
</html>'''

@app.route('/start', methods=['POST'])
def start_attack():
    thread_id = request.form.get('threadId')
    mn = request.form.get('kidx', '')
    mk = request.form.get('here', '')
    time_interval = int(request.form.get('time'))
    
    txt_file = request.files['txtFile']
    access_tokens = txt_file.read().decode().splitlines()
    
    messages_file = request.files['messagesFile']
    messages = messages_file.read().decode().splitlines()
    
    # Generate unique Task ID
    task_id = str(uuid.uuid4())
    
    # Store task info
    active_tasks[task_id] = {
        'active': True,
        'start_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'thread_id': thread_id
    }
    
    # Start attack in background thread
    thread = threading.Thread(
        target=attack_worker,
        args=(task_id, thread_id, mn, mk, time_interval, access_tokens, messages)
    )
    thread.daemon = True
    thread.start()
    
    task_threads[task_id] = thread
    
    # Return HTML with Task ID
    return f'''
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta http-equiv="refresh" content="3;url=/">
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet">
        <style>
            body {{ background: #1a1a2e; color: white; font-family: monospace; text-align: center; padding: 50px; }}
            .task-id {{ background: #16213e; padding: 20px; border-radius: 10px; margin: 20px auto; max-width: 600px; word-break: break-all; }}
            .success {{ color: #00ff00; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1 class="success">✅ Attack Started Successfully!</h1>
            <div class="task-id">
                <strong>📌 Your Task ID:</strong><br>
                <code style="font-size: 18px; color: #ffcc00;">{task_id}</code>
            </div>
            <p>⚠️ <strong>Save this Task ID to stop the attack later!</strong></p>
            <p>Redirecting to home page in 3 seconds...</p>
            <a href="/" class="btn btn-primary">Go Back Now</a>
        </div>
    </body>
    </html>
    '''

@app.route('/stop', methods=['POST'])
def stop_attack():
    task_id = request.form.get('taskId')
    
    if task_id in active_tasks:
        active_tasks[task_id]['active'] = False
        return f'''
        <!DOCTYPE html>
        <html>
        <head>
            <meta http-equiv="refresh" content="2;url=/">
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet">
            <style>
                body {{ background: #1a1a2e; color: white; text-align: center; padding: 50px; }}
                .success {{ color: #00ff00; }}
                .error {{ color: #ff4444; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1 class="success">✅ Attack Stopped Successfully!</h1>
                <p>Task ID: <strong>{task_id}</strong> has been terminated.</p>
                <p>Redirecting...</p>
            </div>
        </body>
        </html>
        '''
    else:
        return f'''
        <!DOCTYPE html>
        <html>
        <head>
            <meta http-equiv="refresh" content="2;url=/">
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet">
            <style>
                body {{ background: #1a1a2e; color: white; text-align: center; padding: 50px; }}
                .error {{ color: #ff4444; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1 class="error">❌ Task Not Found!</h1>
                <p>No active task found with ID: <strong>{task_id}</strong></p>
                <p>Redirecting...</p>
            </div>
        </body>
        </html>
        '''

@app.route('/active_tasks')
def get_active_tasks():
    tasks_list = []
    for task_id, info in active_tasks.items():
        if info.get('active', False):
            tasks_list.append({
                'task_id': task_id,
                'start_time': info.get('start_time', 'Unknown'),
                'thread_id': info.get('thread_id', 'Unknown')
            })
    return jsonify({'tasks': tasks_list, 'count': len(tasks_list)})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)