# Generated by Django 4.2.6 on 2024-01-10 15:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('certificate', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='certificate',
            name='status',
            field=models.CharField(choices=[('cr', 'Создана'), ('pr', 'В обработке'), ('re', 'Готова к выдаче'), ('is', 'Выдана'), ('ca', 'Отменена')], max_length=2),
        ),
    ]
