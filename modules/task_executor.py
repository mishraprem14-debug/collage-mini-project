"""
Module 4: Task Execution Module
Executes system automations, launches applications, handles web browsing, media playback, and hardware controls.
"""
import os
import subprocess
import webbrowser
import datetime
import logging
from config import APP_PATHS, WEBSITES
from modules.system_telemetry import SystemTelemetryModule
from modules.ai_brain import AIBrainModule

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("TaskExecutor")

# Note: pywhatkit is lazily imported inside play_youtube to ensure instantaneous startup


def open_url_in_browser(url: str):
    """Guarantees browser opens and navigates to URL on Windows."""
    logger.info(f"Navigating to browser URL: {url}")
    try:
        # Windows native start command brings browser directly to foreground
        os.system(f'start "" "{url}"')
    except Exception as e:
        logger.warning(f"OS start failed: {e}")
    try:
        webbrowser.open_new_tab(url)
    except Exception as e:
        logger.warning(f"Webbrowser open failed: {e}")

class TaskExecutionModule:
    def __init__(self):
        self.telemetry = SystemTelemetryModule()
        self.brain = AIBrainModule()

    def open_application(self, app_name: str) -> dict:
        """Launches a desktop application."""
        clean_name = app_name.lower().strip()
        cmd = APP_PATHS.get(clean_name)

        if not cmd:
            # Check for partial match
            for k, v in APP_PATHS.items():
                if k in clean_name or clean_name in k:
                    cmd = v
                    clean_name = k
                    break

        if cmd:
            try:
                logger.info(f"Launching application command: {cmd}")
                if cmd.startswith("start "):
                    os.system(cmd)
                else:
                    subprocess.Popen(cmd, shell=True)
                msg = f"Opening {clean_name.capitalize()} for you, sir."
                return {"success": True, "action": "open_app", "speech": msg, "display": msg}
            except Exception as e:
                err = f"Failed to launch {clean_name}: {e}"
                logger.error(err)
                return {"success": False, "action": "open_app", "speech": err, "display": err}
        else:
            # Try to launch directly by name
            try:
                subprocess.Popen(clean_name, shell=True)
                msg = f"Attempting to launch {clean_name}."
                return {"success": True, "action": "open_app", "speech": msg, "display": msg}
            except Exception:
                msg = f"I could not locate application '{app_name}' on this system."
                return {"success": False, "action": "open_app", "speech": msg, "display": msg}

    def close_application(self, app_name: str) -> dict:
        """Closes a running application process."""
        clean_name = app_name.lower().strip()
        proc_name = clean_name
        if not proc_name.endswith(".exe"):
            # Check map
            mapped = APP_PATHS.get(clean_name)
            if mapped and mapped.endswith(".exe"):
                proc_name = mapped
            else:
                proc_name = f"{clean_name}.exe"

        try:
            os.system(f"taskkill /f /im {proc_name} >nul 2>&1")
            msg = f"Closed {clean_name.capitalize()}."
            return {"success": True, "action": "close_app", "speech": msg, "display": msg}
        except Exception as e:
            msg = f"Could not close {clean_name}: {e}"
            return {"success": False, "action": "close_app", "speech": msg, "display": msg}

    def open_website(self, site_name: str) -> dict:
        """Opens and navigates to requested website."""
        from config import WEBSITES
        clean_site = site_name.lower().strip()
        url = WEBSITES.get(clean_site)

        if not url:
            for k, v in WEBSITES.items():
                if k == clean_site or k in clean_site.split():
                    url = v
                    clean_site = k
                    break

        if not url:
            for k, v in WEBSITES.items():
                if k in clean_site:
                    url = v
                    clean_site = k
                    break

        if not url:
            if "." in clean_site:
                url = f"https://{clean_site}" if not clean_site.startswith("http") else clean_site
            else:
                url = f"https://www.google.com/search?q={requests_quote(clean_site)}"

        open_url_in_browser(url)
        display_name = clean_site.replace(".com", "").capitalize()
        msg = f"Opening {display_name} for you, sir."
        return {
            "success": True,
            "action": "open_website",
            "speech": msg,
            "display": f"Navigating to {display_name}...",
            "url": url,
            "platform": clean_site
        }

    def search_platform(self, platform: str, query: str) -> dict:
        """Searches on a specific platform like LinkedIn, Instagram, Twitter, GitHub, YouTube, etc."""
        from config import SEARCH_TEMPLATES
        clean_platform = platform.lower().strip()
        clean_query = query.strip()
        
        template = SEARCH_TEMPLATES.get(clean_platform)
        if not template:
            for k, v in SEARCH_TEMPLATES.items():
                if k in clean_platform:
                    template = v
                    clean_platform = k
                    break

        if template:
            target_url = template.format(query=requests_quote(clean_query))
        else:
            target_url = f"https://www.google.com/search?q={requests_quote(clean_platform + ' ' + clean_query)}"

        open_url_in_browser(target_url)
        disp_plat = clean_platform.capitalize()
        msg = f"Searching for '{clean_query}' on {disp_plat}, sir."
        return {
            "success": True,
            "action": "open_website",
            "speech": msg,
            "display": f"Searching '{clean_query}' on {disp_plat}...",
            "url": target_url,
            "platform": clean_platform,
            "query": clean_query
        }

    def search_google(self, query: str) -> dict:
        """Searches Google for query."""
        search_url = f"https://www.google.com/search?q={requests_quote(query)}"
        open_url_in_browser(search_url)
        msg = f"Searching Google for '{query}', sir."
        return {"success": True, "action": "google_search", "speech": msg, "display": msg, "url": search_url}

    def play_youtube(self, song_or_video: str) -> dict:
        """Plays video/song on YouTube using browser and pywhatkit."""
        clean_query = song_or_video.strip()
        yt_url = f"https://www.youtube.com/results?search_query={requests_quote(clean_query)}"
        open_url_in_browser(yt_url)

        # Optional pywhatkit autoplay
        try:
            import pywhatkit
            pywhatkit.playonyt(clean_query)
        except Exception:
            pass

        msg = f"Playing {clean_query} on YouTube, sir."
        return {"success": True, "action": "play_youtube", "speech": msg, "display": msg, "url": yt_url}

    def get_time_and_date(self, query_type: str = "both") -> dict:
        """Reports current time or date."""
        now = datetime.datetime.now()
        time_str = now.strftime("%I:%M %p")
        date_str = now.strftime("%A, %B %d, %Y")

        if query_type == "time":
            speech = f"Sir, the current time is {time_str}."
        elif query_type == "date":
            speech = f"Today is {date_str}."
        else:
            speech = f"Sir, it is currently {time_str} on {date_str}."

        return {
            "success": True,
            "action": "time_date",
            "speech": speech,
            "display": f"Time: {time_str} | Date: {date_str}",
            "time": time_str,
            "date": date_str
        }

    def execute_screenshot(self) -> dict:
        """Captures a screenshot."""
        res = self.telemetry.capture_screenshot()
        if res.get("success"):
            speech = "Screenshot captured and stored in your records, sir."
            return {
                "success": True,
                "action": "screenshot",
                "speech": speech,
                "display": speech,
                "url": res.get("url"),
                "filename": res.get("filename")
            }
        else:
            speech = f"Could not take screenshot: {res.get('error')}"
            return {"success": False, "action": "screenshot", "speech": speech, "display": speech}

    def execute_volume(self, action: str, level: int = None) -> dict:
        """Adjusts system volume."""
        if action == "mute":
            self.telemetry.mute_volume()
            speech = "Audio volume toggled."
            return {"success": True, "action": "volume", "speech": speech, "display": speech}
        elif action == "set" and level is not None:
            self.telemetry.set_volume(level)
            speech = f"Master volume set to {level} percent."
            return {"success": True, "action": "volume", "speech": speech, "display": speech}
        elif action == "up":
            curr = self.telemetry.get_current_volume()
            new_vol = min(100, curr + 15)
            self.telemetry.set_volume(new_vol)
            speech = f"Volume increased to {new_vol} percent."
            return {"success": True, "action": "volume", "speech": speech, "display": speech}
        elif action == "down":
            curr = self.telemetry.get_current_volume()
            new_vol = max(0, curr - 15)
            self.telemetry.set_volume(new_vol)
            speech = f"Volume decreased to {new_vol} percent."
            return {"success": True, "action": "volume", "speech": speech, "display": speech}

        return {"success": False, "action": "volume", "speech": "Volume command unhandled.", "display": "Volume command unhandled."}

    def execute_system_status(self) -> dict:
        """Returns comprehensive system telemetry."""
        stats = self.telemetry.get_system_stats()
        speech = f"CPU is at {stats['cpu_percent']} percent load. Memory utilization is at {stats['ram_percent']} percent. Battery is at {stats['battery']['percent']} percent."
        return {
            "success": True,
            "action": "system_status",
            "speech": speech,
            "display": f"CPU: {stats['cpu_percent']}% | RAM: {stats['ram_percent']}% | Battery: {stats['battery']['percent']}%",
            "stats": stats
        }

    def execute_lock(self) -> dict:
        """Locks the PC workstation."""
        self.telemetry.lock_workstation()
        speech = "Securing workstation and locking display, sir."
        return {"success": True, "action": "lock_screen", "speech": speech, "display": speech}


def requests_quote(text: str) -> str:
    import urllib.parse
    return urllib.parse.quote_plus(text)
