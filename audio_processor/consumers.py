import asyncio
import json
import numpy as np
import librosa
from channels.generic.websocket import AsyncWebsocketConsumer
from pytubefix import YouTube
import os
import openai
from pydub import AudioSegment
import soundfile as sf
import tempfile  # Add this import
from collections import deque
import base64
from pydub.silence import split_on_silence
from .transcriber import transcriber
from threading import Thread

SAMPLE_RATE = 16000  # Common sample rate for speech processing

MIN_AUDIO_LENGTH = 0.1  # Minimum audio length in seconds
# SAMPLE_RATE = 44100  # Assuming this is your sample rate


SAMPLE_RATE = 16000  # Common sample rate for speech processing

class AudioProcessorConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        self.audio_buffer = np.array([], dtype=np.float32)
        self.openai_client = openai.AsyncOpenAI()
        
        # Download and prepare YouTube audio
        youtube_url = "https://www.youtube.com/watch?v=DkugNK9EvBw"
        self.youtube_audio = await self.prepare_youtube_audio(youtube_url)
        self.youtube_index = 0
        self.buffer = b''
        self.chunk_queue = deque()
        self.processing_task = None
        self.buffer_lock = asyncio.Lock()
        self.chunk_size = 80000  # 2 seconds at 16kHz
        self.overlap = 8000  # 0.5 second overlap
        self.processing_task = None
        
    async def prepare_youtube_audio(self, url):
        yt = YouTube(url)
        audio_stream = yt.streams.filter(only_audio=True).first()
        output_path = audio_stream.download(filename="temp_audio")
        audio = AudioSegment.from_file(output_path)
        audio = audio.set_frame_rate(SAMPLE_RATE).set_channels(1)
        samples = np.array(audio.get_array_of_samples(), dtype=np.float32) / 32768.0
        os.remove(output_path)
        return samples

    async def receive(self, text_data=None, bytes_data=None):
        # print("Received data:")
        if text_data:
            try:
                text_data_json = json.loads(text_data)
                message_type = text_data_json.get('type')
                print(f"Message type: {message_type}")
                if message_type == 'full_audio':
                    audio_data = base64.b64decode(text_data_json.get('audio_data'))
                    await self.process_full_audio(audio_data)
                    transcription = transcriber.get_current_transcription()
                    await self.send(text_data=json.dumps({
                        'transcription': transcription
                    }))
                    
                elif message_type == 'start_chunked_processing':
                    # if self.processing_task is None or self.processing_task.done():
                        # self.processing_task = asyncio.create_task(self.process_chunks())
                    print("Starting chunked processing")
                    # Thread(target=transcriber.process_audio, daemon=True).start(),,/
                else:
                    await self.send(text_data=json.dumps({
                        'type': 'error',
                        'message': f"Unknown message type: {message_type}"
                    }))
            except json.JSONDecodeError:
                await self.send(text_data=json.dumps({
                    'type': 'error',
                    'message': "Invalid JSON format"
                }))
        elif bytes_data:
            # async with self.buffer_lock:
            #     self.buffer += bytes_data
            #     while len(self.buffer) >= self.chunk_size:
            #         chunk = self.buffer[:self.chunk_size]
            #         self.chunk_queue.append(chunk)
            #         self.buffer = self.buffer[self.chunk_size - self.overlap:]

            # Add audio data to the queue
            transcriber.add_audio(bytes_data)
            
            # Get and send current transcription
            # transcription = transcriber.get_current_transcription()
            # await self.send(text_data=json.dumps({
            #     'transcription': transcription
            # }))


    async def process_chunks(self):
        print("Processing chunks------------------------------------------------------------>")
        while True:
            if self.chunk_queue:
                chunk = self.chunk_queue.popleft()
                await self.process_audio(chunk)
            else:
                await asyncio.sleep(0.1)  # Short sleep to prevent busy-waiting

    async def process_audio(self, audio_data):
        print("Processing audio------------------------------------------------------------>")

        try:
            audio_segment = AudioSegment(
                audio_data,
                frame_rate=16000,
                sample_width=2,
                channels=1
            )

            chunks = split_on_silence(audio_segment, min_silence_len=500, silence_thresh=-40)
            print(f"Number of chunks: {len(chunks)}")
            for chunk in chunks:
                # mp3_path = await self.webm_to_mp3(chunk)
                # print(f"MP3 path: {mp3_path}")
                with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_audio:
                    chunk.export(temp_audio.name, format="wav")
                    user_transcription = await self.transcribe_audio(temp_audio.name)
                    print(f"User transcription: {user_transcription}")
                    if user_transcription:
                        await self.send(text_data=json.dumps({
                            'type': 'transcription',
                            'text': user_transcription
                        }))

        except Exception as e:
            error_message = f"Error processing audio: {str(e)}"
            await self.send(text_data=json.dumps({
                'type': 'error',
                'message': error_message
            }))


    async def process_full_audio(self, audio_data):
        try:
            # Convert WebM to numpy array
            mp3_path = await self.webm_to_mp3(audio_data)
                        
            user_transcription = await self.transcribe_audio(mp3_path)
            if user_transcription:
                await self.send(text_data=json.dumps({
                    'type': 'full_transcription',
                    'text': user_transcription
                }))
        except Exception as e:
            error_message = f"Error processing full audio: {str(e)}"
            await self.send(text_data=json.dumps({
                'type': 'error',
                'message': error_message
            }))

    async def webm_to_mp3(self, webm_data):
        # Save the received audio data to a temporary file
        with tempfile.NamedTemporaryFile(suffix='.webm', delete=False) as temp_webm:
            temp_webm.write(webm_data)
            temp_webm_path = temp_webm.name

        # Convert WebM to MP3 (Whisper requires MP3 format)
        audio = AudioSegment.from_file(temp_webm_path, format="webm")
        mp3_path = temp_webm_path.replace(".webm", ".mp3")
        audio.export(mp3_path, format="mp3")
        
        os.remove(temp_webm_path)
        return mp3_path

    async def transcribe_audio(self, mp3_path):
        try:
            with open(mp3_path, 'rb') as audio_file:
                transcript = await self.openai_client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,
                    response_format="text",
                    language="en"
                )
            return transcript
        except Exception as e:
            print(f"Transcription error: {str(e)}")
            return None

    def compare_audio(self, user_chunk, youtube_chunk):
        # Implement audio comparison logic here
        # This is a simplified example
        user_volume = np.mean(np.abs(user_chunk))
        youtube_volume = np.mean(np.abs(youtube_chunk))
        
        if user_volume > youtube_volume * 1.2:
            return "Speaking too loudly"
        elif user_volume < youtube_volume * 0.8:
            return "Speaking too softly"
        else:
            return "Volume is good"


class TestConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print("TestConsumer: Connection attempt")
        await self.accept()
        await self.send(text_data="Hello from TestConsumer!")

    async def disconnect(self, close_code):
        print(f"TestConsumer: Disconnected with code {close_code}")

    async def receive(self, text_data):
        print(f"TestConsumer: Received {text_data}")
        await self.send(text_data=f"You said: {text_data}")