"""
Module 2: Speech-to-Text (STT) Module
Converts raw audio speech signals into structured text strings.
"""
import speech_recognition as sr
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("STTModule")

class SpeechToTextModule:
    def __init__(self, recognizer: sr.Recognizer = None, language: str = "en-US"):
        self.recognizer = recognizer or sr.Recognizer()
        self.language = language

    def convert_audio_to_text(self, audio_data: sr.AudioData) -> dict:
        """
        Converts SpeechRecognition AudioData into text string.
        Returns:
            dict: {
                "success": bool,
                "text": str,
                "error": str or None,
                "engine": str
            }
        """
        if not audio_data:
            return {
                "success": False,
                "text": "",
                "error": "No audio data provided or audio timed out.",
                "engine": "none"
            }

        # 1. Primary: Google Speech Recognition (high accuracy)
        try:
            logger.info("Transcribing audio using Google Speech Recognition...")
            text = self.recognizer.recognize_google(audio_data, language=self.language)
            text = text.strip()
            logger.info(f"Recognized speech: '{text}'")
            return {
                "success": True,
                "text": text,
                "error": None,
                "engine": "google"
            }
        except sr.UnknownValueError:
            logger.warning("Google Speech Recognition could not understand audio.")
            # Try offline Sphinx fallback if available
            return self._fallback_sphinx(audio_data, "Could not understand audio. Please speak clearly.")
        except sr.RequestError as e:
            logger.warning(f"Google Speech Recognition service error: {e}. Trying offline fallback...")
            return self._fallback_sphinx(audio_data, f"Network request error: {e}")
        except Exception as e:
            logger.error(f"Unexpected STT error: {e}")
            return {
                "success": False,
                "text": "",
                "error": str(e),
                "engine": "unknown"
            }

    def _fallback_sphinx(self, audio_data: sr.AudioData, original_error: str) -> dict:
        """Attempts offline pocketsphinx recognition if Google STT fails."""
        try:
            text = self.recognizer.recognize_sphinx(audio_data)
            text = text.strip()
            if text:
                logger.info(f"Sphinx recognized speech (offline): '{text}'")
                return {
                    "success": True,
                    "text": text,
                    "error": None,
                    "engine": "sphinx_offline"
                }
        except Exception as e:
            logger.debug(f"Sphinx offline fallback not available or failed: {e}")

        return {
            "success": False,
            "text": "",
            "error": original_error,
            "engine": "failed"
        }
