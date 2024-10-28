# rewards/urls.py
from django.urls import path
from . import views

app_name = 'rewards'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('history/', views.points_history, name='points_history'),
    path('rewards/', views.available_rewards, name='available_rewards'),
    path('redeem/<int:reward_id>/', views.redeem_reward, name='redeem_reward'),
]