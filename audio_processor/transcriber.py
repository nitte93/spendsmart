import whisper 
import numpy as np
from queue import Queue
from threading import Thread
import torch
from datetime import datetime, timedelta
from pydub import AudioSegment
import io
import tempfile
import subprocess
import logging
from openai import OpenAI
# from dotenv import load_dotenv
import os

logger = logging.getLogger(__name__)

class Transcriber:
    def __init__(self):
                # Load environment variables from .env file
        # load_dotenv()
        
        # Get the API key from environment variable
        # api_key = os.getenv('OPENAI_API_KEY')
        self.model = whisper.load_model("medium")
        self.data_queue = Queue()
        self.phrase_time = None
        self.transcription = ['']
        self.phrase_timeout = 3  # seconds
        self.openai_client = OpenAI(api_key="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")


        # Start the processing thread
        # Thread(target=self.process_audio, daemon=True).start()

    def process_audio(self):
        while True:
            try:
                now = datetime.utcnow()
                if not self.data_queue.empty():
                    phrase_complete = False
                    if self.phrase_time and now - self.phrase_time > timedelta(seconds=self.phrase_timeout):
                        phrase_complete = True
                    self.phrase_time = now

                    # Combine audio data from queue
                    # audio_data = b''.join(self.data_queue.queue)
                    # self.data_queue.queue.clear()

                    # # Convert to numpy array
                    # audio_np = np.frombuffer(audio_data, dtype=np.int16).astype(np.float32) / 32768.0

                    # # Transcribe
                    # result = self.model.transcribe(audio_np,  fp16=torch.cuda.is_available())
                    # text = result['text'].strip()
                    
                    # print(f"Transcribed text: {text}")
                    # Update transcription
                    # if phrase_complete:
                    #     self.transcription.append(text)
                    # else:
                    #     self.transcription[-1] = text

                    # print("Current transcription:", self.transcription[-1])
            except Exception as e:
                print(f"Error in audio processing: {e}")

    def add_audio(self, audio_data):
        self.data_queue.put(audio_data)

    def get_current_transcription(self):
        audio_data = b''.join(self.data_queue.queue)

        # Save the received audio data to a file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.webm') as temp_file:
            temp_file.write(audio_data)
            temp_file_path = temp_file.name

        logger.info(f"Saved received audio to: {temp_file_path}")

        # Play the audio file (this will only work if your server has audio output capabilities)
        try:
            subprocess.run(['ffplay', '-nodisp', '-autoexit', temp_file_path], check=True)
            logger.info("Audio playback completed")
        except subprocess.CalledProcessError as e:
            logger.error(f"Error playing audio: {str(e)}")
        except FileNotFoundError:
            logger.error("ffplay not found. Make sure FFmpeg is installed and in your PATH.")

        # print(f"Audio data: {audio_data}, self.data.queue: {len(self.data_queue.queue)}")
        self.data_queue.queue.clear()
        # Convert the incoming audio data to an AudioSegment
        print("Audio data:")
        audio_segment = AudioSegment.from_file(io.BytesIO(audio_data), format="webm")

        print("audio segment:")
        audio_segment = audio_segment.set_channels(1).set_frame_rate(16000)
        # print("convert to numpy array")
        samples = np.array(audio_segment.get_array_of_samples())

        # # Normalize
        # print("normalize")
        audio_np = samples.astype(np.float32) / 32768.0

        # Export as WAV file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_wav:
            logger.debug(f"Exporting as WAV to {temp_wav.name}...")
            audio_segment.export(temp_wav.name, format="wav")
        
        logger.info("Starting transcription with OpenAI Whisper API...")
        with open(temp_wav.name, 'rb') as audio_file:
            # transcript = self.openai_client.audio.transcriptions.create(
            #     model="whisper-1", 
            #     file=audio_file,
            #     response_format="text"
            # )
            transcript = self.model.transcribe(
                audio_np, 
                fp16=torch.cuda.is_available(),
                language='en',  # Specify language if known
                task='transcribe',
                temperature=0.2,  # Lower temperature for more focused sampling
                best_of=5,  # Generate multiple samples and return the best one
                beam_size=5,  # Use beam search
            )

        
        os.unlink(temp_wav.name)
        logger.debug("Temporary WAV file deleted")
        
        logger.info(f"Go fuck yourself: {transcript}")
        return transcript

        # # Convert to numpy array
        # print("convert to numpy array")
        # samples = np.array(audio_segment.get_array_of_samples())

        # # Normalize
        # print("normalize")
        # audio_np = samples.astype(np.float32) / 32768.0

        # # Transcribe
        # print("transcribe")
        # result = self.model.transcribe(
        #     audio_np, 
        #     fp16=torch.cuda.is_available(),
        #     language='en',  # Specify language if known
        #     task='transcribe',
        #     temperature=0.2,  # Lower temperature for more focused sampling
        #     best_of=5,  # Generate multiple samples and return the best one
        #     beam_size=5,  # Use beam search
        # )
        # text = result['text'].strip()
                    
        # print(f"Transcribed text: {text}")

        # return text

# Global transcriber instance
transcriber = Transcriber()