from django.db import models


class CertificateType(models.Model):

    """ Модель типа справки """

    name = models.CharField(max_length=150, verbose_name='Тип справки')
    description = models.TextField(verbose_name='Описание типа справки')
    is_active = models.BooleanField(default=True, verbose_name='Доступность')

    class Meta:
        verbose_name = 'Вид справки'
        verbose_name_plural = 'Виды справок'

    def __str__(self):
        return f'{self.name}'


class Certificate(models.Model):

    """ Модель справки """

    STATUS_OF_CERTIFICATE = [
        ('cr', 'Создана'),
        ('pr', 'В обработке'),
        ('re', 'Готова к выдаче'),
        ('is', 'Выдана'),
        ('ca', 'Отменена')
    ]

    type = models.ForeignKey('CertificateType', on_delete=models.PROTECT,
                             related_name='certificate_certificatetype', verbose_name='Тип справки')
    user = models.ForeignKey('users.User', on_delete=models.PROTECT,
                             related_name='certificate_user', verbose_name='Заказчик')
    count = models.PositiveSmallIntegerField(verbose_name='Количество справок')
    status = models.CharField(
        max_length=2, choices=STATUS_OF_CERTIFICATE, verbose_name='Статус справки')
    date_add = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата создания')
    date_upd = models.DateTimeField(
        auto_now=True, verbose_name='Дата обновления')
    user_give = models.ForeignKey('users.User', on_delete=models.PROTECT,
                                  null=True, blank=True,
                                  related_name='certificate_usergive', verbose_name='Сотрудник, выдавший справку')

    class Meta:
        verbose_name = 'Справка'
        verbose_name_plural = 'Справки'

    def __str__(self):
        return f'{self.type}, {self.count}, {self.user.fio()}, {self.get_status_display()}' +\
            f', {self.user_give.fio()}' if self.user_give else ''
