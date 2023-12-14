from django.db import models
from django.contrib.auth.models import AbstractUser
from pytils import translit


def user_photo_directory_path(instance, filename):
    """ Путь к файлу фотографии пользователя """
    filebase, extension = filename.split('.')
    return 'users/{0}/photo/{1}.{2}'.format(instance.id, translit.slugify(filebase), extension)


class User(AbstractUser):

    """ Модель пользователя """

    patronymic = models.CharField(max_length=150)
    date_updated = models.DateTimeField(auto_now=True)
    photo = models.ImageField(
        upload_to=user_photo_directory_path, blank=True, null=True)

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

    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    phone = models.CharField(max_length=20)
    birthday = models.DateField()
    place_of_birth = models.CharField(max_length=1000)
    passport_series_and_number = models.CharField(max_length=20, unique=True)
    date_of_issue_of_the_passport = models.DateField()
    the_authority_that_issued_the_passport = models.CharField(max_length=150)
    place_of_registration = models.CharField(max_length=1000)
    place_of_living = models.CharField(max_length=1000)
    inn = models.CharField(max_length=20, unique=True)
    snils = models.CharField(max_length=20, unique=True)
    is_active = models.BooleanField(default=True)
    user = models.OneToOneField(
        'User', related_name='userinfo_user', on_delete=models.PROTECT, blank=True, null=True)

    def __str__(self):
        return f'{self.user.fio()}'


class Student(models.Model):

    """ Модель студента """

    user = models.ForeignKey('User', on_delete=models.PROTECT,
                             related_name='student_user')
    study_group = models.ForeignKey('study.StudyGroup', on_delete=models.PROTECT,
                                    related_name='student_studygroup')
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ['user', 'study_group']

    def __str__(self):
        return f'{self.user.fio()}, {self.study_group.name}'


class Teacher(models.Model):

    """ Модель преподавателя """

    user = models.OneToOneField('User', on_delete=models.PROTECT,
                                related_name='teacher_user')
    rank = models.CharField(max_length=150, blank=True)
    job_title = models.CharField(max_length=150, blank=True)
    cathedra = models.ManyToManyField('university.Cathedra',
                                      related_name='teacher_cathedra',
                                      blank=True)
    courses = models.ManyToManyField('study.Course',
                                     related_name='teacher_courses',
                                     blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.user.fio()}'


class PersonRole(models.Model):

    """ Модель роли персонала """

    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)

    def __str__(self):
        return f'{self.name}'


class Person(models.Model):

    """ Модель персонала """

    user = models.OneToOneField('User', on_delete=models.PROTECT,
                                related_name='person_user')
    roles = models.ManyToManyField('PersonRole',
                                   related_name='person_personrole')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.user}'


class ContactType(models.Model):

    """ Модель типа контакта пользователя"""

    type = models.CharField(max_length=150)

    def __str__(self):
        return f'{self.type}'


class Contact(models.Model):

    """ Модель контакта пользователя """

    contact_ref = models.CharField(max_length=150)
    type = models.ForeignKey('ContactType', on_delete=models.PROTECT,
                             related_name='contact_contacttype')
    user = models.ForeignKey('User', on_delete=models.PROTECT,
                             related_name='contact_user')

    def __str__(self):
        return f'{self.type}, {self.user.fio()}'
