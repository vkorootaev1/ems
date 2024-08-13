from rest_framework import routers
from ads import views

router = routers.DefaultRouter()
router.register(r'files', views.AdvertisementFileViewSet,
                basename='advertisementfile')
router.register(r'', views.AdvertisementViewSet,
                basename='advertisement')
