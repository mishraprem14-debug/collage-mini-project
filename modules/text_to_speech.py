"""
Module 5: Text-to-Speech (TTS) Response Module
Converts textual responses into natural voice audio using pyttsx3.
"""
import pyttsx3
import threading
import queue
import logging
from config import TTS_RATE, TTS_VOLUME, TTS_VOICE_GENDER

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("TTSModule")

class TextToSpeechModule:
    def __init__(self, rate: int = TTS_RATE, volume: float = TTS_VOLUME, gender: str = TTS_VOICE_GENDER):
        self.rate = rate
        self.volume = volume
        self.gender = gender
        self.is_speaking = False
        self._speech_queue = queue.Queue()
        self._worker_thread = None
        self._stop_event = threading.Event()
        self._start_worker()

    def _get_engine(self):
        """Creates a fresh pyttsx3 engine instance for thread-safe operations."""
        try:
            engine = pyttsx3.init()
            engine.setProperty('rate', self.rate)
            engine.setProperty('volume', self.volume)

            # Set voice
            voices = engine.getProperty('voices')
            if voices:
                selected_voice = voices[0] # Default
                for voice in voices:
                    name_lower = voice.name.lower()
                    if self.gender == "female" and ("zira" in name_lower or "female" in name_lower or "catherine" in name_lower):
                        selected_voice = voice
                        break
                    elif self.gender == "male" and ("david" in name_lower or "male" in name_lower or "george" in name_lower):
                        selected_voice = voice
                        break
                engine.setProperty('voice', selected_voice.id)
            return engine
        except Exception as e:
            logger.error(f"Error initializing TTS engine: {e}")
            return None

    def _start_worker(self):
        """Runs a background worker to serialize speech calls and avoid Windows SAPI COM deadlocks."""
        self._worker_thread = threading.Thread(target=self._process_queue, daemon=True)
        self._worker_thread.start()

    def _process_queue(self):
        try:
            import pythoncom
            pythoncom.CoInitialize()
        except Exception:
            pass

        while not self._stop_event.is_set():
            try:
                text = self._speech_queue.get(timeout=0.2)
                if text is None:
                    break
                self.is_speaking = True
                engine = self._get_engine()
                if engine:
                    try:
                        logger.info(f"Speaking: '{text}'")
                        engine.say(text)
                        engine.runAndWait()
                    except Exception as e:
                        logger.error(f"TTS Speech error: {e}")
                    finally:
                        try:
                            engine.stop()
                        except Exception:
                            pass
                self.is_speaking = False
                self._speech_queue.task_done()
            except queue.Empty:
                continue
            except Exception as e:
                logger.error(f"TTS Worker exception: {e}")
                self.is_speaking = False

    def speak(self, text: str, block: bool = False):
        """Queues text to be spoken. If block=True, waits until speech finishes."""
        if not text or not text.strip():
            return
        clean_text = text.strip()
        self._speech_queue.put(clean_text)
        if block:
            self._speech_queue.join()

    def stop(self):
        """Clears queue and stops speaking."""
        with self._speech_queue.mutex:
            self._speech_queue.queue.clear()
        self.is_speaking = False

    def set_properties(self, rate: int = None, volume: float = None, gender: str = None):
        if rate is not None:
            self.rate = max(100, min(300, rate))
        if volume is not None:
            self.volume = max(0.0, min(1.0, volume))
        if gender is not None:
            self.gender = gender

    def get_available_voices(self):
        """Returns list of installed SAPI voices."""
        voices_list = []
        try:
            temp_engine = pyttsx3.init()
            voices = temp_engine.getProperty('voices')
            for v in voices:
                voices_list.append({
                    "id": v.id,
                    "name": v.name,
                    "gender": "Female" if "female" in v.name.lower() or "zira" in v.name.lower() else "Male"
                })
        except Exception as e:
            logger.error(f"Failed to get voices: {e}")
        return voices_list
