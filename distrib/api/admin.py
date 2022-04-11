from django.contrib import admin

from .models import Client, Distrib, Message


class DistribAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'start_time',
        'text',
        'client_filter',
        'finish_time',
        'messages_count'
    )
    search_fields = (
        'text', 'filter'
    )

    def messages_count(self, obj):
        return obj.messages.all().count()

    messages_count.short_description = 'Отправлено сообщений'


class ClientAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'tel_number',
        'code',
        'tag',
        'time_zone',
    )
    search_fields = ('tel_number',)


class MessageAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'sent_time',
        'is_sent',
        'distrib',
        'client',
    )


admin.site.register(Distrib, DistribAdmin)
admin.site.register(Client, ClientAdmin)
admin.site.register(Message, MessageAdmin)
