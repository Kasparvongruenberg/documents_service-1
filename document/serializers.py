from rest_framework import serializers
from .models import Document, FILE_TYPE_CHOICES
import base64
import uuid
from django.core.files.base import ContentFile


class Base64FileField(serializers.FileField):
    base_url = '/file/{}'

    def to_representation(self, value):
        if not value:
            return None

        doc = Document.objects.get(file=value)
        url = self.base_url.format(doc.id)

        request = self.context.get('request', None)
        if request is not None:
            return request.build_absolute_uri(url)

        return url

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


class MaskedThumbnailField(serializers.ReadOnlyField):
    base_url = '/thumbnail/{}'

    def to_representation(self, value):
        if not value:
            return None

        doc = Document.objects.get(thumbnail=value)
        url = self.base_url.format(doc.id)

        request = self.context.get('request', None)
        if request is not None:
            return request.build_absolute_uri(url)

        return url

    def to_internal_value(self, data):
        return None


class DocumentSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    uuid = serializers.ReadOnlyField()
    upload_date = serializers.ReadOnlyField()
    file = Base64FileField()
    thumbnail = MaskedThumbnailField()

    class Meta:
        model = Document
        fields = '__all__'
