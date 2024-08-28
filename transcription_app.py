import customtkinter as ctk
import threading
from playsound import playsound
from audio_handler import AudioHandler, get_audio_devices
from ui_components import UIComponents
from api_handler import APIHandler
from emitter import Emitter
from keyboard_handler import KeyboardHandler

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
                prompt = self.app.ui.prompt_entry.get("1.0", ctk.END).strip()
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
    def __init__(self, master, api_url):
        self.master = master
        self.master.title("Whisper API Transcription App")
        self.master.iconbitmap('assets/images/appIcon.ico')
        self.master.geometry("400x650")
        self.master.protocol("WM_DELETE_WINDOW", self.on_close)

        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        x = (screen_width - 400) // 2
        y = (screen_height - 550) // 2
        self.master.geometry(f"400x650+{x}+{y}")

        self.ui = UIComponents(self.master, self)
        self.api_handler = APIHandler(api_url)
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