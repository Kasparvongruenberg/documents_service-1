from rest_framework import viewsets

from .models import Document
from .serializers import DocumentSerializer


class DocumentViewSet(viewsets.ModelViewSet):
    """
    Documents.
    """
    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return super(DocumentViewSet, self).update(request, *args, **kwargs)

    ordering_fields = ('id', 'upload_date', 'create_date')
    ordering = ('id',)
    filter_fields = ('file_type',)
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
