
import jwt
from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin

from .models import User


class JWTAuthenticationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        auth_header: str = request.headers.get('Authorization')
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(" ")[1]
            
            try:
                claims = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
                user = User.objects.get(id=claims['user_id'])
                print(user)
                request.user = user
            except jwt.ExpiredSignatureError:
                request.auth_err_message = "Token expired"
                request.user = AnonymousUser()
            except jwt.InvalidTokenError:
                request.auth_err_message = "Invalid token"
                request.user = AnonymousUser()
            except Exception as e:
                return JsonResponse({
                    "status": False,
                    "error": { "message": "Internal Server Error" }
                }, status=500)
        else:
            request.auth_err_message = "Token missing"
            request.user = AnonymousUser()
