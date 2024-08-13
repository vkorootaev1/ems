from time import sleep
from rest_framework import viewsets, permissions
from users import models
from rest_framework.decorators import action
from rest_framework.response import Response
from users.serializers import nested_serializers, serializers
import mixins as _mixins
import pagination
import permissions.permissions as _permissions
from users import filters


class UserViewSet(_mixins.StudentMixin,
                  _mixins.TeacherMixin,
                  viewsets.ModelViewSet):

    """ Представление пользователя """

    def get_queryset(self):
        return models.User.objects.all()

    @action(detail=False)
    def details(self, request):
        user = self.request.user
        serializer = self.get_serializer(user)
        return Response(serializer.data)

    @action(detail=False, methods=['patch'])
    def set_email(self, request):
        instance = self.request.user
        serializer = self.get_serializer(data=request.data, instance=instance)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response('Email updated OK')

    @action(detail=False)
    def current(self, request):
        student = self.get_student()
        teacher = self.get_teacher()

        if student:
            serializer_data = student

        elif teacher:
            serializer_data = teacher

        else:
            return Response('Underfined')

        serializer = self.get_serializer(serializer_data)
        return Response(serializer.data)

    def get_serializer_class(self):
        if self.action == 'details':
            return nested_serializers.UserDetailSerializer
        elif self.action == 'set_email':
            return serializers.UserUpdateEmailSerializer
        elif self.action == 'current':
            if self.get_student():
                return nested_serializers.NestedStudentWithGroupEmailSerializer
            else:
                return nested_serializers.NestedTeacherWithEmailSerializer
        else:
            return serializers.UserSerializer

    def get_permissions(self):
        if self.action in ['details', 'set_email', 'current']:
            self.permission_classes = [permissions.IsAuthenticated, ]
        else:
            self.permission_classes = [permissions.IsAdminUser, ]
        return super(self.__class__, self).get_permissions()


class TeachersViewSet(viewsets.ModelViewSet):

    """ Представление преподавателя """

    pagination_class = pagination.SmallPagination
    filterset_class = filters.TeacherFilter

    def get_queryset(self):
        queryset = models.Teacher.objects.all().\
            select_related('user').\
            order_by('user__last_name', 'user__first_name')

        if self.action == 'retrieve':
            queryset = queryset.prefetch_related(
                'courses', 'cathedra', 'user__contact_user')

        return queryset

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.TeacherListSerializer
        elif self.action == 'retrieve':
            return serializers.TeacherRetrieveSerializer
        else:
            return serializers.TeacherListSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            self.permission_classes = [permissions.IsAuthenticated, ]
        else:
            self.permission_classes = [permissions.IsAdminUser, ]
        return super(self.__class__, self).get_permissions()


class ContactViewSet(viewsets.ModelViewSet):

    """ Представление контактов преподавателя и другого персонала """

    filterset_class = filters.ContactFilter

    def get_queryset(self):
        queryset = models.Contact.objects.all().\
            select_related('type', 'user').\
            order_by('user__last_name', 'user__first_name')
        return queryset

    def get_serializer_class(self):
        return serializers.ContactSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            self.permission_classes = [permissions.IsAuthenticated, ]
        elif self.action == 'create':
            self.permission_classes = [_permissions.IsTeacher]
        else:
            self.permission_classes = [
                _permissions.IsOwner,]
        return super(self.__class__, self).get_permissions()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['user'] = self.request.user
        return context


class ContactTypeViewSet(viewsets.ModelViewSet):

    """ Представление для типа контактов """

    def get_queryset(self):
        return models.ContactType.objects.all()

    def get_serializer_class(self):
        return serializers.ContactTypeSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            self.permission_classes = [permissions.IsAuthenticated, ]
        else:
            self.permission_classes = [permissions.IsAdminUser, ]
        return super(self.__class__, self).get_permissions()
