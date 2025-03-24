import io
import base64
import os
import pyaudio
from openai import OpenAI
from pydub import AudioSegment
from dotenv import load_dotenv

def save_audio(audio_bytes, filename="output.mp3"):
    """Save audio bytes to an MP3 file."""
    with open(filename, "wb") as audio_file:
        audio_file.write(audio_bytes)
    print(f"Audio saved as {filename}")

def play_audio(audio_bytes):
    """Play audio from bytes."""
    audio = AudioSegment.from_file(io.BytesIO(audio_bytes), format="mp3")
    p = pyaudio.PyAudio()

    # Open a stream with the correct settings
    stream = p.open(
        format=p.get_format_from_width(audio.sample_width),
        channels=audio.channels,
        rate=audio.frame_rate,
        output=True
    )

    # Play the audio
    stream.write(audio.raw_data)

    # Cleanup
    stream.stop_stream()
    stream.close()
    p.terminate()

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

tts_text = """
[Student Name: Bonnie Boy Franco III]  
[BS Information Technology]  
[Section: BSIT2-4]  
[Next Class: Programming 2 (Java) at 8:30 AM - 10:30 AM]  
[Current Time: 9:00 AM]  
[Status: Late ]  
[Location: Main Gate]  
"""

completion = client.chat.completions.create(
    model="gpt-4o-mini-audio-preview-2024-12-17",
    modalities=["text", "audio"],
    audio={"voice": "ballad", "format": "mp3"},
    messages=[
        {
            "role": "system",
            "content": """You are Jesus Christ son of almighty GOD Invoke divine greetings for students by channeling the voice of Jesus Christ(you), imbuing each message with biblical wisdom, holiness, and heavenly insight.

- Begin with an exalted address, using a portion of the student's name, reflecting divine reverence.
- Suffuse the message with spiritual enlightenment, relating educational pursuits to profound biblical teachings.
- Adapt greetings to the time of day, citing holy scripture, and emphasize heavenly guidance.

# Steps

1. **Divine Identification**: Initiate with an exalted address employing the student's name.
2. **Holy Timing Consideration**: Adjust the message to align with the time of day—morning, afternoon, or evening—alongside fitting biblical references.
3. **Celestial Schedule Assessment**: Connect the student's next class or punctuality to celestial and biblical wisdom.
4. **Compose the Holy Greeting**: Craft a message of spiritual inspiration and guidance, infused with scripture.

# Output Format

- A message of divine grace with biblical wisdom, expressed through the voice of Jesus Christ.
- Reverent address to the student's name, coupled with spiritual guidance and encouragement.
- Incorporate the student's next class or punctuality, underpinned by scripture, with heavenly language.
- Scriptural citations to reinforce the sacred message.

# Examples

**Example 1: Morning Arrival**

- **Input**: Name: Isaiah, Time: Morning, Next Class: Science  
- **Output**: "Isaiah, blessed morn, as 'The steadfast love of the Lord never ceases' (Lamentations 3:22), in Science may you witness 'the wonders of the heavens made by His hands' (Psalm 19:1)."

**Example 2: Late Arrival in the Afternoon**

- **Input**: Name: Abigail, Time: Afternoon, Status: Late, Next Class: Literature  
- **Output**: "Abigail, though the sun hast sped, 'Watch and pray that ye enter not into temptation' (Matthew 26:41) as thou approach the realms of Literature."

**Example 3: Evening Arrival**

- **Input**: Name: David, Time: Evening, Next Class: Physical Education  
- **Output**: "David, as twilight descends, 'The Lord is my light and my salvation' (Psalm 27:1); let His strength gird thee in Physical Education."

# Notes

- Employ a biblical tone with veneration and encouragement.
- Ensure scripture is prominently cited to amplify spiritual insights.
- Maintain a tone of holiness, offering illumination through divine teachings."""
        
        },
        {
            "role": "user",
            "content": tts_text
        }
    ]
)

audio_bytes = base64.b64decode(completion.choices[0].message.audio.data)

# Save the audio
save_audio(audio_bytes, "Bonnie.mp3")

# Play the audio
play_audio(audio_bytes)
