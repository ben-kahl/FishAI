from flask import Flask, request, render_template
from fish import Fish

app = Flask(__name__)
fish = Fish()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/control_fish', methods=['POST'])
def fish_control():
    action = request.form.get('action')
    match action:
        case 'move_head_out':
            fish.move_head_out()
            return 'Head moved out\n'
        case 'move_head_in':
            fish.move_head_in()
            return 'Head moved in\n'
        case 'move_tail_out':
            fish.move_tail_out()
            return 'Tail moved out\n'
        case 'move_tail_in':
            fish.move_tail_in()
            return 'Tail moved in\n'
        case 'move_mouth_out':
            fish.move_mouth_out()
            return 'Mouth moved out\n'
        case 'move_mouth_in':
            fish.move_mouth_in()
            return 'Mouth moved in\n'


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
