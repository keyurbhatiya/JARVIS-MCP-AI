import asyncio
import os
from edge_tts import Communicate
import pygame

from config import VOICE

AUDIO_FILE = "output.mp3"

async def speak(text):
    # Generate speech
    communicate = Communicate(text, VOICE)
    await communicate.save(AUDIO_FILE)

    # Initialize and play using pygame
    pygame.mixer.init()
    pygame.mixer.music.load(AUDIO_FILE)
    pygame.mixer.music.play()

    # Wait until playback is done
    while pygame.mixer.music.get_busy():
        await asyncio.sleep(0.1)

    # Properly unload the file and then remove it
    pygame.mixer.music.unload()
    pygame.mixer.quit()

    try:
        os.remove(AUDIO_FILE)
    except PermissionError:
        print("Warning: Couldn't delete audio file. It may still be in use.")
