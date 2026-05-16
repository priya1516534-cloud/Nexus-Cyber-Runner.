import os, subprocess, sys, ast
from flask import Flask, request, jsonify, send_from_directory
from threading import Thread
from global_config import PORT

app = Flask(__name__, static_folder=".")

def AUTO_SCAN_INSTALL(file_path):
    try:
        # Step 1: Scan Modules
        with open(file_path, "r") as f:
            tree = ast.parse(f.read())
        modules = [n.name.split('.')[0] for node in ast.walk(tree) if isinstance(node, ast.Import) for n in node.names]
        
        # Step 2: Force Install (Render friendly)
        for mod in set(modules):
            subprocess.run([sys.executable, "-m", "pip", "install", mod], check=True)
        
        # Step 3: Start Bot with Logs
        log_file = open("bot_output.log", "a")
        print(f"🚀 Starting Bot: {file_path}")
        # 'nohup' use kar rahe hain taaki process kill na ho
        subprocess.Popen([sys.executable, file_path], stdout=log_file, stderr=log_file)
        
    except Exception as e:
        with open("error.log", "a") as f:
            f.write(f"Error: {str(e)}\n")

@app.route('/')
def home():
    return send_from_directory('.', 'index_dashboard.html')

@app.route('/deploy', methods=['POST'])
def deploy():
    if 'file' not in request.files: return jsonify({"status": "No File"}), 400
    file = request.files['file']
    os.makedirs("VAULT", exist_ok=True)
    path = os.path.join("VAULT", file.filename)
    file.save(path)
    Thread(target=AUTO_SCAN_INSTALL, args=(path,)).start()
    return jsonify({"status": "🚀 BOT DEPLOYED! System is running it in background."})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT)

