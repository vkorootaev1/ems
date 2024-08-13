from django.urls import path, include
from certificate.router import router

app_name = 'certificate'

urlpatterns = [
    path('certificate/', include(router.urls))
]
