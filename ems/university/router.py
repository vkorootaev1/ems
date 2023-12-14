from rest_framework import routers
from university import views

router = routers.DefaultRouter()

router.register(r'classroom', views.ClassRoomViewSet, basename='classroom')
router.register(r'cathedra', views.CathedraViewSet, basename='cathedra')
router.register(r'faculty', views.FacultyViewSet, basename='faculty')
router.register(r'speciality', views.SpecialityViewSet, basename='speciality')
