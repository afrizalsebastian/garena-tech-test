from django.urls import path

from . import views

urlpatterns = [
  path('heroes/', views.get_heroes, name="get_heroes"),
]