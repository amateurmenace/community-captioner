# 🎤 Community Captioner

Free, browser-based live captions for community media and streaming.

## Quick Start

### Step 1: Start the Local Server

**On Mac/Linux:**
```bash
python3 start-server.py
```

**On Windows:**
```bash
python start-server.py
```

This will:
- Start a local web server on port 8080
- Automatically open the control panel in your browser

### Step 2: Set Up OBS

1. In OBS, click **+** under Sources → **Browser**
2. Set the URL to: `http://localhost:8080?overlay=true`
3. Set Width to **1920** and Height to **1080**
4. Click OK

### Step 3: Start Captioning

1. Select your audio input device (capture card, USB audio interface, etc.)
2. Customize the appearance as needed
3. Click **Start Captioning**
4. Watch live captions appear in OBS!

---

## Using External Audio Sources

Community Captioner works with any audio source your computer can detect:

### Blackmagic UltraStudio / DeckLink
1. Install Blackmagic Desktop Video drivers
2. The device will appear in the audio input dropdown
3. Select it and start captioning

### Capture Cards (Elgato, AVerMedia, etc.)
1. Most capture cards appear as audio input devices automatically
2. Select the capture card from the dropdown

### Mixers & Video Switchers
1. Connect the mixer/switcher audio output to a USB audio interface
2. Or use the headphone/monitor output if available
3. Select the audio interface from the dropdown

### Virtual Audio (Advanced)
- **Mac:** Use Loopback or BlackHole to route system audio
- **Windows:** Use VB-Audio Virtual Cable
- **Linux:** Use PulseAudio/PipeWire routing

---

## Customization Options

- **Font Size:** 24px to 96px
- **Font Family:** Multiple options available
- **Colors:** Full color picker for text and background
- **Position:** Top, middle, or bottom of screen
- **Alignment:** Left, center, or right
- **Background:** Toggle on/off, adjust opacity
- **Text Shadow:** Toggle for better readability

---

## Troubleshooting

### Captions not appearing in OBS?
- Make sure you're using `http://localhost:8080?overlay=true` (not a file:// URL)
- Ensure the server is running (you should see the terminal window)
- Try refreshing the browser source in OBS (right-click → Refresh)

### No audio devices showing?
- Allow microphone/audio permissions when prompted
- Check your system audio settings
- Restart the browser

### Speech recognition not working?
- Use Chrome or Edge (Firefox/Safari don't support Web Speech API)
- Check that the correct language is selected
- Speak clearly and at a moderate pace

---

## Technical Details

- Uses the Web Speech API for speech recognition
- Syncs between control panel and overlay via localStorage
- Requires Chrome or Edge browser
- Overlay is 1920×1080 with transparent background

---

## License

Free and open source for community media use.

Made with ❤️ for community media centers everywhere.
