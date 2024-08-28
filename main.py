import os
import customtkinter as ctk
import threading
from playsound import playsound
from pynput import keyboard
import pyperclip
import pyautogui
import signal
import sys

from audio_handler import AudioHandler, get_audio_devices
from ui_components import UIComponents
from api_handler import APIHandler
from emitter import Emitter


# Get API URL from environment variable or use default
API_URL = os.getenv('TRANSCRIPTION_API_URL', 'http://10.68.7.2:8000/v1/audio/transcriptions')

class KeyboardHandler:
    def __init__(self, app):
        self.app = app
        self.current = set()
        self.listener = None

    def setup_listener(self):
        self.RECORD_COMBINATION = self.parse_hotkey(self.app.ui.record_hotkey_var.get())
        self.LANGUAGE_COMBINATION = self.parse_hotkey(self.app.ui.language_hotkey_var.get())
        self.listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
        self.listener.start()
        print("Debug: Keyboard listener setup complete")

    def parse_hotkey(self, hotkey_str):
        keys = hotkey_str.split('+')
        parsed_keys = set()
        for key in keys:
            key = key.strip().lower()
            if key == 'cmd':
                parsed_keys.add(keyboard.Key.cmd)
            elif key == 'ctrl':
                parsed_keys.add(keyboard.Key.ctrl)
            elif len(key) == 1:
                parsed_keys.add(keyboard.KeyCode.from_char(key))
        return parsed_keys

    def on_press(self, key):
        self.current.add(key)
        if all(k in self.current for k in self.RECORD_COMBINATION):
            print("Debug: Record hotkey combination pressed")
            self.app.master.after(0, self.app.toggle_recording)
        elif all(k in self.current for k in self.LANGUAGE_COMBINATION):
            print("Debug: Language toggle hotkey combination pressed")
            self.app.master.after(0, self.app.toggle_language)

    def on_release(self, key):
        try:
            self.current.remove(key)
        except KeyError:
            pass

    def update_hotkeys(self):
        self.RECORD_COMBINATION = self.parse_hotkey(self.app.ui.record_hotkey_var.get())
        self.LANGUAGE_COMBINATION = self.parse_hotkey(self.app.ui.language_hotkey_var.get())
        print("Debug: Hotkeys updated")

class RecordingHandler:
    def __init__(self, app):
        self.app = app
        self.recording = False
        self.audio_handler = AudioHandler()

    def toggle_recording(self):
        if not self.recording:
            self.start_recording()
        else:
            self.stop_recording()

    def start_recording(self):
        self.app.master.iconbitmap('assets/images/appIcon_recording.ico')
        self.app.ui.update_start_button(True)
        self.recording = True
        self.app.ui.update_loading_label("Recording...", "red")

        device_id = int(self.app.ui.device_var.get().split(':')[0])
        self.audio_handler.start_recording(device_id)
        playsound('./assets/sounds/beep.wav')

    def stop_recording(self):
        self.app.master.iconbitmap('assets/images/appIcon.ico')
        self.app.ui.update_start_button(False)
        self.recording = False
        self.app.ui.update_loading_label("Processing...", "orange")
        self.audio_handler.stop_recording()
        threading.Thread(target=self.process_audio).start()
        playsound('./assets/sounds/beep2.wav')

    def process_audio(self):
        try:
            temp_file_path = self.audio_handler.save_audio_to_file()
            if temp_file_path:
                prompt = self.app.ui.prompt_entry.get("1.0", ctk.END).strip()  # Get the prompt from the UI
                transcription = self.app.api_handler.upload_audio_to_whisper(temp_file_path, self.app.ui.language_var.get(), prompt)
                self.audio_handler.cleanup_audio_file(temp_file_path)

                if transcription:
                    print(f"Debug: Transcription received: {transcription}")
                    self.app.ui.update_transcription_text(transcription)
                    self.app.emitter.emit(transcription)
                    self.app.ui.update_loading_label("Transcription complete", "green")
                else:
                    self.app.ui.update_loading_label("Transcription failed", "red")
            else:
                self.app.ui.update_loading_label("No audio recorded", "red")
        except Exception as e:
            print(f"Debug: Error in process_audio: {e}")
            self.app.ui.update_loading_label(f"Error: {str(e)}", "red")

class TranscriptionApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Whisper API Transcription App")
        self.master.iconbitmap('assets/images/appIcon.ico')
        self.master.geometry("400x550")  # Increase window height
        self.master.protocol("WM_DELETE_WINDOW", self.on_close)

        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        x = (screen_width - 400) // 2
        y = (screen_height - 550) // 2  # Adjust window position
        self.master.geometry(f"400x550+{x}+{y}")

        self.ui = UIComponents(self.master, self)
        self.api_handler = APIHandler(API_URL)
        self.emitter = Emitter()
        self.recording_handler = RecordingHandler(self)
        self.keyboard_handler = KeyboardHandler(self)

        self.ui.paste_var.trace_add("write", self.update_paste_setting)

        self.keyboard_handler.setup_listener()

    def update_paste_setting(self, *args):
        should_paste = self.ui.paste_var.get()
        self.emitter.set_should_paste(should_paste)
        print(f"Debug: Updated paste setting to {should_paste}")

    def get_audio_devices(self):
        return get_audio_devices()

    def toggle_language(self):
        if self.ui.language_var.get() == "en":
            self.ui.language_var.set("de")
            playsound('./assets/sounds/german_toggle.wav')
        else:
            self.ui.language_var.set("en")
            playsound('./assets/sounds/english_toggle.wav')

    def toggle_recording(self):
        self.recording_handler.toggle_recording()

    def toggle_pin(self):
        is_pinned = self.master.attributes('-topmost')
        self.master.attributes('-topmost', not is_pinned)
        self.ui.update_pin_button(not is_pinned)
        print(f"Debug: Window {'unpinned' if is_pinned else 'pinned'}")

    def set_hotkeys(self):
        self.keyboard_handler.update_hotkeys()
        self.ui.update_hotkey_display()

    def on_close(self):
        self.recording_handler.audio_handler.stop_recording()
        if self.keyboard_handler.listener:
            self.keyboard_handler.listener.stop()
        self.master.destroy()
        print("Debug: Application closed")

def main():
    print(f"Debug: Using API URL: {API_URL}")
    print("Debug: Starting application")
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("dark-blue")

    root = ctk.CTk()
    app = TranscriptionApp(root)

    def signal_handler(sig, frame):
        print("Debug: CTRL+C pressed. Exiting...")
        app.on_close()
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)

    root.mainloop()

if __name__ == "__main__":
    main()
