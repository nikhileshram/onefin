from rest_framework import views
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from django.conf import settings
import redis
from django.http import JsonResponse

class RequestCountView(views.APIView):

    permission_classes = [IsAuthenticated]

    def __init__(self):
        self.redis_client = redis.StrictRedis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=settings.REDIS_DB
        )

    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            request_counter = int(self.redis_client.get(settings.REDIS_COUNTER))
            print('request counter: ', request_counter)
            return JsonResponse({'requests': request_counter})
        except Exception as e:
            return JsonResponse({'error': str(e)})

    def post(self, request):
        try:
            self.redis_client.set(settings.REDIS_COUNTER, 0)
            print(self.redis_client.get(settings.REDIS_COUNTER))
            return JsonResponse({'message': 'request count reset successfully'})
        except Exception as e:
            return JsonResponse({'error': str(e)})