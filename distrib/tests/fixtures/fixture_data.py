import pytest
from api.models import Client, Distrib


@pytest.fixture
def client(user):
    from api.models import Client
    return Client.objects.create(
        tel_number='79991234567',
        code='999',
        tag='тэг1',
        time_zone=7
    )

@pytest.fixture
def distrib():
    from api.models import Distrib
    return Distrib.objects.create(
        start_time='11/04/2022 22:23:30',
        text='Текст1',
        client_filter='?тэг=тэг1&код=код1',
        finish_time='15/04/2022 22:23:30',
    )
