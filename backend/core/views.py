from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from django.http import JsonResponse
import json

@csrf_exempt
@api_view(['POST'])
def process_video(request):
    try:
        data = json.loads(request.body)
        video_url = data.get('url')
        print(video_url)

        clips = [
            {
                "title": "Sample Clip",
                "thumbnail": "https://picsum.photos/400/225?random=1",
                "url": "https://example.com/sample-clip.mp4"
            },
            {
                "title": "Sample Clip",
                "thumbnail": "https://picsum.photos/400/225?random=1",
                "url": "https://example.com/sample-clip.mp4"
            },
            {
                "title": "Sample Clip",
                "thumbnail": "https://picsum.photos/400/225?random=1",
                "url": "https://example.com/sample-clip.mp4"
            },
            {
                "title": "Sample Clip",
                "thumbnail": "https://picsum.photos/400/225?random=1",
                "url": "https://example.com/sample-clip.mp4"
            }
        ]

        return JsonResponse({"clips": clips}, status=200)

    except Exception as e:
        return JsonResponse({'error': "Error: " + str(e)}, status=400)