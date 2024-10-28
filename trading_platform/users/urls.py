from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('pre-registration/', views.pre_registration, name='pre_registration'),
    path('signup/', views.signup, name='signup'),
    path('profile/', views.profile, name='profile'),
]
