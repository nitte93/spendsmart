# consumers.py
import json
import numpy as np
from channels.generic.websocket import AsyncWebsocketConsumer
from faster_whisper import WhisperModel
from openai import OpenAI
import io
import wave
from pydub import AudioSegment
import tempfile
class SpeechConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        self.model = WhisperModel("base", device="cpu", compute_type="int8")
        self.audio_buffer = []
        self.openai_client = OpenAI()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data=None, bytes_data=None):
        if bytes_data:
            print(f"Received audio data of length: {len(bytes_data)}")
            with tempfile.NamedTemporaryFile(suffix=".mp3", delete=True) as temp_file:
                temp_file.write(bytes_data)
                temp_file_path = temp_file.name
                
                print(temp_file_path)
                audio_file= open(temp_file_path, "rb")

                transcript = self.openai_client.audio.transcriptions.create(
                model="whisper-1", 
                file=audio_file)
                
                print(f"transcript: {transcript.text}")
            # with tempfile.NamedTemporaryFile(suffix=".mp3", delete=True) as temp_file:
            #     temp_file.write(bytes_data)
            #     temp_file_path = temp_file.name
                
            #     print(temp_file_path)
            #     with open(temp_file_path, "rb") as audio_file:
            #         transcript_coroutine = self.openai_client.audio.transcriptions.create(
            #             model="whisper-1", 
            #             file=audio_file
            #         )
            #         transcript = await transcript_coroutine
                
            #     print(f"Transcription result: {transcript}")
                
            #     # Extract the text from the transcript
            #     transcribed_text = transcript.text if hasattr(transcript, 'text') else str(transcript)
                
            #     await self.send(text_data=json.dumps({
            #         'text': transcribed_text
            #     }))
        else:
            print("Received non-bytes data")

