from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Distrib(models.Model):
    start_time = models.CharField(
        'Время запуска рассылки',
        help_text='Время запуска рассылки',
        max_length=20
    )
    text = models.TextField(
        'Текст сообщения',
        help_text='Текст сообщения'
    )
    client_filter = models.CharField(
        'Фильтр свойств',
        help_text='Фильтр свойств',
        max_length=50
    )
    finish_time = models.CharField(
        'Время окончания рассылки',
        help_text='Время окончания рассылки',
        max_length=20
    )

    class Meta:
        ordering = ['-id']
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'

    def __str__(self):
        return self.text[:15]


class Client(models.Model):
    tel_number = models.CharField(
        'Номер телефона',
        help_text='Номер телефона',
        max_length=11
    )
    code = models.CharField(
        'Код оператора',
        help_text='Код оператора',
        max_length=5
    )
    tag = models.CharField(
        'Тэг',
        help_text='Тэг',
        max_length=50
    )
    time_zone = models.IntegerField(
        'Часовой пояс',
        help_text='Часовой пояс'
    )

    class Meta:
        ordering = ['-id']
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

    def __str__(self):
        return self.tel_number


class Message(models.Model):
    sent_time = models.DateTimeField(
        'Дата и время отправки',
        auto_now_add=True
    )
    is_sent = models.BooleanField('Статус отправки')
    distrib = models.ForeignKey(
        Distrib,
        on_delete=models.CASCADE,
        related_name='messages',
        verbose_name='Рассылка',
        help_text='Рассылка'
    )
    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name='messages',
        verbose_name='Клиент',
        help_text='Клиент'
    )

    class Meta:
        ordering = ['-id']
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'

    def __str__(self):
        return f'{self.distrib} {self.client}'
