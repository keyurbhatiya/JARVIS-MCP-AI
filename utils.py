import datetime
import webbrowser

def detect_intent(text):
    lower = text.lower()

    if "time" in lower:
        now = datetime.datetime.now().strftime("%I:%M %p")
        return f"The current time is {now}."

    elif "open youtube" in lower:
        webbrowser.open("https://youtube.com")
        return "Opening YouTube for you."

    elif "open google" in lower:
        webbrowser.open("https://google.com")
        return "Here is Google."

    elif "who are you" in lower:
        return "I am JARVIS, your intelligent assistant built with the MCP protocol and Groq AI."

    return None  # Not a known intent
