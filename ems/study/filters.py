from datetime import datetime
import django_filters
from study import models as study_models
from django.db.models import Q


class TimeTableFilter(django_filters.FilterSet):

    """ Фильтр расписания """

    # Отбор расписания по году
    year = django_filters.NumberFilter(field_name='date', lookup_expr='year')
    # Отбор расписания по недели
    week = django_filters.NumberFilter(field_name='date', lookup_expr='week')
    # Отбор расписания по посещаемости (выставлена ли посещаемость за пару)
    attendance = django_filters.BooleanFilter(field_name='is_attendance')
    # Отбор расписания по дисциплинам
    course_name = django_filters.CharFilter(method='get_by_course_name')
    # Отбор расписания по учебной группе
    group_name = django_filters.CharFilter(method='get_by_group_name')
    # Отбор расписания по триместру
    trimester = django_filters.NumberFilter(method='get_by_trimester')
    # Сортировка расписания по дате
    order = django_filters.OrderingFilter(fields=(
        ('date', 'date'),
    ))

    # Функция отбора расписания по дисциплине
    def get_by_course_name(self, queryset, name, value):
        return queryset.filter(course__name__icontains=value, date__lte=datetime.now().date()).\
            order_by('-date', '-index_pair')

    # Функция отбора расписания по учебной группе
    def get_by_group_name(self, queryset, name, value):
        return queryset.filter(groups__name__icontains=value, date__lte=datetime.now().date()).\
            order_by('-date', '-groups__name')

    # Функция отбора расписания по триместру
    def get_by_trimester(self, queryset, name, value):
        if value == 0:
            trimester = study_models.Trimester.objects.get_current_trimester()
        else:
            trimester = study_models.Trimester.objects.get_trimester_by_id(
                value)

        if trimester:
            return queryset.filter(Q(date__gte=trimester.date_start) &
                                   Q(date__lte=trimester.date_end) &
                                   Q(date__lte=datetime.now().date())).order_by('-date')

        return study_models.TimeTable.objects.none()

    # Мета информация
    class Meta:
        model = study_models.TimeTable
        fields = ['date', 'is_attendance', 'course__name']


class ControlMeasureScoreFilter(django_filters.FilterSet):

    """ Фильтр промежуточной оценки студента """

    trimester = django_filters.NumberFilter(method='get_score_by_trim')

    def get_score_by_trim(self, queryset, name, value):
        queryset = queryset.filter(
            control_measure__course__studyplancourses_course__trimester=value)
        return queryset


class StudyGroupCourseListFilter(django_filters.FilterSet):

    """ Фильтр списка курсов, которые ведет преподаватель у группы в триместре """

    name = django_filters.CharFilter(method='get_by_course_name_group_name')
    trimester = django_filters.NumberFilter(method='get_by_trimester')

    def get_by_course_name_group_name(self, queryset, name, value):

        LIMIT = 5

        values = value.split(' ')

        q = Q()

        for _value in values:
            q &= Q(Q(study_group__name__icontains=_value) |
                   Q(course__course__name__icontains=_value))
        return queryset.filter(q)[:LIMIT]

    def get_by_trimester(self, queryset, name, value):

        trimester_id = value

        if value == 0:
            trimester_id = study_models.Trimester.objects.get_current_trimester().id

        return queryset.filter(trimester_id=trimester_id)


class StudyGroupFilter(django_filters.FilterSet):

    """ Фильтр учебных групп """

    name = django_filters.CharFilter(lookup_expr='icontains')


class AttendanceFilter(django_filters.FilterSet):

    trimester = django_filters.NumberFilter(
        method='get_by_trimester')

    def get_by_trimester(self, queryset, name, value):

        if value == 0:
            trimester = study_models.Trimester.objects.get_current_trimester()
        else:
            trimester = study_models.Trimester.objects.get_trimester_by_id(
                value)

        if trimester:
            return queryset.filter(pair__date__gte=trimester.date_start, pair__date__lte=trimester.date_end).\
                order_by('-date_upd')

        return study_models.Attendance.objects.none()
