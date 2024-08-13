from datetime import date, timedelta

from django.core.management.base import BaseCommand
from study import models as s_models
from users import models as u_models
from university import models as un_models


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        qs = s_models.Course.objects.filter(name__in=['Нейронные сети и интеллектуальные системы',
                                                      'Правовые и организационные основы обеспечения информационной безопасности',
                                                      'Аудит информационных технологий и систем обеспечения информационной безопасности',
                                                      'Технологии информационной безопасности'])
        for c in qs:
            print(c.id, c.name)

        qs1 = u_models.Teacher.objects.filter(
            user__last_name__in=['Балтаев', 'Сеник', 'Ястребов'])
        for t in qs1:
            print(t.id, t.user.last_name)

        qs2 = un_models.Classroom.objects.filter(number__in=[419, 434, 435])

        for cl in qs2:
            print(cl.id, cl.number)

        qs3 = s_models.StudyGroup.objects.filter(name='БАС-19')
        for sg in qs3:
            print(sg.id, sg.name, sg.code)

        date1 = date(2024, 1, 16)
        date2 = date(2024, 1, 17)
        date3 = date(2024, 1, 18)

        for i in range(0, 7):

            _days = 7*2*i

            _date1 = date1 + timedelta(days=_days)

            pair2 = s_models.TimeTable.objects.create(
                date=_date1,
                type_of_pair='LA',
                index_pair=6,
                course_id=81,
                teacher_id=50,
                classroom_id=8,
                is_attendance=False
            )
            pair2.groups.add(1)
            pair2.save()

            _date2 = date2 + timedelta(days=_days)
            pair3 = s_models.TimeTable.objects.create(
                date=_date2,
                type_of_pair='LE',
                index_pair=6,
                course_id=82,
                teacher_id=79,
                classroom_id=4,
                is_attendance=False
            )
            pair3.groups.add(1)
            pair3.save()

            pair4 = s_models.TimeTable.objects.create(
                date=_date2,
                type_of_pair='LE',
                index_pair=7,
                course_id=80,
                teacher_id=79,
                classroom_id=4,
                is_attendance=False
            )
            pair4.groups.add(1)
            pair4.save()

            pair5 = s_models.TimeTable.objects.create(
                date=_date2,
                type_of_pair='LA',
                index_pair=8,
                course_id=80,
                teacher_id=79,
                classroom_id=4,
                is_attendance=False
            )
            pair5.groups.add(1)
            pair5.save()

            _date3 = date3 + timedelta(days=_days)
            pair6 = s_models.TimeTable.objects.create(
                date=_date3,
                type_of_pair='LE',
                index_pair=6,
                course_id=83,
                teacher_id=77,
                classroom_id=8,
                is_attendance=False
            )
            pair6.groups.add(1)
            pair6.save()
