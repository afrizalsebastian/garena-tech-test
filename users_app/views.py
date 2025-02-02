import json
import math
from datetime import datetime, timedelta, timezone

import jwt
from django.conf import settings
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from django.http import JsonResponse

from .form import (InputReferralCode, LoginUserForm, RegisterUserForm,
                   UpdateUserForm)
from .models import User


##############
## REGISTER ##
##############
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

###########
## LOGIN ##
###########
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
  
############
## UPDATE ##
############
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

#####################
## INSERT REFERRAL ##
#####################
def insert_referral(request):
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
      insert_form = InputReferralCode(body)
      if insert_form.is_valid():

        if request.user.own_code == body['referral_code']:
          raise ValidationError('Referral code can\'t use own code.')

        insert_form.save(instance=request.user)
        return JsonResponse({
          "status": True,  
          "data": { "message": "Referral code suscessfully used."}
        }, status=200)
      else:
        errors_message = ''
        for field, errors in insert_form.errors.items():
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
  
###############
## FIND USER ##
###############
def find_user(request):
  if request.method != 'GET':
    return JsonResponse({
        "status": False,  
        "data": { "message": "Method not allowed"}
      }, status=405)
  
  page = request.GET.get('page', 1)
  rows = request.GET.get('rows', 10)
  search_query = request.GET.get('query', '')

  try:
    page = int(page)
    rows = int(rows)
  except ValueError:
    page = 1
    rows = 10

  if rows < 1 :
    return JsonResponse({
      "status": False,  
      "data": { "message": "rows invalid"}
    }, status=400)
  
  try:
    user_count = User.objects.filter(name__icontains=search_query).count()
    if user_count < 1:
      return JsonResponse({
        "status": True,  
        "data": {
          "users": [],
          "page": page,
          "total_page": 0,
        }
      }, status=200)

    max_page = math.ceil(user_count/rows)
    if page < 1 or page > max_page:
      return JsonResponse({
        "status": False,  
        "data": { "message": "page index out of range or invalid"}
      }, status=400)
    

    start = (page - 1) * rows
    end = page * rows
    users = User.objects.filter(name__icontains=search_query).order_by('id')[start:end]    
    
    data = {
      "users": list(map(lambda user: user.to_dict(), users)),
      "page": page,
      "total_page": max_page
    }

    return JsonResponse({
      "status": True,  
      "data": data
    }, status=200)
  
  except Exception as e:
    return JsonResponse({
        "status": False,
        "error": { "message": "Internal Server Error" }
      }, status=500)