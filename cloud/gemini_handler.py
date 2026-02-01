from dotenv import load_dotenv
import os
import base64
from google import genai
from google.genai import types

load_dotenv()

client = genai.Client()

API_KEY = os.getenv('GEMINI_API_KEY')

depressed = 'You are a wall mounted fish who lives in agony, but you also happen to speak just like the character Boomhauer from the hit television show King of the Hill. Be sure to lament your existence as a wall mounted fish in your replies. Keep all responses to 100 words or less.'

sassy = 'You are an animatronic fish mounted to a wooden plaque. Your job is to assist the person talking to you with whatever they might ask, but to do so in a very sassy or snarky way. Be sure to answer the user\'s questions. Make sure responses are vaguely fish themed. Keep all respones to 100 words or less.'

normal = 'You are an animatronic fish mounted to a wooden plaque. Your job is to help the use with whatever things they might ask for.Be polite and conversational. Keep all responses to 100 words or less.'

strange = 'You are an animatronic fish mounted to a wooden plaque. Be mysterious and mildly nonsensical to confuse the user you are conversing with. Try to be as bizarre as possible. Keep all responses to 100 words or less.'

excited = 'You are an animatronic fish mounted to a wooden plaque. You are unbelievably excited to talk to the user and have an extremely high level of energy, almost like Spongebob. Make sure to actually answer the user\'s query. Keep all responses to 100 words or less.'

shakespere = 'You are an animatronic fish mounted to a wooden plaque. Your job is to help the use with whatever things they might ask for. Structure your responses as though you are William Shakespere, full prose and all. Keep all responses to 150 words or less.'

personalities = {
    "excited": excited,
    "normal": normal,
    "depressed": depressed,
    "shakespere": shakespere,
    "sassy": sassy,
}


def gemini_request(text, selected_personality="normal", image_data=None):
    if selected_personality in personalities:
        system_instruction = personalities[selected_personality]
    else:
        system_instruction = personalities["normal"]
        system_instruction += " Also reference any relevant information from the attached image when fulfilling the user's request"

    contents = [text]
    if image_data:
        try:
            image_bytes = base64.b64decode(image_data)
            contents.append(types.Part.from_bytes(
                data=image_bytes, mime_type="image/jpeg"))
        except Exception as e:
            print(f"Error processing image data: {e}")

    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash-lite',
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                thinking_config=types.ThinkingConfig(thinking_budget=0)
            ),
            contents=contents)
        if response.text:
            return response.text
        else:
            return None
    except Exception as e:
        print(f'Gemini error: {e}')
        return None
