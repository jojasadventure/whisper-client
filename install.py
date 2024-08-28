import subprocess
import sys
import os

def install_requirements():
    print("Installing required packages from requirements.txt...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    except subprocess.CalledProcessError as e:
        print(f"Error installing packages: {e}")
        print("Note: If you encounter issues with PyAudio, make sure you have PortAudio installed.")
        sys.exit(1)
    print("All required packages installed successfully.")

def create_directories():
    print("Creating necessary directories...")
    os.makedirs("assets/images", exist_ok=True)
    os.makedirs("assets/sounds", exist_ok=True)
    print("Directories created.")

def main():
    print("Starting installation process for TranscriptionApp...")
    
    # Install required packages
    install_requirements()
    
    # Create necessary directories
    create_directories()
    
    print("\nInstallation complete!")
    print("Please ensure you have the following files in the correct directories:")
    print("assets/images/:")
    print("- appIcon.ico")
    print("- appIcon_recording.ico")
    print("- unpinned.png")
    print("- pinned.png")
    print("assets/sounds/:")
    print("- beep.wav")
    print("- english_toggle.wav")
    print("- german_toggle.wav")
    print("\nYou can now run the TranscriptionApp by executing main.py")

if __name__ == "__main__":
    main()
