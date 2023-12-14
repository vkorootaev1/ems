from django.urls import path, include
from university.router import router

app_name = 'university'

urlpatterns = [
    path('university/', include(router.urls))
]
