# PROJECT REPORT: AI-BASED VOICE ASSISTANT (JARVIS)

---

## 1. Topic Name (Title)
**AI-Based Voice Assistant (JARVIS Ultra Edition)**

---

## 2. Basic Description
The **AI-Based Voice Assistant** is a desktop software application that allows users to seamlessly interact with a computer using natural voice commands. It captures acoustic voice input, converts speech into structured textual data, comprehends the user's intent through Natural Language Processing (NLP), and executes target tasks autonomously. 

These tasks include:
- Launching and terminating operating system applications (Notepad, Chrome, Calculator, VS Code, Terminal, etc.)
- Autonomous web browsing and search queries (Google, Wikipedia, GitHub)
- Automated multimedia playback on YouTube via `pywhatkit`
- Live reporting of time, date, and calendar information
- System diagnostics and hardware telemetry (real-time CPU utilization, RAM consumption, battery health, uptime)
- Operating system automation (volume control, screen capture/screenshots, locking workstation)
- Intelligent knowledge retrieval, live weather forecasts, mathematical calculations, and conversational responses.

To transform this into a cutting-edge showcase application, the system features a **Futuristic Iron Man Cybernetic HUD Interface** with an active HTML5 Canvas Arc Reactor, dynamic sound waveform visualization, and synthesized sci-fi audio effects.

---

## 3. Why Choose That Topic?
- **Artificial Intelligence & Automation**: To explore how speech recognition and NLP interact with system-level automation to improve human-computer interaction (HCI).
- **Practical Python Mastery**: To gain practical experience in multi-threading, asynchronous servers, socket programming, Windows API integration, and modular software design in Python.
- **Hands-on Audio Technologies**: To deeply understand digital signal capture, speech-to-text conversion (Google Speech Recognition / Sphinx), and text-to-speech synthesis (`pyttsx3`).
- **Accessibility & Convenience**: To build a hands-free utility that assists users, enhances multitasking, and offers accessible computer control for individuals with physical limitations.

---

## 4. System Architecture & Data Flow

```
+--------------------------------------------------------------------------+
|                           HUMAN VOICE INPUT                              |
+--------------------------------------------------------------------------+
                                    |
                                    v
+--------------------------------------------------------------------------+
|                  MODULE 1: USER VOICE INPUT MODULE                       |
|  - Microphone initialization via PyAudio / speech_recognition            |
|  - Ambient noise calibration (adjust_for_ambient_noise)                  |
|  - Energy threshold verification                                         |
+--------------------------------------------------------------------------+
                                    |  (AudioData stream)
                                    v
+--------------------------------------------------------------------------+
|                  MODULE 2: SPEECH-TO-TEXT (STT) MODULE                   |
|  - Google Speech Recognition API (Primary Cloud STT)                     |
|  - CMU PocketSphinx Engine (Offline Fallback)                            |
|  - Web Speech API integration in Frontend HUD                            |
+--------------------------------------------------------------------------+
                                    |  (Raw Transcribed Text)
                                    v
+--------------------------------------------------------------------------+
|               MODULE 3: COMMAND PROCESSING (NLP) MODULE                  |
|  - Wake word sanitization ("Jarvis", "Hey Jarvis")                       |
|  - Intent classification & regex parameter extraction                    |
|  - Task routing & error handling                                         |
+--------------------------------------------------------------------------+
             /                                             \
            /                                               \
           v                                                 v
+--------------------------------------+  +--------------------------------+
|  MODULE 4: TASK EXECUTION MODULE     |  |       AI BRAIN MODULE          |
|  - Launch/Close Apps                 |  |  - Wikipedia REST API          |
|  - YouTube Playback (pywhatkit)      |  |  - Live Weather (Open-Meteo)   |
|  - System Diagnostics (psutil)       |  |  - Safe Math Evaluator         |
|  - Screenshot (pyautogui)            |  |  - Programmer Jokes (pyjokes)  |
|  - Audio Volume (pycaw)              |  |  - Conversational NLP          |
+--------------------------------------+  +--------------------------------+
            \                                               /
             \                                             /
              v                                           v
+--------------------------------------------------------------------------+
|               MODULE 5: TEXT-TO-SPEECH (TTS) RESPONSE MODULE             |
|  - Speech synthesis via pyttsx3 (SAPI5 Windows backend)                  |
|  - Thread-safe non-blocking audio queue                                  |
|  - Real-time WebSocket update to Futuristic Web HUD                      |
+--------------------------------------------------------------------------+
```

---

## 5. Detailed Module Breakdown

### Module 1: User Voice Input Module (`modules/voice_input.py`)
- **Purpose**: Establishes connection to physical input hardware (microphone) and captures acoustic speech signals.
- **Key Classes/Methods**:
  - `VoiceInputModule`: Initializes `sr.Recognizer()` and `sr.Microphone()`.
  - `calibrate_noise()`: Reads background noise levels for 1 second and adjusts the recognizer's `energy_threshold` dynamically to prevent false triggers.
  - `listen_raw(timeout, phrase_time_limit)`: Listens for incoming speech with timeout boundaries.

### Module 2: Speech-to-Text Module (`modules/speech_to_text.py`)
- **Purpose**: Translates digital audio waveforms into normalized string representations.
- **Key Methods**:
  - `convert_audio_to_text(audio_data)`: Calls Google Speech Recognition API with `en-US` language model.
  - `_fallback_sphinx()`: Employs local CMU PocketSphinx if internet connectivity is interrupted.
  - Browser Web Speech API (`webkitSpeechRecognition`): Embedded into the HUD for zero-latency client-side transcription.

### Module 3: Command Processing Module (`modules/command_processor.py`)
- **Purpose**: Performs lexical cleaning and intent extraction.
- **Key Methods**:
  - `clean_command(raw_text)`: Eliminates wake phrases, filler tokens ("please", "could you"), and punctuation.
  - `process_command(cmd)`: Uses intent classification rules, regular expressions, and keyword matching to identify user requests.

### Module 4: Task Execution Module (`modules/task_executor.py`)
- **Purpose**: Carries out the required action within Windows and the web.
- **Supported Automations**:
  - `open_application()` / `close_application()`: Interacts with Windows process execution (`subprocess.Popen`, `taskkill`).
  - `play_youtube()`: Executes `pywhatkit.playonyt()` to launch and stream targeted songs and videos.
  - `execute_screenshot()`: Captures display via `pyautogui.screenshot()`, saves with unique timestamps, and exposes preview URLs.
  - `execute_volume()`: Adjusts system audio levels and mute states via `pycaw`.
  - `execute_lock()`: Secures the PC workstation using `ctypes.windll.user32.LockWorkStation()`.

### Module 5: Text-to-Speech Response Module (`modules/text_to_speech.py`)
- **Purpose**: Produces natural audible vocal feedback.
- **Key Methods**:
  - Implements a dedicated worker thread with `queue.Queue` to prevent Windows SAPI COM deadlocks and UI freezes.
  - Configurable speech rate (185 WPM) and voice gender switching (David / Zira).

---

## 6. Advanced "WOW" Features Added

1. **Futuristic Cybernetic HUD UI**:
   - High-tech Arc Reactor Canvas visualizer with rotating segmented arcs and dynamic audio frequency bars.
   - Glassmorphic panels, neon glows, and multiple themes (Arc Cyan, Mark 85 Crimson, Matrix Emerald, Neon Cyberpunk, Solar Gold).
2. **Procedural Web Audio Sound FX**:
   - Synthesizes wake sounds, confirmation chimes, and warnings using the browser's Web Audio API without needing external MP3 files.
3. **Live Hardware Telemetry Dashboard**:
   - Continuously monitors CPU utilization, RAM usage, battery percentage, power charging state, master volume, and system uptime.
4. **Direct Action Command Dock**:
   - Categorized buttons for quick one-click launching of apps, media, and system utilities.
5. **Interactive Neural History Stream**:
   - Glassmorphism terminal feed tracking every command and response with exportable history.

---

## 7. Technologies & Libraries Used

| Technology / Library | Purpose in Project |
|---|---|
| **Python 3.13** | Core programming language for all backend modules |
| **SpeechRecognition** | Capturing and transcribing microphone audio |
| **pyttsx3** | Offline Text-to-Speech audio synthesis |
| **pywhatkit** | YouTube search and automated music playback |
| **psutil** | Hardware telemetry (CPU, RAM, Battery, Uptime) |
| **pyautogui** | Screen capture, screenshots, and GUI hotkeys |
| **pycaw** | Windows Core Audio API volume control |
| **FastAPI & Uvicorn** | Asynchronous REST & WebSocket server connecting backend to UI |
| **HTML5 & CSS3** | Futuristic Cyberpunk Glassmorphic layout and design |
| **JavaScript (ES6+)** | Web Speech API, Canvas visualizer, and Web Audio SFX |

---

## 8. Viva Voce & Presentation Q&A

**Q1: How does ambient noise adjustment work in speech recognition?**
> **Answer**: Ambient noise adjustment (`adjust_for_ambient_noise`) records background sound for a short sample duration (e.g. 1 second) and calculates the root mean square (RMS) energy. The recognizer then sets its dynamic energy threshold slightly above this baseline, ensuring background sounds do not falsely trigger voice recording.

**Q2: What is the difference between offline and online speech recognition?**
> **Answer**: Online recognition (such as Google Speech API) sends audio packets to cloud neural models, offering higher vocabulary accuracy. Offline recognition (like PocketSphinx) uses local acoustic and phonetic models, which function without an internet connection with lower resource overhead.

**Q3: How does the system avoid blocking when speaking?**
> **Answer**: `TextToSpeechModule` utilizes a producer-consumer model with a thread-safe `queue.Queue` and a dedicated daemon background worker thread. When a command finishes, the speech text is enqueued, allowing the main program and web server to continue processing without UI stutter.

**Q4: How do the frontend and backend communicate?**
> **Answer**: Through a dual-channel architecture:
> 1. **REST API**: For sending commands (`POST /api/command`) and triggering actions.
> 2. **WebSockets (`/ws`)**: For streaming real-time hardware telemetry (CPU, RAM, Battery) every 1.5 seconds directly to the HUD.

---

## 9. Conclusion
The **JARVIS 2.0 Ultra Voice Assistant** demonstrates the practical combination of Speech Recognition, Natural Language Processing, Operating System automation, and modern web interfaces. By combining robust Python modular engineering with a futuristic HUD interface, the project exceeds standard academic requirements and provides a production-quality desktop assistant.
