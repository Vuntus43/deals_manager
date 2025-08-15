from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from . import views

urlpatterns = [
    path('', views.page_home, name='home'),
    path('deals/', views.page_deals, name='deals'),
    path('create/', views.page_create, name='create'),

    path('api/save-auth/', csrf_exempt(views.save_auth), name='save_auth'),
    path('api/user/', views.user_current, name='user_current'),
    path('api/deals/', views.user_deals, name='user_deals'),
    path('api/deal-create/', csrf_exempt(views.deal_create), name='deal_create'),
]
