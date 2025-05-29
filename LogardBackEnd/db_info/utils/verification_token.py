import jwt
from datetime import datetime, timedelta
from django.conf import settings

def generate_verification_token(user):
    payload = {
        'user_id': user.id,
        'exp': datetime.utcnow() + timedelta(hours=1),
        'iat': datetime.utcnow()
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
    # PyJWT 2.x devuelve un str, en 1.x un bytes, en caso bytes: token.decode('utf-8')
    return token