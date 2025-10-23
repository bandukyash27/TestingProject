from datetime import datetime, timedelta
from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
import jwt
def create_jwt_token(user):
    """Generate JWT token for user"""
    payload = {
        'user_id': user.id,
        'username': user.username,
        'exp': datetime.utcnow() + timedelta(seconds=settings.JWT_EXPIRATION_DELTA),
        'iat': datetime.utcnow()
    }
    token = jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
    return token




def decode_jwt_token(token):
    """Decode and verify JWT token"""
    try:    
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

# authentication.py - Django Ninja Auth class
from ninja.security import HttpBearer
from django.contrib.auth.models import User

class JWTAuth(HttpBearer):
    def authenticate(self, request, token):
        payload = decode_jwt_token(token)
        if payload:
            try:
                user = User.objects.get(id=payload['user_id'])
                return user
            except User.DoesNotExist:
                return None
        return None
