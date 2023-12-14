from django.db import models


class Classroom(models.Model):
    
    """ Модель аудитории университета """
    
    name = models.CharField(max_length=150, blank=True)
    number = models.CharField(max_length=150)
    house = models.PositiveSmallIntegerField()
    floor = models.PositiveSmallIntegerField()
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ['number', 'house', 'floor']

    def __str__(self):
        return f'ауд. {self.number}, к. {self.house}, эт. {self.floor}'


class Faculty(models.Model):
    
    """ Модель факультета университета """
    
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.name}'


class Cathedra(models.Model):
    
    """ Модель кафедры университета """
    
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    faculty = models.ForeignKey(
        'Faculty', on_delete=models.PROTECT, related_name='cathedra_faculty')
    is_active = models.BooleanField(default=True)

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

    code = models.CharField(max_length=150, unique=True)
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    level_of_higher_education = models.CharField(max_length=2,
                                                 choices=LEVELS_OF_HIGHER_EDUCATION_CHOICES)
    study_period_months = models.PositiveSmallIntegerField()
    form_of_study = models.CharField(
        max_length=4, choices=FORM_OF_STUDY_CHOICES)
    cathedra = models.ForeignKey('Cathedra', on_delete=models.PROTECT,
                                 related_name='speciality_cathedra')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.name}'

