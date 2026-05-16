import requests

def CHECK_CONNECTION():
    try:
        requests.get("https://google.com", timeout=5)
        return True
    except:
        return False
