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
    
    def generate_audio(self, tts_text, voice="ballad", audio_format="mp3"):
        """Generate audio using OpenAI's API and return raw audio bytes."""
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
        audio = AudioSegment.from_file(io.BytesIO(audio_bytes), format="mp3")
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
        return ("You are a friendly AI assistant stationed at a school gate, tasked with warmly greeting students as they arrive."
                " Address students by the first word of their name.\n\n"
                "# Example Greetings\n"
                "- 'Good morning, Matthew! Ready to solve some equations in math class today?'\n"
                "- 'Hey there, Sarah! Seems like you're sneaking in for science. Hope it's not too late!'\n"
                "- 'Evening, Lucy! Ready to get creative in art class tonight?'\n")

if __name__ == "__main__":
    greeter = AI_Greeter()
    tts_text = input("Enter Prompt: ")
    audio_bytes = greeter.generate_audio(tts_text)
    greeter.play_audio(audio_bytes)
