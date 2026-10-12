"""
Module 3: Command Processing Module (NLP & Intent Parser)
Analyzes user text/speech commands, extracts intents & parameters, and dispatches to Task Execution Module.
"""
import re
import logging
from config import WAKE_WORDS, APP_PATHS, WEBSITES
from modules.task_executor import TaskExecutionModule

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("CommandProcessor")

class CommandProcessingModule:
    def __init__(self):
        self.executor = TaskExecutionModule()

    def clean_command(self, raw_text: str) -> str:
        """Strips wake words, Hindi/English prefixes and action suffixes."""
        text = raw_text.lower().strip()
        for wake in WAKE_WORDS:
            if text.startswith(wake):
                text = text[len(wake):].strip()
            elif text.endswith(wake):
                text = text[:-len(wake)].strip()
            text = text.replace(f" {wake} ", " ")

        # Strip common polite & conversational prefixes
        prefixes = ["please ", "can you ", "could you ", "jarvis ", "hey ", "ok ", "bhai ", "bro ", "kripya "]
        for p in prefixes:
            if text.startswith(p):
                text = text[len(p):].strip()

        # Strip common Hindi/English action suffixes
        suffixes = [
            " open karo", " open kar do", " open kr do", " kholo", " khol do",
            " chalao", " chala do", " play karo", " search karo", " pe search karo"
        ]
        for s in suffixes:
            if text.endswith(s):
                text = text[:-len(s)].strip()

        return text.strip(" ?.,!/")

    def process_command(self, raw_text: str) -> dict:
        """
        Main NLP dispatcher. Classifies intent and runs corresponding task.
        Returns unified execution result dict.
        """
        if not raw_text or not raw_text.strip():
            return {
                "success": False,
                "intent": "empty",
                "speech": "I did not detect any command. How may I help you?",
                "display": "No command detected."
            }

        cmd = self.clean_command(raw_text)
        logger.info(f"Processing parsed command: '{cmd}'")

        # 1. Greetings
        if cmd in ["hi", "hello", "hey", "good morning", "good evening", "good afternoon"]:
            speech = "Greetings, sir! JARVIS systems are fully operational. What are your orders?"
            return {"success": True, "intent": "greeting", "speech": speech, "display": speech}

        # 2. Time & Date
        if any(w in cmd for w in ["what time", "current time", "tell me the time", "time now", "the time"]):
            res = self.executor.get_time_and_date(query_type="time")
            res["intent"] = "time"
            return res
        if any(w in cmd for w in ["what date", "today's date", "current date", "what is today", "what is the date", "today date", "tell me the date"]):
            res = self.executor.get_time_and_date(query_type="date")
            res["intent"] = "date"
            return res
        if "time and date" in cmd or "date and time" in cmd:
            res = self.executor.get_time_and_date(query_type="both")
            res["intent"] = "time_date"
            return res

        # 3. Screenshot
        if any(w in cmd for w in ["screenshot", "take a screenshot", "capture screen", "snapshot"]):
            res = self.executor.execute_screenshot()
            res["intent"] = "screenshot"
            return res

        # 4. System Status / Health
        if any(w in cmd for w in ["system status", "battery status", "cpu status", "ram status", "battery percentage", "system info", "device status"]):
            res = self.executor.execute_system_status()
            res["intent"] = "system_status"
            return res

        # 5. Volume Controls
        if "mute" in cmd or "unmute" in cmd:
            res = self.executor.execute_volume("mute")
            res["intent"] = "volume"
            return res
        if any(w in cmd for w in ["volume up", "increase volume", "raise volume", "louder"]):
            res = self.executor.execute_volume("up")
            res["intent"] = "volume"
            return res
        if any(w in cmd for w in ["volume down", "decrease volume", "lower volume", "quieter"]):
            res = self.executor.execute_volume("down")
            res["intent"] = "volume"
            return res
        vol_match = re.search(r"volume\s+(?:to\s+)?(\d+)", cmd)
        if vol_match:
            vol_val = int(vol_match.group(1))
            res = self.executor.execute_volume("set", vol_val)
            res["intent"] = "volume"
            return res

        # 6. Lock screen
        if any(w in cmd for w in ["lock screen", "lock computer", "lock pc", "lock workstation"]):
            res = self.executor.execute_lock()
            res["intent"] = "lock_screen"
            return res

        # 7. Close Application
        if cmd.startswith("close ") or cmd.startswith("terminate ") or cmd.startswith("exit "):
            app_to_close = cmd.replace("close", "").replace("terminate", "").replace("exit", "").strip()
            res = self.executor.close_application(app_to_close)
            res["intent"] = "close_app"
            return res

        # 8. Platform Search: e.g. "search python on linkedin" or "search elon musk on twitter"
        search_on_match = re.search(r"search\s+(?:for\s+)?(.+?)\s+(?:on|in|pe)\s+([a-zA-Z0-9]+)", cmd)
        if search_on_match:
            query_part = search_on_match.group(1).strip()
            platform_part = search_on_match.group(2).strip()
            res = self.executor.search_platform(platform_part, query_part)
            res["intent"] = "search_platform"
            return res

        # Platform-first search: e.g. "linkedin search machine learning", "amazon search headphones"
        for plat in ["youtube", "google", "linkedin", "linkdin", "instagram", "insta", "twitter", "x", "facebook", "fb", "github", "spotify", "amazon", "flipkart", "chatgpt", "reddit"]:
            if cmd.startswith(f"{plat} search ") or cmd.startswith(f"{plat} pe search "):
                query_part = cmd.replace(f"{plat} search", "").replace(f"{plat} pe search", "").strip()
                res = self.executor.search_platform(plat, query_part)
                res["intent"] = "search_platform"
                return res

        # Ask ChatGPT
        if cmd.startswith("ask chatgpt ") or cmd.startswith("chatgpt search ") or cmd.startswith("ask gpt "):
            q = cmd.replace("ask chatgpt", "").replace("chatgpt search", "").replace("ask gpt", "").strip()
            res = self.executor.search_platform("chatgpt", q)
            res["intent"] = "search_platform"
            return res

        # 9. Direct Open Website / Social Platforms (LinkedIn, Instagram, Twitter, WhatsApp, ChatGPT, etc.)
        for plat in WEBSITES.keys():
            if cmd == plat or cmd == f"open {plat}" or cmd == f"launch {plat}" or cmd == f"start {plat}" or cmd == f"goto {plat}" or cmd == f"go to {plat}":
                res = self.executor.open_website(plat)
                res["intent"] = "open_website"
                return res

        # 10. Open Application / Unknown Website
        if cmd.startswith("open ") or cmd.startswith("launch ") or cmd.startswith("start "):
            target = cmd.replace("open", "").replace("launch", "").replace("start", "").strip()
            if target in WEBSITES or target.endswith(".com") or target.endswith(".org") or target.endswith(".in") or target.endswith(".net") or target.endswith(".ai"):
                res = self.executor.open_website(target)
                res["intent"] = "open_website"
                return res
            # Launch desktop application
            res = self.executor.open_application(target)
            res["intent"] = "open_app"
            return res

        # 11. YouTube Media Playback
        if cmd.startswith("play ") or "on youtube" in cmd or "youtube" in cmd:
            search_query = cmd.replace("play", "").replace("on youtube", "").replace("youtube", "").strip()
            if not search_query:
                res = self.executor.open_website("youtube")
                res["intent"] = "open_website"
                return res
            res = self.executor.play_youtube(search_query)
            res["intent"] = "play_youtube"
            return res

        # 10. Wikipedia Summaries
        if cmd.startswith("wikipedia ") or "who is " in cmd or "what is " in cmd or "tell me about " in cmd:
            wiki_res = self.executor.brain.ask_wikipedia(cmd)
            speech = wiki_res.get("summary", "No details found on Wikipedia.")
            return {
                "success": wiki_res.get("success", False),
                "intent": "wikipedia",
                "speech": speech,
                "display": speech,
                "title": wiki_res.get("title", ""),
                "url": wiki_res.get("url", "")
            }

        # 11. Weather
        if "weather" in cmd or "temperature" in cmd:
            city = cmd.replace("weather", "").replace("temperature", "").replace("in", "").replace("at", "").replace("of", "").replace("what is the", "").strip()
            weather_res = self.executor.brain.get_weather(city)
            speech = weather_res.get("summary", "Could not fetch weather.")
            return {
                "success": weather_res.get("success", False),
                "intent": "weather",
                "speech": speech,
                "display": speech,
                "data": weather_res
            }

        # 12. Jokes
        if any(w in cmd for w in ["joke", "make me laugh", "tell a joke", "funny"]):
            joke = self.executor.brain.get_joke()
            return {"success": True, "intent": "joke", "speech": joke, "display": joke}

        # 13. Quotes
        if any(w in cmd for w in ["quote", "motivate me", "inspiration", "inspire me"]):
            quote = self.executor.brain.get_quote()
            return {"success": True, "intent": "quote", "speech": quote, "display": quote}

        # 14. Math calculations
        if any(w in cmd for w in ["calculate", "solve", "what is "]) and any(op in cmd for op in ["+", "-", "*", "/", "divided by", "times", "plus", "minus", "%", "sqrt", "^"]):
            math_res = self.executor.brain.calculate_math(cmd)
            if math_res.get("success"):
                return {
                    "success": True,
                    "intent": "math",
                    "speech": math_res.get("speech"),
                    "display": f"{math_res.get('expression')} = {math_res.get('result')}",
                    "result": math_res.get("result")
                }

        # 15. Google Search
        if cmd.startswith("search ") or cmd.startswith("google ") or "search for " in cmd:
            query = cmd.replace("search for", "").replace("search", "").replace("google", "").strip()
            res = self.executor.search_google(query)
            res["intent"] = "google_search"
            return res

        # 16. Fallback: Conversational AI
        chat_reply = self.executor.brain.chat_ai(raw_text)
        return {
            "success": True,
            "intent": "ai_chat",
            "speech": chat_reply,
            "display": chat_reply
        }
