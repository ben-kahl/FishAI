import atexit  # Import atexit for cleanup
from flask import Flask, render_template, request
from fish import Fish
import gemini_handler
import voice_output


app = Flask(__name__)
fish_instance = None  # Initialize as None


@app.before_request
def initialize_fish():
    # Initialize fish_instance only once
    global fish_instance
    if fish_instance is None:
        fish_instance = Fish()
        # Register the cleanup function to be called on app exit
        atexit.register(fish_instance.cleanup_fish)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/control_fish', methods=['POST'])
def control_fish():
    action = request.form.get('action')
    if fish_instance is None:
        # Should not happen with before_request
        return "Fish instance not initialized.", 500
    if action == 'move_head_out':
        fish_instance.move_head_out()
        return "Head moved out!"
    elif action == 'move_head_in':
        fish_instance.move_head_in()
        return "Head moved in!"
    elif action == 'move_tail_out':
        fish_instance.move_tail_out()
        return "Tail moved out!"
    elif action == 'move_tail_in':
        fish_instance.move_tail_in()
        return "Tail moved in!"
    elif action == 'move_mouth_out':
        fish_instance.talk(None, 1)
        return "Mouth moved out!"
    elif action == 'move_mouth_in':
        fish_instance.move_mouth_in()
        return "Mouth moved in!"
    else:
        return "Invalid action", 400


@app.route('/ask_gemini', methods=['POST'])
def ask_gemini():
    user_text = request.form.get('user_text')
    if not user_text:
        return 'No text input into form', 400

    gemini_res = gemini_handler.gemini_request(user_text)
    print(gemini_res)
    try:
        voice_output.generate_speech(gemini_res)
        return 'Success', 200
    except Exception as e:
        print(f'Error generating speech: {e}')


@app.route('/test_elevenlabs', methods=['POST'])
def test_elevenlabs():
    user_text = request.form.get('user_text')
    if not user_text:
        return 'No text recieved', 400
    try:
        voice_output.generate_speech(user_text)
        return 'Success', 200
    except Exception as e:
        print(f'Error generating speech: {e}')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
