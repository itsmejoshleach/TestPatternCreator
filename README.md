# 🎛 Test Pattern Controller

A Flask + FFmpeg broadcast-style control system for generating,
previewing, and routing test patterns across multiple monitors or file
export, running in a Chrome kiosk interface.

------------------------------------------------------------------------

## 🚀 Features

### 🎨 Test Pattern Generator

-   SMPTE Bars
-   HD Bars
-   RGB test pattern
-   Zone plate
-   Test grids
-   Black screen

------------------------------------------------------------------------

### 🖥 Output Routing

-   Auto-detects all connected monitors
-   Sends output to selected display
-   Exports video files via FFmpeg
-   Download render with Save As dialog (browser controlled)

------------------------------------------------------------------------

### 👁 Live Previews

-   FFmpeg-generated thumbnails
-   Click-to-select pattern interface
-   Instant visual feedback

------------------------------------------------------------------------

### 💾 State Memory

-   Remembers selected pattern
-   Remembers selected output
-   Restores state after refresh/restart

------------------------------------------------------------------------

### 🖥 Kiosk Mode UI

-   Fullscreen Chrome launch
-   No browser UI elements
-   Designed for broadcast / control room use

------------------------------------------------------------------------

## 🧱 Project Structure

    TestPatternController/
    │
    ├-- app.py              # Flask backend + FFmpeg logic
    ├-- main.py             # Chrome kiosk launcher
    │
    └-- templates/
        └-- index.html     # Control UI

------------------------------------------------------------------------

## ⚙️ Requirements

### Python dependencies

``` bash
pip install flask screeninfo
```

### System requirements

-   Python 3.10+
-   FFmpeg installed and available in PATH
-   Google Chrome (for kiosk mode)

------------------------------------------------------------------------

## ▶️ Running the app

### Start system

``` bash
python main.py
```

This will: - Start Flask backend - Launch Chrome in fullscreen kiosk
mode - Open control UI automatically

------------------------------------------------------------------------

## 🎛 How to use

### 1. Select a test pattern (top section)

Click any preview tile to select it.

### 2. Choose output (bottom bar)

-   Any detected monitor
-   Download render (Save As dialog)
-   File export (MP4 generation)

### 3. Press GO

Routes pattern to selected output or triggers file render/download

### 4. STOP

Immediately stops FFplay output

------------------------------------------------------------------------

## 🧠 Architecture

Flask UI → Pattern Selection → FFmpeg / FFplay → Monitor/File Output

------------------------------------------------------------------------

## 🎬 Output Modes

### Monitor Output

-   FFplay fullscreen
-   Borderless window
-   Per-monitor positioning

### File Export

-   FFmpeg MP4 render
-   Local save or download

### Download Mode

-   Server renders file
-   Browser prompts Save As

------------------------------------------------------------------------

## 🧪 FFmpeg Sources

-   smptebars
-   smptehdbars
-   testsrc
-   testsrc2
-   rgbtestsrc
-   zoneplate
-   color=black

------------------------------------------------------------------------

## 🧰 Future Upgrades

-   Program / Preview mode
-   Keyboard shortcuts
-   Monitor routing map
-   Waveform + vectorscope
-   Preset scenes
-   Stream Deck support

------------------------------------------------------------------------

## ⚠️ Notes

-   FFmpeg required in PATH
-   Chrome kiosk mode may need path adjustment
-   Windows-first design

------------------------------------------------------------------------

## 🧑‍💻 Purpose

Broadcast-style test signal generator for AV, broadcast, and
multi-display testing workflows.

©️ 2026 itsmejoshleach