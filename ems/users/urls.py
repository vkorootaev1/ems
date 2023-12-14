from django.urls import path, include
from users.router import router

app_name = 'users' 

urlpatterns = [
    path('user/', include(router.urls)),
]
