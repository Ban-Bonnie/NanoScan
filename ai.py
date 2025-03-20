from dotenv import load_dotenv
import os
from openai import OpenAI

class OpenAIChat:
    def __init__(self, model="gpt-4o-mini-2024-07-18"):
        load_dotenv()
        self.api_key = os.getenv("API_KEY")
        self.client = OpenAI(api_key=self.api_key)
        self.model = model
    
    def get_response(self, user_message: str) -> str:
        try:
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": user_message}
                ]
            )
            return completion.choices[0].message.content
        except Exception as e:
            return f"Error: {str(e)}"

if __name__ == "__main__":
    chat = OpenAIChat()
    user_input = input("Enter your message: ")
    response = chat.get_response(user_input)
    print("AI:", response)
