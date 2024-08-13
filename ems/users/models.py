from django.db import models
from django.contrib.auth.models import AbstractUser
from pytils import translit


def user_photo_directory_path(instance, filename):
    """ Путь к файлу фотографии пользователя """
    filebase, extension = filename.split('.')
    return 'users/{0}/photo/{1}.{2}'.format(instance.id, translit.slugify(filebase), extension)


class User(AbstractUser):

    """ Модель пользователя """

    patronymic = models.CharField(max_length=150, verbose_name='Отчество')
    date_updated = models.DateTimeField(
        auto_now=True, verbose_name='Дата обновления')
    photo = models.ImageField(
        upload_to=user_photo_directory_path, blank=True, null=True, verbose_name='Фото')

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f'{self.fio()}'

    def get_teacher(self):
        try:
            return self.teacher_user

        except:
            return None

    def get_student(self, student_id):
        return self.student_user.filter(pk=student_id)

    def get_certificate_worker(self):
        try:
            return self.person_user.roles.filter(type=1)
        except:
            return None

    def fio(self):
        return f'{self.last_name} {self.first_name} {self.patronymic}'


class UserInfo(models.Model):

    """ Модель информации о пользователе """

    GENDER_CHOICES = [
        ('M', 'Мужской'),
        ('F', 'Женский')
    ]

    gender = models.CharField(
        max_length=1, choices=GENDER_CHOICES, verbose_name='Пол')
    phone = models.CharField(max_length=20, verbose_name='Номер телефона')
    birthday = models.DateField(verbose_name='Дата рождения')
    place_of_birth = models.CharField(
        max_length=1000, verbose_name='Место рождения')
    passport_series_and_number = models.CharField(
        max_length=20, unique=True, verbose_name='Паспортные данные')
    date_of_issue_of_the_passport = models.DateField(
        verbose_name='Дата выдачи паспорта')
    the_authority_that_issued_the_passport = models.CharField(
        max_length=150, verbose_name='Отдел выдачи паспорта')
    place_of_registration = models.CharField(
        max_length=1000, verbose_name='Место регистрации')
    place_of_living = models.CharField(
        max_length=1000, verbose_name='Место жительства')
    inn = models.CharField(max_length=20, unique=True,
                           verbose_name='Номер ИНН')
    snils = models.CharField(max_length=20, unique=True,
                             verbose_name='Номер снилс')
    is_active = models.BooleanField(default=True, verbose_name='Доступность')
    user = models.OneToOneField(
        'User', related_name='userinfo_user', on_delete=models.PROTECT, blank=True, null=True, verbose_name='Пользователь')

    class Meta:
        verbose_name = 'Информация о пользователе'
        verbose_name_plural = 'Информация о пользователях'

    def __str__(self):
        return f'{self.user.fio()}'


class Student(models.Model):

    """ Модель студента """

    user = models.ForeignKey('User', on_delete=models.PROTECT,
                             related_name='student_user', verbose_name='Пользователь')
    study_group = models.ForeignKey('study.StudyGroup', on_delete=models.PROTECT,
                                    related_name='student_studygroup', verbose_name='Учебная группа')
    is_active = models.BooleanField(default=True, verbose_name='Доступность')

    class Meta:
        verbose_name = 'Студент'
        verbose_name_plural = 'Студенты'
        unique_together = ['user', 'study_group']

    def __str__(self):
        return f'{self.user.fio()}, {self.study_group.name}'


class Teacher(models.Model):

    """ Модель преподавателя """

    user = models.OneToOneField('User', on_delete=models.PROTECT,
                                related_name='teacher_user', verbose_name='Пользователь')
    rank = models.CharField(max_length=150, blank=True,
                            verbose_name='Ученая степень')
    job_title = models.CharField(
        max_length=150, blank=True, verbose_name='Должность')
    cathedra = models.ManyToManyField('university.Cathedra',
                                      related_name='teacher_cathedra',
                                      blank=True, verbose_name='Кафедры')
    courses = models.ManyToManyField('study.Course',
                                     related_name='teacher_courses',
                                     blank=True, verbose_name='Преподаваемые дисциплины')
    is_active = models.BooleanField(default=True, verbose_name='Доступность')

    class Meta:
        verbose_name = 'Преподаватель'
        verbose_name_plural = 'Преподаватели'

    def __str__(self):
        return f'{self.user.fio()}'


class PersonRole(models.Model):

    """ Модель роли персонала """

    name = models.CharField(max_length=150, verbose_name='Название')
    description = models.TextField(blank=True, verbose_name='Описание')

    class Meta:
        verbose_name = 'Роль персонала'
        verbose_name_plural = 'Роли персонала'

    def __str__(self):
        return f'{self.name}'


class Person(models.Model):

    """ Модель персонала """

    user = models.OneToOneField('User', on_delete=models.PROTECT,
                                related_name='person_user', verbose_name='Пользователь')
    roles = models.ManyToManyField('PersonRole',
                                   related_name='person_personrole', verbose_name='Роли')
    is_active = models.BooleanField(default=True, verbose_name='Доступность')

    class Meta:
        verbose_name = 'Персона'
        verbose_name_plural = 'Персонал'

    def __str__(self):
        return f'{self.user.fio()}'


class ContactType(models.Model):

    """ Модель типа контакта пользователя"""

    type = models.CharField(max_length=150, verbose_name='Тип')

    class Meta:
        verbose_name = 'Тип контакта'
        verbose_name_plural = 'Типы контактов'

    def __str__(self):
        return f'{self.type}'


class Contact(models.Model):

    """ Модель контакта пользователя """

    contact_ref = models.CharField(max_length=150, verbose_name='Ссылка')
    type = models.ForeignKey('ContactType', on_delete=models.PROTECT,
                             related_name='contact_contacttype', verbose_name='Тип контакта')
    user = models.ForeignKey('User', on_delete=models.PROTECT,
                             related_name='contact_user', verbose_name='Владелец')

    class Meta:
        verbose_name = 'Контакт'
        verbose_name_plural = 'Контакты'

    def __str__(self):
        return f'{self.type}, {self.user.fio()}'
