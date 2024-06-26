# Generated by Django 4.2.6 on 2023-11-29 14:12

import ads.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('study', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ads', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Advertisement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('header', models.CharField(max_length=150)),
                ('text', models.TextField()),
                ('date_add', models.DateTimeField(auto_now_add=True)),
                ('date_upd', models.DateTimeField(auto_now=True)),
                ('groups', models.ManyToManyField(related_name='advertisement_studygroup', to='study.studygroup')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='advertisement_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='AdvertisementFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to=ads.models.advertisement_file_path)),
                ('date_add', models.DateTimeField(auto_now_add=True)),
                ('advertisement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='advertisement_file', to='ads.advertisement')),
            ],
        ),
        migrations.RemoveField(
            model_name='advertismentfile',
            name='advertisment',
        ),
        migrations.DeleteModel(
            name='Advertisment',
        ),
        migrations.DeleteModel(
            name='AdvertismentFile',
        ),
    ]
