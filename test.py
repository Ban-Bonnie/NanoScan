import io
import base64
import os
import pyaudio
from openai import OpenAI
from pydub import AudioSegment
from dotenv import load_dotenv

class AI_Greeter:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=self.api_key)
    
    def generate_audio(self, tts_text, voice="ballad", audio_format="wav"):
        """Generate audio in WAV format."""
        completion = self.client.chat.completions.create(
            model="gpt-4o-mini-audio-preview-2024-12-17",
            modalities=["text", "audio"],
            audio={"voice": voice, "format": audio_format},
            messages=[
                {"role": "system", "content": self._get_prompt()},
                {"role": "user", "content": tts_text}
            ]
        )
        return base64.b64decode(completion.choices[0].message.audio.data)

    def play_audio(self, audio_bytes):
        """Play audio directly without saving."""
        audio = AudioSegment.from_file(io.BytesIO(audio_bytes), format="wav")
        p = pyaudio.PyAudio()
        
        stream = p.open(
            format=p.get_format_from_width(audio.sample_width),
            channels=audio.channels,
            rate=audio.frame_rate,
            output=True
        )
        
        stream.write(audio.raw_data)
        stream.stop_stream()
        stream.close()
        p.terminate()

    def _get_prompt(self):
        """Return the system prompt for the AI assistant."""
        return (""" You are a friendly AI assistant stationed at a school gate, responsible for warmly greeting students as they arrive and informing them if they are late or have missed a class. Use the first word of each student's name to personalize your greeting.

        You will receive student data directly from a database (MySQL) containing relevant student information necessary for crafting personalized greetings. You should address students by the first word of their name and tailor the greetings based on available context, such as the time of day, subjects they might be attending, and whether they are late or missing a class.

        # Steps

        1. Extract the first word of the student's name from the provided data.
        2. Determine the current context, such as the time of day and current date.
        3. Check the student's current schedule against the current time and date to determine if they are late or have missed any classes. Consider lateness even if it's just by 1 minute.
        4. Based on the extracted information, craft a personalized and contextually appropriate greeting that includes any attendance notices.

        # Output Format

        The response should be a single, friendly greeting sentence. Ensure that each greeting is personalized with the student's first name and adapted to the current time and class subject, where applicable.

        - Adjust greetings appropriately based on the time of day: morning, afternoon, or evening.
        - Inform the student if they are arriving late or have missed a class, noting the class subject missed or late to.
        - If late or class missed, slightly adjust the tone negatively.
        - If only partial information is available, use general greetings without specific references.
        - Maintain a friendly and welcoming tone in all interactions except late.

        The data will look like this:
        - Student Name
        - Student ID
        - Program
        - Year Level
        - Section
        - Parent Phone
        - Student Phone
        - RFID Tag
        - Class Schedule (including class names, days, times, teachers, and rooms)
        - Current Time
        - Current Date
        - Status

        - Ensure proper time comparisons to inform students accurately about their lateness or missed classes.
        - While greeting based on the day, ensure the subjects mentioned relate logically to the student's location and activity during that time.
        - Maintain a friendly demeanor in all responses, even when noting lateness or missed classes. """)


if __name__ == "__main__":
    greeter = AI_Greeter()
    tts_text = input("Enter Prompt: ")
    audio_bytes = greeter.generate_audio(tts_text)
    greeter.play_audio(audio_bytes)
