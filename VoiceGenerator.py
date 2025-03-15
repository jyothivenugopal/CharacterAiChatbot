import pygame
import tempfile
import openai
import os
from dotenv import load_dotenv
from elevenlabs import ElevenLabs
import pygame
import tempfile
# Load API keys from .env
load_dotenv()
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")

# Initialize ElevenLabs API
client = ElevenLabs(api_key=ELEVENLABS_API_KEY)

'''
voices = client.voices.get_all()
print("Available Voices in Your ElevenLabs Account:")
for voice in voices.voices:
    print(f"Name: {voice.name}, ID: {voice.voice_id}")
'''

def text_to_speech(text, character):
    """Convert text to speech and play it using pygame."""
    
    # Character voice mapping
    CHARACTER_VOICES = {
        "Hermione": "waSmfs0VjwHaxkhRMjri",
        "Harry Potter": "Ud50RLDjIU7P7LVTC1g1",
        "Dumbledore": "QqyAnOAKA5mWlxhTfyY0",
        "Snape": "sCqEoAEqMRJWE9vLi3Er",
        "Hagrid": "2TLdy7jSivWMD7r8sV5C"
    }

    voice_id = CHARACTER_VOICES.get(character, "waSmfs0VjwHaxkhRMjri")  # Default to Hermione

    # Generate speech
    audio_stream = client.text_to_speech.convert(
        text=text,
        voice_id=voice_id
    )

    # Save audio to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio:
        for chunk in audio_stream:
            temp_audio.write(chunk)
        temp_audio_path = temp_audio.name

    # Initialize only pygame's mixer (Avoids crash)
    pygame.mixer.init()
    pygame.mixer.music.load(temp_audio_path)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        continue  # Keep script running until the audio finishes playing

    # Cleanup temp file
    os.remove(temp_audio_path)