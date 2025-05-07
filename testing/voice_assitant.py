import asyncio
import platform
import speech_recognition as sr
import pyttsx3
from groq import Groq
import re
from collections import defaultdict
import time
# from mcproto.server import Serve
import testing.server as server
from mcproto.packets import PacketDirection, ChatMessagePacket

# Simulated config (replace with your actual GROQ_API_KEY)
GROQ_API_KEY = "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"
MODEL = "llama-3.3-70b-versatile"

# Initialize Groq client
client = Groq(api_key=GROQ_API_KEY)

# Initialize text-to-speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)

# In-memory cache for query-response pairs
interaction_cache = defaultdict(list)
# Feedback store for training
feedback_store = {}

# System prompt for JARVIS
messages = [
    {
        "role": "system",
        "content": (
            "You are JARVIS, an intelligent and loyal voice assistant built by Keyur. "
            "You assist with tasks, answer questions, open applications, search things online, and keep responses friendly and helpful. "
            "Use past interactions to provide faster and more accurate responses. "
            "If corrected, adapt responses based on user feedback. "
            "Always respond like a real assistant would, and ask for clarification if unsure."
        )
    }
]

MAX_MESSAGES = 15

def trim_messages():
    if len(messages) > MAX_MESSAGES:
        messages[1:3] = []  # Keep system + recent turns

def cache_response(query, response):
    interaction_cache[query.lower()].append({
        "response": response,
        "timestamp": time.time(),
        "usage_count": 1
    })

def get_cached_response(query):
    cached = interaction_cache.get(query.lower(), [])
    if cached:
        best_response = max(cached, key=lambda x: x["usage_count"] * 0.7 + x["timestamp"] * 0.3)
        best_response["usage_count"] += 1
        return best_response["response"]
    return None

def apply_feedback(query, feedback):
    if feedback:
        feedback_store[query.lower()] = feedback
        if query.lower() in interaction_cache:
            interaction_cache[query.lower()].append({
                "response": feedback,
                "timestamp": time.time(),
                "usage_count": 1
            })

def detect_intent(user_input):
    user_input = user_input.lower()
    if re.search(r'\bopen\b', user_input):
        return f"JARVIS: Simulating opening {user_input.split('open')[-1].strip()}"
    if re.search(r'\btime\b', user_input):
        return f"JARVIS: The current time is {__import__('datetime').datetime.now().strftime('%H:%M:%S')}"
    return None

async def chat_with_groq(user_input, ask_feedback=False):
    cached_response = get_cached_response(user_input)
    if cached_response:
        messages.append({"role": "user", "content": user_input})
        messages.append({"role": "assistant", "content": cached_response})
        return cached_response

    intent_result = detect_intent(user_input)
    if intent_result:
        messages.append({"role": "user", "content": user_input})
        messages.append({"role": "assistant", "content": intent_result})
        cache_response(user_input, intent_result)
        return intent_result

    if user_input.lower() in feedback_store:
        response = feedback_store[user_input.lower()]
        messages.append({"role": "user", "content": user_input})
        messages.append({"role": "assistant", "content": response})
        cache_response(user_input, response)
        return response

    messages.append({"role": "user", "content": user_input})
    trim_messages()

    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
    )

    reply = response.choices[0].message.content
    messages.append({"role": "assistant", "content": reply})
    cache_response(user_input, reply)

    if ask_feedback:
        feedback_prompt = "Was this response helpful? If not, please provide a better response or correction."
        messages.append({"role": "assistant", "content": feedback_prompt})
        return reply + "\n" + feedback_prompt

    return reply

# Real MCP server using mcproto
class MCPServer:
    def __init__(self, host='0.0.0.0', port=25565):
        self.server = server(host=host, port=port)
        self.server.packet_handler = self.handle_packet

    async def handle_packet(self, packet, client, server):
        if isinstance(packet, ChatMessagePacket) and packet.direction == PacketDirection.SERVERBOUND:
            player_name = client.username or "Unknown"
            message = packet.message
            print(f"Received from {player_name}: {message}")
            response = await chat_with_groq(message)
            print(f"Sending to {player_name}: {response}")
            # Send response back to all clients
            chat_packet = ChatMessagePacket(
                message=f"[JARVIS] {response}",
                direction=PacketDirection.CLIENTBOUND
            )
            await server.broadcast_packet(chat_packet)

    async def start(self):
        print(f"Starting MCP server on {self.server.host}:{self.server.port}")
        await self.server.start()

# Voice recognition
async def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source, timeout=5)
            text = recognizer.recognize_google(audio)
            print(f"Recognized: {text}")
            return text
        except sr.UnknownValueError:
            return "Could not understand audio"
        except sr.RequestError as e:
            return f"Speech recognition error: {e}"

async def main():
    # Start MCP server
    mcp_server = MCPServer()
    asyncio.create_task(mcp_server.start())

    feedback_mode = False
    last_feedback_time = time.time()

    while True:
        if time.time() - last_feedback_time > 300:
            feedback_mode = True
            last_feedback_time = time.time()

        voice_input = await recognize_speech()
        if voice_input and not voice_input.startswith("Could not") and not voice_input.startswith("Speech recognition"):
            if feedback_mode and voice_input.lower().startswith("no"):
                correction = voice_input[2:].strip() or "Please repeat the correct response."
                apply_feedback(messages[-2]["content"], correction)
                response = f"JARVIS: Thank you for the correction: {correction}"
                feedback_mode = False
            else:
                response = await chat_with_groq(voice_input, ask_feedback=feedback_mode)
                if not feedback_mode:
                    print(f"JARVIS: {response}")
                    engine.say(response)
                    engine.runAndWait()

        await asyncio.sleep(1.0)  # Prevent tight loop

if platform.system() == "Emscripten":
    asyncio.ensure_future(main())
else:
    if __name__ == "__main__":
        asyncio.run(main())