# 🎤 Community Captioner

**Free, open-source live captions for OBS and streaming.**

A browser-based tool that generates real-time captions from audio input and displays them as an overlay in OBS or other streaming software.

## Quick Start

### 1. Download & Extract
Download the latest release and extract the zip file.

### 2. Run the Server

**Mac/Linux:**
```bash
cd community-captioner
python3 start-server.py
```

**Windows:**
```bash
cd community-captioner
python start-server.py
```

Your browser will automatically open the control panel.

### 3. Add to OBS
1. In OBS, add a **Browser Source**
2. Set URL to: `http://localhost:8080?overlay=true`
3. Set Width: **1920**, Height: **1080**
4. Click "Start Captioning" in the control panel

## Features

- **Real-time speech recognition** using Web Speech API
- **Customizable captions** - font size, colors, position, padding
- **Smart text limiting** - shows most recent text that fits
- **Multiple deployment options** - local, network, or cloud
- **Pop-out mode** - keeps microphone active when switching apps
- **External audio support** - works with mixers, capture cards, USB interfaces

## Requirements

- Python 3.8+
- Chrome or Edge browser
- Microphone or audio input device

## Files

- `index.html` - Control panel and overlay
- `overlay.html` - Standalone overlay for OBS
- `landing.html` - Download/instructions page (for cloud deployment)
- `start-server.py` - Local server
- `cloud-server.py` - Cloud relay server (for remote access)

## License

This work is licensed under a [Creative Commons Attribution-ShareAlike 4.0 International License](https://creativecommons.org/licenses/by-sa/4.0/).

## Credits

A community AI project from [Brookline Interactive Group](https://brooklineinteractive.org)

Designed and developed by [Stephen Walter](https://weirdmachine.org)

---

Made with ❤️ for community media centers everywhere.
