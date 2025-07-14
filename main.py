import threading
from server import app
from stt import run_pipeline


def run_flask():
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)


if __name__ == "__main__":
    # Create web server and voice to response program
    flask_thread = threading.Thread(target=run_flask)
    picovoice_thread = threading.Thread(target=run_pipeline)

    # Start created threads
    flask_thread.start()
    picovoice_thread.start()

    # Join threads on close
    flask_thread.join()
    picovoice_thread.join()
