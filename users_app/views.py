import json

from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .form import RegisterUserForm


# Create your views here.
@csrf_exempt
@require_http_methods(['POST'])
def regiter_user(request):
  if request.method != 'POST':
    return JsonResponse({
        "status": False,
        "data": { "message": "Method Not Allowed" }
      }, status=405)

  try:
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
        "data": { "message": e.message}
      }, status=400)
  except Exception as e:
    return JsonResponse({
        "status": False,
        "data": { "message": "Internal Server Error" }
      }, status=500)
