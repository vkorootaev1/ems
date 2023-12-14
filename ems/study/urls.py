from django.urls import path, include
from study.router import router
from study import views

app_name = 'study'

urlpatterns = [
    path('study/', include(router.urls)),
    path('study/teacher/groups/', views.StudyGroupCourseListAPIView.as_view(),
         name='studygroupcourseteacher')
]
