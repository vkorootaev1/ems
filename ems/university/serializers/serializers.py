from rest_framework import serializers
from university import models


class ClassRoomSerializer(serializers.ModelSerializer):
    
    """ Сериализатор аудитории университета """

    class Meta:
        model = models.Classroom
        fields = '__all__'


class FacultySerializer(serializers.ModelSerializer):
    
    """ Сериализатор фалькультета """

    class Meta:
        model = models.Faculty
        fields = '__all__'


class CathedraSerializer(serializers.ModelSerializer):
    
    """ Сериализатор кафедры """
    
    faculty = serializers.SlugRelatedField(read_only=True, slug_field='name')

    class Meta:
        model = models.Cathedra
        fields = ['id', 'name', 'description', 'faculty', 'is_active']


class SpecialitySerializer(serializers.ModelSerializer):
    
    """ Сериализатор специальности """
    
    cathedra = CathedraSerializer(read_only=True)
    level_of_higher_education = serializers.CharField(
        source='get_level_of_higher_education_display')
    form_of_study = serializers.CharField(source='get_form_of_study_display')

    class Meta:
        model = models.Speciality
        fields = ['id', 'code', 'name', 'description',
                  'study_period_months', 'level_of_higher_education', 'form_of_study',
                  'cathedra', 'is_active']
