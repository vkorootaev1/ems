import os.path

from django.db.models.signals import post_delete
from django.dispatch import receiver
from ads import models as ads_models


@receiver(post_delete, sender=ads_models.AdvertisementFile)
def delete_file_advertisemet(sender, instance, **kwargs):
    """ Сигнал настроенный на удаление файлов (объявлений) с жесткого диска """

    file_path = instance.file.path

    if os.path.isfile(file_path):
        os.remove(file_path)

    dir_path = os.path.dirname(instance.file.path)

    if not len(os.listdir(dir_path)):
        os.rmdir(dir_path)
