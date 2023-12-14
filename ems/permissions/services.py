from study import models as study_models


def get_study_group(request):
    """ Получение группы по ее id """
    try:
        study_group_id = request.query_params.get('study_group_id', None)
        return study_models.StudyGroup.objects.get(pk=study_group_id)
    except:
        return None


def get_studyplan_course(request):
    """ Получение курса учебного плана по его id """
    try:
        studyplan_course_id = request.query_params.get(
            'studyplan_course_id', None)
        return study_models.StudyPlanCourses.objects.get(pk=studyplan_course_id)
    except:
        return None


def get_pair(request):
    """ Получение пары по ее id """
    try:
        pair_id = request.query_params.get('pair_id', None)
        return study_models.TimeTable.objects.get(pk=pair_id)
    except:
        return None


def get_course_teacher_study_group(study_group, studyplan_course):
    """ получение информации, ведет ли преподаватель заданный курс у заданной группы """
    try:
        return study_models.CourseTeacherStudyGroup.objects.\
            get(study_group=study_group, course=studyplan_course)
    except:
        return None
