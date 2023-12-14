from django.contrib.auth.models import User
from django.db import models


class ToDo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField('Название задания', max_length=500)
    is_complete = models.BooleanField('Завершено', default=False)
    deadline = models.DateField('Срок выполнения', null=True, blank=True)

    PRIORITY_CHOICES = (
        (1, 'Важно'),
        (2, 'Средней важности'),
        (3, 'Незначительно'),
    )

    priority = models.IntegerField(choices=PRIORITY_CHOICES, default=3)

    def get_priority_display(self):
        return dict(self.PRIORITY_CHOICES).get(self.priority)

    class Meta:
        verbose_name = 'Задание'
        verbose_name_plural = 'Задания'

    def __str__(self):
        return self.title
