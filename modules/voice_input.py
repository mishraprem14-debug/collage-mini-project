"""
Module 1: User Voice Input Module
Handles microphone initialization, ambient noise calibration, and capturing raw voice input.
"""
import speech_recognition as sr
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("VoiceInputModule")

class VoiceInputModule:
    def __init__(self, energy_threshold: int = 300, dynamic_energy: bool = True):
        self.recognizer = sr.Recognizer()
        self.recognizer.energy_threshold = energy_threshold
        self.recognizer.dynamic_energy_threshold = dynamic_energy
        self.recognizer.pause_threshold = 0.8
        self.microphone = None
        self._init_microphone()

    def _init_microphone(self):
        try:
            self.microphone = sr.Microphone()
            logger.info("Microphone initialized successfully.")
        except Exception as e:
            logger.warning(f"Microphone initialization failed: {e}. Fallback to text input.")
            self.microphone = None

    def calibrate_noise(self, duration: float = 1.0) -> bool:
        """Calibrates recognizer energy threshold according to ambient background noise."""
        if not self.microphone:
            return False
        try:
            with self.microphone as source:
                logger.info("Calibrating for ambient noise...")
                self.recognizer.adjust_for_ambient_noise(source, duration=duration)
                logger.info(f"Calibration complete. Energy threshold: {self.recognizer.energy_threshold}")
                return True
        except Exception as e:
            logger.error(f"Error during noise calibration: {e}")
            return False

    def listen_raw(self, timeout: int = 5, phrase_time_limit: int = 10):
        """
        Listens to user's voice from microphone.
        Returns sr.AudioData or None if timeout/error occurs.
        """
        if not self.microphone:
            logger.warning("No microphone detected.")
            return None
        try:
            with self.microphone as source:
                logger.info("Listening for voice input...")
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
                return audio
        except sr.WaitTimeoutError:
            logger.info("Listening timed out while waiting for phrase.")
            return None
        except Exception as e:
            logger.error(f"Error while listening: {e}")
            return None

    def is_microphone_available(self) -> bool:
        return self.microphone is not None
