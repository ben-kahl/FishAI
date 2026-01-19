import os
from dotenv import load_dotenv
from elevenlabs import ElevenLabs
import base64

load_dotenv()

API_KEY = os.getenv('ELEVENLABS_API_KEY')

hank = '6F5Zhi321D3Oq7v1oNT4'
james = 'EkK5I93UQWFDigLMpZcX'
voice_ids = [hank, james]

client = ElevenLabs(
    api_key=API_KEY,
)


def generate_audio(text, voice_id=voice_ids[0]):
    '''
    Returns a tuple (audio_bytes, timestamps)
    '''
    try:
        response = client.text_to_speech.convert_with_timestamps(
            voice_id=voice_id,
            output_format='mp3_44100_128',
            text=text,
            model_id='eleven_flash_v2_5'
        )

        audio_stream = response.audio_base_64
        audio_bytes = base64.b64decode(audio_stream)
        timestamps = response.alignment.character_start_times_seconds

        return audio_bytes, timestamps
    except Exception as e:
        print(f'Error occured with speech generation {e}')
        return None, None
