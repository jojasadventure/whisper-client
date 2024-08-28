import customtkinter as ctk
import tkinter as tk
from PIL import Image

class UIComponents:
    def __init__(self, master, app):
        self.master = master
        self.app = app
        self.setup_ui()

    def setup_ui(self):
        self.unpinned_icon = ctk.CTkImage(Image.open('assets/images/unpinned.png'), size=(24, 24))
        self.pinned_icon = ctk.CTkImage(Image.open('assets/images/pinned.png'), size=(24, 24))

        main_frame = ctk.CTkFrame(self.master)
        main_frame.pack(fill="both", expand=True)

        self.create_device_selection(main_frame)
        self.create_language_selection(main_frame)
        self.create_hotkey_settings(main_frame)

        # Add paste checkbox above the start button and transcription text
        self.paste_var = tk.BooleanVar(value=True)
        self.paste_checkbox = ctk.CTkCheckBox(main_frame, text="Paste after copying", variable=self.paste_var)
        self.paste_checkbox.pack(pady=5)

        # Add prompt entry field
        self.prompt_label = ctk.CTkLabel(main_frame, text="Prompt:")
        self.prompt_label.pack(pady=(10, 5))
        self.prompt_entry = ctk.CTkTextbox(main_frame, height=50, width=380, border_width=1, corner_radius=5)
        self.prompt_entry.pack(pady=(0, 10))

        self.start_button = ctk.CTkButton(main_frame, text="Start Recording", command=self.app.toggle_recording)
        self.start_button.pack(pady=10)

        self.transcription_text = ctk.CTkTextbox(main_frame, height=100, width=380)
        self.transcription_text.pack(pady=10)

        self.loading_label = ctk.CTkLabel(main_frame, text="", font=("Arial", 12, "bold"), fg_color="transparent")
        self.loading_label.pack(pady=10)

        self.pin_button = ctk.CTkButton(self.master, text='', image=self.unpinned_icon, command=self.app.toggle_pin,
                                        width=20, corner_radius=0, bg_color="transparent", fg_color="transparent")
        self.pin_button.place(relx=1, rely=0, anchor="ne")

    def create_device_selection(self, frame):
        device_frame = ctk.CTkFrame(frame)
        device_frame.pack(pady=10)

        device_label = ctk.CTkLabel(device_frame, text="Select Audio Device:")
        device_label.grid(row=0, column=0, padx=10)

        self.device_var = tk.StringVar()
        device_options = self.app.get_audio_devices()
        self.device_dropdown = ctk.CTkComboBox(device_frame, variable=self.device_var, values=device_options, state="readonly")
        self.device_dropdown.set(device_options[0] if device_options else "No devices found")
        self.device_dropdown.grid(row=0, column=1)

    def create_language_selection(self, frame):
        language_frame = ctk.CTkFrame(frame)
        language_frame.pack(pady=10)

        language_label = ctk.CTkLabel(language_frame, text="Language:")
        language_label.grid(row=0, column=0, padx=10)

        self.language_var = tk.StringVar(value="en")
        self.language_button = ctk.CTkButton(language_frame, textvariable=self.language_var, command=self.app.toggle_language)
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

        set_hotkeys_button = ctk.CTkButton(hotkey_frame, text="Set Hotkeys", command=self.app.set_hotkeys)
        set_hotkeys_button.grid(row=2, column=0, columnspan=2, pady=10)

        self.hotkey_display = ctk.CTkLabel(hotkey_frame, text="", font=("Arial", 10))
        self.hotkey_display.grid(row=3, column=0, columnspan=2, pady=5)
        self.update_hotkey_display()

    def update_hotkey_display(self):
        display_text = f"Record: {self.record_hotkey_var.get()}\nLanguage: {self.language_hotkey_var.get()}"
        self.hotkey_display.configure(text=display_text)

    def update_pin_button(self, is_pinned):
        self.pin_button.configure(image=self.pinned_icon if is_pinned else self.unpinned_icon)

    def update_start_button(self, is_recording):
        self.start_button.configure(text="Stop Recording" if is_recording else "Start Recording")

    def update_loading_label(self, text, color):
        self.loading_label.configure(text=text, fg_color=color, corner_radius=5)

    def update_transcription_text(self, text):
        self.transcription_text.delete("1.0", ctk.END)
        self.transcription_text.insert(ctk.END, text)