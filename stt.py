from dotenv import load_dotenv
import os
import pvleopard
from pvrecorder import PvRecorder
import pvporcupine
import time
import gemini_handler
import voice_output


load_dotenv()

API_KEY = os.getenv('PICOVOICE_API_KEY')


def run_pipeline():
    leopard = None
    recorder = None
    porcupine = None
    try:
        leopard = pvleopard.create(access_key=API_KEY)
        recorder = PvRecorder(device_index=-1, frame_length=512)
        # change keyword to custom model once it's created
        porcupine = pvporcupine.create(API_KEY, keywords=['bumblebee'])

        print('Picovoice pipeline running')

        while True:
            recorder.start()
            keyword_index = porcupine.process(recorder.read())
            if keyword_index >= 0:
                print('Wake word detected')
                recorder.stop()

                audio_frames = []
                start_time = time.time()
                recorder.start()
                while time.time() - start_time < 5:
                    audio_frames.extend(recorder.read())

                transcript, _ = leopard.process(audio_frames)
                recorder.stop()
                print(f'pico transcription: {transcript}')

                if transcript:
                    gemini_res = gemini_handler.gemini_request(transcript)
                    print(f'Gemini response: {gemini_res}')
                    voice_output.generate_speech(gemini_res)
    except KeyboardInterrupt:
        print('Stopping picovoice pipeline...')
    finally:
        if recorder:
            recorder.delete()
        if porcupine:
            porcupine.delete()
        if leopard:
            leopard.delete()


if __name__ == '__main__':
    run_pipeline()
