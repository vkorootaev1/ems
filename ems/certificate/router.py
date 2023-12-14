from rest_framework import routers
from certificate import views

router = routers.DefaultRouter()
router.register(r'type', views.CertificateTypeViewSet,
                basename='certificatetype')
router.register(r'', views.CertificateViewSet, basename='certificate')
