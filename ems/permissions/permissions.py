from rest_framework import permissions
import permissions.services as services


class IsTeacher(permissions.BasePermission):
    
    """ Разрешение - является ли пользователь преподавателем """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.get_teacher())


class IsStudent(permissions.BasePermission):
    
    """ Разрешение - является ли пользователь студентом """

    def has_permission(self, request, view):
        student_id = request.headers.get('Student', None)
        return bool(student_id and request.user and request.user.is_authenticated and request.user.get_student(student_id))


class IsOwner(permissions.BasePermission):
    
    """ Разрешение - может ли пользователь редактировать запись """

    def has_permission(self, request, view):
        return bool(request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsTeacherAndHasEdit(permissions.BasePermission):
    
    """ Разрешение - может ли преподаватель редактировать запись """
    """ Посещаемость, промежуточные оценки, итоговые оценки """

    def has_permission(self, request, view):
        teacher = request.user.get_teacher()

        if bool(request.user and request.user.is_authenticated and teacher):

            if view.basename == 'attendance':
                pair = services.get_pair(request)

                if pair:
                    return bool(pair.teacher == teacher)

            if view.basename in ['resultscore', 'controlmeasurescore']:
                study_group = services.get_study_group(request)
                studyplan_course = services.get_studyplan_course(request)
                course_teacher_study_group = services.get_course_teacher_study_group(
                    study_group, studyplan_course)

                if study_group and studyplan_course and course_teacher_study_group:
                    return bool(course_teacher_study_group.teacher == teacher)
            
            return request.user.is_staff