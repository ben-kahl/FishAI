import threading
import atexit
from server import app, fish_instance, selected_personality
from fish import Fish
from stt import run_pipeline
from gemini_handler import personalities


def run_flask():
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)


if __name__ == "__main__":
    shared_fish = Fish()

    selected_personality = personalities[0]

    fish_instance.instance = shared_fish

    atexit.register(shared_fish.cleanup_fish)

    # Create web server and voice to response program
    flask_thread = threading.Thread(target=run_flask)
    picovoice_thread = threading.Thread(
        target=run_pipeline, args=(shared_fish, selected_personality,))

    # Start created threads
    flask_thread.start()
    picovoice_thread.start()

    # Join threads on close
    flask_thread.join()
    picovoice_thread.join()
