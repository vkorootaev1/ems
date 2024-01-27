from users import models
from rest_framework import serializers
from study.serializers import nested_serializers as study_nested_serializers


class NestedContactSerializer(serializers.ModelSerializer):

    """ Вложенный сериализатор контакта пользователя """

    type = serializers.SlugRelatedField(slug_field='type', read_only=True)

    class Meta:
        model = models.Contact
        fields = ['id', 'contact_ref', 'type', 'user']


class NestedUserFIOSerializer(serializers.ModelSerializer):

    """ Вложееный сериализатор ФИО пользователя """

    class Meta:
        model = models.User
        fields = ['last_name', 'first_name', 'patronymic']


class NestedUserFIOWithEmailSerializer(serializers.ModelSerializer):

    """ Вложенный сериализатор ФИО и email пользователя """

    class Meta:
        model = models.User
        fields = ['last_name', 'first_name', 'patronymic', 'email']


class NestedUserWithPhotoSerializer(serializers.ModelSerializer):

    """ Вложенный сериализатор ФИО польльзователя с фото """

    class Meta:
        model = models.User
        fields = ['last_name', 'first_name', 'patronymic', 'photo']


class NestedUserWithPhotoContactsSerializer(serializers.ModelSerializer):

    """ Вложенный сериализатор ФИО, фото и контактов пользователя """

    contacts = NestedContactSerializer(
        source='contact_user', many=True, read_only=True)

    class Meta:
        model = models.User
        fields = ['last_name', 'first_name', 'patronymic', 'photo', 'contacts']


class NestedStudentWithGroupEmailSerializer(serializers.ModelSerializer):

    """ Вложенный сериализатор ФИО студента, email и группы """

    user = NestedUserFIOWithEmailSerializer(read_only=True)
    study_group = study_nested_serializers.NestedStudyGroupSerializer(
        read_only=True)
    role = serializers.ReadOnlyField(default='student')

    class Meta:
        model = models.Student
        fields = ['id', 'user', 'study_group', 'role']


class NestedStudentWithGroupSerializer(serializers.ModelSerializer):

    """ Вложенный сериализатор ФИО студента и его группы  """

    user = NestedUserFIOSerializer(read_only=True)
    study_group = study_nested_serializers.NestedStudyGroupSerializer(
        read_only=True)

    class Meta:
        model = models.Student
        fields = ['id', 'user', 'study_group']


class NestedStudentSerializer(serializers.ModelSerializer):

    """ Вложенный сериализатор ФИО студента """

    user = NestedUserFIOSerializer(read_only=True)

    class Meta:
        model = models.Student
        fields = ['id', 'user']


class NestedTeacherWithEmailSerializer(serializers.ModelSerializer):

    """ Вложенный сериализатор ФИО преподавателя и email """

    user = NestedUserFIOWithEmailSerializer(read_only=True)
    role = serializers.ReadOnlyField(default='teacher')

    class Meta:
        model = models.Teacher
        fields = ['id', 'user', 'role']


class NestedTeacherSerializer(serializers.ModelSerializer):

    """ Вложенный сериализатор ФИО преподавателя """

    user = NestedUserFIOSerializer(read_only=True)

    class Meta:
        model = models.Teacher
        fields = ['id', 'user']


class UserDetailSerializer(serializers.ModelSerializer):

    """ Вложенный сериализатор деталей о пользователе """

    students = NestedStudentWithGroupEmailSerializer(
        read_only=True, many=True, source='student_user')
    teacher = NestedTeacherWithEmailSerializer(source='teacher_user',
                                               read_only=True)
    is_admin = serializers.BooleanField(source='is_staff')

    class Meta:
        model = models.User
        fields = ['students', 'teacher', 'is_admin']
