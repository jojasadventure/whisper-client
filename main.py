import customtkinter as ctk
import signal
import sys

from transcription_app import TranscriptionApp

def main():
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