import os
from pytubefix import YouTube
from moviepy.editor import AudioFileClip
from openai import OpenAI
import logging
from pytube.exceptions import PytubeError
from pydub import AudioSegment

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

import yt_dlp
import os

client = OpenAI()

def download_youtube_audio(url, output_path):
    print("url", url)
    logger.error(f"Attempting to download audio from URL: {url}")
    try:
        yt = YouTube(url)
        logger.error(f"YouTube object created successfully: {yt.title}")
        
        # Try to get audio streams with specific formats
        audio_streams = yt.streams.filter(only_audio=True, file_extension='mp4')
        # audio_streams = yt.streams.filter(only_audio=True)
        if not audio_streams:
            logger.error("No audio streams found for this video")
            audio_streams = yt.streams.filter(only_audio=True)
        
        if not audio_streams:
            logger.error("No audio streams found for this video")
            raise ValueError("No audio streams found for this video")
            
        audio = audio_streams.first()
        logger.error(f"Selected audio stream: {audio}")
        
        output_file = audio.download(output_path=output_path, filename="audio.mp4")
        logger.error(f"Audio downloaded successfully to: {output_file}")
        
        return output_file
    except PytubeError as e:
        logger.error(f"PyTube error occurred: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"An unexpected error occurred: {str(e)}")
        raise

def convert_mp4_to_mp3(input_path, output_path):
    audio = AudioFileClip(input_path)
    audio.write_audiofile(output_path)
    audio.close()

def split_audio(input_file, max_size_mb=25):
    audio = AudioSegment.from_file(input_file)
    duration_ms = len(audio)
    chunk_size_ms = int((max_size_mb * 1024 * 1024 * 8) / (audio.frame_rate * audio.sample_width * audio.channels)) * 1000

    chunks = []
    for start in range(0, duration_ms, chunk_size_ms):
        end = min(start + chunk_size_ms, duration_ms)
        chunk = audio[start:end]
        chunk_file = f"{input_file}_chunk_{start}.mp3"
        chunk.export(chunk_file, format="mp3")
        chunks.append(chunk_file)
    return chunks

def transcribe_audio(audio_file_path):
    chunks = split_audio(audio_file_path)
    full_transcript = ""
    segments = []

    for chunk in chunks:
        with open(chunk, "rb") as audio_file:
            transcript = client.audio.transcriptions.create(
                model="whisper-1", 
                file=audio_file,
                response_format="verbose_json",
                timestamp_granularities=["word"]
            )
            # The transcript is now the entire response, not split into segments
            full_transcript += transcript.text + " "
            
            # Process words if available
            words = getattr(transcript, 'words', [])
            
            segment_info = {
                "text": transcript.text,
                "words": [{"word": w['word'], "start": w['start'], "end": w['end']} for w in words]
            }
            
            segments.append(segment_info)

        os.remove(chunk)  # Remove the temporary chunk file
    return segments

    # return full_transcript.strip()

def summarize_text(text):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that summarizes text."},
            {"role": "user", "content": f"Please summarize the following text:\n\n{text}"}
        ]
    )
    return response.choices[0].message.content