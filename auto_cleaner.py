import os, time

def CLEAN_VAULT():
    # Deletes files older than 24 hours to save space
    now = time.time()
    for f in os.listdir("VAULT"):
        f_path = os.path.join("VAULT", f)
        if os.stat(f_path).st_mtime < now - 86400:
            os.remove(f_path)
