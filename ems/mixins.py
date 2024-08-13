import datetime
from django.shortcuts import get_object_or_404
from users import models as users_models
from study import models as study_models
from rest_framework.response import Response
from rest_framework import status


class StudentMixin:

    def get_student(self):
        student_id = self.request.headers.get('Student', None)
        try:
            return users_models.Student.objects.get(pk=student_id, user=self.request.user)
        except:
            return None


class TeacherMixin:

    def get_teacher(self):
        return self.request.user.get_teacher()


class ByTeacherMixin:

    def get_by_teacher(self):
        teacher_id = self.request.query_params.get('teacher_id', None)
        try:
            return users_models.Teacher.objects.get(pk=teacher_id)
        except:
            return None


class StudyGroupMixin:

    def get_study_group(self):
        study_group_id = self.request.query_params.get('study_group_id', None)
        try:
            return study_models.StudyGroup.objects.get(pk=study_group_id)
        except:
            return None


class StudyPlanCourseMixin:

    def get_studyplan_course(self):
        studyplan_course_id = self.request.query_params.get(
            'studyplan_course_id', None)
        try:
            return study_models.StudyPlanCourses.objects.get(pk=studyplan_course_id)
        except:
            return None


class TimeTablePairMixin:

    def get_pair(self):
        pair_id = self.request.query_params.get('pair_id', None)
        try:
            return study_models.TimeTable.objects.get(pk=pair_id)
        except:
            return None


class MultipleUpdateMixin:

    """ Multiple update by ids """

    multiple_update_model = None

    def __get__instances(self, data, **filter_kwargs):
        instances = []
        errors = []
        for item in data:
            try:
                instances.append(self.multiple_update_model.objects.get(
                    pk=item.get('id', None), **filter_kwargs))
            except:
                errors.append({'item': item})
        return instances, errors

    def multiple_update(self, request, **filter_kwargs):
        assert self.multiple_update_model, "set multiple_update_model"
        data_list = request.data
        if not isinstance(data_list, list):
            return Response('Only multiple update', status=status.HTTP_400_BAD_REQUEST)
        instances, errors = self.__get__instances(data_list, **filter_kwargs)
        if errors:
            return Response({'errors': errors}, status=status.HTTP_400_BAD_REQUEST)
        for index in range(0, len(instances)):
            serializer = self.get_serializer(
                instance=instances[index], data=data_list[index])
            serializer.is_valid(raise_exception=True)
            serializer.save()
        return Response('Updated OK')
