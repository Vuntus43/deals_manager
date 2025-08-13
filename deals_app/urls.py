from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from . import views

urlpatterns = [
    path('', csrf_exempt(views.index), name='index'),                # Б24 POST к корню
    path('api/save-auth/', csrf_exempt(views.save_auth), name='save_auth'),  # сохраняем токен
    path('api/user/', views.user_current, name='user_current'),              # читаем имя
]
