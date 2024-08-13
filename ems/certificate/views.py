from time import sleep
from rest_framework import viewsets, permissions
from certificate import models
from certificate.serializers import serializers
import permissions.permissions as _permissions
import pagination


class CertificateViewSet(viewsets.ModelViewSet):

    """ Представление справок """

    pagination_class = pagination.SmallPagination

    def get_queryset(self):
        user = self.request.user
        queryset = models.Certificate.objects.filter(user=user).\
            select_related('type', 'user').\
            order_by('-date_add')
        return queryset

    def get_serializer_class(self):
        return serializers.CertificateSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'create']:
            self.permission_classes = [permissions.IsAuthenticated, ]
        elif self.action == 'partial_update':
            if not self.request.user.get_certificate_worker():
                self.permission_classes = [_permissions.IsOwner]
            else:
                self.permission_classes = [permissions.IsAdminUser, ]
        else:
            self.permission_classes = [permissions.IsAdminUser, ]
        return super(self.__class__, self).get_permissions()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['user'] = self.request.user
        return context


class CertificateTypeViewSet(viewsets.ModelViewSet):

    """ Представление вида справок """

    def get_queryset(self):
        sleep(0.3)
        return models.CertificateType.objects.all().\
            order_by('name')

    def get_serializer_class(self):
        return serializers.CertificateTypeSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            self.permission_classes = [permissions.IsAuthenticated, ]
        else:
            self.permission_classes = [permissions.IsAdminUser, ]
        return super(self.__class__, self).get_permissions()
