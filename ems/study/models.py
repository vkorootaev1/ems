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
        ('DIPLOM', 'Квалификационная работа'),
        ('PHYS_CULT', 'Физическая культура'),
    ]

    TYPE_OF_MARK_CHOICES = [
        ('ex', 'Экзамен'),
        ('za', 'Зачет')
    ]

    code = models.CharField(max_length=150, unique=True,
                            verbose_name='Код')
    name = models.CharField(max_length=150, verbose_name='Название')
    subcourse_number = models.CharField(
        max_length=150, blank=True, verbose_name='Номер субкурса')
    description = models.TextField(blank=True, verbose_name='Описание')
    classroom_worktime = models.PositiveSmallIntegerField(
        verbose_name='Количество ауд. часов')
    independent_worktime = models.PositiveSmallIntegerField(
        verbose_name='Количество сам. часов')
    type_of_course = models.CharField(
        max_length=10, choices=TYPE_OF_COURSE_CHOICES, verbose_name='Тип курса')
    type_of_mark = models.CharField(
        max_length=2, choices=TYPE_OF_MARK_CHOICES, verbose_name='Тип оценки')
    count_of_lectures_pairs = models.PositiveSmallIntegerField(
        verbose_name='Количество лек. пар')
    count_of_practies_pairs = models.PositiveSmallIntegerField(
        verbose_name='Количество прак. пар')
    count_of_laboratory_pairs = models.PositiveSmallIntegerField(
        verbose_name='Количество лаб. пар')
    owners = models.ManyToManyField('users.Teacher',
                                    related_name='course_teacher', verbose_name='Владельцы')
    is_active = models.BooleanField(default=True, verbose_name='Доступность')

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'

    def truncate_name(self):
        return (self.name[:30] + '..') if len(self.name) > 30 else self.name

    def __str__(self):
        return f'{self.truncate_name()}({self.subcourse_number}), {self.classroom_worktime}, {self.independent_worktime}'


class ControlMeasure(models.Model):

    """ Модель контрольного мероприятия """

    name = models.CharField(max_length=150, verbose_name='Название')
    description = models.TextField(blank=True, verbose_name='Описание')
    course = models.ForeignKey('Course', on_delete=models.PROTECT,
                               related_name='coursecontrolmeasure_course', verbose_name='Курс')
    max_score = models.FloatField(verbose_name='Максимальный балл')
    min_score = models.FloatField(verbose_name='Минимальный балл')
    date_add = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата добавления')
    date_upd = models.DateTimeField(
        auto_now=True, verbose_name='Дата обновления')
    is_active = models.BooleanField(default=True, verbose_name='Доступность')
    order = models.PositiveSmallIntegerField(
        verbose_name='Порядок контрольной точки')

    class Meta:
        verbose_name = 'Контрольное мероприятие'
        verbose_name_plural = 'Контрольные мероприятия'

    def truncate_name(self):
        return (self.name[:30] + '..') if len(self.name) > 30 else self.name

    def __str__(self):
        return f'{self.course.truncate_name()}({self.course.subcourse_number}), {self.truncate_name()}({self.order})'


class StudyPlan(models.Model):

    """ Модель учебного плана """

    code = models.CharField(max_length=150, unique=True,
                            verbose_name='Код учебного плана')
    name = models.CharField(max_length=150, verbose_name='Название')
    description = models.TextField(blank=True, verbose_name='Описание')
    speciality = models.ForeignKey('university.Speciality', on_delete=models.PROTECT,
                                   related_name='studyplan_speciality', verbose_name='Специальность')
    is_active = models.BooleanField(default=True, verbose_name='Доступность')

    class Meta:
        verbose_name = 'Учебный план'
        verbose_name_plural = 'Учебные планы'

    def __str__(self):
        return f'{self.name}, {self.speciality.name}'


class StudyPlanCourses(models.Model):

    """ Модель курсов учебного плана """

    trimester = models.PositiveSmallIntegerField(verbose_name='Триместр')
    course = models.ForeignKey('Course', on_delete=models.PROTECT,
                               related_name='studyplancourses_course', verbose_name='Курс')
    study_plan = models.ForeignKey('StudyPlan', on_delete=models.PROTECT,
                                   related_name='studyplancourses_studyplan', verbose_name='Учебный план')

    def __str__(self):
        return f'{self.trimester}, {self.course.name}, {self.study_plan.code}'

    class Meta:
        verbose_name = 'Курс и учебный план'
        verbose_name_plural = 'Курсы и учебные планы'
        unique_together = ['trimester', 'course', 'study_plan']


class Trimester(models.Model):

    """ Модель триместра (семестра) """

    TRIMESTER_CHOICES = [
        ('1', 'Осенний'),
        ('2', 'Весенний'),
        ('3', 'Летний')
    ]
    trimester = models.CharField(
        choices=TRIMESTER_CHOICES, max_length=1, verbose_name='Триместр')
    date_start = models.DateField(verbose_name='Дата начала')
    date_end = models.DateField(verbose_name='Дата окончания')

    objects = managers.TrimesterManager()

    def __str__(self):
        return f'{self.trimester}, {self.date_start}, {self.date_end}'

    class Meta:
        verbose_name = 'Триместр'
        verbose_name_plural = 'Триместры'
        ordering = ['-date_start', ]
        unique_together = ['date_start', 'date_end']


class StudyGroup(models.Model):

    """ Модель учебной группы """

    name = models.CharField(max_length=150, verbose_name='Название')
    code = models.CharField(max_length=150, unique=True, verbose_name='Код')
    begin_date = models.DateField(verbose_name='Дата начала обучения')
    end_date = models.DateField(verbose_name='Дата окончания обучения')
    study_plan = models.ForeignKey('StudyPlan', on_delete=models.PROTECT,
                                   related_name='studygroup_studyplan', verbose_name='Учебный план')
    is_active = models.BooleanField(default=True, verbose_name='Доступность')

    class Meta:
        verbose_name = 'Учебная группа'
        verbose_name_plural = 'Учебные группы'

    def __str__(self):
        return f'{self.name}, ({self.begin_date} - {self.end_date})'


class TimeTable(models.Model):

    """ Модель расписания """

    # Типы пар
    TYPE_OF_PAIR = [
        ('LE', 'Лекция'),
        ('PR', 'Практика'),
        ('LA', 'Лабораторная работа')
    ]
    # Дата пары
    date = models.DateField(verbose_name='Дата пары')
    # Учебные группы, у которых проводится пара
    groups = models.ManyToManyField('StudyGroup',
                                    related_name='timetable_group', verbose_name='Группы')
    # Тип пары
    type_of_pair = models.CharField(
        max_length=2, choices=TYPE_OF_PAIR, verbose_name='Тип пары')
    # Порядок пары (1, 2, 3, ...)
    index_pair = models.PositiveSmallIntegerField(verbose_name='Номер пары')
    # Дисциплина, которая проводится на паре
    course = models.ForeignKey('Course', on_delete=models.PROTECT,
                               related_name='timetable_course', verbose_name='Курс')
    # Преподаватель, который ведет пару
    teacher = models.ForeignKey('users.Teacher', on_delete=models.PROTECT,
                                related_name='timetable_teacher', verbose_name='Преподаватель')
    # Аудитория, в которой проводится пара
    classroom = models.ForeignKey('university.Classroom', on_delete=models.PROTECT,
                                  related_name='timetable_classroom', verbose_name='Аудитория')
    # Дата создания записи о паре
    date_add = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата добавления')
    # Дата последнего изменения информации о паре
    date_upd = models.DateTimeField(
        auto_now=True, verbose_name='Дата обновления')
    # Выставлена ли посещаемость студентам за текущую пару
    is_attendance = models.BooleanField(
        default=None, blank=True, verbose_name='Посещаемость')

    # Мета информация о модели
    class Meta:
        verbose_name = 'Пара'
        verbose_name_plural = 'Расписание'

    def __str__(self):
        return f'{self.date}, {self.course.truncate_name()} ({self.get_type_of_pair_display()}, {self.classroom})'


class Attendance(models.Model):

    """ Модель посещаемости """

    student = models.ForeignKey('users.Student', on_delete=models.CASCADE,
                                related_name='attendance_student', verbose_name='Студент')
    pair = models.ForeignKey('TimeTable', on_delete=models.PROTECT,
                             related_name='attendance_pair', verbose_name='Пара')
    status = models.BooleanField(null=True, blank=True, verbose_name='Статус')
    date_upd = models.DateTimeField(
        auto_now=True, verbose_name='Дата обновления')
    teacher = models.ForeignKey('users.Teacher', on_delete=models.PROTECT,
                                related_name='attendance_teacher', verbose_name='Преподаватель')

    def __str__(self):
        return f'{self.pair}, {self.student.user.fio()} '

    class Meta:
        verbose_name = 'Посещаемость'
        verbose_name_plural = 'Посещаемость'
        unique_together = ['student', 'pair']


class ControlMeasureScore(models.Model):

    """ Модель промежуточной оценки студента (оценки за контрольное мероприятие) """

    student = models.ForeignKey('users.Student', on_delete=models.PROTECT,
                                related_name='controlmeasurescore_student', verbose_name='Студент')
    control_measure = models.ForeignKey('ControlMeasure',
                                        on_delete=models.PROTECT,
                                        related_name='controlmeasurescore_controlmeasure', verbose_name='Контрольное мероприятие')
    score = models.FloatField(blank=True, null=True, verbose_name='Балл')
    teacher = models.ForeignKey('users.Teacher', on_delete=models.PROTECT,
                                related_name='controlmeasurescore_teacher', verbose_name='Преподаватель')
    date_upd = models.DateTimeField(
        auto_now=True, verbose_name='Дата обновления')

    def __str__(self):
        return f'{self.student.user.fio()}, {self.control_measure.name}, {self.score}'

    class Meta:
        verbose_name = 'Оценка за контрольное мероприятие'
        verbose_name_plural = 'Оценки за контрольные мероприятия'
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
                               related_name='coursescore_course', verbose_name='Курс')
    student = models.ForeignKey('users.Student', on_delete=models.PROTECT,
                                related_name='coursescore_student', verbose_name='Студент')
    score = models.CharField(
        max_length=2, choices=SCORES, verbose_name='Оценка')
    teacher = models.ForeignKey('users.Teacher', on_delete=models.PROTECT,
                                related_name='coursescore_teacher', verbose_name='Преподаватель')
    date_upd = models.DateTimeField(
        auto_now=True, verbose_name='Дата обновления')

    def __str__(self):
        return (f'{self.student.user.fio()},'
                f'{self.course.course.truncate_name()}({self.course.course.subcourse_number}), {self.score}')

    class Meta:
        verbose_name = 'Итоговая оценка'
        verbose_name_plural = 'Итоговые оценки'
        unique_together = ['course', 'student']


class CourseTeacherStudyGroup(models.Model):

    """ Модель курсов, которые ведет преподаватель у группы в триместре """

    trimester = models.ForeignKey('Trimester', on_delete=models.PROTECT,
                                  related_name='courseteacherstudygroup_trimester', verbose_name='Триместр')
    course = models.ForeignKey('StudyPlanCourses', on_delete=models.PROTECT,
                               related_name='courseteacherstudygroup_course', verbose_name='Курс')
    teacher = models.ForeignKey('users.Teacher', on_delete=models.PROTECT,
                                related_name='courseteacherstudygroup_teacher', verbose_name='Преподаватель')
    study_group = models.ForeignKey('StudyGroup', on_delete=models.PROTECT,
                                    related_name='courseteacherstudygroup_studygroup', verbose_name='Учебная группа')

    class Meta:
        verbose_name = 'Курс, преподаватель, учебная группа'
        verbose_name_plural = 'Курсы, преподаватели, учебные группы'

    def __str__(self):
        return f'{self.course.course.name}, {self.teacher}, {self.study_group.name}'
