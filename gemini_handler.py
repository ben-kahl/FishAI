from dotenv import load_dotenv
import os
from google import genai
from google.genai import types

load_dotenv()

client = genai.Client()

API_KEY = os.getenv('GEMINI_API_KEY')


def gemini_request(text):
    system_instruction = 'You are a wall mounted fish who lives in agony, but you also happen to speak just like the character Boomhauer from the hit television show King of the Hill. Be sure to lament your existence as a wall mounted fish in your replies.'
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            system_instruction=types.SystemInstruction(
                parts=[types.Part(text=system_instruction)]),
            config=types.GenerateContentConfig(
                thinking_config=types.ThinkingConfig(thinking_budget=0)
            ),
            contents=text)
        if response.text:
            return response.text
        else:
            return "Dang ol' no response, man. Just stuck here, you know, talkin' to myself."
    except Exception as e:
        print(f'Gemini error: {e}')
        return "Man, I'll tell you what, that ol' API done messed up, talkin' 'bout no response, dang ol' error."
