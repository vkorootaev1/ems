from django.db.models import Manager
from study import models
from datetime import datetime


class TrimesterManager(Manager):

    """ Менеджер модели <Триместр> """

    def get_current_trimester(self):
        now = datetime.now().date()
        try:
            return models.Trimester.objects.get(date_start__lte=now, date_end__gte=now)
        except:
            return None

    def get_current_student_trimester(self, student):
        now = datetime.now().date()
        current_trimester = models.Trimester.objects.\
            filter(date_start__range=(
                student.study_group.begin_date, now)).count()
        return current_trimester

    def get_trimester_by_id(self, trimester_id):
        try:
            return models.Trimester.objects.get(pk=trimester_id)
        except:
            return None
