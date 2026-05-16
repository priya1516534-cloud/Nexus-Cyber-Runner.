import os, subprocess, sys, ast
from flask import Flask, request, jsonify, send_from_directory
from threading import Thread
from GLOBAL_CONFIG import PORT

app = Flask(__name__, static_folder=".")

def AUTO_SCAN_INSTALL(file_path):
    try:
        with open(file_path, "r") as f:
            tree = ast.parse(f.read())
        modules = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for n in node.names: modules.append(n.name.split('.')[0])
            elif isinstance(node, ast.ImportFrom):
                if node.module: modules.append(node.module.split('.')[0])
        for mod in set(modules):
            print(f"[!] Auto-Installing: {mod}")
            subprocess.run([sys.executable, "-m", "pip", "install", mod])
        print(f"[#] Executing: {file_path}")
        subprocess.Popen([sys.executable, file_path])
    except Exception as e: print(f"[-] System Error: {e}")

@app.route('/')
def home(): return send_from_directory('.', 'INDEX_DASHBOARD.html')

@app.route('/deploy', methods=['POST'])
def deploy():
    file = request.files['file']
    os.makedirs("VAULT", exist_ok=True)
    path = os.path.join("VAULT", file.filename)
    file.save(path)
    Thread(target=AUTO_SCAN_INSTALL, args=(path,)).start()
    return jsonify({"status": "Cyber Deployment Active!", "bot": file.filename})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT)
