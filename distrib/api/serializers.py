import json
import os
import time
from datetime import datetime as dt
from threading import Thread
from urllib import parse

import requests
from dotenv import load_dotenv
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import Client, Distrib, Message

load_dotenv()

time_format = '%d/%m/%Y %H:%M:%S'
url = 'https://probe.fbrq.cloud/v1/send/'
headers = {'Authorization': 'Bearer '+ str(os.getenv('TOKEN1'))
            + str(os.getenv('TOKEN2')) + str(os.getenv('TOKEN3'))}

def send_message(message, payload):
    try:
        response = requests.post(
            url + str(message.id), headers=headers, data=json.dumps(payload)
        )
        if response.status_code == 200:
            message.is_sent = True
            message.save()
    except Exception:
        pass    # возможны доп. действия в случае неотправки сообщения


def make_distrib(clients, distrib, start_dt, end_dt, delay):
    time.sleep(delay)
    for client in clients:
        if start_dt < dt.now() < end_dt:
            if not Message.objects.filter(client=client).filter(
                distrib=distrib
            ).exists():
                message = Message.objects.create(
                    client=client, distrib=distrib, is_sent=False
                )
                payload = {
                    "id": message.id,
                    "phone": int(client.tel_number),
                    "text": distrib.text
                }
                send_message(message, payload)
            else:
                message = Message.objects.filter(
                                client=client
                         ).filter(distrib=distrib)[0]
                if not message.is_sent:
                    payload = {
                        "id": message.id,
                        "phone": int(client.tel_number),
                        "text": distrib.text
                    }
                    send_message(message, payload)

class ClientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Client
        fields = ('id', 'tel_number', 'code', 'tag', 'time_zone')

        validators = [
            UniqueTogetherValidator(
                message=('Не может быть двух клиентов с одинаковым номером'
                         'в одном часовом поясе'),
                queryset=Client.objects.all(),
                fields=('tel_number', 'time_zone')
            )
        ]


class MessageSerializer(serializers.ModelSerializer):
    client = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Message
        fields = ('id', 'sent_time', 'is_sent', 'client')


class DistribDetailSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Distrib
        fields = (
            'id', 'start_time', 'text', 'client_filter',
            'finish_time', 'messages'
        )


class DistribListSerializer(serializers.ModelSerializer):
    messages_sent = serializers.SerializerMethodField()
    messages_not_sent = serializers.SerializerMethodField()

    class Meta:
        model = Distrib
        fields = (
            'id', 'start_time', 'text', 'client_filter',
            'finish_time', 'messages_sent', 'messages_not_sent'
        )

    def get_messages_sent(self, obj):
        return Message.objects.filter(distrib=obj).filter(is_sent=True).count()

    def get_messages_not_sent(self, obj):
        return (
            Message.objects.filter(distrib=obj).filter(is_sent=False).count()
        )


class DistribCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Distrib
        fields = ('start_time', 'text', 'client_filter', 'finish_time')

    def validate(self, data):
        try:
            start_dt = dt.strptime(data['start_time'], time_format)
        except Exception:
            raise serializers.ValidationError(
                'Формат начала рассылки не соответствует {time_format}'
            )
        try:
            end_dt = dt.strptime(data['finish_time'], time_format)
        except Exception:
            raise serializers.ValidationError(
                f'Формат окончания рассылки не соответствует {time_format}'
            )
        if start_dt > end_dt:
            raise serializers.ValidationError(
                'Дата начала рассылки не может быть позже даты завершения!')
        return data

    def create(self, validated_data):
        filter_string = validated_data.get('client_filter')
        try:
            filters = dict(
                parse.parse_qsl(parse.urlsplit(filter_string).query)
            )
        except Exception:
            raise serializers.ValidationError(
                'Фильтр свойств клиентов должен быть в формате'
                '"?свойство=значение&свойство=значение"'
            )
        obj = super().create(validated_data)
        if 'код' in filters and 'тэг' in filters:
            clients = Client.objects.all()
            clients = clients.filter(tag=filters['тэг']).filter(
                code=filters['код']
            )
            start_dt = dt.strptime(
                validated_data['start_time'], time_format
            )
            end_dt = dt.strptime(
                validated_data['finish_time'], time_format
            )
            if start_dt > dt.now():
                delayed_distrib = Thread(
                    target=make_distrib,
                    args=(clients, obj, start_dt, end_dt, (
                        start_dt - dt.now()
                    ).total_seconds())
                )
                delayed_distrib.start()
            if start_dt < dt.now() < end_dt:
                make_distrib(clients, obj, start_dt, end_dt, 0)
        return obj

    def update(self, obj, validated_data):
        if 'client_filter' in validated_data:
            filter_string = validated_data.get('client_filter')
            try:
                filters = dict(
                    parse.parse_qsl(parse.urlsplit(filter_string).query)
                )
            except Exception:
                raise serializers.ValidationError(
                    'Фильтр свойств клиентов должен быть в формате'
                    ' "?свойство=значение&свойство=значение"'
                )
        obj = super().update(obj, validated_data)
        if not filters:
            filter_string = obj.client_filter
            filters = dict(
                parse.parse_qsl(parse.urlsplit(filter_string).query)
            )
        if 'код' in filters and 'тэг' in filters:
            clients = Client.objects.all()
            clients = clients.filter(tag=filters['тэг']).filter(
                code=filters['код']
            )
            start_dt = dt.strptime(validated_data['start_time'], time_format)
            end_dt = dt.strptime(validated_data['finish_time'], time_format)
            if start_dt > dt.now():
                delayed_distrib = Thread(
                    target=make_distrib,
                    args=(clients, obj, start_dt, end_dt, (
                        start_dt - dt.now()
                    ).total_seconds())
                )
                delayed_distrib.start()
            if start_dt < dt.now() < end_dt:
                make_distrib(clients, obj, start_dt, end_dt, 0)
        return obj
