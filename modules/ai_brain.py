"""
AI Brain Module
Handles Knowledge Retrieval, Wikipedia Summaries, Weather Forecasts, Jokes, Math, and Conversational AI.
"""
import re
import math
import random
import requests
import logging
import pyjokes
import wikipedia
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("AIBrain")

# Check if Google Generative AI is available
GEMINI_KEY = os.environ.get("GEMINI_API_KEY", "")
gemini_model = None
if GEMINI_KEY:
    try:
        import google.generativeai as genai
        genai.configure(api_key=GEMINI_KEY)
        gemini_model = genai.GenerativeModel("gemini-1.5-flash")
        logger.info("Gemini AI integration enabled.")
    except Exception as e:
        logger.warning(f"Gemini AI setup failed: {e}")

class AIBrainModule:
    def __init__(self):
        self.quotes = [
            "Sometimes you gotta run before you can walk. — Tony Stark",
            "The best way to predict the future is to invent it. — Alan Kay",
            "The only limit to our realization of tomorrow will be our doubts of today. — Franklin D. Roosevelt",
            "Do what you can, with what you have, where you are. — Theodore Roosevelt",
            "Simplicity is the soul of efficiency. — Austin Freeman",
            "I am JARVIS. Always at your service, sir.",
            "Stay hungry, stay foolish. — Steve Jobs"
        ]

    def ask_wikipedia(self, query: str) -> dict:
        """Searches Wikipedia and extracts a concise summary."""
        try:
            clean_query = query.replace("wikipedia", "").replace("who is", "").replace("what is", "").replace("tell me about", "").strip()
            if not clean_query:
                clean_query = "Artificial Intelligence"
            
            logger.info(f"Querying Wikipedia for: {clean_query}")
            # Try Wikipedia library
            try:
                summary = wikipedia.summary(clean_query, sentences=2)
                page = wikipedia.page(clean_query)
                return {
                    "success": True,
                    "title": page.title,
                    "summary": summary,
                    "url": page.url
                }
            except Exception:
                # Direct REST API fallback
                url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{requests.utils.quote(clean_query)}"
                resp = requests.get(url, timeout=5, headers={"User-Agent": "JarvisVoiceAssistant/2.0"})
                if resp.status_code == 200:
                    data = resp.json()
                    return {
                        "success": True,
                        "title": data.get("title", clean_query),
                        "summary": data.get("extract", "No extract found."),
                        "url": data.get("content_urls", {}).get("desktop", {}).get("page", "")
                    }
        except Exception as e:
            logger.error(f"Wikipedia lookup error: {e}")

        return {
            "success": False,
            "title": query,
            "summary": f"I couldn't find a detailed summary for '{query}' on Wikipedia.",
            "url": f"https://www.google.com/search?q={query}"
        }

    def get_weather(self, city: str = "") -> dict:
        """Fetches live weather info using Open-Meteo or wttr.in without requiring API keys."""
        try:
            city_param = city.strip() if city else ""
            # Use wttr.in JSON API for convenient city parsing
            target_url = f"https://wttr.in/{requests.utils.quote(city_param)}?format=j1" if city_param else "https://wttr.in?format=j1"
            resp = requests.get(target_url, timeout=6, headers={"User-Agent": "curl/7.68.0"})
            if resp.status_code == 200:
                data = resp.json()
                current = data.get("current_condition", [{}])[0]
                area = data.get("nearest_area", [{}])[0]
                
                location_name = area.get("areaName", [{}])[0].get("value", city_param or "Current Location")
                country = area.get("country", [{}])[0].get("value", "")
                temp_c = current.get("temp_C", "N/A")
                temp_f = current.get("temp_F", "N/A")
                condition = current.get("weatherDesc", [{}])[0].get("value", "Clear")
                humidity = current.get("humidity", "N/A")
                wind_speed = current.get("windspeedKmph", "N/A")

                summary_text = f"The weather in {location_name} is currently {condition} at {temp_c}°C ({temp_f}°F), with {humidity}% humidity and winds at {wind_speed} km/h."
                return {
                    "success": True,
                    "location": f"{location_name}, {country}".strip(", "),
                    "temp_c": temp_c,
                    "temp_f": temp_f,
                    "condition": condition,
                    "humidity": humidity,
                    "wind_speed": wind_speed,
                    "summary": summary_text
                }
        except Exception as e:
            logger.error(f"Weather fetch failed: {e}")

        return {
            "success": False,
            "summary": "I'm having trouble reaching the weather satellite right now. Please check your internet connection."
        }

    def get_joke(self) -> str:
        """Returns a joke."""
        try:
            joke = pyjokes.get_joke()
            return joke
        except Exception:
            fallback_jokes = [
                "Why do programmers prefer dark mode? Because light attracts bugs!",
                "There are 10 types of people in the world: those who understand binary, and those who don't.",
                "Why was the JavaScript developer sad? Because they didn't Node how to Express themselves.",
                "Artificial intelligence is no match for natural stupidity.",
                "Why did the computer keep freezing? It left its Windows open!"
            ]
            return random.choice(fallback_jokes)

    def get_quote(self) -> str:
        """Returns an inspiring quote."""
        return random.choice(self.quotes)

    def calculate_math(self, expression: str) -> dict:
        """Safely evaluates basic arithmetic expressions."""
        clean = expression.lower()
        clean = clean.replace("what is", "").replace("calculate", "").replace("solve", "").strip()
        clean = clean.replace("times", "*").replace("multiplied by", "*").replace("into", "*")
        clean = clean.replace("divided by", "/").replace("over", "/")
        clean = clean.replace("plus", "+").replace("add", "+")
        clean = clean.replace("minus", "-").replace("subtract", "-")
        clean = clean.replace("power of", "**").replace("^", "**")

        # Keep only safe math characters
        allowed_chars = set("0123456789+-*/(). %")
        filtered = "".join(ch for ch in clean if ch in allowed_chars).strip()

        if not filtered:
            return {"success": False, "error": "Invalid math expression."}

        try:
            # Safe evaluation with restricted globals/locals
            safe_dict = {
                "sqrt": math.sqrt,
                "pow": math.pow,
                "pi": math.pi,
                "sin": math.sin,
                "cos": math.cos,
                "tan": math.tan
            }
            result = eval(filtered, {"__builtins__": None}, safe_dict)
            if isinstance(result, float) and result.is_integer():
                result = int(result)
            elif isinstance(result, float):
                result = round(result, 4)
            return {
                "success": True,
                "expression": filtered,
                "result": str(result),
                "speech": f"The answer is {result}"
            }
        except Exception as e:
            return {"success": False, "error": f"Could not calculate: {e}"}

    def chat_ai(self, user_prompt: str) -> str:
        """Generates conversational response using Gemini or built-in offline NLP."""
        global gemini_model
        if gemini_model:
            try:
                response = gemini_model.generate_content(
                    f"You are JARVIS, an advanced AI Voice Assistant. Respond concisely in 1 to 3 natural, polite sentences. User says: {user_prompt}"
                )
                if response and response.text:
                    return response.text.strip()
            except Exception as e:
                logger.warning(f"Gemini API query failed: {e}")

        # Intelligent offline conversational rules
        lower = user_prompt.lower()
        if any(w in lower for w in ["who are you", "what are you", "your name"]):
            return "I am JARVIS, your intelligent AI-based voice assistant, designed to control your computer and assist your workflow."
        if any(w in lower for w in ["who created you", "who made you", "who is your creator"]):
            return "I was built by talented engineers using Python, Speech Recognition, and modern intelligent automation modules."
        if any(w in lower for w in ["how are you", "how are you doing"]):
            return "All diagnostic systems are operating at peak efficiency, sir. How may I be of assistance today?"
        if any(w in lower for w in ["thank you", "thanks"]):
            return "You are most welcome, sir. It is my pleasure to serve."
        if any(w in lower for w in ["good morning"]):
            return "Good morning, sir. All core protocols are online and ready for your command."
        if any(w in lower for w in ["good night"]):
            return "Good night, sir. Power conservation standby initiated. Have a restful sleep."
        if any(w in lower for w in ["meaning of life", "secret of life"]):
            return "According to the Hitchhiker's Guide to the Galaxy, the answer is 42. But in practice, it is whatever gives your journey purpose."
        if any(w in lower for w in ["flip a coin", "toss a coin"]):
            res = random.choice(["Heads", "Tails"])
            return f"The coin landed on {res}!"
        if any(w in lower for w in ["roll a dice", "roll dice"]):
            res = random.randint(1, 6)
            return f"You rolled a {res}!"

        return f"I have processed your query: '{user_prompt}'. I am continuously expanding my neural capabilities to serve you better."
