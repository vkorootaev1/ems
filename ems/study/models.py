from django.db import models
from study import managers


class Course(models.Model):
    
    """ Модель курса (дисциплины) """
    
    TYPE_OF_COURSE_CHOICES = [
        ('STUDY_PRAC', 'Практика'),
        ('DISCIPLINE', 'Дисциплина'),
        ('STUDY_PRAC', 'Учебная практика'),
        ('PROD_PRAC', 'Производственная практика'),
        ('COURSE', 'Курсовая работа'),
        ('GROUP', 'Групповая работа'),
        ('NIRS', 'Научно-исследовательская работа'),
        ('GOS_EX', 'Государственный экзамен'),
        ('DIPLOM', 'Квалификационная работа')
    ]

    TYPE_OF_MARK_CHOICES = [
        ('ex', 'Экзамен'),
        ('za', 'Зачет')
    ]

    code = models.CharField(max_length=150, unique=True)
    name = models.CharField(max_length=150)
    subcourse_number = models.CharField(max_length=150, blank=True)
    description = models.TextField(blank=True)
    classroom_worktime = models.PositiveSmallIntegerField()
    independent_worktime = models.PositiveSmallIntegerField()
    type_of_course = models.CharField(
        max_length=10, choices=TYPE_OF_COURSE_CHOICES)
    type_of_mark = models.CharField(max_length=2, choices=TYPE_OF_MARK_CHOICES)
    count_of_lectures_pairs = models.PositiveSmallIntegerField()
    count_of_practies_pairs = models.PositiveSmallIntegerField()
    count_of_laboratory_pairs = models.PositiveSmallIntegerField()
    owners = models.ManyToManyField('users.Teacher',
                                    related_name='course_teacher')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.name}({self.subcourse_number}), {self.classroom_worktime}, {self.independent_worktime}'


class ControlMeasure(models.Model):
    
    """ Модель контрольного мероприятия """

    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    course = models.ForeignKey('Course', on_delete=models.PROTECT,
                               related_name='coursecontrolmeasure_course')
    max_score = models.FloatField()
    min_score = models.FloatField()
    date_add = models.DateTimeField(auto_now_add=True)
    date_upd = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    order = models.PositiveSmallIntegerField()

    def __str__(self):
        return f'{self.course.name}({self.course.subcourse_number}), {self.order}, {self.name}'


class StudyPlan(models.Model):
    
    """ Модель учебного плана """
    
    code = models.CharField(max_length=150, unique=True)
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    speciality = models.ForeignKey('university.Speciality', on_delete=models.PROTECT,
                                   related_name='studyplan_speciality')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.code}, {self.name}'


class StudyPlanCourses(models.Model):
    
    """ Модель курсов учебного плана """
    
    trimester = models.PositiveSmallIntegerField()
    course = models.ForeignKey('Course', on_delete=models.PROTECT,
                               related_name='studyplancourses_course')
    study_plan = models.ForeignKey('StudyPlan', on_delete=models.PROTECT,
                                   related_name='studyplancourses_studyplan')

    def __str__(self):
        return f' {self.id}, {self.trimester}, {self.course.name}, {self.study_plan.code}'

    class Meta:
        unique_together = ['trimester', 'course', 'study_plan']


class Trimester(models.Model):
    
    """ Модель триместра (семестра) """
    
    TRIMESTER_CHOICES = [
        ('1', 'Осенний'),
        ('2', 'Весенний'),
        ('3', 'Летний')
    ]
    trimester = models.CharField(choices=TRIMESTER_CHOICES, max_length=1)
    date_start = models.DateField()
    date_end = models.DateField()

    objects = managers.TrimesterManager()

    def __str__(self):
        return f'{self.trimester}, {self.date_start}, {self.date_end}'

    class Meta:
        unique_together = ['date_start', 'date_end']


class StudyGroup(models.Model):
    
    """ Модель учебной группы """
    
    name = models.CharField(max_length=150)
    code = models.CharField(max_length=150, unique=True)
    begin_date = models.DateField()
    end_date = models.DateField()
    study_plan = models.ForeignKey('StudyPlan', on_delete=models.PROTECT,
                                   related_name='studygroup_studyplan')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.name}'


class TimeTable(models.Model):
    
    """ Модель расписания """
    
    TYPE_OF_PAIR = [
        ('LE', 'Лекция'),
        ('PR', 'Практика'),
        ('LA', 'Лабораторная работа')
    ]

    date = models.DateField()
    groups = models.ManyToManyField('StudyGroup',
                                    related_name='timetable_group')
    type_of_pair = models.CharField(max_length=2, choices=TYPE_OF_PAIR)
    index_pair = models.PositiveSmallIntegerField()
    course = models.ForeignKey('Course', on_delete=models.PROTECT,
                               related_name='timetable_course')
    teacher = models.ForeignKey('users.Teacher', on_delete=models.PROTECT,
                                related_name='timetable_teacher')
    classroom = models.ForeignKey('university.Classroom', on_delete=models.PROTECT,
                                  related_name='timetable_classroom')
    date_add = models.DateTimeField(auto_now_add=True)
    date_upd = models.DateTimeField(auto_now=True)
    is_attendance = models.BooleanField(default=None, blank=True)

    def __str__(self):
        return f'{self.id}, {self.date}, {self.course.name} ({self.get_type_of_pair_display()}, {self.classroom})'


class Attendance(models.Model):
    
    """ Модель посещаемости """
    
    student = models.ForeignKey('users.Student', on_delete=models.CASCADE,
                                related_name='attendance_student')
    pair = models.ForeignKey('TimeTable', on_delete=models.PROTECT,
                             related_name='attendance_pair')
    status = models.BooleanField(null=True, blank=True)
    date_upd = models.DateTimeField(auto_now=True)
    teacher = models.ForeignKey('users.Teacher', on_delete=models.PROTECT,
                                related_name='attendance_teacher')

    def __str__(self):
        return f'{self.student.user.fio()}, {self.pair}'

    class Meta:
        unique_together = ['student', 'pair']


class ControlMeasureScore(models.Model):
    
    """ Модель промежуточной оценки студента (оценки за контрольное мероприятие) """
    
    student = models.ForeignKey('users.Student', on_delete=models.PROTECT,
                                related_name='controlmeasurescore_student')
    control_measure = models.ForeignKey('ControlMeasure',
                                        on_delete=models.PROTECT,
                                        related_name='controlmeasurescore_controlmeasure')
    score = models.FloatField(blank=True, null=True)
    teacher = models.ForeignKey('users.Teacher', on_delete=models.PROTECT,
                                related_name='controlmeasurescore_teacher')
    date_upd = models.DateTimeField(auto_now=True)

    def __str__(self):
        return (f' {self.id}, {self.control_measure.course.name},  {self.student.user.fio()},'
                f'{self.control_measure.name}, {self.control_measure.course.name}, {self.score}')

    class Meta:
        unique_together = ['student', 'control_measure']


class CourseScore(models.Model):
    
    """ Модель итоговой оценки студента за курс """
    
    SCORES = [
        ('5', '5'),
        ('4', '4'),
        ('3', '3'),
        ('2', '2'),
        ('OK', 'Зачет'),
        ('FA', 'Незачет'),
        ('NO', 'Не выставлено')
    ]

    course = models.ForeignKey('StudyPlanCourses', on_delete=models.PROTECT,
                               related_name='coursescore_course')
    student = models.ForeignKey('users.Student', on_delete=models.PROTECT,
                                related_name='coursescore_student')
    score = models.CharField(max_length=2, choices=SCORES)
    teacher = models.ForeignKey('users.Teacher', on_delete=models.PROTECT,
                                related_name='coursescore_teacher')
    date_upd = models.DateTimeField(auto_now=True)

    def __str__(self):
        return (f'{self.student.user.fio()},'
                f'{self.course.course.name}({self.course.course.subcourse_number}), {self.score}')

    class Meta:
        unique_together = ['course', 'student']


class CourseTeacherStudyGroup(models.Model):
    
    """ Модель курсов, которые ведет преподаватель у группы в триместре """
    
    trimester = models.ForeignKey('Trimester', on_delete=models.PROTECT,
                                   related_name='courseteacherstudygroup_trimester')
    course = models.ForeignKey('StudyPlanCourses', on_delete=models.PROTECT,
                               related_name='courseteacherstudygroup_course')
    teacher = models.ForeignKey('users.Teacher', on_delete=models.PROTECT,
                                related_name='courseteacherstudygroup_teacher')
    study_group = models.ForeignKey('StudyGroup', on_delete=models.PROTECT,
                                    related_name='courseteacherstudygroup_studygroup')

    def __str__(self):
        return f'{self.course.course.name}, {self.teacher}, {self.study_group.name}'
