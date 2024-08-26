# whisper-client
Very simple Python based client for Whisper compatible endpoint

I made this to replace built in macOS transcription with a private whisper openai compatible endpoint i.e. https://github.com/fedirz/faster-whisper-server

It listens to a hotkey (CTRL CMD `) to toggle recording and will transcribe at the end (not streaming right now) and input keys to wherever window i am at the given moment when the transcription is ready. 

NOTE  experimental!!! , will not work out of the box, needs assets, only tested on older mac os, will play havoc if you accidentally tab away while it's inputting characters


# status 26-08-24

# TranscriptionApp Project Status Report

## Date: August 26, 2024

### Current Status

The TranscriptionApp has been successfully refactored and enhanced with several new features. All functionalities are working as intended.

### Key Features Implemented

1. **Language Toggle:**
   - Separate hotkey for toggling between English and German
   - Visual indicator in the UI for current language
   - Sound feedback for language changes

2. **Configurable Hotkeys:**
   - User interface for setting custom hotkeys for recording and language toggle
   - Display of current hotkey settings in the UI

3. **Clipboard Integration:**
   - Automatic copying of transcribed text to clipboard
   - Instant pasting of transcribed text using system paste command

4. **Enhanced UI:**
   - Increased window size to accommodate new features
   - Added frames for language selection and hotkey configuration

5. **Improved Error Handling and Debugging:**
   - Additional debug print statements throughout the code

6. **Retained Core Functionalities:**
   - Audio device selection
   - Start/Stop recording with visual feedback
   - Window pinning
   - Transcription display in the app

### Recent Changes

1. Implemented separate hotkeys for recording toggle (default: Cmd+Ctrl+`) and language toggle (default: Cmd+Ctrl+/)
2. Added UI elements for custom hotkey configuration
3. Integrated clipboard functionality for instant pasting of transcribed text
4. Updated the process_audio method to use clipboard for text insertion
5. Refactored keyboard listener setup to use configurable hotkeys

### Next Steps

1. Conduct thorough testing of all new features, especially under various system conditions
2. Consider implementing a configuration file to save user preferences (e.g., preferred language, custom hotkeys)
3. Explore options for supporting additional languages beyond English and German
4. Investigate potential improvements in transcription accuracy or speed
5. Consider adding a feature for saving transcription history

### Open Issues

None reported at this time. All implemented features are functioning as expected.

### Project Files Status

1. `TranscriptionApp.py`: Up to date with all recent changes and new features
2. `assets/images/appIcon.ico`: Current
3. `assets/images/appIcon_recording.ico`: Current
4. `assets/images/unpinned.png`: Current
5. `assets/images/pinned.png`: Current
6. `assets/beep.wav`: Current
7. `assets/english_toggle.wav`: Current
8. `assets/german_toggle.wav`: Current

### Dependencies

Ensure all required libraries are installed:
- customtkinter
- pynput
- sounddevice
- scipy
- requests
- pillow
- pyautogui
- pyperclip

### Notes

The project has made significant progress with the implementation of user-requested features. The application now offers a more flexible and user-friendly experience with configurable hotkeys and improved language switching capabilities.
