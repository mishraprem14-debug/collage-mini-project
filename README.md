# ⚡ JARVIS 2.0 ULTRA — AI-Based Voice Assistant

An advanced, production-grade **AI-Based Voice Assistant** featuring an **Iron Man Holographic Cybernetic HUD Interface**, real-time audio waveform visualizer, comprehensive Windows automation, dual speech recognition engines, and smart conversational intelligence.

---

## 🌟 Key Highlights & "WOW" Features

1. **Futuristic Cybernetic Cockpit UI**:
   - **Interactive Arc Reactor Canvas**: Real-time rotating concentric rings, radar ticks, and particle wave oscillators reacting directly to speech frequencies and assistant states (`STANDBY`, `LISTENING`, `ANALYZING`, `RESPONDING`).
   - **Glassmorphism & Neon HUD Design**: Sleek dark-mode aesthetic with customizable themes (**Arc Cyan**, **Mark 85 Crimson**, **Matrix Emerald**, **Neon Cyberpunk**, **Solar Gold**).
   - **Integrated Sci-Fi Sound FX**: Dynamic procedural synthesizer generating high-tech audio chimes for wake words, confirmations, and actions via Web Audio API.

2. **Dual-Mode Voice Recognition**:
   - **Web Speech API**: Zero-latency voice recognition directly inside the browser HUD with live real-time speech transcription.
   - **Python Backend Microphone Engine**: High-fidelity microphone capture via `SpeechRecognition` with ambient noise calibration and Google Speech API / Sphinx fallback.

3. **Real-Time Hardware Telemetry (Live HUD Gauges)**:
   - Live CPU load percentage and core diagnostics.
   - Real-time RAM memory usage (GB utilized vs total).
   - Live Battery indicator (percentage & AC charging state).
   - Master volume slider & instant mute toggle.
   - System uptime counter and Windows OS information.

4. **Multi-Category Automation & Task Dock**:
   - **System Applications**: One-touch or voice launching for Notepad, Calculator, Chrome, VS Code, File Explorer, Terminal/CMD, Task Manager, MS Paint.
   - **System Controls**: Instant Screenshot capture (with modal preview and download), Workstation Screen Lock, Minimize All Windows, Audio Volume controls.
   - **Web & Media**: Search YouTube, play specific songs/videos directly (`pywhatkit.playonyt`), Google Search, Wikipedia summaries.
   - **Smart Utilities & AI Brain**: Wikipedia knowledge lookup, Live Weather forecasts, programmer jokes (`pyjokes`), inspiring quotes, safe arithmetic math solver, and conversational AI.

5. **Interactive Neural Activity Log**:
   - Searchable, persistent conversation stream with user transcripts, Jarvis responses, timestamps, and history export.

---

## 🏗️ Architectural Modules

This project strictly implements the 5 core modules from the syllabus/specification:

```
┌────────────────────────────────────────────────────────────────────────┐
│                          USER VOICE INPUT                              │
│       (Microphone capture, ambient noise calibration, AudioData)       │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                        SPEECH-TO-TEXT (STT)                            │
│           (Google Speech API, PocketSphinx fallback, NLP clean)        │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                     COMMAND PROCESSING (NLP)                           │
│        (Intent classification, keyword extraction, entity parser)      │
└───────────────────┬───────────────────────────────┬────────────────────┘
                    │                               │
                    ▼                               ▼
┌──────────────────────────────────────┐  ┌──────────────────────────────┐
│        TASK EXECUTION MODULE         │  │        AI BRAIN MODULE       │
│  (Apps, YouTube, System Diagnostics, │  │   (Wikipedia, Live Weather,  │
│   Volume, Screenshot, Lock PC)       │  │    Jokes, Math, Conversational)
└───────────────────┬──────────────────┘  └──────────────┬───────────────┘
                    │                                    │
                    └──────────────────┬─────────────────┘
                                       │
                                       ▼
┌────────────────────────────────────────────────────────────────────────┐
│                      TEXT-TO-SPEECH (TTS)                              │
│       (pyttsx3 speech synthesis, thread-safe queue, audio playback)    │
└────────────────────────────────────────────────────────────────────────┘
```

1. **User Voice Input Module** (`modules/voice_input.py`):
   - Initializes audio capture via `speech_recognition.Microphone()`.
   - Performs noise calibration (`adjust_for_ambient_noise`) to prevent false triggers in noisy environments.
2. **Speech-to-Text Module** (`modules/speech_to_text.py`):
   - Converts voice waveforms into text with Google Speech Recognition and Sphinx fallback.
3. **Command Processing Module** (`modules/command_processor.py`):
   - Cleans wake words ("Jarvis", "Hey Jarvis"), extracts intent parameters, and routes to appropriate executors.
4. **Task Execution Module** (`modules/task_executor.py`):
   - Interacts with Windows OS, sub-processes, browsers, and media players.
5. **Text-to-Speech Response Module** (`modules/text_to_speech.py`):
   - Thread-safe background worker powered by `pyttsx3` with adjustable voice pitch, rate, and gender.

---

## 🚀 Quick Start Guide

### 1. Requirements
Ensure Python 3.10+ is installed on your Windows PC.

### 2. Launch (One-Click)
Simply double-click:
```bash
launch.bat
```

### 3. Launch via Command Line
```powershell
# Run with Futuristic Web HUD GUI (Default):
python main.py

# Or run in Pure Terminal CLI Mode:
python main.py --cli
```

Jarvis will start the server at `http://127.0.0.1:8000` and automatically open your default browser to the Holographic Cockpit!

---

## 🎙️ Example Voice & Text Commands

| Category | Example Command | What JARVIS Does |
|---|---|---|
| **Greetings** | *"Hello Jarvis"*, *"Good morning"* | Greets you with status report |
| **Time & Date** | *"What time is it?"*, *"Tell me today's date"* | Reports time/date with voice and HUD display |
| **Applications** | *"Open Notepad"*, *"Launch Chrome"*, *"Open Calculator"* | Automatically launches the desktop app |
| **Closing Apps** | *"Close Notepad"*, *"Close Chrome"* | Terminates the application process |
| **Media & Music** | *"Play Shape of You on YouTube"*, *"Play Believer"* | Opens and autoplays YouTube music video |
| **Web Search** | *"Search for Artificial Intelligence on Google"* | Opens browser with targeted Google search |
| **Wikipedia** | *"Who is Elon Musk?"*, *"Wikipedia Quantum Computing"* | Summarizes 2-3 key sentences with link |
| **Weather** | *"What is the weather in New York?"*, *"Weather today"* | Live temperature, humidity & wind conditions |
| **Diagnostics** | *"System status"*, *"Battery percentage"* | Reads live CPU %, RAM %, and Battery % |
| **Screenshot** | *"Take a screenshot"* | Captures screen, shows modal preview & download |
| **Volume** | *"Volume up"*, *"Volume down"*, *"Set volume to 80"*, *"Mute"* | Adjusts Windows master audio level |
| **System Control**| *"Lock workstation"*, *"Lock screen"* | Secures and locks your Windows computer |
| **Jokes & Quotes**| *"Tell me a joke"*, *"Motivate me"* | Reads a programmer joke or motivational quote |
| **Math** | *"Calculate 45 times 8"*, *"What is 250 divided by 5"* | Evaluates math expressions instantly |
| **Conversational**| *"Who created you?"*, *"How are you doing?"* | Responds naturally with assistant persona |

---

## 📁 Project Directory Structure

```
MyJarvis/
├── config.py                 # Central configurations & app paths
├── main.py                   # Main entry point (GUI / CLI modes)
├── server.py                 # FastAPI backend with REST & WebSocket API
├── launch.bat                # One-click Windows batch launcher
├── requirements.txt          # Python dependencies
├── README.md                 # Project guide & instructions
├── PROJECT_REPORT.md         # Full project report for academic viva/submission
├── modules/
│   ├── __init__.py
│   ├── voice_input.py        # Module 1: Microphone & noise calibration
│   ├── speech_to_text.py     # Module 2: STT conversion engine
│   ├── command_processor.py  # Module 3: NLP intent classification
│   ├── task_executor.py      # Module 4: OS, browser & app automations
│   ├── text_to_speech.py     # Module 5: pyttsx3 speech synthesizer
│   ├── system_telemetry.py   # Live hardware stats & volume/screenshot
│   └── ai_brain.py           # Knowledge, Wikipedia, weather & Q&A
├── screenshots/              # Folder storing captured screenshots
└── static/
    ├── index.html            # Futuristic Cybernetic HUD
    ├── css/
    │   └── style.css         # Glassmorphism & Neon HUD styles
    └── js/
        ├── visualizer.js     # Canvas Arc Reactor & audio waveforms
        └── app.js            # Web Speech API & UI controller
```

---

## 🛠️ Technologies Used
- **Language**: Python 3.13 / 3.10+
- **Speech & Audio**: `SpeechRecognition`, `pyttsx3`, `PyAudio`
- **Automation & System**: `pywhatkit`, `pyautogui`, `psutil`, `pycaw`, `webbrowser`, `os`, `subprocess`
- **Backend & Network**: `FastAPI`, `Uvicorn`, `WebSockets`, `requests`
- **Frontend HUD**: Vanilla HTML5, CSS3 Glassmorphism, Vanilla JavaScript, HTML5 Canvas, Web Audio API, Web Speech API
