from rest_framework import serializers
from users.serializers import nested_serializers as users_serializers
from certificate import models


class CertificateTypeSerializer(serializers.ModelSerializer):

    """ Сериализатор типа справки """

    class Meta:
        model = models.CertificateType
        fields = ['id', 'name', 'description']


class CertificateSerializer(serializers.ModelSerializer):

    """ Сериализатор справки """

    type = serializers.SlugRelatedField(slug_field='name', read_only=True)
    type_id = serializers.PrimaryKeyRelatedField(
        source='type', queryset=models.CertificateType.objects.all(), write_only=True)
    user = users_serializers.NestedUserFIOSerializer(read_only=True)
    status = serializers.CharField(source='get_status_display', read_only=True)
    status_write = serializers.ChoiceField(source='status',
                                           choices=models.Certificate.STATUS_OF_CERTIFICATE,
                                           write_only=True)
    user_give = users_serializers.NestedUserFIOSerializer(read_only=True)

    class Meta:
        model = models.Certificate
        fields = ['id', 'type', 'type_id', 'user', 'status', 'count',
                  'status_write', 'user_give', 'date_add', 'date_upd']

    def validate_status_write(self, value):
        instance = getattr(self, 'instance', None)
        if instance:
            is_certificate_worker = self.context.get(
                'user').get_certificate_worker()
            if not is_certificate_worker:
                if instance.status == 'ca':
                    raise serializers.ValidationError('Certificate already cancel')
                if value not in ['ca']:
                    raise serializers.ValidationError('status only: <cr> or <ca>')
        return value

    def validate_count(self, value):
        if not 0 < value <= 3:
            raise serializers.ValidationError('Count range = (1, 3]')
        return value

    def create(self, validated_data):
        user = self.context.get('user')
        del validated_data['status']
        return models.Certificate.objects.create(user=user, status='cr', **validated_data)

    def update(self, instance, validated_data):
        user = self.context.get('user')
        if user.get_certificate_worker():
            instance.person_give = user
        instance.status = validated_data['status']
        instance.save()
        return instance
