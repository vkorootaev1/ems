# Generated by Django 4.2.6 on 2023-12-03 02:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('study', '0004_alter_courseteacherstudygroup_course'),
    ]

    operations = [
        migrations.RenameField(
            model_name='courseteacherstudygroup',
            old_name='trimeseter',
            new_name='trimester',
        ),
    ]
