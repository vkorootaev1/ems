from rest_framework import serializers
from users import models
from users.serializers import nested_serializers


class UserSerializer(serializers.ModelSerializer):
    
    """ Сериализатор пользователя """

    class Meta:
        model = models.User
        fields = '__all__'


class UserUpdateEmailSerializer(serializers.ModelSerializer):
    
    """ Сериализатор обновления email пользователя """
    
    email = serializers.EmailField(write_only=True)

    class Meta:
        model = models.User
        fields = ['email', ]

    def validate_email(self, value):
        if models.User.objects.filter(email=value).exists():
            raise serializers.ValidationError('This email already exists')
        return value


class TeacherListSerializer(serializers.ModelSerializer):
    
    """ Сериализатор списка преподавателей """
    
    user = nested_serializers.NestedUserWithPhotoSerializer(read_only=True)

    class Meta:
        model = models.Teacher
        fields = ['id', 'user']


class TeacherRetrieveSerializer(serializers.ModelSerializer):
    
    """ Сериализатор ФИО, фото, контактов, кафедры, курсы преподавателя """
    
    user = nested_serializers.NestedUserWithPhotoContactsSerializer(
        read_only=True)
    cathedras = serializers.SlugRelatedField(
        source='cathedra', slug_field='name', read_only=True, many=True)
    courses = serializers.SlugRelatedField(
        slug_field='name', read_only=True, many=True)

    class Meta:
        model = models.Teacher
        fields = ['id', 'user', 'cathedras', 'courses']


class ContactTypeSerializer(serializers.ModelSerializer):
    
    """ Сериализатор типа контакта преподавателя """

    class Meta:
        model = models.ContactType
        fields = '__all__'


class ContactSerializer(serializers.ModelSerializer):
    
    """ Сериализатор контакта пользователя """
    
    type = ContactTypeSerializer(read_only=True)
    type_id = serializers.PrimaryKeyRelatedField(
        source='type', queryset=models.ContactType.objects.all(), write_only=True)
    user = nested_serializers.NestedUserFIOSerializer(read_only=True)

    class Meta:
        model = models.Contact
        fields = ['id', 'type', 'type_id', 'contact_ref', 'user']

    def create(self, validated_data):
        user = self.context.get('user')
        return models.Contact.objects.create(user=user, **validated_data)
