from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
@csrf_exempt
def check_status(request):
  if request.method != 'GET':
    return JsonResponse(
    {
      "status": False,
      "data": {
        "message": "Method Not Allowed"
      }
    }, status=405
  )

  return JsonResponse(
    {
      "status": True,
      "data": {
        "message": "API status OK"
      }
    }, status=200
  )

@csrf_exempt
def custom_404(request, exception):
  return JsonResponse(
    {
      "status": False,
      "data": {
        "message": "Endpoint Not Found"
      }
    }, status=404
  )