#!/usr/bin/env python3
"""
Community Captioner - Local Server with Python Speech Recognition
Run this script to start the captioner on localhost.
Speech recognition runs in the background, independent of browser focus.
"""

import http.server
import socketserver
import webbrowser
import os
import json
import threading
import time
import socket
from urllib.parse import urlparse

def get_local_ip():
    """Get the local IP address for LAN access"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"

# Try to import speech recognition
try:
    import speech_recognition as sr
    SPEECH_AVAILABLE = True
except ImportError:
    SPEECH_AVAILABLE = False
    print("⚠️  SpeechRecognition not installed. Run: pip3 install SpeechRecognition pyaudio")

PORT = 8080

# Change to the directory where this script is located
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Store caption data in memory
caption_data = {
    "caption": "",
    "settings": {
        "fontSize": 48,
        "fontFamily": "Open Sans",
        "textColor": "#FFFFFF",
        "backgroundColor": "#000000",
        "backgroundOpacity": 70,
        "textAlign": "center",
        "position": "bottom",
        "maxLines": 2,
        "showBackground": True,
        "textShadow": True,
        "language": "en-US"
    },
    "listening": False,
    "available_mics": [],
    "selected_mic": None,
    "mode": "python"  # "python" or "browser"
}

# Speech recognition thread control
speech_thread = None
stop_listening = threading.Event()

def limit_to_lines(text, max_lines=2):
    """Limit text to approximate line count based on character length"""
    chars_per_line = 60
    max_chars = max_lines * chars_per_line

    if len(text) <= max_chars:
        return text

    # Trim from the beginning, try to break at word boundary
    trimmed = text[-max_chars:]
    first_space = trimmed.find(' ')
    return trimmed[first_space + 1:] if first_space > 0 else trimmed

def speech_recognition_loop(mic_index=None):
    """Background thread for continuous speech recognition"""
    global caption_data

    if not SPEECH_AVAILABLE:
        print("❌ Speech recognition not available")
        return

    recognizer = sr.Recognizer()
    recognizer.energy_threshold = 150  # Lower threshold for better sensitivity
    recognizer.dynamic_energy_threshold = True
    recognizer.pause_threshold = 0.6  # Shorter pause before considering speech ended

    print(f"🎤 Starting speech recognition (mic_index={mic_index})...")
    caption_data["listening"] = True
    full_caption = ""

    try:
        # Create microphone instance
        if mic_index is not None:
            mic = sr.Microphone(device_index=mic_index)
        else:
            mic = sr.Microphone()

        # Adjust for ambient noise first
        print("   Adjusting for ambient noise...")
        with mic as source:
            recognizer.adjust_for_ambient_noise(source, duration=1)
        print("   Ready! Listening...")

        while not stop_listening.is_set():
            try:
                with mic as source:
                    audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)

                try:
                    # Use Google's free speech recognition
                    text = recognizer.recognize_google(audio)
                    if text:
                        full_caption = (full_caption + " " + text).strip()
                        max_lines = caption_data["settings"].get("maxLines", 2)
                        caption_data["caption"] = limit_to_lines(full_caption, max_lines)
                        print(f"   📝 {text}")
                except sr.UnknownValueError:
                    # Speech was unintelligible
                    pass
                except sr.RequestError as e:
                    print(f"   ⚠️ Recognition service error: {e}")

            except sr.WaitTimeoutError:
                # No speech detected within timeout, continue listening
                pass
            except Exception as e:
                if not stop_listening.is_set():
                    print(f"   ⚠️ Listen error: {e}")
                    time.sleep(0.5)  # Brief pause before retry

    except Exception as e:
        print(f"❌ Error initializing microphone: {e}")

    caption_data["listening"] = False
    print("🛑 Stopped listening")

def get_available_microphones():
    """Get list of available microphones"""
    if not SPEECH_AVAILABLE:
        return []

    try:
        mics = []
        for i, name in enumerate(sr.Microphone.list_microphone_names()):
            mics.append({"index": i, "name": name})
        return mics
    except Exception as e:
        print(f"Error getting microphones: {e}")
        return []

class CaptionHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)

        # API endpoint to get current caption
        if parsed.path == '/api/caption':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
            self.end_headers()
            self.wfile.write(json.dumps(caption_data).encode())
            return

        # API endpoint to get available microphones
        if parsed.path == '/api/microphones':
            mics = get_available_microphones()
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({"microphones": mics, "speech_available": SPEECH_AVAILABLE}).encode())
            return

        # Serve static files normally
        super().do_GET()

    def do_POST(self):
        global speech_thread, stop_listening
        parsed = urlparse(self.path)

        # API endpoint to update caption
        if parsed.path == '/api/caption':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)

            try:
                data = json.loads(post_data.decode())
                if 'caption' in data:
                    caption_data['caption'] = data['caption']
                if 'settings' in data:
                    caption_data['settings'].update(data['settings'])

                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "ok"}).encode())
            except json.JSONDecodeError:
                self.send_response(400)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"error": "Invalid JSON"}).encode())
            return

        # API endpoint to start Python speech recognition
        if parsed.path == '/api/start':
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length) if content_length > 0 else b'{}'

            try:
                data = json.loads(post_data.decode()) if post_data else {}
                mic_index = data.get('mic_index')

                # Stop existing thread if running
                if speech_thread and speech_thread.is_alive():
                    stop_listening.set()
                    speech_thread.join(timeout=2)

                # Start new thread
                stop_listening.clear()
                caption_data["caption"] = ""
                caption_data["mode"] = "python"
                speech_thread = threading.Thread(target=speech_recognition_loop, args=(mic_index,), daemon=True)
                speech_thread.start()

                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "started"}).encode())
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode())
            return

        # API endpoint to stop Python speech recognition
        if parsed.path == '/api/stop':
            stop_listening.set()
            if speech_thread and speech_thread.is_alive():
                speech_thread.join(timeout=2)
            caption_data["listening"] = False

            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "stopped"}).encode())
            return

        # API endpoint to clear captions
        if parsed.path == '/api/clear':
            caption_data["caption"] = ""

            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "cleared"}).encode())
            return

        self.send_response(404)
        self.end_headers()

    def do_OPTIONS(self):
        # Handle CORS preflight
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def log_message(self, format, *args):
        # Only log non-API requests to reduce noise
        try:
            if args and '/api/' not in str(args[0]):
                super().log_message(format, *args)
        except:
            super().log_message(format, *args)

# Initialize microphone list
caption_data["available_mics"] = get_available_microphones()

LOCAL_IP = get_local_ip()

print(f"""
╔═══════════════════════════════════════════════════════════════════╗
║              🎤 COMMUNITY CAPTIONER SERVER 🎤                      ║
╠═══════════════════════════════════════════════════════════════════╣
║                                                                   ║
║  LOCAL ACCESS:                                                    ║
║    Control Panel:  http://localhost:{PORT}                         ║
║    Overlay URL:    http://localhost:{PORT}?overlay=true            ║
║                                                                   ║
║  NETWORK ACCESS (for other machines):                             ║
║    Control Panel:  http://{LOCAL_IP}:{PORT}                         ║
║    Overlay URL:    http://{LOCAL_IP}:{PORT}?overlay=true            ║
║                                                                   ║
║  ➤ Use the Network Overlay URL in OBS on another machine         ║
║  ➤ Set Browser Source dimensions to 1920 x 1080                  ║
║                                                                   ║
║  Python Speech Recognition: {"✅ Available" if SPEECH_AVAILABLE else "❌ Not Available"}               ║
║                                                                   ║
║  Press Ctrl+C to stop the server                                  ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝
""")

# Open the control panel in default browser
webbrowser.open(f'http://localhost:{PORT}')

class ReusableTCPServer(socketserver.TCPServer):
    allow_reuse_address = True

with ReusableTCPServer(("", PORT), CaptionHandler) as httpd:
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        stop_listening.set()
        print("\n\nServer stopped. Goodbye!")
