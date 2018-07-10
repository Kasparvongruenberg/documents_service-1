# -*- coding: utf-8 -*-
from datetime import datetime
import uuid

from django.test import TestCase
from rest_framework.test import APIRequestFactory
from django.core.exceptions import ValidationError

from . import model_factories as mfactories
from ..models import Document, timezone
from ..views import DocumentViewSet
import re
import mock
from django.core.files import File
from django.test.utils import override_settings


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
        mfactories.Document()
        view = DocumentViewSet.as_view({'get': 'list'})
        response = view(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

        document_data = response.data[0]
        self.assertTrue('id' in document_data)
        self.assertEqual(document_data['file_name'], 'test.jpg')

    def test_list_documents_anonymoususer(self):
        request_get = self.factory.get('')
        view = DocumentViewSet.as_view({'get': 'list'})
        response = view(request_get)
        self.assertEqual(response.status_code, 403)

    def test_list_documents_filter_by_file_type(self):
        mfactories.Document(file_name='Document1.png')
        mfactories.Document(file_name='Document2.png')
        mfactories.Document(file_name='Document3.jpg')

        request = self.factory.get('?file_type={}'.format('png'))
        request.user = self.user
        view = DocumentViewSet.as_view({'get': 'list'})
        response = view(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

        document_data = response.data[0]
        self.assertEqual(document_data['file_type'], 'png')
        self.assertEqual(response.data[0]['file_name'], 'Document1.png')
        self.assertEqual(response.data[1]['file_name'], 'Document2.png')

    def test_list_documents_filter_by_related_wf1(self):
        wf1uuids = [str(uuid.uuid4()), str(uuid.uuid4())]

        mfactories.Document(file_name='Document1.png',
                            workflowlevel1_uuids=wf1uuids)
        mfactories.Document(file_name='Document2.png',
                            workflowlevel1_uuids=wf1uuids)
        mfactories.Document(file_name='Document3.jpg')

        request = self.factory.get('?workflowlevel1_uuid={}'.format(
            wf1uuids[0]))
        request.user = self.user
        view = DocumentViewSet.as_view({'get': 'list'})
        response = view(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

        self.assertEqual(response.data[0]['file_name'], 'Document1.png')
        self.assertEqual(response.data[1]['file_name'], 'Document2.png')

    def test_list_documents_filter_by_related_wf2(self):
        wf2uuids = [str(uuid.uuid4()), str(uuid.uuid4())]

        mfactories.Document(file_name='Document1.png')
        mfactories.Document(file_name='Document2.png',
                            workflowlevel2_uuids=wf2uuids)
        mfactories.Document(file_name='Document3.jpg',
                            workflowlevel2_uuids=wf2uuids)

        request = self.factory.get('?workflowlevel2_uuid={}'.format(
            wf2uuids[0]))
        request.user = self.user
        view = DocumentViewSet.as_view({'get': 'list'})
        response = view(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

        self.assertEqual(response.data[0]['file_name'], 'Document2.png')
        self.assertEqual(response.data[1]['file_name'], 'Document3.jpg')

    def test_list_documents_filter_by_related_contact(self):
        contact_uuid = str(uuid.uuid4())

        mfactories.Document(file_name='Document1.png')
        mfactories.Document(file_name='Document2.png',
                            contact_uuid=contact_uuid)
        mfactories.Document(file_name='Document3.jpg',
                            contact_uuid=contact_uuid)

        request = self.factory.get('?contact_uuid={}'.format(
            contact_uuid))
        request.user = self.user
        view = DocumentViewSet.as_view({'get': 'list'})
        response = view(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

        self.assertEqual(response.data[0]['file_name'], 'Document2.png')
        self.assertEqual(response.data[1]['file_name'], 'Document3.jpg')

    def test_paginate_large_result_sets(self):
        for i in range(0, 32):
            mfactories.Document(file_name='Document{}.png'.format(i))

        request = self.factory.get('?paginate=true')
        request.user = self.user
        view = DocumentViewSet.as_view({'get': 'list'})
        response = view(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 30)
        self.assertIsNotNone(response.data['next'])
        self.assertIsNone(response.data['previous'])

        m = re.search('=(.*)&', response.data['next'])
        cursor = m.group(1)

        page2_request = self.factory.get('?cursor={}&paginate=true'.format(
            cursor))
        page2_request.user = self.user
        page2_response = view(page2_request)
        self.assertEqual(page2_response.status_code, 200)
        self.assertEqual(len(page2_response.data['results']), 2)
        self.assertIsNone(page2_response.data['next'])
        self.assertIsNotNone(page2_response.data['previous'])

    def test_paginate_large_result_sets_max_size(self):
        for i in range(0, 102):
            mfactories.Document(file_name='Document{}.png'.format(i))

        request = self.factory.get('?paginate=true&page_size=100')
        request.user = self.user
        view = DocumentViewSet.as_view({'get': 'list'})
        response = view(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 100)
        self.assertIsNotNone(response.data['next'])
        self.assertIsNone(response.data['previous'])

        m = re.search('=(.*)&', response.data['next'])
        cursor = m.group(1)

        page2_request = self.factory.get('?cursor={}&paginate=true'.format(
            cursor))
        page2_request.user = self.user
        page2_response = view(page2_request)
        self.assertEqual(page2_response.status_code, 200)
        self.assertEqual(len(page2_response.data['results']), 2)
        self.assertIsNone(page2_response.data['next'])
        self.assertIsNotNone(page2_response.data['previous'])

    def test_list_documents_ordering(self):
        for i in range(0, 3):
            mfactories.Document(file_name='Document{}.png'.format(i))

        request = self.factory.get('?ordering=-id')
        request.user = self.user
        view = DocumentViewSet.as_view({'get': 'list'})
        response = view(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 3)

        self.assertEqual(response.data[0]['file_name'], 'Document2.png')
        self.assertEqual(response.data[1]['file_name'], 'Document1.png')
        self.assertEqual(response.data[2]['file_name'], 'Document0.png')

    @override_settings(AWS_ACCESS_KEY_ID='dummy')
    @override_settings(AWS_SECRET_ACCESS_KEY='ex123')
    @override_settings(BOTO_S3_BUCKET='example')
    @override_settings(BOTO_S3_HOST='example.com')
    def test_list_documents_url(self):
        file_mock = mock.MagicMock(spec=File, name='FileMock')
        file_mock.name = 'test1.jpg'

        mfactories.Document(file_name='Document1.png',
                            file=file_mock)

        mfactories.Document(file_name='Document2.png')

        request = self.factory.get('')
        request.user = self.user
        view = DocumentViewSet.as_view({'get': 'list'})
        response = view(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

        now = timezone.now()
        expected_file = "https://example.example.com/uploads/" \
                        "%s-%s/%s/\S{36}.jpg" % (now.year, now.month, now.day)

        self.assertRegexpMatches(response.data[0]['file'], expected_file)
        self.assertIsNone(response.data[1]['file'])


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
        contact_uuid = str(uuid.uuid4())

        data = {
            'file_name': u'Testfile.pdf',
            'file': 'data:image/png;base64,'
                    'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR'
                    '42mP8z/C/HgAGgwJ/lK3Q6wAAAABJRU5ErkJggg==',
            'workflowlevel1_uuids': [str(uuid.uuid4())],
            'contact_uuid': contact_uuid,
        }

        request = self.factory.post('', data)
        request.user = self.user
        view = DocumentViewSet.as_view({'post': 'create'})
        response = view(request)
        self.assertEqual(response.status_code, 201)

        document = Document.objects.get(id=response.data['id'])
        self.assertEqual(document.file_name, data['file_name'])
        self.assertEqual(document.file_type, 'pdf')
        self.assertEqual(document.contact_uuid, contact_uuid)

    def test_create_document(self):
        create_date = datetime(2018, 1, 1, 12, 15)\
            .strftime("%Y-%m-%dT%H:%M:%S+01:00")
        workflowlevel1_uuids = [str(uuid.uuid4()), str(uuid.uuid4())]
        workflowlevel2_uuids = [str(uuid.uuid4()), str(uuid.uuid4())]
        organization_uuid = str(uuid.uuid4())
        contact_uuid = str(uuid.uuid4())

        data = {
            'file_name': u'Testfile.png',
            'file': 'data:image/png;base64,'
                    'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR'
                    '42mP8z/C/HgAGgwJ/lK3Q6wAAAABJRU5ErkJggg==',
            'create_date': create_date,
            'workflowlevel1_uuids': workflowlevel1_uuids,
            'workflowlevel2_uuids': workflowlevel2_uuids,
            'organization_uuid': organization_uuid,
            'contact_uuid': contact_uuid,
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
        self.assertEqual(document.file_type, 'png')
        self.assertEqual(document.create_date.strftime(
            "%Y-%m-%dT%H:%M:%SZ"), data['create_date'])
        self.assertEqual(document.workflowlevel1_uuids, workflowlevel1_uuids)
        self.assertEqual(document.workflowlevel2_uuids, workflowlevel2_uuids)
        self.assertEqual(document.organization_uuid, organization_uuid)
        self.assertEqual(document.contact_uuid, contact_uuid)

    def test_create_document_anonymoususer(self):
        request = self.factory.post('', {})
        view = DocumentViewSet.as_view({'post': 'create'})
        response = view(request)
        self.assertEqual(response.status_code, 403)

    def test_create_document_fails_empty_field(self):
        create_date = datetime(2018, 1, 1, 12, 15)\
            .strftime("%Y-%m-%dT%H:%M:%S+01:00")
        workflowlevel1_uuids = [uuid.uuid4(), uuid.uuid4()]
        contact_uuid = str(uuid.uuid4())

        data = {
            'create_date': create_date,
            'workflowlevel1_uuids': workflowlevel1_uuids,
            'contact_uuid': contact_uuid,
        }

        request = self.factory.post('', data)
        request.user = self.user
        view = DocumentViewSet.as_view({'post': 'create'})
        response = view(request)
        self.assertEqual(response.status_code, 400)

    def test_create_document_fails_invalid_file_type(self):
        contact_uuid = str(uuid.uuid4())
        data = {
            'file_name': u'Testfile.exe',
            'file': 'data:image/png;base64,'
                    'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR'
                    '42mP8z/C/HgAGgwJ/lK3Q6wAAAABJRU5ErkJggg==',
            'workflowlevel1_uuids': [str(uuid.uuid4())],
            'contact_uuid': contact_uuid,
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
