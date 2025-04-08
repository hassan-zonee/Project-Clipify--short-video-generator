from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from django.http import JsonResponse
from .video_processing_main import process_video
import json

@csrf_exempt
@api_view(['POST'])
def generate_clips(request):
    try:
        data = json.loads(request.body)
        video_url = data.get('url')
        results = process_video(video_url)

        return JsonResponse({"clips": results[:100]}, status=200)

    except Exception as e:
        return JsonResponse({'error': "Error: " + str(e)}, status=400)