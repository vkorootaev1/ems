from django.urls import path, include
from ads.router import router

app_name = 'ads'

urlpatterns = [
    path('advertisement/', include(router.urls)),
]
