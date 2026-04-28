# 🎛 Broadcast Test Pattern & Streaming Controller

A self-contained **Flask-based broadcast control system** for generating test patterns, streaming via RTSP/RTMP/SRT/UDP, recording to file, and outputting to local monitors.

It integrates:
- 🎥 FFmpeg (encoding & streaming)
- 📡 MediaMTX (RTSP/RTMP/SRT server)
- 🖥 FFplay (monitor output)
- 🎮 Bitfocus Companion (Stream Deck control)
- 🌐 Flask web UI (control surface)

---

# 🚀 Features

## 🎥 Test Pattern Generator
- SMPTE Bars
- HD Bars
- Test Grid / Test Grid 2
- RGB test pattern
- Zone Plate
- Black screen

---

## 📡 Output Modes

### Stream Outputs
- RTSP → MediaMTX
- RTMP → MediaMTX
- SRT → MediaMTX
- UDP → Local network stream

### Local Outputs
- 📁 File recording (MP4)
- 🖥 Monitor fullscreen output (FFplay)

---

## 🧠 Stream Control System
- Named streams (user-defined IDs)
- Multiple concurrent streams
- Start / Stop per stream
- Live status monitoring

---

## 🖥 Multi-Monitor Support
- Detects all system monitors
- Select target display for fullscreen preview

---

## 🎮 Companion Integration (Stream Deck)
Full HTTP API for control:

- Start stream
- Stop stream
- Query status

---

# 🧱 System Architecture

```
Browser UI (Flask frontend)
        ↓
Flask API (control layer)
        ↓
FFmpeg / FFplay (media engine)
        ↓
MediaMTX (stream server)
```

---

# 📦 Requirements

## 🧩 System Tools

### FFmpeg
Ensure installed and in PATH:
```bash
ffmpeg -version
```

### MediaMTX
Download:
https://github.com/bluenviron/mediamtx

Place in project root:
```
mediamtx.exe
```

---

## 🐍 Python Dependencies

```bash
pip install flask screeninfo
```

---

# ▶ Running the Application

```bash
python app.py
```

Then open:

```
http://127.0.0.1:5000
```

---

# 🎛 Using the Interface

## 1. Select Test Pattern
Click any preview tile.

## 2. Set Stream Name
This becomes:
- RTSP path
- RTMP key
- SRT stream ID
- File name (for recordings)

## 3. Choose Output Type
- RTSP / RTMP / SRT / UDP
- File recording
- Monitor output

## 4. Select Monitor (if needed)

## 5. Press GO
Starts the stream immediately.

---

# 📡 Streaming Endpoints

## RTSP
```
rtsp://127.0.0.1:8554/<stream_name>
```

## RTMP
```
rtmp://127.0.0.1:1935/live/<stream_name>
```

## SRT
```
srt://127.0.0.1:8890?streamid=<stream_name>
```

---

# 📁 File Output

Generates:

```
<stream_name>.mp4
```

---

# 🖥 Monitor Mode

- Launches FFplay fullscreen
- Uses selected monitor index
- Real-time test pattern preview

---

# 🎮 Bitfocus Companion Integration

## Start Stream

**POST**
```
/api/stream/start
```

```json
{
  "pattern": "Test Grid",
  "protocol": "rtsp",
  "mode": "stream",
  "name": "CAM_A"
}
```

---

## Stop Stream

**POST**
```
/api/stream/stop
```

```json
{
  "id": "CAM_A"
}
```

---

## Status

**GET**
```
/api/status
```

Returns all active streams.

---

# 📊 Status Dashboard

Shows:
- Stream name
- Pattern type
- Output mode
- Running state (live tracking)

Auto-refreshes every second.

---

# ⚙️ Configuration Notes

## MediaMTX must be running
The app auto-starts it if available:

```
mediamtx.exe
```

---

## Ports Used

| Service | Port |
|--------|------|
| Flask UI | 5000 |
| RTSP | 8554 |
| RTMP | 1935 |
| SRT | 8890 |

---

# 🧠 Behaviour Notes

- Streams persist until manually stopped
- File mode records for 60 seconds
- Monitor mode opens fullscreen FFplay window
- Multiple streams can run at once

---

# 🔥 Future Enhancements

- 🎛 OBS-style scene switching
- 📡 Multi-output per stream (RTSP + file + SRT)
- 📊 Live bitrate / FPS monitoring
- 🌐 Browser-based video preview (no VLC needed)
- 🎮 Native Stream Deck plugin (Companion module)
- 💾 Save/load broadcast profiles
- 🎬 Transition effects between patterns

---

# 🧑‍💻 Purpose

Built as a **broadcast test and simulation engine** for:

- Video signal testing
- Streaming pipeline validation
- Multi-output encoding workflows
- Live production experimentation
- Broadcast engineering learning tool

---

# 📄 License
 ©️ 2026 itsmejoshleach