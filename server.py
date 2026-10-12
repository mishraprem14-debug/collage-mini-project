"""
FastAPI Server & API Bridge
Connects the Python AI Assistant modules with the Futuristic Web HUD UI.
"""
import os
import asyncio
from pathlib import Path
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import logging

from config import STATIC_DIR, SCREENSHOTS_DIR, SERVER_HOST, SERVER_PORT
from modules.voice_input import VoiceInputModule
from modules.speech_to_text import SpeechToTextModule
from modules.command_processor import CommandProcessingModule
from modules.text_to_speech import TextToSpeechModule
from modules.system_telemetry import SystemTelemetryModule

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("JarvisServer")

app = FastAPI(title="AI Voice Assistant JARVIS HUD", version="2.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Assistant Modules
voice_input_mod = VoiceInputModule()
stt_mod = SpeechToTextModule(recognizer=voice_input_mod.recognizer)
cmd_processor = CommandProcessingModule()
tts_mod = TextToSpeechModule()
telemetry_mod = SystemTelemetryModule()

# Request Models
class CommandRequest(BaseModel):
    text: str
    speak_response: bool = True

class SpeakRequest(BaseModel):
    text: str

class VolumeRequest(BaseModel):
    level: int

# REST Endpoints
@app.get("/api/system-stats")
def get_system_stats():
    """Returns current real-time system diagnostic metrics."""
    return telemetry_mod.get_system_stats()

@app.post("/api/command")
def execute_command(req: CommandRequest):
    """Processes user text/speech command and triggers tasks."""
    result = cmd_processor.process_command(req.text)
    speech_text = result.get("speech", "")
    if req.speak_response and speech_text:
        tts_mod.speak(speech_text)
    return result

@app.post("/api/listen")
def trigger_microphone_listen(timeout: int = 5):
    """
    Triggers backend microphone listening, transcribes speech, and runs command.
    Useful for offline/desktop audio input.
    """
    if not voice_input_mod.is_microphone_available():
        return {
            "success": False,
            "error": "No physical microphone detected. Please use the browser mic or type in commands."
        }

    audio = voice_input_mod.listen_raw(timeout=timeout, phrase_time_limit=8)
    if not audio:
        return {
            "success": False,
            "error": "Microphone timed out waiting for voice input."
        }

    transcription = stt_mod.convert_audio_to_text(audio)
    if not transcription.get("success"):
        return {
            "success": False,
            "error": transcription.get("error", "Could not transcribe audio.")
        }

    spoken_text = transcription.get("text", "")
    result = cmd_processor.process_command(spoken_text)
    result["transcription"] = spoken_text
    
    if result.get("speech"):
        tts_mod.speak(result["speech"])

    return result

@app.post("/api/speak")
def speak_text(req: SpeakRequest):
    """Speaks given text aloud using pyttsx3."""
    tts_mod.speak(req.text)
    return {"success": True, "message": "Spoken"}

@app.post("/api/screenshot")
def take_screenshot():
    """Captures desktop screenshot."""
    res = telemetry_mod.capture_screenshot()
    return res

@app.post("/api/volume")
def adjust_volume(req: VolumeRequest):
    """Sets master volume level."""
    success = telemetry_mod.set_volume(req.level)
    return {"success": success, "level": req.level}

@app.get("/api/voices")
def list_voices():
    """Returns list of installed system voices."""
    return tts_mod.get_available_voices()

# WebSocket for real-time telemetry streaming
@app.websocket("/ws")
async def websocket_telemetry(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            stats = telemetry_mod.get_system_stats()
            await websocket.send_json({"type": "telemetry", "data": stats})
            await asyncio.sleep(1.5)
    except WebSocketDisconnect:
        logger.info("WebSocket client disconnected.")
    except Exception as e:
        logger.error(f"WebSocket error: {e}")

# Mount static files and screenshot directories
app.mount("/screenshots", StaticFiles(directory=str(SCREENSHOTS_DIR)), name="screenshots")
app.mount("/", StaticFiles(directory=str(STATIC_DIR), html=True), name="static")

def start_server():
    uvicorn.run(app, host=SERVER_HOST, port=SERVER_PORT, log_level="info")

if __name__ == "__main__":
    start_server()
