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

def text_to_speech(text, character):
    """Convert text to speech and play it using pygame."""
    
    # ✅ Character voice mapping
    CHARACTER_VOICES = {
        "Hermione": "9BWtsMINqrJLrRacOk9x",
        "Harry Potter": "pAqVPhB92dJKQXxUVRhV",
        "Dumbledore": "YvDVW8cUqzFj9TbuLKks",
        "Snape": "mFZbPwnF8A47Uj3n2K7F",
        "Hagrid": "2TLdy7jSivWMD7r8sV5C"
    }

    voice_id = CHARACTER_VOICES.get(character, "9BWtsMINqrJLrRacOk9x")  # Default to Hermione

    # ✅ Generate speech
    audio_stream = client.text_to_speech.convert(
        text=text,
        voice_id=voice_id
    )

    # ✅ Save audio to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio:
        for chunk in audio_stream:
            temp_audio.write(chunk)
        temp_audio_path = temp_audio.name

    # ✅ Initialize only pygame's mixer (Avoids crash)
    pygame.mixer.init()
    pygame.mixer.music.load(temp_audio_path)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        continue  # Keep script running until the audio finishes playing

    # ✅ Cleanup temp file
    os.remove(temp_audio_path)

'''
def play_audio(file_path):
    """Play MP3 using pygame for cross-platform support."""
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        continue  # Keep script running until the audio finishes playing

# ✅ Get available voices

voices = client.voices.get_all()

print("Available Voices in Your ElevenLabs Account:")
for voice in voices.voices:
    print(f"Name: {voice.name}, ID: {voice.voice_id}")


# ✅ Generate speech
audio = client.text_to_speech.convert(
    text="Hello, I am Hermione Granger!", 
    voice_id="9BWtsMINqrJLrRacOk9x"  # Use a real voice ID from ElevenLabs
)

# ✅ Save audio properly
with open("hermione_voice.mp3", "wb") as f:
    for chunk in audio:  # Iterate over the generator
        f.write(chunk)

# ✅ Play the audio (Windows/macOS/Linux compatible)
play_audio("hermione_voice.mp3")
#os.system("start hermione_voice.mp3" if os.name == "nt" else "mpg321 hermione_voice.mp3")
'''