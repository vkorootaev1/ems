from rest_framework import serializers
from ads import models, validators
from study.serializers import nested_serializers as study_serializers
from users.serializers import nested_serializers as users_serializers
from study import models as study_models


class AdvertisementFileSerializer(serializers.ModelSerializer):

    """ Сериализатор файла объявления """

    origin_name = serializers.ReadOnlyField()

    class Meta:
        model = models.AdvertisementFile
        fields = ['id', 'origin_name', 'file']


class AdvertisementSerializer(serializers.ModelSerializer):

    """ Сериализатор объявления """

    user = users_serializers.NestedUserFIOSerializer(read_only=True)
    groups = study_serializers.NestedStudyGroupSerializer(
        read_only=True, many=True)
    groups_write = serializers.ListField(
        source='groups', required=True, write_only=True, child=serializers.PrimaryKeyRelatedField(
            queryset=study_models.StudyGroup.objects.all()
        ))
    files = AdvertisementFileSerializer(
        required=False, source='advertisement_file', read_only=True, many=True)
    files_upload = serializers.ListField(
        required=False, write_only=True, child=serializers.FileField(
            max_length=1000000,
            allow_empty_file=False,
            use_url=False,
            validators=[validators.validate_file_extension,
                        validators.validate_file_size]
        ))

    class Meta:
        model = models.Advertisement
        fields = ['id', 'body', 'user', 'groups', 'groups_write',
                  'files', 'files_upload', 'date_add', 'date_upd']

    def create(self, validated_data):
        user = self.context.get('user')
        groups = validated_data.pop('groups')
        files = validated_data.pop('files_upload', None)

        advertisement = models.Advertisement.objects.create(
            user=user, **validated_data)

        for group in groups:
            advertisement.groups.add(group)
        advertisement.save()

        if files:
            for file in files:
                models.AdvertisementFile.objects.create(
                    user=user, advertisement=advertisement, file=file)

        return advertisement

    def update(self, instance, validated_data):
        user = self.context.get('user')
        groups = validated_data.pop('groups')
        files = validated_data.pop('files_upload', None)
        body = validated_data.pop('body')

        instance.body = body

        instance.groups.clear()
        for group in groups:
            instance.groups.add(group)

        if files:
            for file in files:
                models.AdvertisementFile.objects.create(
                    user=user, advertisement=instance, file=file)

        return instance
