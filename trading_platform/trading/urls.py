# trading/urls.py
from django.urls import path
from . import views

app_name = 'trading'

urlpatterns = [
    path('', views.StrategyListView.as_view(), name='strategy_list'),
    path('<int:pk>/', views.StrategyDetailView.as_view(), name='strategy_detail'),
    path('new/', views.generate_strategy, name='generate_strategy'),
    path('<int:pk>/update/', views.update_strategy, name='update_strategy'),
    path('<int:pk>/delete/', views.delete_strategy, name='delete_strategy'),
    path('<int:pk>/toggle-favorite/', views.toggle_favorite, name='toggle_favorite'),
    path('user/<int:user_id>/strategies/', views.user_strategies_view, name='user_strategies'),
    path('create_strategy/', views.create_strategy_view, name='create_strategy'),
    path('strategy_summary/', views.strategy_summary_view, name='strategy_summary'),
    path('confirm_strategy/', views.confirm_strategy_view, name='confirm_strategy'),
]
