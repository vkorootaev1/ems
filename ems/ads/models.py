from django.db import models
from pytils import translit


def advertisement_file_path(instance, filename):
    """ Путь к файлу объявления """
    filebase, extension = filename.split('.')
    return 'adv/{0}/{1}.{2}'.format(instance.advertisement_id, translit.slugify(filebase), extension)


class Advertisement(models.Model):

    """ Модель объявления """

    body = models.TextField(verbose_name='Текст объявления')
    user = models.ForeignKey('users.User', on_delete=models.PROTECT,
                             related_name='advertisement_user', verbose_name='Владелец')
    groups = models.ManyToManyField('study.StudyGroup',
                                    related_name='advertisement_studygroup', verbose_name='Группы')
    date_add = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата создания')
    date_upd = models.DateTimeField(
        auto_now=True, verbose_name='Дата обновления')

    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'
        ordering = ['id']

    def truncate_body(self):
        return (self.body[:30] + '..') if len(self.body) > 30 else self.body

    def __str__(self):
        return f'{self.truncate_body()}, {self.user.fio()}'


class AdvertisementFile(models.Model):

    """ Модель файла объявления """

    advertisement = models.ForeignKey('Advertisement', on_delete=models.CASCADE,
                                      related_name='advertisement_file', verbose_name='Объявление')
    origin_name = models.CharField(
        blank=True, verbose_name='Оригинальное название файла')
    file = models.FileField(
        upload_to=advertisement_file_path, verbose_name='Файл')
    user = models.ForeignKey(
        'users.User', on_delete=models.PROTECT, related_name='advertisementfile_user', verbose_name='Владелец файла')
    date_add = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата добавления')

    class Meta:
        verbose_name = 'Файл объявления'
        verbose_name_plural = 'Файлы объявлений'
        ordering = ['advertisement']

    def __str__(self):
        return f'{self.id}, {self.origin_name}, {self.user.fio()}'

    def save(self, *args, **kwargs):
        self.origin_name = self.file.name
        super(AdvertisementFile, self).save(*args, **kwargs)
