from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from django.http import JsonResponse
from . import video_processing_main
import json

@csrf_exempt
@api_view(['POST'])
def generate_clips(request):
    data = json.loads(request.body)
    video_url = data.get('url')
    results = video_processing_main.process_video(video_url)

    return JsonResponse({"clips": results}, status=200)