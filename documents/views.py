from rest_framework import viewsets, filters
from rest_framework.response import Response

from .models import Document
from .serializers import DocumentSerializer
import django_filters


class DocumentViewSet(viewsets.ModelViewSet):
    """
    Documents.
    """
    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return super(DocumentViewSet, self).update(request, *args, **kwargs)

    def list(self, request):
        # Use this queryset or the django-filters lib will not work
        queryset = self.filter_queryset(self.get_queryset())

        workflowlevel1_uuid = self.request.query_params.get(
            'workflowlevel1_uuid', None)
        if workflowlevel1_uuid is not None:
            queryset = queryset.filter(
                workflowlevel1_uuids__contains=[workflowlevel1_uuid])

        workflowlevel2_uuid = self.request.query_params.get(
            'workflowlevel2_uuid', None)
        if workflowlevel2_uuid is not None:
            queryset = queryset.filter(
                workflowlevel2_uuids__contains=[workflowlevel2_uuid])

        paginate = request.GET.get('paginate')
        if paginate and (paginate.lower() == 'true' or paginate == '1'):
            # Add this or pagination will not be available
            page = self.paginate_queryset(queryset)
            if page:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    ordering_fields = ('id', 'upload_date', 'create_date')
    ordering = ('id',)
    filter_fields = ('file_type', 'contact_uuid')
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,
                       filters.OrderingFilter)
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
