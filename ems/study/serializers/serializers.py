from rest_framework import serializers
from study import models
from users.serializers import nested_serializers as users_serializers
from university.serializers import nested_serializers as university_serializers
from study.serializers import nested_serializers


class TimeTableSerializer(serializers.ModelSerializer):

    """ Сериализатор расписания """

    type_of_pair = serializers.CharField(
        read_only=True, source='get_type_of_pair_display')
    course = serializers.SlugRelatedField(read_only=True, slug_field='name')
    teacher = users_serializers.NestedTeacherSerializer(read_only=True)
    classroom = university_serializers.NestedClassRoomSerializer(
        read_only=True)
    groups = serializers.SlugRelatedField(
        read_only=True, slug_field='name', many=True)

    class Meta:
        model = models.TimeTable
        fields = ['id', 'date', 'type_of_pair', 'index_pair',
                  'course', 'teacher', 'classroom', 'is_attendance', 'groups']


class StudyPlanCourseSerializer(serializers.ModelSerializer):

    """ Сериализатор курсов учебного плана """

    course = nested_serializers.NestedCourseSerializer(read_only=True)

    class Meta:
        model = models.StudyPlanCourses
        fields = ['id', 'trimester', 'course']


class ControlMeasure(serializers.ModelSerializer):

    """ Сериализатор контрольного мероприятия """

    course = nested_serializers.NestedCourseShortSerializer(read_only=True)

    class Meta:
        model = models.ControlMeasure
        fields = ['id', 'name', 'course', 'max_score', 'min_score']


class ControlMeasureScore(serializers.ModelSerializer):

    """ Сериализатор промежуточной оценки студента """

    control_measure = ControlMeasure(read_only=True)
    student = users_serializers.NestedStudentSerializer(read_only=True)
    teacher = users_serializers.NestedTeacherSerializer(read_only=True)

    class Meta:
        model = models.ControlMeasureScore
        fields = ['id', 'control_measure', 'student',
                  'score', 'teacher', 'date_upd']


class ControlMeasureScoreMultipleUpdateSerializer(serializers.Serializer):

    """ Сериализатор для массового обновления промежуточной оценки студента """

    score = serializers.FloatField(write_only=True)

    def validate_score(self, value):
        instance = self.instance
        if not (0 <= value <= instance.control_measure.max_score):
            raise serializers.ValidationError(
                {'error': f'Wrong score: {value}, id:{instance.id}'})
        return value

    def update(self, instance, validated_data):
        teacher = self.context.get('teacher')
        instance.score = validated_data.get('score')
        instance.teacher = teacher
        instance.save()
        return instance


class CourseScoreSerializer(serializers.ModelSerializer):

    """ Сериализатор оценки студента за курс """

    course = nested_serializers.NestedStudyPlanCoursesSerializer(
        read_only=True)
    student = users_serializers.NestedStudentSerializer(read_only=True)
    score = serializers.CharField(source='get_score_display')
    teacher = users_serializers.NestedTeacherSerializer(read_only=True)

    class Meta:
        model = models.CourseScore
        fields = ['id', 'course', 'student',
                  'score', 'teacher', 'date_upd']


class AttendanceSerializer(serializers.ModelSerializer):

    """ Сериализатор посещаемости """

    pair = nested_serializers.NestedTimeTableSerializer(read_only=True)
    student = users_serializers.NestedStudentWithGroupSerializer(
        read_only=True)
    teacher = users_serializers.NestedTeacherSerializer(read_only=True)

    class Meta:
        model = models.Attendance
        fields = ['id', 'pair', 'student', 'status', 'date_upd', 'teacher']


class AttendanceMultipleUpdateSerializer(serializers.Serializer):

    """ Сериализатор для массового обновления посещаемости """

    status = serializers.BooleanField(write_only=True)

    def update(self, instance, validated_data):
        teacher = self.context.get('teacher')
        instance.status = validated_data.get('status')
        instance.teacher = teacher
        instance.save()
        return instance


class CourseScoreOtherMultipleUpdateSerializer(serializers.Serializer):

    """ Сериализатор для массового обновления итоговых оценок (для практик, физ. кульутры и т.д.)"""

    score = serializers.ChoiceField(choices=models.CourseScore.SCORES)

    def validate_score(self, value):
        instance = self.instance
        type_of_mark = self.context.get('type_of_mark')
        if (type_of_mark == 'ex' and value not in ['2', '3', '4', '5', 'NO']) or (type_of_mark == 'za' and value not in ['OK', 'FA', 'NO']):
            raise serializers.ValidationError(
                {'error': f'Wrong score: {value}, id:{instance.id}'})
        return value

    def update(self, instance, validated_data):
        teacher = self.context.get('teacher')
        instance.score = validated_data.get('score')
        instance.teacher = teacher
        instance.save()
        return instance


class TrimesterSerializer(serializers.ModelSerializer):

    """ Сериализатор триместра """

    class Meta:
        model = models.Trimester
        fields = '__all__'


class StudyGroupCourseListSerializer(serializers.ModelSerializer):

    """ Сериализатор курсов, которые ведет преподаватель у группы в триместре """

    trimester = TrimesterSerializer(read_only=True)
    study_plan_course = StudyPlanCourseSerializer(
        source='course', read_only=True)
    study_group = nested_serializers.NestedStudyGroupSerializer(read_only=True)

    class Meta:
        model = models.CourseTeacherStudyGroup
        fields = ['id', 'study_group',  'trimester', 'study_plan_course']


class StudyGroupSerializer(serializers.ModelSerializer):

    """ Сериализатор учебной группы """

    class Meta:
        model = models.StudyGroup
        fields = '__all__'
