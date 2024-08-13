from rest_framework import routers
from study import views

router = routers.DefaultRouter()
router.register(r'timetable', views.TimeTableViewSet, basename='timetable')
router.register(r'studyplan', views.StudyPlanViewSet, basename='studyplan')
router.register(r'score/trim', views.ControlMeasureScoreViewSet,
                basename='controlmeasurescore')
router.register(r'score/result', views.CourseScoreViewSet,
                basename='resultscore')
router.register(r'attendance', views.AttendanceViewSet, basename='attendance')
router.register(r'trimester', views.TrimesterViewSet, basename='trimester')
router.register(r'studygroup', views.StudyGroupViewSet, basename='studygroup')
