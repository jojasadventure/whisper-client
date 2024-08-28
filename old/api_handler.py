import requests
import json

class APIHandler:
    def __init__(self, api_url):
        self.api_url = api_url
        print(f"Debug: API URL set to {self.api_url}")

    def upload_audio_to_whisper(self, file_path, language, prompt):
        try:
            with open(file_path, 'rb') as audio_file:
                files = {'file': ('audio.wav', audio_file, 'audio/wav')}
                data = {
                    'model': 'Systran/faster-whisper-medium',
                    'language': language,
                    'prompt': prompt,
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