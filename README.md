# whisper-client
Very simple Python based client for Whisper compatible endpoint

I made this to replace built in macOS transcription with a private whisper openai compatible endpoint i.e. https://github.com/fedirz/faster-whisper-server

It listens to a hotkey (CTRL CMD `) to toggle recording and will transcribe at the end (not streaming right now) and input keys to wherever window i am at the given moment when the transcription is ready. 

NOTE  experimental!!! , will not work out of the box, needs assets, only tested on older mac os, will play havoc if you accidentally tab away while it's inputting characters
