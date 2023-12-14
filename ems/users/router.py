from rest_framework import routers
from users import views

router = routers.DefaultRouter()
router.register(r'contacts/type', views.ContactTypeViewSet,
                basename='contacttype')
router.register(r'contacts', views.ContactViewSet, basename='contacts')
router.register(r'teacher', views.TeachersViewSet, basename='teachers')
router.register(r'', views.UserViewSet, basename='user')
