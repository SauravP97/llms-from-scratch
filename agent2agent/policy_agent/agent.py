from dotenv import load_dotenv
from google import genai
from google.genai import types

import os


class PolicyAgent:
    def __init__(self):
        load_dotenv()
        self.client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
        self.model_name = 'gemini-3.1-pro-preview'
    
    def answer_query(self, prompt: str) -> str:
        response = self.client.models.generate_content(
            model=self.model_name,
            contents=prompt,
            config=types.GenerateContentConfig(
                # Temperature: 0.0 is precise/deterministic, 1.0 is creative/random
                temperature=1.0, 
                
                # System Instructions: Sets the behavior/persona of the model
                system_instruction="You are an assistant to answer user questions"
            )
        )

        return response.text
