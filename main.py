"""
AI-Based Voice Assistant (JARVIS)
Main Entry Point
Supports both Futuristic Web HUD GUI Mode and Pure Terminal CLI Mode.
"""
import sys
import time
import webbrowser
import threading
import argparse
import uvicorn
from config import SERVER_HOST, SERVER_PORT, ASSISTANT_NAME, ASSISTANT_VERSION
from modules.voice_input import VoiceInputModule
from modules.speech_to_text import SpeechToTextModule
from modules.command_processor import CommandProcessingModule
from modules.text_to_speech import TextToSpeechModule

BANNER = rf"""
========================================================================
       __ ___     ____     _    __ _____ ____     ____   ____  
      / //   |   / __ \   | |  / //_  _// __ \   / __ \ / __ \ 
 __  / // /| |  / /_/ /   | | / /  / / / / / /  / / / // / / / 
/ /_/ // ___ | / _, _/    | |/ / _/ / / /_/ /  / /_/ // /_/ /  
\____//_/  |_|/_/ |_|     |___/ /___//_____/   \____/ \____/   
                                                               
                AI-BASED VOICE ASSISTANT v{ASSISTANT_VERSION}
                 Iron Man Cybernetic HUD Edition
========================================================================
"""

def run_server():
    from server import app
    uvicorn.run(app, host=SERVER_HOST, port=SERVER_PORT, log_level="warning")

def start_gui_mode():
    print(BANNER)
    print(f"[*] Starting {ASSISTANT_NAME} Server at http://{SERVER_HOST}:{SERVER_PORT}")
    print("[*] Launching Futuristic Holographic HUD Interface...")

    # Start server in thread
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()

    # Wait a moment for server to bind
    time.sleep(1.2)

    # Greet user via TTS in background
    tts = TextToSpeechModule()
    threading.Thread(target=lambda: tts.speak(f"{ASSISTANT_NAME} online. Systems fully operational. Welcome back, sir."), daemon=True).start()

    # Open Browser
    url = f"http://{SERVER_HOST}:{SERVER_PORT}"
    webbrowser.open(url)
    print(f"\n[+] {ASSISTANT_NAME} HUD is now active at: {url}")
    print("[+] Press Ctrl+C in this terminal to shut down.\n")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print(f"\n[*] Powering down {ASSISTANT_NAME}. Goodbye, sir.")
        sys.exit(0)

def start_cli_mode():
    print(BANNER)
    print(f"[*] {ASSISTANT_NAME} Terminal CLI Mode Initialized.")
    
    voice_input = VoiceInputModule()
    stt = SpeechToTextModule(recognizer=voice_input.recognizer)
    cmd_processor = CommandProcessingModule()
    tts = TextToSpeechModule()

    tts.speak(f"{ASSISTANT_NAME} initialized in terminal mode. How can I help you, sir?")

    print("\nSelect Input Mode:")
    print("1) Voice Mode (Speak into Microphone)")
    print("2) Text Mode (Type commands)")
    choice = input("Enter choice (1/2) [Default 1]: ").strip() or "1"

    while True:
        try:
            user_text = ""
            if choice == "1":
                print("\n[🎙️ Listening...] Speak your command (or type 'exit' to quit):")
                audio = voice_input.listen_raw(timeout=6, phrase_time_limit=8)
                if audio:
                    transcription = stt.convert_audio_to_text(audio)
                    if transcription["success"]:
                        user_text = transcription["text"]
                        print(f"[User Said]: {user_text}")
                    else:
                        print(f"[Notice]: {transcription['error']}")
                        continue
                else:
                    print("[Notice]: No audio detected. Retrying...")
                    continue
            else:
                user_text = input(f"\n[You] > ").strip()

            if not user_text:
                continue

            if user_text.lower() in ["exit", "quit", "stop", "shutdown"]:
                tts.speak(f"Shutting down {ASSISTANT_NAME}. Have a good day, sir.", block=True)
                print("[*] Goodbye!")
                break

            print("[⚡ Processing]...")
            result = cmd_processor.process_command(user_text)
            reply = result.get("speech", result.get("display", ""))
            print(f"[{ASSISTANT_NAME}]: {reply}")

            tts.speak(reply)

        except KeyboardInterrupt:
            print(f"\n[*] Exiting {ASSISTANT_NAME}.")
            break
        except Exception as e:
            print(f"[Error]: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AI-Based Voice Assistant (JARVIS)")
    parser.add_argument("--cli", action="store_true", help="Launch in pure terminal CLI mode")
    parser.add_argument("--gui", action="store_true", help="Launch with Futuristic Web HUD GUI (Default)")
    args = parser.parse_args()

    if args.cli:
        start_cli_mode()
    else:
        start_gui_mode()
