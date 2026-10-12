"""
System Telemetry and OS Automation Module
Provides real-time hardware telemetry (CPU, RAM, Battery) and Windows system controls (Volume, Brightness, Screenshot, Lock PC).
"""
import os
import time
import datetime
import platform
import ctypes
import logging
from pathlib import Path
import psutil
import pyautogui
from config import SCREENSHOTS_DIR

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("SystemTelemetry")

# Try to import pycaw for volume control
try:
    from comtypes import CLSCTX_ALL
    from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
    PYCAW_AVAILABLE = True
except Exception as e:
    logger.warning(f"Pycaw not fully available: {e}")
    PYCAW_AVAILABLE = False

# Try screen brightness control
try:
    import screen_brightness_control as sbc
    SBC_AVAILABLE = True
except Exception:
    SBC_AVAILABLE = False

class SystemTelemetryModule:
    def __init__(self):
        self.boot_time = datetime.datetime.fromtimestamp(psutil.boot_time())

    def get_system_stats(self) -> dict:
        """Returns hardware telemetry metrics."""
        cpu_percent = psutil.cpu_percent(interval=None)
        cpu_count = psutil.cpu_count(logical=True)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')

        # Battery
        battery = psutil.sensors_battery()
        battery_data = {
            "percent": battery.percent if battery else 100,
            "power_plugged": battery.power_plugged if battery else True,
            "has_battery": battery is not None
        }

        # Current Volume
        current_vol = self.get_current_volume()

        # Uptime
        uptime_seconds = int(time.time() - psutil.boot_time())
        hours, remainder = divmod(uptime_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        uptime_str = f"{hours}h {minutes}m {seconds}s"

        return {
            "cpu_percent": round(cpu_percent, 1),
            "cpu_count": cpu_count,
            "ram_percent": round(memory.percent, 1),
            "ram_used_gb": round(memory.used / (1024**3), 2),
            "ram_total_gb": round(memory.total / (1024**3), 2),
            "disk_percent": round(disk.percent, 1),
            "disk_free_gb": round(disk.free / (1024**3), 1),
            "battery": battery_data,
            "volume_percent": current_vol,
            "uptime": uptime_str,
            "os_name": f"{platform.system()} {platform.release()} ({platform.machine()})",
            "time_str": datetime.datetime.now().strftime("%I:%M:%S %p"),
            "date_str": datetime.datetime.now().strftime("%A, %B %d, %Y")
        }

    def get_current_volume(self) -> int:
        """Returns the master audio volume level (0-100)."""
        if not PYCAW_AVAILABLE:
            return 50
        try:
            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            volume = ctypes.cast(interface, ctypes.POINTER(IAudioEndpointVolume))
            current = volume.GetMasterVolumeLevelScalar()
            return int(round(current * 100))
        except Exception as e:
            logger.debug(f"Could not read volume: {e}")
            return 50

    def set_volume(self, level_percent: int) -> bool:
        """Sets the master audio volume (0 to 100)."""
        level_percent = max(0, min(100, level_percent))
        if PYCAW_AVAILABLE:
            try:
                devices = AudioUtilities.GetSpeakers()
                interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
                volume = ctypes.cast(interface, ctypes.POINTER(IAudioEndpointVolume))
                volume.SetMasterVolumeLevelScalar(level_percent / 100.0, None)
                return True
            except Exception as e:
                logger.error(f"Error setting volume with pycaw: {e}")

        # Fallback using pyautogui volume keys
        try:
            for _ in range(50):
                pyautogui.press('volumedown')
            steps = int(level_percent / 2)
            for _ in range(steps):
                pyautogui.press('volumeup')
            return True
        except Exception:
            return False

    def mute_volume(self) -> bool:
        """Mutes / unmutes the audio."""
        if PYCAW_AVAILABLE:
            try:
                devices = AudioUtilities.GetSpeakers()
                interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
                volume = ctypes.cast(interface, ctypes.POINTER(IAudioEndpointVolume))
                is_muted = volume.GetMute()
                volume.SetMute(not is_muted, None)
                return True
            except Exception:
                pass
        try:
            pyautogui.press('volumemute')
            return True
        except Exception:
            return False

    def capture_screenshot(self) -> dict:
        """Takes a full screen screenshot and returns details."""
        try:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"screenshot_{timestamp}.png"
            filepath = SCREENSHOTS_DIR / filename
            screenshot = pyautogui.screenshot()
            screenshot.save(filepath)
            logger.info(f"Screenshot saved to {filepath}")
            return {
                "success": True,
                "filename": filename,
                "filepath": str(filepath),
                "url": f"/screenshots/{filename}"
            }
        except Exception as e:
            logger.error(f"Failed to capture screenshot: {e}")
            return {"success": False, "error": str(e)}

    def lock_workstation(self) -> bool:
        """Locks the Windows computer."""
        try:
            ctypes.windll.user32.LockWorkStation()
            return True
        except Exception as e:
            logger.error(f"Failed to lock workstation: {e}")
            return False

    def minimize_all(self):
        """Minimizes all windows to show desktop."""
        try:
            pyautogui.hotkey('win', 'd')
            return True
        except Exception:
            return False
