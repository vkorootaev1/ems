import django_filters
from django.db.models import Q


class ContactFilter(django_filters.FilterSet):

    """ Фильтр для контакта пользователя """

    own = django_filters.BooleanFilter(method='get_own_contacts')

    def get_own_contacts(self, queryset, name, value):

        if value:
            user = self.request.user
            queryset = queryset.filter(user=user)

        return queryset


class TeacherFilter(django_filters.FilterSet):

    """ Фильтр для преподавателя """

    name = django_filters.CharFilter(method='get_teacher')

    def get_teacher(self, queryset, name, value):
        values = value.split(' ')
        q = Q()
        for _value in values:
            q &= Q(Q(user__first_name__icontains=_value) |
                   Q(user__last_name__icontains=_value) |
                   Q(user__patronymic__icontains=_value))

        return queryset.filter(q)
