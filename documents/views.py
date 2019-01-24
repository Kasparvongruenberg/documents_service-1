from rest_framework import viewsets, filters
from rest_framework.decorators import api_view
from django.utils.decorators import method_decorator
from rest_framework.parsers import MultiPartParser

from .autoschema import DocumentSwaggerAutoSchema
from .models import Document
from .serializers import DocumentSerializer
import django_filters
from django.http import FileResponse
from django.http import HttpResponseNotFound

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

DOCUMENT_AUTO_SCHEMA = swagger_auto_schema(
        auto_schema=DocumentSwaggerAutoSchema,
        parser_classes=(MultiPartParser,),
)


@method_decorator(name='create', decorator=DOCUMENT_AUTO_SCHEMA)
@method_decorator(name='update', decorator=DOCUMENT_AUTO_SCHEMA)
@method_decorator(name='partial_update', decorator=DOCUMENT_AUTO_SCHEMA)
class DocumentViewSet(viewsets.ModelViewSet):
    """
    Documents.
    """
    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return super(DocumentViewSet, self).update(request, *args, **kwargs)

    workflowlevel1_uuid = openapi.Parameter(
        'workflowlevel1_uuid', openapi.IN_QUERY,
        description='Filter by workflowlevel1_uuid.', type=openapi.TYPE_STRING)
    workflowlevel2_uuid = openapi.Parameter(
        'workflowlevel2_uuid', openapi.IN_QUERY,
        description='Filter by workflowlevel2_uuid.', type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[workflowlevel1_uuid,
                                            workflowlevel2_uuid, ])
    def list(self, request, *args, **kwargs):
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

        page = self.paginate_queryset(queryset)

        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    ordering_fields = ('id', 'upload_date', 'create_date')
    ordering = ('id',)
    filter_fields = ('file_type', 'contact_uuid')
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,
                       filters.OrderingFilter)
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer


@api_view(['GET'])
def document_thumbnail_view(request, id):
    document = Document.objects.get(pk=id)
    data = document.thumbnail

    if not data:
        return HttpResponseNotFound()

    response = FileResponse(data)
    response['Content-Disposition'] = \
        'attachment; filename=thumbnail_%s' % document.file_name

    response['Content-Length'] = data.size

    return response


@api_view(['GET'])
def document_download_view(request, id):
    document = Document.objects.get(pk=id)
    data = document.file

    if not data:
        return HttpResponseNotFound()

    response = FileResponse(data)
    response['Content-Disposition'] = \
        'attachment; filename=%s' % document.file_name

    response['Content-Length'] = data.size

    return response
