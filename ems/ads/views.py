from rest_framework import viewsets, permissions
from ads import models
from ads.serializers import serializers
import mixins as _mixins
import pagination
import permissions.permissions as _permissions


class AdvertisementViewSet(_mixins.StudentMixin,
                           _mixins.TeacherMixin,
                           viewsets.ModelViewSet):

    """ Представление объявлений """

    pagination_class = pagination.SmallPagination

    def get_queryset(self):
        student = self.get_student()
        user = self.request.user

        queryset = models.Advertisement.objects.all().\
            select_related('user').\
            prefetch_related('advertisement_file', 'groups').\
            order_by('-date_add')

        if student:
            queryset = queryset.filter(groups__id=student.study_group_id)

        if not user.is_staff and not student:
            queryset = queryset.filter(user=user)

        return queryset

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['user'] = self.request.user
        return context

    def get_serializer_class(self):
        return serializers.AdvertisementSerializer

    def get_permissions(self):
        if self.action == 'list':
            self.permission_classes = [permissions.IsAuthenticated, ]
        elif self.action == 'create':
            self.permission_classes = [
                _permissions.IsTeacher | permissions.IsAdminUser]
        elif self.action in ['update', 'destroy', 'retrieve']:
            self.permission_classes = [
                _permissions.IsOwner, permissions.IsAuthenticated, ]
        else:
            self.permission_classes = [permissions.IsAdminUser, ]
        return super(self.__class__, self).get_permissions()


class AdvertisementFileViewSet(viewsets.ModelViewSet):

    permission_classes = [_permissions.IsOwner | permissions.IsAdminUser]

    """ Представление файлов объявлений """

    def get_queryset(self):
        user = self.request.user
        return models.AdvertisementFile.objects.filter(user=user)

    def get_serializer_class(self):
        return serializers.AdvertisementFileSerializer
