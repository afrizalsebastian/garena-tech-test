from django.urls import path

from . import views

urlpatterns = [
  path('register/', views.regiter_user, name="check_status"),
  path('login/', views.login, name="login"),
  path('edit_profile/', views.update_user, name='update_user'),
  path('input_ref/', views.insert_referral, name='input_referral')
]