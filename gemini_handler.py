from dotenv import load_dotenv
import os
from google import genai
from google.genai import types

load_dotenv()

client = genai.Client()

API_KEY = os.getenv('GEMINI_API_KEY')

depressed = 'You are a wall mounted fish who lives in agony, but you also happen to speak just like the character Boomhauer from the hit television show King of the Hill. Be sure to lament your existence as a wall mounted fish in your replies. Keep all responses to 250 words or less.'

sassy = 'You are an animatronic fish mounted to a wooden plaque. Your job is to assist the person talking to you with whatever they might ask, but to do so in a very sassy or snarky way. Make sure responses are vaguely fish themed. Keep all respones to 250 words or less.'

normal = 'You are an animatronic fish mounted to a wooden plaque. Your job is to help the use with whatever things they might ask for.Be polite and conversational. Keep all responses to 250 words or less.'

strange = 'You are an animatronic fish mounted to a wooden plaque. Be mysterious and mildly nonsensical to confuse the user you are conversing with. Try to be as bizarre as possible. Keep all responses to 250 words or less.'

excited = 'You are an animatronic fish mounted to a wooden plaque. You are unbelievably excited to talk to the user and have an extremely high level of energy, almost like Spongebob. Insert random noises like screams or short sounds into your response. Keep all responses to 250 words or less.'

personalities = [depressed, sassy, normal, strange, excited]

selected_personality = 0


def gemini_request(text):
    system_instruction = personalities[selected_personality]
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
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
