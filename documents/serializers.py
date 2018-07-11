from rest_framework import serializers
from .models import Document
import base64
import uuid
from django.core.files.base import ContentFile
from .models import FILE_TYPE_CHOICES, get_file_storage


class Base64FileField(serializers.FileField):
    def to_representation(self, value):
        if not value:
            return None

        try:
            file_storage = get_file_storage()

            prefix = 'https'
            if file_storage.force_http:
                prefix = 'http'

            return '{}://{}.{}/{}'.format(prefix, file_storage.bucket_name,
                                          file_storage.host, value.name)
        except AttributeError:
            pass
        except ValueError:
            pass

        return None

    def to_internal_value(self, data):
        if isinstance(data, str) and (data.startswith('data:')):
            format, filestr = data.split(';base64,')
            ext = format.split('/')[-1]

            if ext not in [ft[0] for ft in FILE_TYPE_CHOICES]:
                super(Base64FileField, self).fail('invalid')

            id = uuid.uuid4()
            data = ContentFile(base64.b64decode(filestr),
                               name=id.urn[9:] + '.' + ext)
        return super(Base64FileField, self).to_internal_value(data)


class DocumentSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    uuid = serializers.ReadOnlyField()
    upload_date = serializers.ReadOnlyField()
    file = Base64FileField()

    class Meta:
        model = Document
        fields = '__all__'
