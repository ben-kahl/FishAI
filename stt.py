from dotenv import load_dotenv
import os
import pvleopard
from pvrecorder import PvRecorder
import pvporcupine
import time


load_dotenv()

API_KEY = os.getenv('PICOVOICE_API_KEY')

leopard = pvleopard.create(access_key=API_KEY)
recorder = PvRecorder(device_index=-1, frame_length=512)
# change keyword to custom model once it's created
porcupine = pvporcupine.create(API_KEY, keywords=['bumblebee'])


def list_inputs():
    for index, device in enumerate(PvRecorder.get_available_devices()):
        print(f'[{index}] {device}')


def get_next_audio_frame():
    audio = []
    try:
        recorder.start()
        frame = recorder.read()
        audio.extend(frame)
        recorder.stop()
        return audio
    except Exception as e:
        print(f"Error getting audio frame {e}")


def wakeword_detection():
    audio_frame = get_next_audio_frame()
    keyword_index = porcupine.process(audio_frame)
    if keyword_index == 0:
        print('wakeword detected, start speech to text')
        speech_to_text()
        return False
    else:
        return True


def get_audio_data():
    audio = []
    start = time.time()
    duration = 5
    try:
        print('starting audio recording')
        recorder.start()
        while time.time() - start < duration:
            frame = recorder.read()
            audio.extend(frame)
        recorder.stop()
        return audio
    except Exception as e:
        print(f"Error getting audio data {e}")


def speech_to_text():
    input = get_audio_data()
    if input:
        transcript, words = leopard.process(input)
        print(transcript)
        return transcript


if __name__ == "__main__":
    print('listing inputs...')
    list_inputs()
    detected = True
    while detected:
        detected = wakeword_detection()
    recorder.delete()
    porcupine.delete()
    leopard.delete()
