from rest_framework import serializers
from university import models


class NestedClassRoomSerializer(serializers.ModelSerializer):
    
    """ Вложенный сериализатор аудитории университета """

    class Meta:
        model = models.Classroom
        fields = ['number', 'house', 'floor']
