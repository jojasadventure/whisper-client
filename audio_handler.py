import numpy as np
import sounddevice as sd
from scipy.io import wavfile
import tempfile
import os

class AudioHandler:
    def __init__(self):
        self.audio_data = []
        self.stream = None

    def start_recording(self, device_id):
        self.audio_data = []

        def audio_callback(indata, frames, time, status):
            if status:
                print(f"Debug: Audio callback status: {status}")
            self.audio_data.append(indata.copy())

        self.stream = sd.InputStream(device=device_id, channels=1, callback=audio_callback, samplerate=16000)
        self.stream.start()
        print("Debug: Recording started")

    def stop_recording(self):
        if self.stream:
            self.stream.stop()
            self.stream.close()
        print("Debug: Recording stopped")

    def get_audio_data(self):
        if not self.audio_data:
            print("Debug: No audio data to process")
            return None

        print("Debug: Processing audio")
        return np.concatenate(self.audio_data)

    def save_audio_to_file(self):
        audio_data = self.get_audio_data()
        if audio_data is None:
            return None

        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
            wavfile.write(temp_file.name, 16000, audio_data)
            return temp_file.name

    @staticmethod
    def cleanup_audio_file(file_path):
        os.unlink(file_path)

def get_audio_devices():
    return [f"{i}: {device['name']}" for i, device in enumerate(sd.query_devices()) if device['max_input_channels'] > 0]