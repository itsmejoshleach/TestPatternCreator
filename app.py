from flask import Flask, render_template, request, jsonify, Response
import subprocess
import uuid
import os
from screeninfo import get_monitors

app = Flask(__name__)

# ---------------- MEDIA SERVER ----------------
mediamtx_process = None
MEDIAMTX_PATH = os.path.join(os.getcwd(), "mediamtx.exe")

def ensure_mediamtx_running():
    global mediamtx_process

    if mediamtx_process and mediamtx_process.poll() is None:
        return

    if not os.path.exists(MEDIAMTX_PATH):
        print("MediaMTX not found")
        return

    mediamtx_process = subprocess.Popen(
        [MEDIAMTX_PATH],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

# ---------------- STATE ----------------
streams = {}

# ---------------- PATTERNS ----------------
patterns = {
    "SMPTE Bars": "smptebars=size=1280x720:rate=30",
    "HD Bars": "smptehdbars=size=1920x1080:rate=30",
    "Test Grid": "testsrc=size=1280x720:rate=30",
    "Test Grid 2": "testsrc2=size=1280x720:rate=30",
    "RGB Pattern": "rgbtestsrc=size=1280x720:rate=30",
    "Black": "color=c=black:size=1280x720:rate=30",
    "Zone Plate": "zoneplate=size=1280x720:rate=30"
}

# ---------------- MONITORS ----------------
def list_monitors():
    mons = get_monitors()
    return [
        {
            "id": i,
            "name": f"Monitor {i} ({m.width}x{m.height})"
        }
        for i, m in enumerate(mons)
    ]

# ---------------- OUTPUT ----------------
def build_output(protocol, name):
    if protocol == "rtsp":
        return f"rtsp://127.0.0.1:8554/{name}"
    if protocol == "rtmp":
        return f"rtmp://127.0.0.1:1935/live/{name}"
    if protocol == "srt":
        return f"srt://127.0.0.1:8890?streamid={name}"
    if protocol == "udp":
        return f"udp://127.0.0.1:1234"

# ---------------- STREAM CMD ----------------
def ffmpeg_stream(pattern, output, protocol):

    base = [
        "ffmpeg",
        "-re",
        "-f", "lavfi",
        "-i", pattern,
        "-c:v", "libx264",
        "-preset", "veryfast",
        "-pix_fmt", "yuv420p",
        "-g", "50"
    ]

    if protocol == "rtsp":
        return base + ["-f", "rtsp", "-rtsp_transport", "tcp", output]

    if protocol == "rtmp":
        return base + ["-f", "flv", output]

    return base + ["-f", "mpegts", output]

# ---------------- START ----------------
@app.route("/start_stream", methods=["POST"])
def start_stream():

    ensure_mediamtx_running()

    data = request.json

    pattern = patterns[data["pattern"]]
    mode = data.get("mode", "stream")
    protocol = data.get("protocol")
    name = data.get("name") or str(uuid.uuid4())[:8]
    monitor_id = int(data.get("monitor", 0))

    proc = None
    output = None

    # ---------------- STREAM ----------------
    if mode == "stream":

        output = build_output(protocol, name)
        cmd = ffmpeg_stream(pattern, output, protocol)

        proc = subprocess.Popen(cmd)

    # ---------------- FILE ----------------
    elif mode == "file":

        filename = f"{name}.mp4"

        cmd = [
            "ffmpeg", "-y",
            "-f", "lavfi",
            "-i", pattern,
            "-t", "60",
            "-c:v", "libx264",
            filename
        ]

        proc = subprocess.Popen(cmd)
        output = filename

    # ---------------- MONITOR ----------------
    elif mode == "monitor":

        cmd = [
            "ffplay",
            "-f", "lavfi",
            "-i", pattern,
            "-fs"
        ]

        proc = subprocess.Popen(cmd)
        output = f"monitor:{monitor_id}"

    streams[name] = {
        "id": name,
        "pattern": data["pattern"],
        "protocol": protocol,
        "mode": mode,
        "output": output,
        "proc": proc
    }

    return jsonify({"id": name})

# ---------------- STOP ----------------
@app.route("/stop_stream/<sid>", methods=["POST"])
def stop_stream(sid):
    if sid in streams:
        p = streams[sid]["proc"]
        if p and p.poll() is None:
            p.terminate()
        del streams[sid]
    return "ok"

# ---------------- STATUS ----------------
@app.route("/status")
def status():
    out = []

    for s in streams.values():
        p = s["proc"]
        out.append({
            "id": s["id"],
            "pattern": s["pattern"],
            "protocol": s["protocol"],
            "mode": s["mode"],
            "output": s["output"],
            "running": p and p.poll() is None
        })

    return jsonify(out)

# ---------------- PREVIEW ----------------
@app.route("/preview/<name>")
def preview(name):
    cmd = [
        "ffmpeg",
        "-f", "lavfi",
        "-i", patterns[name],
        "-vframes", "1",
        "-f", "image2pipe",
        "-vcodec", "png",
        "-"
    ]

    img = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    return Response(img.stdout, mimetype="image/png")

# ---------------- UI ----------------
@app.route("/")
def index():
    return render_template(
        "index.html",
        patterns=patterns,
        monitors=list_monitors()
    )

# ---------------- BOOT ----------------
if __name__ == "__main__":
    ensure_mediamtx_running()
    app.run("127.0.0.1", 5000, debug=False)