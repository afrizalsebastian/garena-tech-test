import os

import requests as fetch
from django.core.cache import cache
from django.http import JsonResponse
from dotenv import load_dotenv

load_dotenv()


def get_heroes(request):
  if request.method != 'GET':
    return JsonResponse({
        "status": False,  
        "data": { "message": "Method not allowed"}
      }, status=405)
  
  heroes_query = request.GET.get('query', None)
  if not heroes_query:
    return JsonResponse({
      "status": False,
      "error": { "message" : f"partial heroes name required in query params" }
    }, status=400)
  
  cahce_key = request.get_full_path()
  print(cahce_key)
  cache_data = cache.get(cahce_key)
  if cache_data:
    return JsonResponse({
      "status": True,
      "data": cache_data,
    })

  try:
    heroes_url = str(os.getenv('HEROES_BASE_URL'))
    response = fetch.get(heroes_url)

    if response.ok :
      data = response.json()
      heroes_list: dict = data.get('data')
      
      hero_item = next(filter(lambda x: heroes_query in x[0].lower(), heroes_list.items()), None)
      if not hero_item :
        return JsonResponse({
          "status": False,
          "error": { "message" : "hero not found"}
        }, status=404)

      hero_detail = hero_item[1]
      cache.set(cahce_key, hero_detail, timeout=60 * 60 * 2) ## Two Hours
      return JsonResponse({
        "status": True,
        "data": hero_detail,
      })
    else:
      return JsonResponse({
        "status": False,
        "error": { "message" : f"fetch heroes API {response.status_code}"},
      }, status=200)
  except Exception:
    return JsonResponse({
        "status": False,
        "error": { "message": "Internal Server Error" }
      }, status=500)