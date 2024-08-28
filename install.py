import subprocess
import sys
import os
from config_handler import ConfigHandler

def install_requirements():
    print("Installing required packages from requirements.txt...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    except subprocess.CalledProcessError as e:
        print(f"Error installing packages: {e}")
        print("Note: If you encounter issues with PyAudio, make sure you have PortAudio installed.")
        sys.exit(1)
    print("All required packages installed successfully.")

""" def create_directories():
    print("Creating necessary directories...")
    os.makedirs("assets/images", exist_ok=True)
    os.makedirs("assets/sounds", exist_ok=True)
    print("Directories created.") """

def setup_config():
    config = ConfigHandler()
    print("Enter the API URL in the format: http(s)://domain:port/v1/audio/transcriptions")
    api_url = input("Full Whisper API URL: ")
    config.set('API_URL', api_url)
    print("Configuration saved.")

def main():
    print("Starting installation process for TranscriptionApp...")
    setup_config()
    install_requirements()
    # create_directories()
    

    print("\nInstallation complete!")
    print("\nYou can now run the TranscriptionApp by executing main.py")

"""     print("Please ensure you have the following files in the correct directories:")
    print("assets/images/:")
    print("- appIcon.ico")
    print("- appIcon_recording.ico")
    print("- unpinned.png")
    print("- pinned.png")
    print("assets/sounds/:")
    print("- beep.wav")
    print("- english_toggle.wav")
    print("- german_toggle.wav") """

    

if __name__ == "__main__":
    main()