import json
from datetime import datetime, timedelta, timezone

import jwt
from django.conf import settings
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from django.http import JsonResponse

from .form import LoginUserForm, RegisterUserForm, UpdateUserForm


def regiter_user(request):
  if request.method != 'POST':
    return JsonResponse({
        "status": False,  
        "data": { "message": "Method not allowed"}
      }, status=405)

  try:
    if not request.body:
      raise ValidationError("Required body request")

    body = json.loads(request.body)
    register_form = RegisterUserForm(body)

    if register_form.is_valid():
      user = register_form.save()
      return JsonResponse({
        "status": True,  
        "data": user.to_dict()
      }, status=201)
    else:
      errors_message = ''
      for field, errors in register_form.errors.items():
        errors_message += '{}: {} '.format(field, ','.join(errors))
      raise ValidationError(errors_message)
    
  except ValidationError as e:
    return JsonResponse({
        "status": False,  
        "error": { "message": e.message}
      }, status=400)
  
  except Exception as e:
    return JsonResponse({
        "status": False,
        "error": { "message": "Internal Server Error" }
      }, status=500)

def login(request):
  if request.method != 'POST':
    return JsonResponse({
        "status": False,  
        "data": { "message": "Method not allowed"}
      }, status=405)
  
  try:
    if not request.body:
      raise ValidationError("Required body request")

    body = json.loads(request.body)
    login_form = LoginUserForm(body)

    if login_form.is_valid():
      user = authenticate(username=login_form.get_username, password=login_form.get_password)
      if user:
        claims = {
          "user_id": user.id,
          "exp": datetime.now(tz=timezone.utc) + timedelta(hours=6),
          "iat": datetime.now(tz=timezone.utc)
        }

        token = jwt.encode(claims, settings.SECRET_KEY, algorithm='HS256')

        return JsonResponse({
          "status": True,  
          "data": { "token": token }
        }, status=201)

      else:
        raise ValidationError('username or password incorrect')

    else:
      errors_message = ''
      for field, errors in login_form.errors.items():
        errors_message += '{}: {} '.format(field, ','.join(errors))
      raise ValidationError(errors_message) 

  except ValidationError as e:
    return JsonResponse({
        "status": False,  
        "error": { "message": e.message}
      }, status=400)
      
  except Exception as e:
    return JsonResponse({
        "status": False,
        "error": { "message": "Internal Server Error" }
      }, status=500)
  
def update_user(request):
  if request.method != 'PUT':
    return JsonResponse({
        "status": False,  
        "data": { "message": "Method not allowed"}
      }, status=405)
  
  try:
    if not request.body:
      raise ValidationError("Required body request")

    body = json.loads(request.body)
    if request.user.is_authenticated:
      update_form = UpdateUserForm(body)
      if update_form.is_valid():
        user = update_form.save(request.user)
        return JsonResponse({
          "status": True,  
          "data": user.to_dict()
        }, status=200)
      else:
        errors_message = ''
        for field, errors in update_form.errors.items():
          errors_message += '{}: {} '.format(field, ','.join(errors))
        raise ValidationError(errors_message)
      
    else:
        return JsonResponse({
          "status": False,
          "error": { "message": request.auth_err_message }
        }, status=401)
    
  except ValidationError as e:
    return JsonResponse({
        "status": False,  
        "error": { "message": e.message}
      }, status=400)
  
  except Exception as e:
    return JsonResponse({
        "status": False,
        "error": { "message": "Internal Server Error" }
      }, status=500)