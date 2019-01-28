# -*- coding: utf-8 -*-
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.conf import settings
from rest_framework.test import APIRequestFactory
import boto3
from moto import mock_s3

from . import model_factories as mfactories
from ..serializers import DocumentSerializer


@mock_s3
class DocumentSerializerTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = mfactories.User()
        conn = boto3.resource('s3', region_name='us-east-1')
        conn.create_bucket(Bucket=settings.AWS_STORAGE_BUCKET_NAME)

    def test_contains_expected_fields(self):
        # Mock with pdf since image files will trigger thumbnail generation
        file_mock = SimpleUploadedFile('test1.pdf', b'some content')

        document = mfactories.Document(file_name='Document1.pdf',
                                       file=file_mock)

        serializer = DocumentSerializer(instance=document)

        data = serializer.data

        keys = [
            'workflowlevel1_uuids',
            'file_type',
            'user_uuid',
            'workflowlevel2_uuids',
            'organization_uuid',
            'upload_date',
            'create_date',
            'contact_uuid',
            'uuid',
            'file_description',
            'id',
            'file',
            'file_name',
            'thumbnail'
        ]

        self.assertEqual(set(data.keys()), set(keys))

    def test_mock_s3(self):
        # Mock with pdf since image files will trigger thumbnail generation
        file_mock = SimpleUploadedFile('test1.pdf', b'some content')

        self.document = mfactories.Document(file_name='Document1.pdf',
                                            file=file_mock)

        expected_file = "/file/{}/".format(self.document.pk)

        serializer = DocumentSerializer(instance=self.document)
        self.assertEquals(serializer.data['file'], expected_file)

    def test_without_file(self):
        self.document = mfactories.Document(file_name='Document1.jpg',
                                            file=None)

        serializer = DocumentSerializer(instance=self.document)
        self.assertIsNone(serializer.data['file'])
