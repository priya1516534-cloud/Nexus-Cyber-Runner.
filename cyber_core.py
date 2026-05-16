import os, subprocess, sys, ast
from flask import Flask, request, jsonify, send_from_directory
from threading import Thread

app = Flask(__name__)

# --- SMART LIBRARY CHECKER ---
def install_missing_libs(file_path):
    try:
        with open(file_path, "r") as f:
            tree = ast.parse(f.read())
        
        # Script ke andar se imports dhoondna
        imported_libs = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for n in node.names: imported_libs.append(n.name.split('.')[0])
            elif isinstance(node, ast.ImportFrom):
                if node.module: imported_libs.append(node.module.split('.')[0])
        
        # System libraries ko chhod kar baaki install karna
        exclude = ['os', 'sys', 'time', 'math', 'threading', 'json', 're', 'ast']
        for lib in set(imported_libs):
            if lib not in exclude:
                print(f"[!] NEXUS-INSTALLER: Installing {lib}...")
                subprocess.run([sys.executable, "-m", "pip", "install", lib])
        
        # Bot ko background mein start karna
        print(f"[#] NEXUS-CORE: Launching {file_path}")
        subprocess.Popen([sys.executable, file_path])
        
    except Exception as e:
        print(f"[-] NEXUS-ERROR: {e}")

@app.route('/')
def home():
    return send_from_directory('.', 'index_dashboard.html')

@app.route('/deploy', methods=['POST'])
def deploy():
    if 'file' not in request.files: return jsonify({"status": "File Missing"}), 400
    
    file = request.files['file']
    os.makedirs("VAULT", exist_ok=True)
    f_path = os.path.join("VAULT", file.filename)
    file.save(f_path)
    
    # Nayi thread mein install aur run karna
    Thread(target=install_missing_libs, args=(f_path,)).start()
    
    return jsonify({
        "status": "DEPLOYMENT INITIALIZED 🚀",
        "bot": file.filename,
        "msg": "Libraries are being checked and installed..."
    })

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
