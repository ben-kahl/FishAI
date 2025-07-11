import tempfile
import os
from dotenv import load_dotenv
import subprocess
from elevenlabs import ElevenLabs

load_dotenv()

API_KEY = os.getenv('ELEVENLABS_API_KEY')

client = ElevenLabs(
    api_key=API_KEY,
)


def generate_speech(text, voice_id='6F5Zhi321D3Oq7v1oNT4'):
    temp_file_path = None
    try:
        audio_stream = client.text_to_speech.convert(
            voice_id=voice_id,
            output_format='mp3_44100_128',
            text=text,
            model_id='eleven_flash_v2_5'
        )

        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as temp_audio_file:
            for chunk in audio_stream:
                temp_audio_file.write(chunk)
            temp_file_path = temp_audio_file.name

        print(f'Audio saved to: {temp_file_path}')

        try:
            subprocess.run(['mpg123', '-q', temp_file_path], check=True)
        except FileNotFoundError:
            print('Error: mpg123 not found')
        except subprocess.CalledProcessError as e:
            print(f'error with audio playback: {e}')
        except Exception as e:
            print('Unexpected playback error: {e}')
    except Exception as e:
        print(f'Error occured with speech generation {e}')
    finally:
        if temp_file_path and os.path.exists(temp_file_path):
            os.remove(temp_file_path)
