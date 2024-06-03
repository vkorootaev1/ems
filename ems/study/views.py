from datetime import datetime
from rest_framework import viewsets, permissions, generics
from study import models
from study.serializers import serializers
import permissions.permissions as _permissions
from study import filters
import mixins as _mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Sum, F, Q, Count
from users import models as users_models
import pagination
from rest_framework import status


class TimeTableViewSet(_mixins.StudentMixin,
                       _mixins.TeacherMixin,
                       _mixins.ByTeacherMixin,
                       viewsets.ModelViewSet):

    """ Представление Расписания """

    filterset_class = filters.TimeTableFilter
    pagination_class = pagination.SmallPagination

    def get_queryset(self):
        student = self.get_student()
        teacher = self.get_teacher()
        by_teacher = self.get_by_teacher()

        queryset = models.TimeTable.objects.\
            select_related('teacher__user', 'course', 'classroom').\
            prefetch_related('groups').\
            order_by('date', 'index_pair')

        if by_teacher:
            return queryset.filter(teacher=by_teacher)

        if student:
            return queryset.filter(groups__student_studygroup=student)

        if teacher:
            return queryset.filter(teacher=teacher)

        return queryset

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return serializers.TimeTableSerializer
        else:
            return None

    def get_permissions(self):
        if self.action == 'list':
            self.permission_classes = [
                _permissions.IsStudent | _permissions.IsTeacher | permissions.IsAdminUser]
        elif self.action == 'retrieve':
            self.permission_classes = [_permissions.IsTeacher, ]
        else:
            self.permission_classes = [permissions.IsAdminUser, ]
        return super(self.__class__, self).get_permissions()


class StudyPlanViewSet(_mixins.StudentMixin, viewsets.ModelViewSet):

    """ Представление учебного плана студента """

    def get_queryset(self):
        student = self.get_student()

        queryset = models.StudyPlanCourses.objects.all().\
            select_related('course').\
            order_by('trimester', 'course__name')

        if student:
            queryset = queryset.filter(
                study_plan__studygroup_studyplan__student_studygroup=student)

        return queryset

    def get_serializer_class(self):
        if self.action in ['retrieve', 'list']:
            return serializers.StudyPlanCourseSerializer
        else:
            return None

    def get_permissions(self):
        if self.action == 'list':
            self.permission_classes = [
                _permissions.IsStudent | permissions.IsAdminUser]
        else:
            self.permission_classes = [permissions.IsAdminUser, ]
        return super(self.__class__, self).get_permissions()


class ControlMeasureScoreViewSet(_mixins.StudentMixin,
                                 _mixins.TeacherMixin,
                                 _mixins.StudyPlanCourseMixin,
                                 _mixins.StudyGroupMixin,
                                 _mixins.MultipleUpdateMixin,
                                 viewsets.ModelViewSet):

    """ Представление промежуточных оценок """

    filterset_class = filters.ControlMeasureScoreFilter
    multiple_update_model = models.ControlMeasureScore

    def get_queryset(self):
        student = self.get_student()
        teacher = self.get_teacher()
        studyplancourse = self.get_studyplan_course()
        study_group = self.get_study_group()

        if not ((study_group and studyplancourse) or student or self.request.user.is_staff):
            return models.ControlMeasureScore.objects.none()

        queryset = models.ControlMeasureScore.objects.all().\
            select_related('student__user', 'teacher__user',
                           'control_measure__course')

        if student:
            return queryset.filter(student=student).\
                order_by('control_measure__course__id',
                         'control_measure__order')

        if teacher:
            return queryset.filter(student__study_group=study_group,
                                   control_measure__course=studyplancourse.course).\
                order_by('student__user__last_name', 'control_measure__order')

        return queryset

    @action(detail=False, methods=['put'])
    def multiple_update(self, request):
        study_group = self.get_study_group()
        course = self.get_studyplan_course().course
        filter_kwargs = {'student__study_group': study_group,
                         'control_measure__course': course}
        return super().multiple_update(request, **filter_kwargs)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['teacher'] = self.get_teacher()
        return context

    def get_serializer_class(self):
        if self.action == 'multiple_update':
            return serializers.ControlMeasureScoreMultipleUpdateSerializer
        else:
            return serializers.ControlMeasureScore

    def get_permissions(self):
        if self.action == 'list':
            self.permission_classes = [
                _permissions.IsStudent | _permissions.IsTeacher | permissions.IsAdminUser]
        elif self.action == 'multiple_update':
            self.permission_classes = [
                _permissions.IsTeacherAndHasEdit,]
        else:
            self.permission_classes = [permissions.IsAdminUser, ]
        return super(self.__class__, self).get_permissions()


class CourseScoreViewSet(_mixins.StudentMixin,
                         _mixins.TeacherMixin,
                         _mixins.StudyPlanCourseMixin,
                         _mixins.StudyGroupMixin,
                         _mixins.MultipleUpdateMixin,
                         viewsets.ModelViewSet):

    """ Представление итоговых оценок """

    multiple_update_model = models.CourseScore

    def get_queryset(self):
        student = self.get_student()
        teacher = self.get_teacher()
        studyplancourse = self.get_studyplan_course()
        study_group = self.get_study_group()

        if not ((study_group and studyplancourse) or student or self.request.user.is_staff):
            return models.CourseScore.objects.none()

        queryset = models.CourseScore.objects.all().\
            select_related('course__course', 'student__user',
                           'teacher__user')

        if student:
            return queryset.filter(student=student).\
                exclude(score='NO').\
                order_by('course__trimester',
                         'course__course__name')

        if teacher:
            return queryset.filter(student__study_group=study_group,
                                   course=studyplancourse).\
                order_by('student__user__last_name')

        return queryset

    def get_student_sum_trim_score_by_course(self, student_id, course):
        return models.ControlMeasureScore.objects.\
            filter(student_id=student_id,
                   control_measure__course=course).\
            values('student_id').\
            annotate(not_pass_count=Count('score', filter=Q(
                score__lt=F('control_measure__min_score')))).\
            annotate(sum=Sum('score'))[0]

    def calculate_course_score(self, student_id, course):
        type_of_mark = course.type_of_mark
        trim_scores = self.get_student_sum_trim_score_by_course(
            student_id, course)
        if trim_scores['not_pass_count'] or not trim_scores['sum']:
            return '2' if type_of_mark == 'ex' else 'FA'
        if type_of_mark == 'ex':
            if trim_scores['sum'] > 81:
                return '5'
            elif trim_scores['sum'] > 61:
                return '4'
            else:
                return '3'
        return 'OK'

    @action(detail=False, methods=['put'])
    def set_scores_discipline(self, request):
        studyplancourse = self.get_studyplan_course()
        study_group = self.get_study_group()
        course = models.Course.objects.get(pk=studyplancourse.course.id)
        teacher = self.get_teacher()

        course_scores = models.CourseScore.objects.\
            filter(student__study_group=study_group,
                   course=studyplancourse).select_related('student__user').\
            order_by('student__user__last_name')

        for course_score in course_scores:
            course_score.score = self.calculate_course_score(
                course_score.student_id, course)
            course_score.teacher = teacher
            course_score.save()

        serializer = self.get_serializer(course_scores, many=True)

        return Response(serializer.data)

    @action(detail=False, methods=['put'])
    def set_scores_other(self, request):
        studyplancourse = self.get_studyplan_course()
        if studyplancourse.course.type_of_course == 'DISCIPLINE':
            return Response(status=status.HTTP_400_BAD_REQUEST)
        study_group = self.get_study_group()
        filter_kwargs = {'student__study_group': study_group,
                         'course': studyplancourse}
        return super().multiple_update(request, **filter_kwargs)

    def get_serializer_class(self):
        if self.action == 'set_scores_other':
            return serializers.CourseScoreOtherMultipleUpdateSerializer
        return serializers.CourseScoreSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        if self.action == 'set_scores_other':
            context['teacher'] = self.get_teacher()
            context['type_of_mark'] = self.get_studyplan_course(
            ).course.type_of_mark
        return context

    def get_permissions(self):
        if self.action == 'list':
            self.permission_classes = [
                _permissions.IsStudent | _permissions.IsTeacher | permissions.IsAdminUser]
        elif self.action in ['set_scores_discipline', 'set_scores_other']:
            self.permission_classes = [
                _permissions.IsTeacherAndHasEdit]
        else:
            self.permission_classes = [permissions.IsAdminUser, ]
        return super(self.__class__, self).get_permissions()


class AttendanceViewSet(_mixins.StudentMixin,
                        _mixins.TeacherMixin,
                        _mixins.TimeTablePairMixin,
                        _mixins.MultipleUpdateMixin,
                        viewsets.ModelViewSet):

    """ Представление посещаемости """

    filterset_class = filters.AttendanceFilter
    multiple_update_model = models.Attendance
    pagination_class = pagination.SmallPagination

    def get_queryset(self):
        student = self.get_student()
        teacher = self.get_teacher()
        pair = self.get_pair()

        if not ((pair and pair.teacher == teacher) or student):
            return models.Attendance.objects.none()

        queryset = models.Attendance.objects.all().\
            select_related('pair__course', 'student__user', 'teacher__user', 'student__study_group').\
            order_by('-date_upd')

        if student:
            return queryset.filter(student=student, status=False).\
                order_by('date_upd')

        if teacher:
            if not pair.is_attendance:
                self.create_attendance_list(pair, teacher)
            return queryset.filter(pair=pair).\
                order_by('student__user__last_name')

        return queryset

    def create_attendance_list(self, pair, teacher):
        students = users_models.Student.objects.\
            filter(study_group__timetable_group=pair).\
            prefetch_related('study_group__timetable_group')

        for student in students:
            models.Attendance.objects.create(
                student=student,
                pair=pair,
                teacher=teacher
            )

        pair.is_attendance = True
        pair.save()

    @action(detail=False, methods=['put'])
    def multiple_update(self, request):
        pair = self.get_pair()
        filter_kwargs = {'pair': pair}
        return super().multiple_update(request, **filter_kwargs)

    def get_serializer_class(self):
        if self.action == 'multiple_update':
            return serializers.AttendanceMultipleUpdateSerializer
        else:
            return serializers.AttendanceSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['teacher'] = self.get_teacher()
        return context

    def get_permissions(self):
        if self.action == 'list':
            self.permission_classes = [
                _permissions.IsStudent | _permissions.IsTeacher | permissions.IsAdminUser]
        elif self.action == 'multiple_update':
            self.permission_classes = [
                _permissions.IsTeacherAndHasEdit]
        else:
            self.permission_classes = [permissions.IsAdminUser, ]
        return super(self.__class__, self).get_permissions()


class TrimesterViewSet(_mixins.StudentMixin, viewsets.ModelViewSet):

    """ Представление триместра """
    """ Код по созданию, изменению, удалению записи о триместре 
        создается автоматически самим Django REST Framework и может быть переписан"""

    # Получение всех записей о триместрах из БД
    def get_queryset(self):
        queryset = models.Trimester.objects.all().order_by('-date_start')

        if not self.request.user.is_staff:
            now = datetime.now().date()
            queryset = queryset.filter(date_start__lte=now)

        return queryset

    # Получение сериализатора
    def get_serializer_class(self):
        return serializers.TrimesterSerializer

    # Получение текущего триместра
    @action(detail=False, url_path='current')
    def get_current_trimester(self, request):
        current_trimester = models.Trimester.objects.get_current_trimester()
        if not current_trimester:
            return Response({'error': 'current trimester not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(current_trimester)
        return Response(serializer.data)

    # Получение текущего триместра студента (на каком курсе и каком триместре он обучается в данный момент времени)
    @action(detail=False, url_path='student')
    def get_current_student_trimester(self, request):
        student = self.get_student()
        if student:
            current_student_trimester = models.Trimester.objects.get_current_student_trimester(
                student)
            return Response({'current_student_trimester': current_student_trimester})
        return Response({'error': 'current student trimester not found'}, status=status.HTTP_404_NOT_FOUND)

    # Получение прошедших триместров студента
    @action(detail=False, url_path='student/passed')
    def get_passed_student_trimester(self, request):
        student = self.get_student()
        if student:
            study_group = models.StudyGroup.objects.get(
                pk=student.study_group.id)
            trimesters = models.Trimester.objects.filter(
                Q(date_start__gte=study_group.begin_date) &
                Q(date_start__lte=datetime.now().date())
                & Q(date_end__lte=study_group.end_date)).\
                order_by('-date_start')
            serializer = self.get_serializer(trimesters, many=True)
            return Response(serializer.data)
        return Response({'error': 'passed student trimesters not found'}, status=status.HTTP_404_NOT_FOUND)

    # Проверка прав доступа
    def get_permissions(self):
        if self.action in ['retrieve', 'list', 'get_current_trimester']:
            self.permission_classes = [
                permissions.IsAuthenticated, ]
        elif self.action in ['get_current_student_trimester', 'get_passed_student_trimester']:
            self.permission_classes = [_permissions.IsStudent, ]
        else:
            self.permission_classes = [permissions.IsAdminUser, ]
        return super(self.__class__, self).get_permissions()


class StudyGroupCourseListAPIView(_mixins.TeacherMixin,
                                  generics.ListAPIView):

    """ Представление учебной группы и их курсов у преподавателя"""

    permission_classes = [_permissions.IsTeacher, ]
    filterset_class = filters.StudyGroupCourseListFilter
    pagination_class = pagination.SmallPagination

    def get_queryset(self):
        teacher = self.get_teacher()
        return models.CourseTeacherStudyGroup.objects.filter(
            teacher=teacher).\
            select_related('trimester', 'course', 'study_group').\
            order_by('trimester', 'study_group__name')

    def get_serializer_class(self):
        return serializers.StudyGroupCourseListSerializer


class StudyGroupViewSet(viewsets.ModelViewSet):

    """ Представление учебной группы """

    filterset_class = filters.StudyGroupFilter

    def get_queryset(self):
        return models.StudyGroup.objects.all()

    def get_serializer_class(self):
        return serializers.StudyGroupSerializer

    def get_permissions(self):
        if self.action in ['retrieve', 'list']:
            self.permission_classes = [
                permissions.IsAuthenticated, ]
        else:
            self.permission_classes = [permissions.IsAdminUser, ]
        return super(self.__class__, self).get_permissions()
