from django.contrib import admin
from study import models


@admin.register(models.Course)
class CourseAdmin(admin.ModelAdmin):
    readonly_fields = ['id', ]
    fields = ['id', 'code', 'name', 'subcourse_number',
              'description', 'classroom_worktime', 'independent_worktime',
              'type_of_course', 'type_of_mark', 'count_of_lectures_pairs', 'count_of_practies_pairs',
              'count_of_laboratory_pairs', 'owners', 'is_active']
    list_display = ['id', 'name', 'subcourse_number',
                    'type_of_course', 'type_of_mark', ]
    search_fields = ['id', 'name', ]
    list_filter = ["type_of_mark", "type_of_course"]
    autocomplete_fields = ['owners', ]


@admin.register(models.ControlMeasure)
class ControlMeasureAdmin(admin.ModelAdmin):
    readonly_fields = ['id', 'date_add', 'date_upd']
    fields = ['id', 'name', 'description', 'course',
              'max_score', 'min_score', 'order',
              'date_add', 'date_upd', 'is_active', ]
    list_display = ['id', 'name', 'course', 'max_score', 'min_score']
    search_fields = ['id', 'name', 'course__name']
    autocomplete_fields = ['course', ]


@admin.register(models.StudyPlan)
class StudyPlanAdmin(admin.ModelAdmin):
    readonly_fields = ['id', ]
    fields = ['id', 'code', 'name', 'description',
              'speciality', 'is_active', ]
    list_display = ['id', 'name', 'speciality', ]
    search_fields = ['name', 'code', 'speciality__name']
    autocomplete_fields = ['speciality', ]


@admin.register(models.StudyPlanCourses)
class StudyPlanCoursesAdmin(admin.ModelAdmin):
    readonly_fields = ['id', ]
    fields = ['id', 'trimester', 'course', 'study_plan', ]
    list_display = ['id', 'trimester', 'course', 'study_plan', ]
    search_fields = ['course__name', 'study_plan__name', 'study_plan__code', ]
    autocomplete_fields = ['course', 'study_plan', ]


@admin.register(models.Trimester)
class TrimesterAdmin(admin.ModelAdmin):
    readonly_fields = ['id', ]
    fields = ['id', 'date_start', 'date_end', ]
    list_display = ['id', 'date_start', 'date_end', ]


@admin.register(models.StudyGroup)
class StudyGroupAdmin(admin.ModelAdmin):
    readonly_fields = ['id', ]
    fields = ['id', 'name', 'code', 'study_plan',
              'begin_date', 'end_date', 'is_active', ]
    list_display = ['name', 'begin_date', 'end_date', ]
    search_fields = ['name', 'code', 'study_plan__code', 'study_plan__name', ]
    autocomplete_fields = ['study_plan', ]
    list_filter = ['is_active', ]


@admin.register(models.TimeTable)
class TimeTableAdmin(admin.ModelAdmin):
    readonly_fields = ['id', 'date_add', 'date_upd', ]
    fields = ['id', 'date', 'course', 'groups', 'type_of_pair', 'index_pair',
              'teacher', 'classroom', 'date_add', 'date_upd', 'is_attendance', ]
    list_display = ['id', 'date', 'course',
                    'type_of_pair', 'index_pair', 'teacher']
    search_fields = ['course__name', 'teacher__user__last_name',
                     'teacher__user__first_name', ]
    autocomplete_fields = ['course', 'teacher', 'classroom', 'groups', ]
    list_filter = ['type_of_pair', 'index_pair', 'is_attendance', ]


@admin.register(models.Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    readonly_fields = ['id', 'date_upd', ]
    fields = ['id', 'pair', 'student', 'status', 'teacher',
              'date_upd', ]
    list_display = ['id', 'pair', 'student',
                    'status', ]
    search_fields = ['student__user__last_name',
                     'student__user__first_name', 'pair__course__name', ]
    autocomplete_fields = ['student', 'teacher', 'pair', ]
    list_filter = ['status', ]


@admin.register(models.ControlMeasureScore)
class ControlMeasureScoreAdmin(admin.ModelAdmin):
    readonly_fields = ['id', 'date_upd', ]
    fields = ['id', 'control_measure', 'student', 'score', 'teacher',
              'date_upd', ]
    list_display = ['id', 'control_measure', 'student',
                    'score', ]
    search_fields = ['student__user__last_name', 'student__user__first_name',
                     'control_measure__name', 'control_measure__course__name', ]
    autocomplete_fields = ['student', 'teacher', 'control_measure', ]


@admin.register(models.CourseScore)
class CourseScoreScoreAdmin(admin.ModelAdmin):
    readonly_fields = ['id', 'date_upd', ]
    fields = ['id', 'course', 'student', 'score', 'teacher',
              'date_upd', ]
    list_display = ['id', 'course', 'student',
                    'score', ]
    search_fields = ['student__user__last_name', 'student__user__first_name',
                     'course__course__name', ]
    autocomplete_fields = ['student', 'teacher', 'course', ]
    list_filter = ['score', ]


@admin.register(models.CourseTeacherStudyGroup)
class CourseTeacherStudyGroupAdmin(admin.ModelAdmin):
    readonly_fields = ['id', ]
    fields = ['id', 'trimester', 'course', 'teacher',
              'study_group', ]
    list_display = ['id', 'trimester', 'course',
                    'teacher', 'study_group', ]
    search_fields = ['course__course__name', 'teacher__user__last_name',
                     'teacher__user__first_name', 'study_group__name', ]
    autocomplete_fields = ['study_group', 'teacher', 'course', ]
    list_filter = ['trimester', ]
