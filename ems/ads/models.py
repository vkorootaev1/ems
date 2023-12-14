from django.db import models
from pytils import translit


def advertisement_file_path(instance, filename):
    """ Путь к файлу объявления """
    filebase, extension = filename.split('.')
    return 'adv/{0}/{1}.{2}'.format(instance.advertisement_id, translit.slugify(filebase), extension)


class Advertisement(models.Model):
    
    """ Модель объявления """
    
    body = models.TextField()
    user = models.ForeignKey('users.User', on_delete=models.PROTECT,
                             related_name='advertisement_user')
    groups = models.ManyToManyField('study.StudyGroup',
                                    related_name='advertisement_studygroup')
    date_add = models.DateTimeField(auto_now_add=True)
    date_upd = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.id}, {self.user.fio()}'


class AdvertisementFile(models.Model):
    
    """ Модель файла объявления """
    
    advertisement = models.ForeignKey('Advertisement', on_delete=models.CASCADE,
                                      related_name='advertisement_file')
    origin_name = models.CharField(blank=True)
    file = models.FileField(upload_to=advertisement_file_path)
    user = models.ForeignKey(
        'users.User', on_delete=models.PROTECT, related_name='advertisementfile_user')
    date_add = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.id}, {self.user.fio()}, {self.origin_name}'

    def save(self, *args, **kwargs):
        self.origin_name = self.file.name
        super(AdvertisementFile, self).save(*args, **kwargs)
