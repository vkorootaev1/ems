from django.db import models


class Classroom(models.Model):

    """ Модель аудитории университета """

    name = models.CharField(max_length=150, blank=True,
                            verbose_name='Название')
    number = models.CharField(max_length=150, verbose_name='Номер аудитории')
    house = models.PositiveSmallIntegerField(verbose_name='Корпус')
    floor = models.PositiveSmallIntegerField(verbose_name='Этаж')
    description = models.TextField(blank=True, verbose_name='Описание')
    is_active = models.BooleanField(default=True, verbose_name='Доступность')

    class Meta:
        verbose_name = 'Аудитория'
        verbose_name_plural = 'Аудитории'
        unique_together = ['number', 'house', 'floor']

    def __str__(self):
        return f'ауд. {self.number}, к. {self.house}, эт. {self.floor}'


class Faculty(models.Model):

    """ Модель факультета университета """

    name = models.CharField(max_length=150, verbose_name='Название')
    description = models.TextField(blank=True, verbose_name='Описание')
    is_active = models.BooleanField(default=True, verbose_name='Доступность')

    class Meta:
        verbose_name = 'Факультет'
        verbose_name_plural = 'Факультеты'

    def __str__(self):
        return f'{self.name}'


class Cathedra(models.Model):

    """ Модель кафедры университета """

    name = models.CharField(max_length=150, verbose_name='Название')
    description = models.TextField(blank=True, verbose_name='Описание')
    faculty = models.ForeignKey(
        'Faculty', on_delete=models.PROTECT, related_name='cathedra_faculty', verbose_name='Факультет')
    is_active = models.BooleanField(default=True, verbose_name='Доступность')

    class Meta:
        verbose_name = 'Кафедра'
        verbose_name_plural = 'Кафедры'

    def __str__(self):
        return f'{self.name}, {self.faculty}'


class Speciality(models.Model):

    """ Модель специальности """

    LEVELS_OF_HIGHER_EDUCATION_CHOICES = [
        ('BA', 'Бакалавриат'),
        ('SP', 'Специалитет'),
        ('MA', 'Магистратура'),
        ('AS', 'Аспирантура')
    ]

    FORM_OF_STUDY_CHOICES = [
        ('INTO', 'Очное'),
        ('EXTR', 'Заочное'),
        ('EVEN', 'Очно-заочное')
    ]

    code = models.CharField(max_length=150, unique=True, verbose_name='Код')
    name = models.CharField(max_length=150, verbose_name='Название')
    description = models.TextField(blank=True, verbose_name='Описание')
    level_of_higher_education = models.CharField(max_length=2,
                                                 choices=LEVELS_OF_HIGHER_EDUCATION_CHOICES, verbose_name='Уровень образования')
    study_period_months = models.PositiveSmallIntegerField(
        verbose_name='Период обучения(мес.)')
    form_of_study = models.CharField(
        max_length=4, choices=FORM_OF_STUDY_CHOICES, verbose_name='Форма обучения')
    cathedra = models.ForeignKey('Cathedra', on_delete=models.PROTECT,
                                 related_name='speciality_cathedra', verbose_name='Кафедра')
    is_active = models.BooleanField(default=True, verbose_name='Доступность')

    class Meta:
        verbose_name = 'Специальность'
        verbose_name_plural = 'Специальности'

    def __str__(self):
        return f'{self.name}, {self.get_level_of_higher_education_display()}, {self.get_form_of_study_display()} ({self.study_period_months})'
