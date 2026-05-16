import subprocess, sys

def RUN_BOT(path):
    print(f"[*] NEXUS EXECUTOR: Starting {path}")
    return subprocess.Popen([sys.executable, path])
