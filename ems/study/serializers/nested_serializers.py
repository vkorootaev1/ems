from rest_framework import serializers
from study import models


class NestedStudyGroupSerializer(serializers.ModelSerializer):

    """ Вложенный сериализатор учебной группы """

    class Meta:
        model = models.StudyGroup
        fields = ['id', 'name', 'begin_date', 'end_date']


class NestedCourseSerializer(serializers.ModelSerializer):

    """ Вложенный сериализатор курса """

    type_of_course = serializers.CharField(
        read_only=True, source='get_type_of_course_display')
    type_of_mark = serializers.CharField(
        read_only=True, source='get_type_of_mark_display')

    class Meta:
        model = models.Course
        fields = ['id', 'name', 'classroom_worktime',
                  'independent_worktime', 'type_of_course', 'type_of_mark']


class NestedCourseShortSerializer(serializers.ModelSerializer):

    """ Вложенный сериализатор курса (укороченный) """

    type_of_mark = serializers.CharField(
        read_only=True, source='get_type_of_mark_display')

    class Meta:
        model = models.Course
        fields = ['id', 'name', 'type_of_mark']


class NestedStudyPlanCoursesSerializer(serializers.ModelSerializer):

    """ Вложенный сериализатор курсов учебного плана """

    course = NestedCourseShortSerializer(read_only=True)

    class Meta:
        model = models.StudyPlanCourses
        fields = ['course', 'trimester']


class NestedTimeTableSerializer(serializers.ModelSerializer):

    """ Вложенный сериализатор расписания """

    course = serializers.SlugRelatedField(slug_field='name', read_only=True)
    type_of_pair = serializers.CharField(
        source='get_type_of_pair_display', read_only=True)

    class Meta:
        model = models.TimeTable
        fields = ['id', 'date', 'course', 'type_of_pair']
