import atexit  # Import atexit for cleanup
from flask import Flask, render_template, request
from fish import Fish

app = Flask(__name__)
fish_instance = None  # Initialize as None


@app.before_request
def initialize_fish():
    # Initialize fish_instance only once
    global fish_instance
    if fish_instance is None:
        fish_instance = Fish()
        # Register the cleanup function to be called on app exit
        atexit.register(cleanup_fish)


def cleanup_fish():
    # This function will be called when the application exits
    print("Cleaning up GPIO pins...")
    if fish_instance:
        fish_instance.__head_motor.close()
        fish_instance.__tail_motor.close()
        fish_instance.__mouth_motor.close()
        print("GPIO pins released.")


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
        fish_instance.move_mouth_out()
        return "Mouth moved out!"
    elif action == 'move_mouth_in':
        fish_instance.move_mouth_in()
        return "Mouth moved in!"
    else:
        return "Invalid action", 400


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
