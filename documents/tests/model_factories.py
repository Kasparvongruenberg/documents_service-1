from datetime import datetime

from factory import DjangoModelFactory, Iterator, PostGenerationMethodCall
import pytz
from django.contrib.auth.models import User
import uuid

from ..models import Document as DocumentM

# Todo use moto==1.3.3 to test with aws boto file interface
class Document(DjangoModelFactory):
    class Meta:
        model = DocumentM

    file_name = Iterator(['test.jpg', 'test.png', 'test.pdf'])
    file_type = Iterator(['jpg', 'png', 'pdf'])
    workflowlevel1_uuids = [str(uuid.uuid4())]
    workflowlevel2_uuids = [str(uuid.uuid4())]

    upload_date = datetime(2018, 1, 1, 12, 30, tzinfo=pytz.UTC)
    create_date = datetime(2018, 1, 1, 15, 15, tzinfo=pytz.UTC)


class UserFactory(DjangoModelFactory):
    FACTORY_FOR = User

    email = 'admin@example.com'
    username = 'admin'
    password = PostGenerationMethodCall('set_password', 'adm1n')

    is_superuser = True
    is_staff = True
    is_active = True
