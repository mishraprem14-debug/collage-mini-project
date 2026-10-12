"""
AI-Based Voice Assistant (JARVIS)
Configuration File
"""
import os
from pathlib import Path

# Base Paths
BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"
SCREENSHOTS_DIR = BASE_DIR / "screenshots"
SCREENSHOTS_DIR.mkdir(exist_ok=True)

# Assistant Identity
ASSISTANT_NAME = "JARVIS"
ASSISTANT_VERSION = "2.0 Ultra"
WAKE_WORDS = ["jarvis", "hey jarvis", "ok jarvis", "hello jarvis"]

# Text to Speech Configuration
TTS_RATE = 185          # Speed of speech (words per minute)
TTS_VOLUME = 1.0        # Volume (0.0 to 1.0)
TTS_VOICE_GENDER = "male" # 'male' or 'female'

# Server Configuration
SERVER_HOST = "127.0.0.1"
SERVER_PORT = 8000
DEBUG = False

# Application Quick-Launch Shortcuts for Windows
APP_PATHS = {
    "notepad": "notepad.exe",
    "calculator": "calc.exe",
    "calc": "calc.exe",
    "chrome": "chrome.exe",
    "google chrome": "chrome.exe",
    "vs code": "code",
    "visual studio code": "code",
    "code": "code",
    "file explorer": "explorer.exe",
    "explorer": "explorer.exe",
    "my computer": "explorer.exe",
    "cmd": "cmd.exe",
    "command prompt": "cmd.exe",
    "terminal": "wt.exe",
    "task manager": "taskmgr.exe",
    "paint": "mspaint.exe",
    "ms paint": "mspaint.exe",
    "settings": "start ms-settings:",
    "spotify": "spotify.exe",
    "camera": "start microsoft.windows.camera:",
}

# Quick Website Shortcuts & Web Applications
WEBSITES = {
    "youtube": "https://www.youtube.com",
    "yt": "https://www.youtube.com",
    "google": "https://www.google.com",
    "github": "https://www.github.com",
    "gmail": "https://mail.google.com",
    "mail": "https://mail.google.com",
    "whatsapp": "https://web.whatsapp.com",
    "wa": "https://web.whatsapp.com",
    "linkedin": "https://www.linkedin.com",
    "linkdin": "https://www.linkedin.com",
    "instagram": "https://www.instagram.com",
    "insta": "https://www.instagram.com",
    "twitter": "https://twitter.com",
    "x": "https://x.com",
    "facebook": "https://www.facebook.com",
    "fb": "https://www.facebook.com",
    "chatgpt": "https://chatgpt.com",
    "chat gpt": "https://chatgpt.com",
    "openai": "https://chatgpt.com",
    "gemini": "https://gemini.google.com",
    "claude": "https://claude.ai",
    "spotify": "https://open.spotify.com",
    "netflix": "https://www.netflix.com",
    "amazon": "https://www.amazon.in",
    "flipkart": "https://www.flipkart.com",
    "reddit": "https://www.reddit.com",
    "wikipedia": "https://www.wikipedia.org",
    "stackoverflow": "https://stackoverflow.com",
    "telegram": "https://web.telegram.org",
    "discord": "https://discord.com/app",
    "pinterest": "https://www.pinterest.com",
    "maps": "https://maps.google.com",
    "google maps": "https://maps.google.com",
}

# Platform Search URL Templates
SEARCH_TEMPLATES = {
    "youtube": "https://www.youtube.com/results?search_query={query}",
    "google": "https://www.google.com/search?q={query}",
    "linkedin": "https://www.linkedin.com/search/results/all/?keywords={query}",
    "linkdin": "https://www.linkedin.com/search/results/all/?keywords={query}",
    "instagram": "https://www.instagram.com/explore/tags/{query}/",
    "insta": "https://www.instagram.com/explore/tags/{query}/",
    "twitter": "https://twitter.com/search?q={query}",
    "x": "https://twitter.com/search?q={query}",
    "facebook": "https://www.facebook.com/search/top/?q={query}",
    "fb": "https://www.facebook.com/search/top/?q={query}",
    "github": "https://github.com/search?q={query}",
    "spotify": "https://open.spotify.com/search/{query}",
    "amazon": "https://www.amazon.in/s?k={query}",
    "flipkart": "https://www.flipkart.com/search?q={query}",
    "chatgpt": "https://chatgpt.com/?q={query}",
    "reddit": "https://www.reddit.com/search/?q={query}",
    "wikipedia": "https://en.wikipedia.org/wiki/Special:Search?search={query}",
    "maps": "https://www.google.com/maps/search/{query}",
}

