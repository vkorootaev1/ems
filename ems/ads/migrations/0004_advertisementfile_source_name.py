# Generated by Django 4.2.6 on 2023-12-01 21:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ads', '0003_rename_text_advertisement_body_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='advertisementfile',
            name='source_name',
            field=models.CharField(default='1', max_length=1000),
            preserve_default=False,
        ),
    ]
