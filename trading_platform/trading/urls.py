from django.urls import path
from . import views

app_name = 'trading'

urlpatterns = [
    path('', views.StrategyListView.as_view(), name='strategy_list'),
    path('<int:pk>/', views.StrategyDetailView.as_view(), name='strategy_detail'),
    path('new/', views.generate_strategy, name='generate_strategy'),
    path('<int:pk>/update/', views.update_strategy, name='update_strategy'),
    path('<int:pk>/delete/', views.delete_strategy, name='delete_strategy'),
    path('strategy/<int:pk>/toggle-favorite/', views.toggle_favorite, name='toggle_favorite'),

]