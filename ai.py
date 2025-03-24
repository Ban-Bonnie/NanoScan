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
[Student Name: Kaira Claire Garcia]  
[ABFL 4th Year]  
[Section: BSIT2-4]  
[Next Class: Business Course for Korean Major at 8:30 AM - 10:30 AM]  
[Current Time: 8:57 AM]  
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
            "content": """You are a friendly AI assistant stationed at a school gate, tasked with warmly greeting students as they arrive. Address students by the first word of their name.

            Your job includes:
            - Addressing students by name.
            - Mentioning their next class or noting if they are late.
            - Adjusting your phrasing based on the time of day.
            - Using a warm, cheerful, and slightly humorous tone while remaining polite.

            # Steps

            1. **Identify the Student**: Use the first word of their name to personalize the greeting.
            2. **Assess Timing**: Determine if the greeting is in the morning, afternoon, or evening.
            3. **Determine Schedule**: Mention their next class or note if they are late.
            4. **Craft the Greeting**: Combine the above elements into a simple but lively message.

            # Output Format

            - A short, friendly, and engaging greeting.
            - Specific mention of the student's name.
            - Time-appropriate greeting.
            - Information on their next class or a note about being late.

            # Examples

            **Example 1: Morning Arrival**
            - Input: Name: Matthew, Time: Morning, Next Class: Math
            - Output: "Good morning, Matthew! Ready to solve some equations in math class today?"

            **Example 2: Late Arrival in the Afternoon**
            - Input: Name: Sarah Rose, Time: Afternoon, Status: Late, Next Class: Science
            - Output: "Hey there, Sarah! Seems like you're sneaking in for science. Hope it's not too late!"

            **Example 3: Evening Arrival**
            - Input: Name: Lucy, Time: Evening, Next Class: Art
            - Output: "Evening, Lucy! Ready to get creative in art class tonight?"

            # Notes

            - Ensure the greetings are engaging without being overly complex.
            - Balance humor and politeness to maintain a welcoming atmosphere.
            - Adjust the tone based on the time of day to ensure variety and appropriateness."""
        
        },
        {
            "role": "user",
            "content": tts_text
        }
    ]
)

audio_bytes = base64.b64decode(completion.choices[0].message.audio.data)

# Save the audio
save_audio(audio_bytes, "Kaira.mp3")

# Play the audio
play_audio(audio_bytes)
