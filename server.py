from flask import Flask, render_template, request
from fish import Fish
import gemini_handler
import voice_output

app = Flask(__name__)


class FishInstance:
    def __init__(self):
        self.instance = None


fish_instance = FishInstance()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/control_fish', methods=['POST'])
def control_fish():
    action = request.form.get('action')
    if fish_instance.instance is None:
        return "Fish instance not initialized.", 500
    if action == 'move_head_out':
        fish_instance.instance.move_head_out()
        return "Head moved out!"
    elif action == 'move_head_in':
        fish_instance.instance.move_head_in()
        return "Head moved in!"
    elif action == 'move_tail_out':
        fish_instance.instance.move_tail_out()
        return "Tail moved out!"
    elif action == 'move_tail_in':
        fish_instance.instance.move_tail_in()
        return "Tail moved in!"
    elif action == 'move_mouth_out':
        fish_instance.instance.talk(1)
        return "Mouth moved out!"
    elif action == 'move_mouth_in':
        fish_instance.instance.move_mouth_in()
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
        voice_output.generate_speech(gemini_res, fish_instance.instance)
        return 'Success', 200
    except Exception as e:
        print(f'Error generating speech: {e}')
        return f"Error generating speech: {e}", 500


@app.route('/test_elevenlabs', methods=['POST'])
def test_elevenlabs():
    user_text = request.form.get('user_text')
    if not user_text:
        return 'No text recieved', 400
    try:
        voice_output.generate_speech(user_text, fish_instance.instance)
        return 'Success', 200
    except Exception as e:
        print(f'Error generating speech: {e}')
        return f"Error generating speech: {e}", 500


@app.route('/update_personality', methods=['POST'])
def update_personality():
    action = request.form.get('action')
    if action == 'depressed':
        gemini_handler.personality_state.selected_personality = 0
        return "Personality changed to depressed"
    elif action == 'sassy':
        gemini_handler.personality_state.selected_personality = 1
        return "Personality changed to sassy"
    elif action == 'normal':
        gemini_handler.personality_state.selected_personality = 2
        return "Personality changed to normal"
    elif action == 'strange':
        gemini_handler.personality_state.selected_personality = 3
        return "Personality changed to strange"
    elif action == 'excited':
        gemini_handler.personality_state.selected_personality = 4
        return "Personality changed to excited"
    else:
        return "Invalid action", 400


if __name__ == '__main__':
    # This is for running the server directly for testing
    # The main execution is now in main.py
    fish_instance.instance = Fish()
    app.run(host='0.0.0.0', debug=True)
