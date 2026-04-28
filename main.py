import threading
import time
import subprocess
import os
from app import app

def run():
    app.run(host="127.0.0.1", port=5000, debug=False)

def get_chrome():
    paths = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
    ]
    for p in paths:
        if os.path.exists(p):
            return p
    return None

if __name__ == "__main__":
    threading.Thread(target=run, daemon=True).start()
    time.sleep(1.5)

    chrome = get_chrome()
    url = "http://127.0.0.1:5000"

    if chrome:
        subprocess.Popen([
            chrome,
            "--kiosk",
            "--app=" + url,
            "--no-first-run",
            "--disable-infobars"
        ])
    else:
        import webbrowser
        webbrowser.open(url)
