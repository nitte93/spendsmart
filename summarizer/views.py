import os
import tempfile
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.conf import settings
from .utils import download_youtube_audio, convert_mp4_to_mp3, transcribe_audio, summarize_text

@csrf_exempt
@require_http_methods(["POST"])
def summarize_youtube_video(request):
    try:
        data = json.loads(request.body)
        youtube_url = data.get('url')
        print(youtube_url)
        if not youtube_url:
            return JsonResponse({'error': 'YouTube URL is required'}, status=400)

        try:
            with tempfile.TemporaryDirectory() as temp_dir:
                # Download YouTube audio
                print("audio_mp4_path")
                audio_mp4_path = download_youtube_audio(youtube_url, temp_dir)
                print("audio_mp4_path", audio_mp4_path)
                # Convert MP4 to MP3
                audio_mp3_path = os.path.join(temp_dir, "audio.mp3")
                convert_mp4_to_mp3(audio_mp4_path, audio_mp3_path)
                
                # Transcribe audio
                transcript = transcribe_audio(audio_mp3_path)
                # print("transcript", transcript)
                # Summarize transcript
                # summary = summarize_text(transcript)
                summary = "summary"
                print("summary", summary)
            return JsonResponse({'summary': summary, 'transcript': transcript})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)