# Generated by Django 4.2.6 on 2024-02-01 09:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import users.models


class Migration(migrations.Migration):

    dependencies = [
        ('study', '0006_alter_attendance_options_and_more'),
        ('university', '0002_alter_cathedra_options_alter_classroom_options_and_more'),
        ('users', '0005_alter_teacher_cathedra_alter_teacher_courses'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='contact',
            options={'verbose_name': 'Контакт', 'verbose_name_plural': 'Контакты'},
        ),
        migrations.AlterModelOptions(
            name='contacttype',
            options={'verbose_name': 'Тип контакта', 'verbose_name_plural': 'Типы контактов'},
        ),
        migrations.AlterModelOptions(
            name='person',
            options={'verbose_name': 'Персона', 'verbose_name_plural': 'Персонал'},
        ),
        migrations.AlterModelOptions(
            name='personrole',
            options={'verbose_name': 'Роль персонала', 'verbose_name_plural': 'Роли персонала'},
        ),
        migrations.AlterModelOptions(
            name='student',
            options={'verbose_name': 'Студент', 'verbose_name_plural': 'Студенты'},
        ),
        migrations.AlterModelOptions(
            name='teacher',
            options={'verbose_name': 'Преподаватель', 'verbose_name_plural': 'Преподаватели'},
        ),
        migrations.AlterModelOptions(
            name='user',
            options={'verbose_name': 'Пользователь', 'verbose_name_plural': 'Пользователи'},
        ),
        migrations.AlterModelOptions(
            name='userinfo',
            options={'verbose_name': 'Информация о пользователе', 'verbose_name_plural': 'Информация о пользователях'},
        ),
        migrations.AlterField(
            model_name='contact',
            name='contact_ref',
            field=models.CharField(max_length=150, verbose_name='Ссылка'),
        ),
        migrations.AlterField(
            model_name='contact',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='contact_contacttype', to='users.contacttype', verbose_name='Тип контакта'),
        ),
        migrations.AlterField(
            model_name='contact',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='contact_user', to=settings.AUTH_USER_MODEL, verbose_name='Владелец'),
        ),
        migrations.AlterField(
            model_name='contacttype',
            name='type',
            field=models.CharField(max_length=150, verbose_name='Тип'),
        ),
        migrations.AlterField(
            model_name='person',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='Доступность'),
        ),
        migrations.AlterField(
            model_name='person',
            name='roles',
            field=models.ManyToManyField(related_name='person_personrole', to='users.personrole', verbose_name='Роли'),
        ),
        migrations.AlterField(
            model_name='person',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='person_user', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
        migrations.AlterField(
            model_name='personrole',
            name='description',
            field=models.TextField(blank=True, verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='personrole',
            name='name',
            field=models.CharField(max_length=150, verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='student',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='Доступность'),
        ),
        migrations.AlterField(
            model_name='student',
            name='study_group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='student_studygroup', to='study.studygroup', verbose_name='Учебная группа'),
        ),
        migrations.AlterField(
            model_name='student',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='student_user', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='cathedra',
            field=models.ManyToManyField(blank=True, related_name='teacher_cathedra', to='university.cathedra', verbose_name='Кафедры'),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='courses',
            field=models.ManyToManyField(blank=True, related_name='teacher_courses', to='study.course', verbose_name='Преподаваемые дисциплины'),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='Доступность'),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='job_title',
            field=models.CharField(blank=True, max_length=150, verbose_name='Должность'),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='rank',
            field=models.CharField(blank=True, max_length=150, verbose_name='Ученая степень'),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='teacher_user', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
        migrations.AlterField(
            model_name='user',
            name='date_updated',
            field=models.DateTimeField(auto_now=True, verbose_name='Дата обновления'),
        ),
        migrations.AlterField(
            model_name='user',
            name='patronymic',
            field=models.CharField(max_length=150, verbose_name='Отчество'),
        ),
        migrations.AlterField(
            model_name='user',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to=users.models.user_photo_directory_path, verbose_name='Фото'),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='birthday',
            field=models.DateField(verbose_name='Дата рождения'),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='date_of_issue_of_the_passport',
            field=models.DateField(verbose_name='Дата выдачи паспорта'),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='gender',
            field=models.CharField(choices=[('M', 'Мужской'), ('F', 'Женский')], max_length=1, verbose_name='Пол'),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='inn',
            field=models.CharField(max_length=20, unique=True, verbose_name='Номер ИНН'),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='Доступность'),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='passport_series_and_number',
            field=models.CharField(max_length=20, unique=True, verbose_name='Паспортные данные'),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='phone',
            field=models.CharField(max_length=20, verbose_name='Номер телефона'),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='place_of_birth',
            field=models.CharField(max_length=1000, verbose_name='Место рождения'),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='place_of_living',
            field=models.CharField(max_length=1000, verbose_name='Место жительства'),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='place_of_registration',
            field=models.CharField(max_length=1000, verbose_name='Место регистрации'),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='snils',
            field=models.CharField(max_length=20, unique=True, verbose_name='Номер снилс'),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='the_authority_that_issued_the_passport',
            field=models.CharField(max_length=150, verbose_name='Отдел выдачи паспорта'),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='userinfo_user', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
    ]
