"""
URL configuration for ems project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from ems import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

BASE_API_V_1 = 'api/v1'

admin.site.site_title = 'Система управления учебным процессом'
admin.site.site_header = 'Система управления учебным процессом'

urlpatterns = [
    path('admin/', admin.site.urls),
    path(f'{BASE_API_V_1}/', include('university.urls')),
    path(f'{BASE_API_V_1}/', include('study.urls')),
    path(f'{BASE_API_V_1}/', include('users.urls')),
    path(f'{BASE_API_V_1}/', include('certificate.urls')),
    path(f'{BASE_API_V_1}/', include('ads.urls')),
    path(f'{BASE_API_V_1}/auth/', include('auth.urls')),
    path(f'{BASE_API_V_1}/auth/', include('djoser.urls')),
    path('silk/', include('silk.urls', namespace='silk')),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
