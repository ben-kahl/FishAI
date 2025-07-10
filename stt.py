from dotenv import load_dotenv
import os
import pvleopard
from pvrecorder import PvRecorder
import wave
import struct


load_dotenv()

API_KEY = os.getenv('PICOVOICE_API_KEY')

leopard = pvleopard.create(access_key=API_KEY)
recorder = PvRecorder(device_index=-1, frame_length=512)


def list_inputs():
    for index, device in enumerate(PvRecorder.get_available_devices()):
        print(f'[{index}] {device}')


def get_audio_data():
    audio = []
    try:
        recorder.start()
        while True:
            frame = recorder.read()
            audio.extend(frame)
        recorder.stop()
        with wave.open('/user_input.wav', 'w') as f:
            f.setparams((1, 2, 16000, 512, 'NONE', 'NONE'))
            f.writeframes(struct.pack('h', * len(audio), *audio))
        return audio
    finally:
        recorder.delete()


def speech_to_text():
    # input = get_audio_data()
    if input:
        transcript, words = leopard.process(input)
        print(transcript)


list_inputs()
