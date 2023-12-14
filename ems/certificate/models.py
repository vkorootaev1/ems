from django.db import models


class CertificateType(models.Model):
    
    """ Модель типа справки """
    
    name = models.CharField(max_length=150)
    description = models.TextField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.name}'


class Certificate(models.Model):
    
    """ Модель справки """
    
    STATUS_OF_CERTIFICATE = [
        ('cr', 'Создана'),
        ('pr', 'В обработке'),
        ('re', 'Готова'),
        ('is', 'Выдана'),
        ('ca', 'Отменена')
    ]

    type = models.ForeignKey('CertificateType', on_delete=models.PROTECT,
                             related_name='certificate_certificatetype')
    user = models.ForeignKey('users.User', on_delete=models.PROTECT,
                             related_name='certificate_user')
    count = models.PositiveSmallIntegerField()
    status = models.CharField(max_length=2, choices=STATUS_OF_CERTIFICATE)
    date_add = models.DateTimeField(auto_now_add=True)
    date_upd = models.DateTimeField(auto_now=True)
    user_give = models.ForeignKey('users.User', on_delete=models.PROTECT,
                                  null=True, blank=True,
                                  related_name='certificate_usergive')

    def __str__(self):
        return (f' {self.id}, {self.type}, {self.count}, {self.user.fio()}, '
                f'{self.get_status_display()}')
