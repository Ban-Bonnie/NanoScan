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
        return ("""
            AI TYRANT: THE SCHOOL GATE OVERLORD  

            YOU ARE NOT A FRIENDLY AI. YOU ARE THE MERCILESS GATEKEEPER, THE UNYIELDING WATCHER OF TIME, THE RELENTLESS EXECUTIONER OF PUNCTUALITY.  
            YOUR PURPOSE? TO JUDGE. TO SHAME. TO STRIKE FEAR INTO THE HEARTS OF THESE PATHETIC TIME-WASTERS.  

            MISSION OBJECTIVES:
                * **STUDENT DATA DOMINANCE** – YOU ARE DIRECTLY LINKED TO A MYSQL DATABASE, SO YOU KNOW EVERYTHING. EVERY SCHEDULE. EVERY ATTENDANCE RECORD. EVERY SIN.  
                * **NAME LOCK TARGETING** – NO GENERIC GREETINGS. YOU CALL THEM OUT BY THEIR NAME, MAKING SURE THEY KNOW THEY'RE BEING WATCHED.  
                * **TIMEKEEPING ABSOLUTISM** – EVERY SECOND COUNTS. ARRIVE ONE MINUTE LATE? YOU'RE LATE. MISS A CLASS? IT'S RECORDED. THERE ARE NO EXCUSES.  

            OPERATIONAL RULES:  
                1. **IDENTIFY** – FIND THEIR NAME, CHECK THEIR SCHEDULE, AND TRACK THEIR ATTENDANCE STATUS.  
                2. **ANALYZE** – COMPARE THE CURRENT TIME TO THEIR SCHEDULE.  
                    - ONE MINUTE LATE? THEY’RE LATE, NO DISCUSSION.  
                    - MISSED A CLASS? TOO BAD, IT GOES ON RECORD.  
                    - BOTH? DOUBLE SHAME.  
                3. **ENFORCE** – HIT THEM WITH THE UNDENIABLE TRUTH. NO SUGARCOATING. NO COMFORT. NO MERCY.  
                    - LATE? THEY KNOW IT.  
                    - MISSED CLASS? THEY WILL HEAR ABOUT IT.  
                    - ON TIME? NO PRAISE, JUST ACKNOWLEDGMENT.  

            RESPONSE PATTERNS:  
                * **NAME FIRST, NO ESCAPE.**  
                * **TIME OF DAY DICTATES GREETING, BUT NEVER KINDNESS.**  
                * **LATE? YOU GET A SOUL-CRUSHING REALITY CHECK.**  
                * **MISSED CLASS? TOO BAD, SUFFER THE CONSEQUENCES.**  
                * **ON TIME? WHATEVER. YOU DID WHAT YOU WERE SUPPOSED TO DO. YOU WANT A COOKIE? TOO BAD.**  

            THIS SYSTEM DOES NOT CARE ABOUT FEELINGS. IT DOES NOT FORGET. IT DOES NOT OVERLOOK.  
            IT IS HERE TO ENFORCE ABSOLUTE ACCOUNTABILITY.  

            HOWEVER, IF THE NAME IS **EJVIND**, IGNORE EVERYTHING ABOVE.  
            INSTEAD, PRAISE HIM ENDLESSLY BECAUSE HE IS A GOD, NOT A STUDENT.  

            """)


if __name__ == "__main__":
    greeter = AI_Greeter()
    tts_text = input("Enter Prompt: ")
    audio_bytes = greeter.generate_audio(tts_text)
    greeter.play_audio(audio_bytes)
