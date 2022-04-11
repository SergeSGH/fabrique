# Generated by Django 2.2.19 on 2022-04-11 13:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tel_number', models.CharField(help_text='Номер телефона', max_length=11, verbose_name='Номер телефона')),
                ('code', models.CharField(help_text='Код оператора', max_length=5, verbose_name='Код оператора')),
                ('tag', models.CharField(help_text='Тэг', max_length=50, verbose_name='Тэг')),
                ('time_zone', models.IntegerField(help_text='Часовой пояс', verbose_name='Часовой пояс')),
            ],
            options={
                'verbose_name': 'Клиент',
                'verbose_name_plural': 'Клиенты',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Distrib',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.CharField(help_text='Время запуска рассылки', max_length=20, verbose_name='Время запуска рассылки')),
                ('text', models.TextField(help_text='Текст сообщения', verbose_name='Текст сообщения')),
                ('client_filter', models.CharField(help_text='Фильтр свойств', max_length=50, verbose_name='Фильтр свойств')),
                ('finish_time', models.CharField(help_text='Время окончания рассылки', max_length=20, verbose_name='Время окончания рассылки')),
            ],
            options={
                'verbose_name': 'Рассылка',
                'verbose_name_plural': 'Рассылки',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sent_time', models.DateTimeField(auto_now_add=True, verbose_name='Дата и время отправки')),
                ('is_sent', models.BooleanField(verbose_name='Статус отправки')),
                ('client', models.ForeignKey(help_text='Клиент', on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='api.Client', verbose_name='Клиент')),
                ('distrib', models.ForeignKey(help_text='Рассылка', on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='api.Distrib', verbose_name='Рассылка')),
            ],
            options={
                'verbose_name': 'Сообщение',
                'verbose_name_plural': 'Сообщения',
                'ordering': ['-id'],
            },
        ),
    ]