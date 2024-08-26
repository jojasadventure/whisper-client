# Note, the variable below must be replaced with OpenAI audio compatible endpoint.
# self.api_url
#

import numpy as np
import os
import pyautogui
import customtkinter as ctk
import tkinter as tk
from PIL import Image
import requests
import sounddevice as sd
from scipy.io import wavfile
import threading
import tempfile
from playsound import playsound
from pynput import keyboard
import json
import pyperclip

class TranscriptionApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Whisper API Transcription App")
        self.master.iconbitmap('assets/images/appIcon.ico')
        self.master.geometry("400x425")
        self.master.protocol("WM_DELETE_WINDOW", self.on_close)

        self.unpinned_icon = ctk.CTkImage(Image.open('assets/images/unpinned.png'), size=(24, 24))
        self.pinned_icon = ctk.CTkImage(Image.open('assets/images/pinned.png'), size=(24, 24))

        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        x = (screen_width - 400) // 2
        y = (screen_height - 425) // 2
        self.master.geometry(f"400x425+{x}+{y}")

        main_frame = ctk.CTkFrame(self.master)
        main_frame.pack(fill="both", expand=True)

        self.create_device_selection(main_frame)
        self.create_language_selection(main_frame)
        self.create_hotkey_settings(main_frame)

        self.recording = False
        self.audio_data = []

        self.loading_label = ctk.CTkLabel(main_frame, text="", font=("Arial", 12, "bold"), fg_color="transparent")
        self.loading_label.pack(pady=10)

        self.pin_button = ctk.CTkButton(self.master, text='', image=self.unpinned_icon, command=self.toggle_pin,
                                        width=20, corner_radius=0, bg_color="transparent", fg_color="transparent")
        self.pin_button.place(relx=1, rely=0, anchor="ne")

        self.start_button = ctk.CTkButton(main_frame, text="Start Recording", command=self.toggle_recording)
        self.start_button.pack(pady=10)

        self.transcription_text = ctk.CTkTextbox(main_frame, height=100, width=380)
        self.transcription_text.pack(pady=10)

        self.api_url = 'http://10.68.7.2:8000/v1/audio/transcriptions'

        self.setup_keyboard_listener()

    def create_device_selection(self, frame):
        device_frame = ctk.CTkFrame(frame)
        device_frame.pack(pady=10)

        device_label = ctk.CTkLabel(device_frame, text="Select Audio Device:")
        device_label.grid(row=0, column=0, padx=10)

        self.device_var = tk.StringVar()
        device_options = [f"{i}: {device['name']}" for i, device in enumerate(sd.query_devices()) if device['max_input_channels'] > 0]
        self.device_dropdown = ctk.CTkComboBox(device_frame, variable=self.device_var, values=device_options, state="readonly")
        self.device_dropdown.set(device_options[0] if device_options else "No devices found")
        self.device_dropdown.grid(row=0, column=1)

    def create_language_selection(self, frame):
        language_frame = ctk.CTkFrame(frame)
        language_frame.pack(pady=10)

        language_label = ctk.CTkLabel(language_frame, text="Language:")
        language_label.grid(row=0, column=0, padx=10)

        self.language_var = tk.StringVar(value="en")
        self.language_button = ctk.CTkButton(language_frame, textvariable=self.language_var, command=self.toggle_language)
        self.language_button.grid(row=0, column=1)

    def create_hotkey_settings(self, frame):
        hotkey_frame = ctk.CTkFrame(frame)
        hotkey_frame.pack(pady=10)

        self.record_hotkey_var = tk.StringVar(value="Cmd+Ctrl+`")
        self.language_hotkey_var = tk.StringVar(value="Cmd+Ctrl+/")

        record_label = ctk.CTkLabel(hotkey_frame, text="Record Hotkey:")
        record_label.grid(row=0, column=0, padx=10, pady=5)
        record_entry = ctk.CTkEntry(hotkey_frame, textvariable=self.record_hotkey_var)
        record_entry.grid(row=0, column=1, padx=10, pady=5)

        language_label = ctk.CTkLabel(hotkey_frame, text="Language Hotkey:")
        language_label.grid(row=1, column=0, padx=10, pady=5)
        language_entry = ctk.CTkEntry(hotkey_frame, textvariable=self.language_hotkey_var)
        language_entry.grid(row=1, column=1, padx=10, pady=5)

        set_hotkeys_button = ctk.CTkButton(hotkey_frame, text="Set Hotkeys", command=self.set_hotkeys)
        set_hotkeys_button.grid(row=2, column=0, columnspan=2, pady=10)

        self.hotkey_display = ctk.CTkLabel(hotkey_frame, text="", font=("Arial", 10))
        self.hotkey_display.grid(row=3, column=0, columnspan=2, pady=5)
        self.update_hotkey_display()

    def set_hotkeys(self):
        self.RECORD_COMBINATION = self.parse_hotkey(self.record_hotkey_var.get())
        self.LANGUAGE_COMBINATION = self.parse_hotkey(self.language_hotkey_var.get())
        self.update_hotkey_display()
        print("Debug: Hotkeys updated")

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

    def update_hotkey_display(self):
        display_text = f"Record: {self.record_hotkey_var.get()}\nLanguage: {self.language_hotkey_var.get()}"
        self.hotkey_display.configure(text=display_text)

    def toggle_language(self):
        if self.language_var.get() == "en":
            self.language_var.set("de")
            playsound('./assets/german_toggle.wav')
        else:
            self.language_var.set("en")
            playsound('./assets/english_toggle.wav')

    def toggle_recording(self):
        if not self.recording:
            self.start_recording()
        else:
            self.stop_recording()

    def start_recording(self):
        self.master.iconbitmap('assets/images/appIcon_recording.ico')
        self.start_button.configure(text="Stop Recording")
        self.recording = True
        self.audio_data = []
        self.loading_label.configure(text="Recording...", fg_color="red", corner_radius=5)
        
        device_id = int(self.device_var.get().split(':')[0])
        
        def audio_callback(indata, frames, time, status):
            if status:
                print(f"Debug: Audio callback status: {status}")
            self.audio_data.append(indata.copy())

        self.stream = sd.InputStream(device=device_id, channels=1, callback=audio_callback, samplerate=16000)
        self.stream.start()
        print("Debug: Recording started")
        playsound('./assets/beep.wav')

    def stop_recording(self):
        self.master.iconbitmap('assets/images/appIcon.ico')
        self.start_button.configure(text="Start Recording")
        self.recording = False
        self.loading_label.configure(text="Processing...", fg_color="orange", corner_radius=5)
        
        if hasattr(self, 'stream'):
            self.stream.stop()
            self.stream.close()
        
        print("Debug: Recording stopped")
        threading.Thread(target=self.process_audio).start()

    def process_audio(self):
        if not self.audio_data:
            print("Debug: No audio data to process")
            self.loading_label.configure(text="No audio recorded", fg_color="red", corner_radius=5)
            return

        print("Debug: Processing audio")
        audio_data = np.concatenate(self.audio_data)
        
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
            wavfile.write(temp_file.name, 16000, audio_data)
            transcription = self.upload_audio_to_whisper(temp_file.name)
        
        os.unlink(temp_file.name)

        if transcription:
            print(f"Debug: Transcription received: {transcription}")
            self.transcription_text.delete("1.0", ctk.END)
            self.transcription_text.insert(ctk.END, transcription)
            pyperclip.copy(transcription)
            pyautogui.hotkey('command', 'v')  # This pastes the content
            self.loading_label.configure(text="Transcription complete", fg_color="green", corner_radius=5)
        else:
            self.loading_label.configure(text="Transcription failed", fg_color="red", corner_radius=5)

    def upload_audio_to_whisper(self, file_path):
        try:
            with open(file_path, 'rb') as audio_file:
                files = {'file': ('audio.wav', audio_file, 'audio/wav')}
                data = {
                    'model': 'Systran/faster-whisper-medium',
                    'language': self.language_var.get(),
                }
                print(f"Debug: Sending request to {self.api_url}")
                print(f"Debug: Request data: {data}")
                response = requests.post(self.api_url, files=files, data=data)
            
            print(f"Debug: Response status code: {response.status_code}")
            print(f"Debug: Response headers: {response.headers}")
            print(f"Debug: Response content: {response.text}")
            
            if response.status_code == 200:
                try:
                    result = response.json()
                    transcription = result.get('text', '')
                    if not transcription:
                        print("Debug: Received empty transcription from server")
                    else:
                        print(f"Debug: Received transcription: {transcription}")
                    return transcription
                except json.JSONDecodeError:
                    print("Debug: Failed to parse JSON response")
                    return response.text
            else:
                print(f"Debug: Error: {response.status_code} - {response.text}")
                return ''
        except Exception as e:
            print(f"Debug: Error during upload: {e}")
            return ''

    def toggle_pin(self):
        if self.master.attributes('-topmost'):
            self.master.attributes('-topmost', False)
            self.pin_button.configure(image=self.unpinned_icon)
            print("Debug: Window unpinned")
        else:
            self.master.attributes('-topmost', True)
            self.pin_button.configure(image=self.pinned_icon)
            print("Debug: Window pinned")

    def setup_keyboard_listener(self):
        self.RECORD_COMBINATION = self.parse_hotkey(self.record_hotkey_var.get())
        self.LANGUAGE_COMBINATION = self.parse_hotkey(self.language_hotkey_var.get())
        self.current = set()
        self.listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
        self.listener.start()
        print("Debug: Keyboard listener setup complete")

    def on_press(self, key):
        self.current.add(key)
        if all(k in self.current for k in self.RECORD_COMBINATION):
            print("Debug: Record hotkey combination pressed")
            self.master.after(0, self.toggle_recording)
        elif all(k in self.current for k in self.LANGUAGE_COMBINATION):
            print("Debug: Language toggle hotkey combination pressed")
            self.master.after(0, self.toggle_language)

    def on_release(self, key):
        try:
            self.current.remove(key)
        except KeyError:
            pass

    def on_close(self):
        if hasattr(self, 'stream'):
            self.stream.stop()
            self.stream.close()
        if hasattr(self, 'listener'):
            self.listener.stop()
        self.master.destroy()
        print("Debug: Application closed")

def main():
    print("Debug: Starting application")
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("dark-blue")

    root = ctk.CTk()
    app = TranscriptionApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()