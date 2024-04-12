from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from .models import UploadedFile
from rest_framework.decorators import api_view
from rest_framework.parsers import MultiPartParser

# Create your views here.
def index(request, question_id):
    return HttpResponse("You're inside upload index %s." % question_id)


@api_view(['POST'])
def upload_file(request):
    if request.method == 'POST':
        file = request.FILES['file']
        uploaded_file = UploadedFile(file=file)
        uploaded_file.save()
        return JsonResponse({'message': 'File uploaded successfully!'}, status=200)

    return JsonResponse({'error': 'An error occurred'}, status=400)
