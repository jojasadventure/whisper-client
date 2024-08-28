"""
# Whisper API Transcription App

This is the main entry point for the Whisper API Transcription App. The application allows users to record audio, transcribe it using the OpenAI Whisper API, and automatically copy the transcription to the clipboard and paste it into the active window.

## Application Structure

The application consists of the following main components:

- `KeyboardHandler`: Handles keyboard events and hotkeys for recording and language switching.
- `RecordingHandler`: Manages the audio recording and transcription process.
- `TranscriptionApp`: The main application class that sets up the user interface and coordinates the different components.
- `UIComponents`: Defines the user interface elements and their interactions.
- `APIHandler`: Handles communication with the Whisper API server.
- `Emitter`: Manages the copying and pasting of transcriptions.

## Configuration

- The `TRANSCRIPTION_API_URL` environment variable can be set to specify the URL of the Whisper API server. If not set, it defaults to `http://10.68.7.2:8000/v1/audio/transcriptions`.
- Hotkeys for recording and language switching can be customized in the application's settings menu.
- The window size and position can be adjusted by modifying the `geometry` parameters in the `TranscriptionApp` class.

## Error Handling

- The application gracefully handles errors during the transcription process and displays appropriate error messages to the user.
- A signal handler is implemented to gracefully quit the application when CTRL+C is pressed in the terminal.

## Dependencies

- The application relies on several external libraries, including `customtkinter`, `playsound`, `pynput`, `pyperclip`, and `pyautogui`. These dependencies are listed in the `requirements.txt` file.

For more information on how to use and contribute to the Whisper API Transcription App, please refer to the README.md file.
"""
