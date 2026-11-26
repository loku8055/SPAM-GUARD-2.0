from django.urls import path
from . import views

urlpatterns = [
    # Full UI Paths
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('predict/', views.predict_view, name='predict'),
    path('result/<int:prediction_id>/', views.result_view, name='result'),
    
    # Existing API Paths
    path('classify/', views.classify, name='classify'),
    path('history/', views.history, name='history'),

    # New Requested API / Easter Egg Paths
    path('api/detect/', views.api_detect_spam, name='api_detect_spam'),
    path('antigravity/', views.antigravity_view, name='antigravity'),
]
