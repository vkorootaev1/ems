from rest_framework import viewsets, permissions
from university import models
from university.serializers import serializers


class ClassRoomViewSet(viewsets.ModelViewSet):

    """ Представление учебных аудиторий """

    serializer_class = serializers.ClassRoomSerializer

    def get_queryset(self):
        queryset = models.Classroom.objects.all()
        return queryset

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            self.permission_classes = [permissions.IsAuthenticated, ]
        else:
            self.permission_classes = [permissions.IsAdminUser, ]
        return super(self.__class__, self).get_permissions()


class FacultyViewSet(viewsets.ModelViewSet):

    """ Представление факультетов """

    serializer_class = serializers.ClassRoomSerializer

    def get_queryset(self):
        queryset = models.Faculty.objects.all()
        return queryset

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            self.permission_classes = [permissions.IsAuthenticated, ]
        else:
            self.permission_classes = [permissions.IsAdminUser, ]
        return super(self.__class__, self).get_permissions()


class CathedraViewSet(viewsets.ModelViewSet):

    """ Представление кафедр """

    serializer_class = serializers.ClassRoomSerializer

    def get_queryset(self):
        queryset = models.Cathedra.objects.all()
        return queryset

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            self.permission_classes = [permissions.IsAuthenticated, ]
        else:
            self.permission_classes = [permissions.IsAdminUser, ]
        return super(self.__class__, self).get_permissions()


class SpecialityViewSet(viewsets.ModelViewSet):

    """ Представление специальностей """

    serializer_class = serializers.ClassRoomSerializer

    def get_queryset(self):
        queryset = models.Speciality.objects.all()
        return queryset

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            self.permission_classes = [permissions.IsAuthenticated, ]
        else:
            self.permission_classes = [permissions.IsAdminUser, ]
        return super(self.__class__, self).get_permissions()
