import json
import logging
from channels.generic.websocket import AsyncWebsocketConsumer
import speech_recognition as sr
import io
import asyncio
import numpy as np

logger = logging.getLogger(__name__)

class SpeechRecognitionConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.recognizer = sr.Recognizer()
        self.audio_buffer = io.BytesIO()
        self.total_bytes_received = 0

    async def connect(self):
        await self.accept()
        logger.info("WebSocket connection established")

    async def receive(self, text_data=None, bytes_data=None):
        if bytes_data:
            self.total_bytes_received += len(bytes_data)
            self.audio_buffer.write(bytes_data)
            logger.info(f"Received {len(bytes_data)} bytes. Total received: {self.total_bytes_received}")

            # Process audio when we have received enough data (e.g., 5 seconds of audio)
            if self.total_bytes_received >= 160000:  # 16000 * 2 * 5 (5 seconds of 16kHz 16-bit audio)
                await self.process_audio()

    async def process_audio(self):
        self.audio_buffer.seek(0)
        audio_data = self.audio_buffer.read()

        logger.info(f"Audio data length: {len(audio_data)} bytes")

        if len(audio_data) == 0:
            logger.warning("Received empty audio data")
            return

        try:
            # Convert to numpy array
            numpy_data = np.frombuffer(audio_data, dtype=np.int16)
            logger.info(f"Numpy data shape: {numpy_data.shape}")

            # Check if the audio data has a reasonable amplitude
            if len(numpy_data) > 0 and np.abs(numpy_data).mean() > 100:
                # Create AudioData object
                audio = sr.AudioData(numpy_data.tobytes(), 16000, 2)

                try:
                    # Use Google's speech recognition
                    logger.info(f"Processing {len(numpy_data)} samples")
                    text = await asyncio.to_thread(self.recognizer.recognize_google, audio)
                    logger.info(f"Recognized: {text}")
                    await self.send(text_data=json.dumps({
                        'type': 'recognition_result',
                        'text': text,
                    }))
                except sr.UnknownValueError:
                    logger.info("Google Speech Recognition could not understand audio")
                    await self.send(text_data=json.dumps({
                        'type': 'recognition_error',
                        'error': 'Could not understand audio',
                    }))
                # ... rest of the error handling ...
            else:
                logger.info("Skipping processing due to empty or low amplitude audio")
        except Exception as e:
            logger.error(f"Error processing audio data: {str(e)}")
            await self.send(text_data=json.dumps({
                'type': 'recognition_error',
                'error': 'Error processing audio data',
            }))

        # Clear the buffer after processing
        self.audio_buffer = io.BytesIO()
        self.total_bytes_received = 0

    async def disconnect(self, close_code):
        logger.info(f"WebSocket disconnected. Total bytes received: {self.total_bytes_received}")