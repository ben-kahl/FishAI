import os
import time
import threading
import json
import subprocess
import base64
import requests
import psutil
import cv2
from fish import Fish
import pvleopard
from pvrecorder import PvRecorder
import pvporcupine
from dotenv import load_dotenv

load_dotenv()

CLOUD_URL = os.getenv('CLOUD_URL', 'http://192.168.87.237:5000')
API_KEY = os.getenv('PICOVOICE_API_KEY')
KEYWORD_PATH = "./wake_word.ppn"
MICROPHONE_INDEX = int(os.getenv('MICROPHONE_INDEX', -1))
CAMERA_INDEX = int(os.getenv('CAMERA_INDEX', 0))


class FishClient:
    def __init__(self):
        self.fish = Fish()
        self.running = True

    def start(self):
        poll_thread = threading.Thread(target=self.poll_cloud)
        listen_thread = threading.Thread(target=self.listen)
        health_thread = threading.Thread(target=self.send_health)
        poll_thread.start()
        listen_thread.start()
        health_thread.start()

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.running = False
            self.fish.cleanup_fish()
            print("Shutting down...")

    def capture_image_async(self, container):
        try:
            cap = cv2.VideoCapture(CAMERA_INDEX)
            if cap.isOpened():
                # Warm up camera? Sometimes first frame is black.
                # Just reading one frame for now to keep it fast.
                ret, frame = cap.read()
                if ret:
                    _, buffer = cv2.imencode('.jpg', frame)
                    container['data'] = base64.b64encode(
                        buffer).decode('utf-8')
                cap.release()
        except Exception as e:
            print(f"Image capture failed: {e}")

    def play_audio_from_payload(self, audio_b64, timestamps):
        try:
            audio_bytes = base64.b64decode(audio_b64)

            temp_file = "/tmp/fish_response.mp3"
            with open(temp_file, "wb") as f:
                f.write(audio_bytes)

            talk_thread = threading.Thread(
                target=self.fish.talk, args=(timestamps,))
            talk_thread.start()
            subprocess.run(['mpg123', '-q', temp_file], check=True)
            talk_thread.join()

            if os.path.exists(temp_file):
                os.remove(temp_file)
        except Exception as e:
            print(f"Error with playback: {e}")

    def poll_cloud(self):
        print("Polling...")
        while self.running:
            try:
                response = requests.get(
                    f"{CLOUD_URL}/get_commands", timeout=25)
                if response.status_code == 200:
                    data = response.json()
                    cmd = data.get("command")
                    if cmd:
                        if cmd.get('type') == 'motor':
                            action = cmd.get('action')
                            match action:
                                case 'move_head_out':
                                    self.fish.move_head_out()
                                case 'move_head_in':
                                    self.fish.move_head_in()
                                case 'move_tail_out':
                                    self.fish.move_tail_out()
                                case 'move_tail_in':
                                    self.fish.move_tail_in()
                                case 'move_mouth_out':
                                    self.fish.move_mouth_out()
                                case 'move_mouth_in':
                                    self.fish.move_mouth_in()
                        elif cmd.get('type') == 'speach':
                            print(f"Response: {data}")
                            self.play_audio_from_payload(
                                cmd.get('audio_data'), cmd.get('timestamps'))
                        elif cmd.get('type') == 'volume':
                            level = cmd.get('level')
                            print(f"Setting volume to {level}%")
                            try:
                                subprocess.run(
                                    ['amixer', 'sset', 'PCM', f'{level}%'], check=False)
                            except Exception as e:
                                print(f"Failed to set volume: {e}")
            except requests.Timeout:
                continue
            except Exception as e:
                print(f"Connection Error: {e}")
                time.sleep(2)

    def listen(self):
        leopard = None
        recorder = None
        porcupine = None
        try:
            leopard = pvleopard.create(access_key=API_KEY)
            recorder = PvRecorder(
                device_index=MICROPHONE_INDEX, frame_length=512)
            porcupine = pvporcupine.create(
                access_key=API_KEY, keyword_paths=[KEYWORD_PATH],
                sensitivities=[0.8])

            print(f'Picovoice pipeline running using device index: {
                  MICROPHONE_INDEX}')

            recorder.start()
            while self.running:
                pcm = recorder.read()
                keyword_index = porcupine.process(pcm)
                if keyword_index >= 0:
                    print('Wake word detected')

                    # Capture image in parallel
                    image_holder = {}
                    capture_thread = threading.Thread(
                        target=self.capture_image_async, args=(image_holder,))
                    capture_thread.start()

                    if self.fish:
                        listen_thread = threading.Thread(
                            target=self.fish.listen, args=(5,))
                        listen_thread.start()

                    audio_frames = []
                    start_time = time.time()
                    while time.time() - start_time < 5:
                        audio_frames.extend(recorder.read())

                    if self.fish:
                        listen_thread.join()

                    # Ensure image capture is done
                    capture_thread.join()

                    transcript, _ = leopard.process(audio_frames)
                    print(f'pico transcription: {transcript}')

                    if transcript:
                        payload = {'user_text': transcript}
                        if 'data' in image_holder:
                            payload['image_data'] = image_holder['data']
                            print("Attaching image data to request")

                        requests.post(
                            f"{CLOUD_URL}/generate_query", data=payload)
                        print("Sent query to cloud.")
        except Exception as e:
            print(f'Audio Error: {e}')
        finally:
            if recorder:
                recorder.delete()
            if porcupine:
                porcupine.delete()
            if leopard:
                leopard.delete()

    def send_health(self):
        while self.running:
            try:
                try:
                    temp = subprocess.check_output(
                        "vcgencmd measure_temp", shell=True)
                    temp = temp.decode(
                        'utf-8').replace("temp=", "").replace("'C\n", "")
                except:
                    temp = "N/A"

                payload = {
                    "cpu_usage": psutil.cpu_percent(),
                    "memory_usage": psutil.virtual_memory().percent,
                    "temperature": temp,
                    "platform": "Raspberry Pi 4b"
                }

                requests.post(f"{CLOUD_URL}/health", json=payload, timeout=2)
            except Exception as e:
                print(f"Health check failed: {e}")
            time.sleep(30)


if __name__ == "__main__":
    client = FishClient()
    client.start()
