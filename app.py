from flask import Flask, render_template, request, redirect, url_for
import subprocess
from screeninfo import get_monitors

app = Flask(__name__)

current_process = None

patterns = {
    "SMPTE Bars": "smptebars=size=1280x720:rate=30",
    "HD Bars": "smptehdbars=size=1920x1080:rate=30",
    "Test Grid": "testsrc=size=1280x720:rate=30",
    "Test Grid 2": "testsrc2=size=1280x720:rate=30",
    "RGB Pattern": "rgbtestsrc=size=1280x720:rate=30",
    "Black": "color=c=black:size=1280x720:rate=30",
    "Zone Plate": "zoneplate=size=1280x720:rate=30",
}


def get_monitor_map():
    monitors = get_monitors()
    monitor_map = {}
    for i, m in enumerate(monitors):
        monitor_map[f"Monitor {i+1} ({m.width}x{m.height})"] = {
            "left": m.x,
            "top": m.y
        }
    return monitor_map


def stop_current():
    global current_process
    if current_process and current_process.poll() is None:
        current_process.terminate()
        current_process = None


@app.route("/")
def index():
    monitors = get_monitor_map()
    return render_template("index.html", patterns=patterns, monitors=monitors)


@app.route("/play", methods=["POST"])
def play():
    global current_process

    pattern_name = request.form.get("pattern")
    monitor_name = request.form.get("monitor")

    monitors = get_monitor_map()

    if pattern_name not in patterns or monitor_name not in monitors:
        return redirect(url_for("index"))

    stop_current()

    monitor = monitors[monitor_name]

    cmd = [
        "ffplay",
        "-f", "lavfi",
        "-i", patterns[pattern_name],
        "-left", str(monitor["left"]),
        "-top", str(monitor["top"]),
        "-fs",
        "-noborder",
        "-alwaysontop"
    ]

    current_process = subprocess.Popen(cmd)

    return redirect(url_for("index"))


@app.route("/stop", methods=["POST"])
def stop():
    stop_current()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)