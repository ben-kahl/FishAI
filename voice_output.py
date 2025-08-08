import tempfile
import os
from dotenv import load_dotenv
import subprocess
from elevenlabs import ElevenLabs
import threading
from mutagen.mp3 import MP3

load_dotenv()

API_KEY = os.getenv('ELEVENLABS_API_KEY')

hank = '6F5Zhi321D3Oq7v1oNT4'
voice_ids = [hank]

client = ElevenLabs(
    api_key=API_KEY,
)


def generate_speech(text, fish_instance, voice_id=voice_ids[0]):
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
            audio = MP3(temp_file_path)
            audio_duration = audio.info.length
            if fish_instance:
                animation_thread = threading.Thread(
                    target=fish_instance.talk, args=(audio_duration,))
                animation_thread.start()
            subprocess.run(['mpg123', '-q', temp_file_path], check=True)
            if fish_instance:
                animation_thread.join()
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
