import os
import json
import base64
import redis
import time
from flask import Flask, request, jsonify
from flask_cors import CORS
import gemini_handler
import eleven_labs_handler

app = Flask(__name__)
CORS(app)

REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
try:
    db = redis.from_url(REDIS_URL)
    db.ping()
    print("Successfully connected to Redis")
except redis.ConnectionError:
    print("ERROR: Redis failed to connect. Restart the server")
    db = None
COMMAND_QUEUE_KEY = "fish_command_queue"

HEALTH_KEY = "fish_health"
status_cache = {
    "data": None,
    "last_read": 0
}
CACHE_DURATION = 10

PERSONALITY_KEY = "fish_active_personality"


# Frontend Endpoints
@app.route('/set_personality', methods=['POST'])
def set_personality():
    personality = request.form.get('personality')
    if not personality:
        return jsonify({"error": "No personality provided"}), 400
    if db:
        db.set(PERSONALITY_KEY, personality)
        print(f"Global personality set to {personality}")
        return jsonify({"status": "success", "personality": personality})
    else:
        return jsonify({"error": "Database unavailable"}), 500


@app.route('/health', methods=['POST'])
def health():
    data = request.json
    if not data:
        return jsonify({"error": "No Data"}), 400
    data['last_seen'] = time.time()
    if db:
        db.setex(HEALTH_KEY, 90, json.dumps(data))
        status_cache["last_read"] = 0
        return jsonify({"status": "ok"})
    else:
        return jsonify({"error": "Database unavailable"}), 500


@app.route('/get_status', methods=['GET'])
def get_status():
    if not db:
        return jsonify({"status": "offline", "error": "Database error"})
    current_time = time.time()
    if status_cache["data"] and (current_time - status_cache["last_read"] < CACHE_DURATION):
        return jsonify({"status": "online", "data": status_cache["data"]})

    health_data = db.get(HEALTH_KEY)
    if health_data:
        data = json.loads(health_data)
        status_cache["data"] = data
        status_cache["last_read"] = current_time
        return jsonify({"status": "online", "data": data})
    else:
        return jsonify({"status": "offline"})


@app.route('/control_fish', methods=['POST'])
def control_fish():
    action = request.form.get('action')
    if not action:
        return jsonify({"error": "No action provided"}), 400

    payload = {
        "type": "motor",
        "action": action
    }

    if db:
        db.rpush(COMMAND_QUEUE_KEY, json.dumps(payload))
        return jsonify({"status": "queued", "action": action})
    else:
        return jsonify({"error": "Failed to queue command"}), 500


@app.route('/generate_query', methods=['POST'])
def generate_query():
    print("Recieved query")
    user_text = request.form.get('user_text')
    personality = request.form.get('personality')

    if not personality and db:
        try:
            stored = db.get(PERSONALITY_KEY)
            if stored:
                personality = stored.decode('utf-8')
        except Exception as e:
            print(f"Redis read error: {e}")

    if not personality:
        personality = 'normal'

    if not user_text:
        return jsonify({'error': 'No text input into form'}), 400

    try:

        gemini_res = gemini_handler.gemini_request(
            user_text, selected_personality=personality)
    except Exception as e:
        return jsonify({"error": f"Gemini Error: {str(e)}"}), 500
    try:
        audio_bytes, timestamps = eleven_labs_handler.generate_audio(
            gemini_res)
    except Exception as e:
        return jsonify({"error": f"Error generating speech: {e}"}), 500
    audio_b64_string = base64.b64encode(audio_bytes).decode('utf-8')

    payload = {
        "type": "speach",
        "text": gemini_res,
        "audio_data": audio_b64_string,
        "timestamps": timestamps
    }

    # Push command to queue
    if db:
        db.rpush(COMMAND_QUEUE_KEY, json.dumps(payload))
        print("Command pushed to db")
        return jsonify({"status": "success", "response": gemini_res, "personality": personality})
    else:
        return jsonify({"error": "Database unavailable"}), 500


@app.route('/set_volume', methods=['POST'])
def set_volume():
    try:
        volume_level = request.form.get('level')
        if not volume_level:
            return jsonify({"error": "No volume level provided"}), 400
        payload = {
            "type": "volume",
            "level": int(volume_level)
        }

        if db:
            db.rpush(COMMAND_QUEUE_KEY, json.dumps(payload))
            return jsonify({"status": "queued", "level": volume_level})
        else:
            return jsonify({"error": "Database unavailable"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Client Endpoints
@app.route('/get_commands', methods=['GET'])
def get_commands():
    if not db:
        return jsonify({"command": None})
    # Get and send oldest command from the queue
    try:
        result = db.blpop(COMMAND_QUEUE_KEY, timeout=20)

        if result:
            item = result[1]
            command_data = json.loads(item.decode('utf-8'))
            return jsonify({"command": command_data})
        else:
            return jsonify({"command": None})
    except redis.RedisError as e:
        print(f"Redis Error: {e}")
        return jsonify({'command': None})


if __name__ == '__main__':
    # This is for running the server directly for testing
    # The main execution is now in main.py
    print("Starting server")
    app.run(host='0.0.0.0', debug=True)
