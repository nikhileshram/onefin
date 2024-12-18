import jwt
from onefin_movie_collection import settings


SECRET_KEY = settings.SECRET_KEY

def decode_jwt_token(token):
    try:
        decoded_payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return decoded_payload
    except jwt.ExpiredSignatureError:
        raise Exception("Token has expired")
    except jwt.InvalidTokenError:
        raise Exception("Invalid token")