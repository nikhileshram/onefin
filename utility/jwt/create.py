import datetime
import jwt
from onefin_movie_collection import settings


SECRET_KEY = settings.SECRET_KEY

def create_jwt_token(user):
    
    payload = {
        'user_id': str(user.id),
        'username': user.username,
        'exp': datetime.now() + datetime.timedelta(days=1),  # Token expires in 1 day
        'iat': datetime.now(),  # Issued at time
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    
    return token