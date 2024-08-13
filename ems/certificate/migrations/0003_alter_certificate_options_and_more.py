# Generated by Django 4.2.6 on 2024-02-01 09:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('certificate', '0002_alter_certificate_status'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='certificate',
            options={'verbose_name': 'Справка', 'verbose_name_plural': 'Справки'},
        ),
        migrations.AlterModelOptions(
            name='certificatetype',
            options={'verbose_name': 'Вид справки', 'verbose_name_plural': 'Виды справок'},
        ),
        migrations.AlterField(
            model_name='certificate',
            name='count',
            field=models.PositiveSmallIntegerField(verbose_name='Количество справок'),
        ),
        migrations.AlterField(
            model_name='certificate',
            name='date_add',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Дата создания'),
        ),
        migrations.AlterField(
            model_name='certificate',
            name='date_upd',
            field=models.DateTimeField(auto_now=True, verbose_name='Дата обновления'),
        ),
        migrations.AlterField(
            model_name='certificate',
            name='status',
            field=models.CharField(choices=[('cr', 'Создана'), ('pr', 'В обработке'), ('re', 'Готова к выдаче'), ('is', 'Выдана'), ('ca', 'Отменена')], max_length=2, verbose_name='Статус справки'),
        ),
        migrations.AlterField(
            model_name='certificate',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='certificate_certificatetype', to='certificate.certificatetype', verbose_name='Тип справки'),
        ),
        migrations.AlterField(
            model_name='certificate',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='certificate_user', to=settings.AUTH_USER_MODEL, verbose_name='Заказчик'),
        ),
        migrations.AlterField(
            model_name='certificate',
            name='user_give',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='certificate_usergive', to=settings.AUTH_USER_MODEL, verbose_name='Сотрудник, выдавший справку'),
        ),
        migrations.AlterField(
            model_name='certificatetype',
            name='description',
            field=models.TextField(verbose_name='Описание типа справки'),
        ),
        migrations.AlterField(
            model_name='certificatetype',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='Доступность'),
        ),
        migrations.AlterField(
            model_name='certificatetype',
            name='name',
            field=models.CharField(max_length=150, verbose_name='Тип справки'),
        ),
    ]