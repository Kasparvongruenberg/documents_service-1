from rest_framework import serializers
from .models import Document


class DocumentSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()
    uuid = serializers.ReadOnlyField()
    upload_date = serializers.ReadOnlyField()

    class Meta:
        model = Document
        fields = '__all__'