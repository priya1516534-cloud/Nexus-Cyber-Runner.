import datetime

def GET_TIMESTAMP():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def FORMAT_LOG(msg):
    return f"[{GET_TIMESTAMP()}] {msg}"
