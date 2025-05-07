import asyncio
from speech_input import get_voice_input
from voice_output import speak
from groq_agent import chat_with_groq
from command_handler import handle_command

print("JARVIS is now running...")

while True:
    voice = get_voice_input().lower()
    if voice:
        command_response = handle_command(voice)
        if command_response:
            asyncio.run(speak(command_response))
        else:
            ai_reply = chat_with_groq(voice)
            print("JARVIS:", ai_reply)
            asyncio.run(speak(ai_reply))
