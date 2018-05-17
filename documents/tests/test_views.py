# -*- coding: utf-8 -*-
from datetime import datetime
import uuid

from django.conf import settings
from django.test import TestCase
import pytz
from rest_framework.reverse import reverse
from rest_framework.test import APIRequestFactory
from django.core.exceptions import ValidationError

from . import model_factories as mfactories
from ..models import Document
from ..views import DocumentViewSet


class DocumentListViewsTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = mfactories.User()

    def test_list_empty(self):
        request = self.factory.get('')
        request.user = self.user
        view = DocumentViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, [])

    def test_list_documents(self):
        request = self.factory.get('')
        request.user = self.user
        view = DocumentViewSet.as_view({'get': 'list'})
        response = view(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

        document_data = response.data[0]
        self.assertTrue('id' in document_data)
        self.assertEqual(document_data['file_name'], 'Testfile.pdf')

    def test_list_documents_anonymoususer(self):
        request_get = self.factory.get('')
        view = DocumentViewSet.as_view({'get': 'list'})
        response = view(request_get)
        self.assertEqual(response.status_code, 403)


class DocumentRetrieveViewsTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = mfactories.User()

    def test_retrieve_document(self):
        document = mfactories.Document()
        request = self.factory.get('')
        request.user = self.user
        view = DocumentViewSet.as_view({'get': 'retrieve'})
        response = view(request, pk=document.pk)
        self.assertEqual(response.status_code, 200)

    def test_retrieve_document_anonymoususer(self):
        request_get = self.factory.get('')
        view = DocumentViewSet.as_view({'get': 'retrieve'})
        response = view(request_get)
        self.assertEqual(response.status_code, 403)


class DocumentCreateViewsTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = mfactories.User()

    def test_create_document_minimal(self):

        data = {
            'file_name': u'Testfile.pdf',
            'workflowlevel1_uuids': [str(uuid.uuid4())],
        }

        request = self.factory.post('', data)
        request.user = self.user
        view = DocumentViewSet.as_view({'post': 'create'})
        response = view(request)
        self.assertEqual(response.status_code, 201)

        document = Document.objects.get(id=response.data['id'])
        self.assertEqual(document.file_name, data['file_name'])
        self.assertEqual(document.file_type, 'pdf')

    def test_create_document(self):
        create_date = datetime(2018, 1, 1, 12, 15)\
            .strftime("%Y-%m-%dT%H:%M:%S+01:00")
        workflowlevel1_uuids = [str(uuid.uuid4()), str(uuid.uuid4())]
        workflowlevel2_uuids = [str(uuid.uuid4()), str(uuid.uuid4())]
        organization_uuid = str(uuid.uuid4())

        data = {
            'file_name': u'Testfile.pdf',
            'create_date': create_date,
            'workflowlevel1_uuids': workflowlevel1_uuids,
            'workflowlevel2_uuids': workflowlevel2_uuids,
            'organization_uuid': organization_uuid,
        }
        request = self.factory.post('', data)
        request.user = self.user
        view = DocumentViewSet.as_view({'post': 'create'})
        response = view(request)
        self.assertEqual(response.status_code, 201)

        data = response.data
        document = Document.objects.get(id=data['id'])
        self.assertEqual(response.status_code, 201)
        self.assertEqual(document.file_name, data['file_name'])
        self.assertEqual(document.file_type, 'pdf')
        self.assertEqual(document.create_date.strftime(
            "%Y-%m-%dT%H:%M:%SZ"), data['create_date'])
        self.assertEqual(document.workflowlevel1_uuids, workflowlevel1_uuids)
        self.assertEqual(document.workflowlevel2_uuids, workflowlevel2_uuids)
        self.assertEqual(document.organization_uuid, organization_uuid)

    def test_create_document_anonymoususer(self):
        request = self.factory.post('', {})
        view = DocumentViewSet.as_view({'post': 'create'})
        response = view(request)
        self.assertEqual(response.status_code, 403)

    def test_create_document_fails_empty_field(self):
        create_date = datetime(2018, 1, 1, 12, 15)\
            .strftime("%Y-%m-%dT%H:%M:%S+01:00")
        workflowlevel1_uuids = [uuid.uuid4(), uuid.uuid4()]

        data = {
            'create_date': create_date,
            'workflowlevel1_uuids': workflowlevel1_uuids,
        }

        request = self.factory.post('', data)
        request.user = self.user
        view = DocumentViewSet.as_view({'post': 'create'})
        response = view(request)
        self.assertEqual(response.status_code, 400)

    def test_create_document_fails_invalid_file_type(self):
        data = {
            'file_name': u'Testfile.exe',
            'workflowlevel1_uuids': [str(uuid.uuid4())],
        }

        request = self.factory.post('', data)
        request.user = self.user
        view = DocumentViewSet.as_view({'post': 'create'})
        try:
            view(request)
            self.fail()
        except ValidationError:
            pass

class DocumentUpdateViewsTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = mfactories.User()

    def test_update_document(self):
        document = mfactories.Document()

        workflowlevel1_uuids = [str(uuid.uuid4()), str(uuid.uuid4())]

        data = {
            'file_name': u'Testfile.pdf',
            'workflowlevel1_uuids': workflowlevel1_uuids,
        }

        request = self.factory.post('', data)
        request.user = self.user
        view = DocumentViewSet.as_view({'post': 'update'})
        response = view(request, pk=document.pk)
        self.assertEqual(response.status_code, 200)

        document = Document.objects.get(id=response.data['id'])
        self.assertEqual(document.workflowlevel1_uuids, workflowlevel1_uuids)

    def test_update_document_fails_blank_field(self):
        document = mfactories.Document()

        data = {
            'file_name': u'',
        }
        request = self.factory.post('', data)
        request.user = self.user
        view = DocumentViewSet.as_view({'post': 'update'})
        response = view(request, pk=document.pk)
        self.assertEqual(response.status_code, 400)

    def test_update_document_fails_invalid_file_type(self):
        document = mfactories.Document()

        data = {
            'file_name': u'Testfile.notavirus',
        }
        request = self.factory.post('', data)
        request.user = self.user
        view = DocumentViewSet.as_view({'post': 'update'})
        try:
            view(request, pk=document.pk)
            self.fail()
        except ValidationError:
            pass


    def test_update_document_anonymoususer_forbidden(self):
        request = self.factory.post('', {})
        view = DocumentViewSet.as_view({'post': 'update'})
        response = view(request)
        self.assertEqual(response.status_code, 403)
