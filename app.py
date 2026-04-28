from flask import Flask, render_template, request, redirect, url_for, Response, send_file
import subprocess
from screeninfo import get_monitors

app = Flask(__name__)

# ----------------------------
# STATE (remembers selections)
# ----------------------------
selected_pattern = None
selected_output = "file"
current_process = None

# ----------------------------
# PATTERNS
# ----------------------------
patterns = {
    "SMPTE Bars": "smptebars=size=1280x720:rate=30",
    "HD Bars": "smptehdbars=size=1920x1080:rate=30",
    "Test Grid": "testsrc=size=1280x720:rate=30",
    "Test Grid 2": "testsrc2=size=1280x720:rate=30",
    "RGB Pattern": "rgbtestsrc=size=1280x720:rate=30",
    "Black": "color=c=black:size=1280x720:rate=30",
    "Zone Plate": "zoneplate=size=1280x720:rate=30"
}

# ----------------------------
# MONITORS
# ----------------------------
def get_monitor_list():
    return list(enumerate(get_monitors()))

# ----------------------------
# STOP OUTPUT
# ----------------------------
def stop_process():
    global current_process
    if current_process and current_process.poll() is None:
        current_process.terminate()
        current_process = None

# ----------------------------
# PREVIEW IMAGE
# ----------------------------
@app.route("/preview/<name>")
def preview(name):
    if name not in patterns:
        return "", 404

    cmd = [
        "ffmpeg",
        "-f", "lavfi",
        "-i", patterns[name],
        "-vframes", "1",
        "-f", "image2pipe",
        "-vcodec", "png",
        "-"
    ]

    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    return Response(result.stdout, mimetype="image/png")

# ----------------------------
# DOWNLOAD RENDER
# ----------------------------
@app.route("/download/<pattern>")
def download(pattern):
    if pattern not in patterns:
        return "Invalid pattern", 404

    filename = f"{pattern.replace(' ', '_')}.mp4"

    subprocess.run([
        "ffmpeg",
        "-f", "lavfi",
        "-i", patterns[pattern],
        "-t", "10",
        filename
    ])

    return send_file(filename, as_attachment=True)

# ----------------------------
# MAIN UI
# ----------------------------
@app.route("/", methods=["GET", "POST"])
def index():
    global selected_pattern, selected_output, current_process

    monitors = get_monitor_list()

    if request.method == "POST":
        selected_pattern = request.form.get("pattern", selected_pattern)
        selected_output = request.form.get("output", selected_output)

        if selected_pattern:
            stop_process()

            # FILE DOWNLOAD MODE
            if selected_output == "download":
                return redirect(url_for("download", pattern=selected_pattern))

            # MONITOR OUTPUT MODE
            if selected_output.startswith("monitor_"):
                idx = int(selected_output.split("_")[1])
                m = monitors[idx][1]

                current_process = subprocess.Popen([
                    "ffplay",
                    "-f", "lavfi",
                    "-i", patterns[selected_pattern],
                    "-left", str(m.x),
                    "-top", str(m.y),
                    "-fs",
                    "-noborder",
                    "-alwaysontop",
                    "-loglevel", "quiet"
                ])

        return redirect(url_for("index"))

    return render_template(
        "index.html",
        patterns=patterns,
        monitors=monitors,
        selected_pattern=selected_pattern,
        selected_output=selected_output
    )

# ----------------------------
# STOP BUTTON
# ----------------------------
@app.route("/stop", methods=["POST"])
def stop():
    stop_process()
    return redirect(url_for("index"))

# ----------------------------
# RUN
# ----------------------------
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)