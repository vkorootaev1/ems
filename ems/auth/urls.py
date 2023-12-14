from django.urls import path, include
from knox import views as knox_views
from auth import views
app_name = 'auth'

urlpatterns = [
    path('login/', views.LoginView.as_view()),
    path('logout/', knox_views.LogoutView.as_view()),
    path('logoutall/', knox_views.LogoutAllView.as_view()),
]
