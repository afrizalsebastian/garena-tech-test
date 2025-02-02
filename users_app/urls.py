from django.urls import path

from . import views

urlpatterns = [
  path('register/', views.regiter_user, name="check_status"),
  path('login/', views.login, name="login"),
]