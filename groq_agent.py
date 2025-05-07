from groq import Groq
from config import GROQ_API_KEY, MODEL
from utils import detect_intent  # custom helper to parse commands

client = Groq(api_key=GROQ_API_KEY)

# System prompt to enhance behavior
messages = [
    {
        "role": "system",
        "content": (
            "You are JARVIS, an intelligent and loyal voice assistant built by Keyur. "
            "You assist with tasks, answer questions, open applications, search things online, and keep responses friendly and helpful. "
            "Always respond like a real assistant would, and ask for clarification if unsure."
            "short and sweet responses are preferred."
        )
    }
]

# Optional: limit number of messages (to avoid hitting token limits)
MAX_MESSAGES = 15

def trim_messages():
    if len(messages) > MAX_MESSAGES:
        del messages[1:3]  # keep system + most recent turns

def chat_with_groq(user_input):
    # Optional: handle voice commands (open app, time, etc.)
    intent_result = detect_intent(user_input)
    if intent_result:
        return intent_result

    # Add user message to chat
    messages.append({"role": "user", "content": user_input})

    # Trim if too long
    trim_messages()

    # Groq API call
    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
    )

    # Response from Groq
    reply = response.choices[0].message.content
    messages.append({"role": "assistant", "content": reply})
    return reply
