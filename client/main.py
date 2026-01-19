import threading
import atexit
import base64
import requests
from fish import Fish
from stt import run_pipeline


if __name__ == "__main__":
    shared_fish = Fish()

    atexit.register(shared_fish.cleanup_fish)

    selected_personality = 0
    # Create web server and voice to response program
    picovoice_thread = threading.Thread(
        target=run_pipeline, args=(shared_fish, selected_personality,))

    # Start created threads
    picovoice_thread.start()

    # Join threads on close
    picovoice_thread.join()
