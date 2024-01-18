import django_filters
from study import models as study_models
from django.db.models import Q


class TimeTableFilter(django_filters.FilterSet):

    """ Фильтр расписания """

    year = django_filters.NumberFilter(field_name='date', lookup_expr='year')
    week = django_filters.NumberFilter(field_name='date', lookup_expr='week')

    class Meta:
        model = study_models.TimeTable
        fields = ['date']


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
