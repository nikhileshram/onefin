import redis
from django.conf import settings
from django.utils.deprecation import MiddlewareMixin

class IncrementRequestApiCountMiddleware(MiddlewareMixin):
    """
    Middleware to increment a Redis counter safely whenever the API is hit, 
    handling concurrent requests.
    """

    def __init__(self, get_response=None):
        super().__init__(get_response)
        # Configure your Redis connection
        self.redis_client = redis.StrictRedis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=settings.REDIS_DB
        )

    def process_view(self, request, view_func, view_args, view_kwargs):
        # Increment the counter only during the request phase
        if request.path.startswith("/"):
            key = settings.REDIS_COUNTER
            self.redis_client.incr(key)
            print('Redis key: ', self.redis_client.get(settings.REDIS_COUNTER))
