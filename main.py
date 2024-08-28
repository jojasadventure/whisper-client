import os
import customtkinter as ctk
import signal
import sys

from transcription_app import TranscriptionApp

API_URL = os.getenv('TRANSCRIPTION_API_URL', 'http://10.68.7.2:8000/v1/audio/transcriptions')

def main():
    print(f"Debug: Using API URL: {API_URL}")
    print("Debug: Starting application")
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("dark-blue")

    root = ctk.CTk()
    app = TranscriptionApp(root, API_URL)

    def signal_handler(sig, frame):
        print("Debug: CTRL+C pressed. Exiting...")
        app.on_close()
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)

    root.mainloop()

if __name__ == "__main__":
    main()