# -*- coding: utf-8 -*-
from datetime import datetime
from io import BytesIO
import uuid

from PIL import Image
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.core.files.base import ContentFile
from django.conf import settings
import pytz
import boto3
from moto import mock_s3

from ..models import Document


class DocumentTest(TestCase):
    def test_document_save_required_fields(self):
        file_name = "Test File 1.jpg"
        contact_uuid = str(uuid.uuid4())

        document = Document.objects.create(
            file_name=file_name,
            workflowlevel1_uuids=[str(uuid.uuid4())],
            contact_uuid=contact_uuid
        )

        document_db = Document.objects.get(pk=document.pk)
        self.assertEqual(document_db.file_name, file_name)
        self.assertEqual(document_db.contact_uuid, contact_uuid)

    def test_document_save_all_fields(self):
        file_name = "Test File 1.jpg"
        file_description = "Test File 1"
        contact_uuid = str(uuid.uuid4())

        document = Document.objects.create(
            file_name=file_name,
            file_description=file_description,
            file_type='jpg',
            upload_date=datetime(2018, 1, 1, 12, 30, tzinfo=pytz.UTC),
            organization_uuid="TestUUID",
            workflowlevel1_uuids=['TestWF1UUID'],
            workflowlevel2_uuids=['TestWF2UUID'],
            contact_uuid=contact_uuid
        )

        document_db = Document.objects.get(pk=document.pk)
        self.assertEqual(document_db.file_name, file_name)
        self.assertEqual(document_db.file_description, file_description)
        self.assertEqual(document_db.organization_uuid, 'TestUUID')
        self.assertEqual(document_db.workflowlevel1_uuids, ['TestWF1UUID'])
        self.assertEqual(document_db.workflowlevel2_uuids, ['TestWF2UUID'])
        self.assertEqual(document_db.contact_uuid, contact_uuid)

    def test_document_save_fails_missing_filename(self):
        document = Document(
            file_type='jpg',
            upload_date=datetime(2018, 1, 1, 12, 30, tzinfo=pytz.UTC),
            organization_uuid="TestUUID",
            workflowlevel1_uuids=['TestWF1UUID'],
            workflowlevel2_uuids=['TestWF2UUID'],
            contact_uuid=str(uuid.uuid4())
        )

        self.assertRaises(ValidationError, document.save)

    def test_document_save_fails_wrong_file_type(self):
        document = Document(
            file_name='file1.x',
            file_type='x',
            upload_date=datetime(2018, 1, 1, 12, 30, tzinfo=pytz.UTC),
            organization_uuid="TestUUID",
            workflowlevel1_uuids=['TestWF1UUID'],
            workflowlevel2_uuids=['TestWF2UUID'],
            contact_uuid=str(uuid.uuid4())
        )

        self.assertRaises(ValidationError, document.save)

    def test_document_save_fails_wrong_file_type2(self):
        document = Document(
            file_name='file1.x',
            file_type='png',
            upload_date=datetime(2018, 1, 1, 12, 30, tzinfo=pytz.UTC),
            organization_uuid="TestUUID",
            workflowlevel1_uuids=['TestWF1UUID'],
            workflowlevel2_uuids=['TestWF2UUID'],
            contact_uuid=str(uuid.uuid4())
        )

        self.assertRaises(ValidationError, document.save)

    def test_document_save_fails_wrong_date_format(self):
        document = Document(
            file_name='file2.jpg',
            file_type='jpg',
            upload_date='2018.5.5',
            contact_uuid=str(uuid.uuid4())
        )

        self.assertRaises(ValidationError, document.save)

    def test_document_save_file_type_jpg(self):
        file_name = "Test File 1.jpg"
        contact_uuid = str(uuid.uuid4())

        document = Document.objects.create(
            file_name=file_name,
            workflowlevel1_uuids=[str(uuid.uuid4())],
            contact_uuid=contact_uuid
        )

        document_db = Document.objects.get(pk=document.pk)
        self.assertEqual(document_db.file_name, file_name)
        self.assertEqual(document_db.contact_uuid, contact_uuid)

    def test_document_save_file_type_jpeg(self):
        file_name = "Test File 1.jpeg"
        contact_uuid = str(uuid.uuid4())

        document = Document.objects.create(
            file_name=file_name,
            workflowlevel1_uuids=[str(uuid.uuid4())],
            contact_uuid=contact_uuid
        )

        document_db = Document.objects.get(pk=document.pk)
        self.assertEqual(document_db.file_name, file_name)
        self.assertEqual(document_db.contact_uuid, contact_uuid)

    def test_document_save_file_type_png(self):
        file_name = "Test File 1.png"
        contact_uuid = str(uuid.uuid4())

        document = Document.objects.create(
            file_name=file_name,
            workflowlevel1_uuids=[str(uuid.uuid4())],
            contact_uuid=contact_uuid
        )

        document_db = Document.objects.get(pk=document.pk)
        self.assertEqual(document_db.file_name, file_name)
        self.assertEqual(document_db.contact_uuid, contact_uuid)

    def test_document_save_file_type_gif(self):
        file_name = "Test File 1.gif"
        contact_uuid = str(uuid.uuid4())

        document = Document.objects.create(
            file_name=file_name,
            workflowlevel1_uuids=[str(uuid.uuid4())],
            contact_uuid=contact_uuid
        )

        document_db = Document.objects.get(pk=document.pk)
        self.assertEqual(document_db.file_name, file_name)
        self.assertEqual(document_db.contact_uuid, contact_uuid)

    def test_document_save_file_type_pdf(self):
        file_name = "Test File 1.pdf"
        contact_uuid = str(uuid.uuid4())

        document = Document.objects.create(
            file_name=file_name,
            workflowlevel1_uuids=[str(uuid.uuid4())],
            contact_uuid=contact_uuid
        )

        document_db = Document.objects.get(pk=document.pk)
        self.assertEqual(document_db.file_name, file_name)
        self.assertEqual(document_db.contact_uuid, contact_uuid)

    def test_document_save_file_type_txt(self):
        file_name = "Test File 1.txt"
        contact_uuid = str(uuid.uuid4())

        document = Document.objects.create(
            file_name=file_name,
            workflowlevel1_uuids=[str(uuid.uuid4())],
            contact_uuid=contact_uuid
        )

        document_db = Document.objects.get(pk=document.pk)
        self.assertEqual(document_db.file_name, file_name)
        self.assertEqual(document_db.contact_uuid, contact_uuid)

    def test_document_save_file_type_doc(self):
        file_name = "Test File 1.doc"
        contact_uuid = str(uuid.uuid4())

        document = Document.objects.create(
            file_name=file_name,
            workflowlevel1_uuids=[str(uuid.uuid4())],
            contact_uuid=contact_uuid
        )

        document_db = Document.objects.get(pk=document.pk)
        self.assertEqual(document_db.file_name, file_name)
        self.assertEqual(document_db.contact_uuid, contact_uuid)

    def test_document_save_file_type_docx(self):
        file_name = "Test File 1.docx"
        contact_uuid = str(uuid.uuid4())

        document = Document.objects.create(
            file_name=file_name,
            workflowlevel1_uuids=[str(uuid.uuid4())],
            contact_uuid=contact_uuid
        )

        document_db = Document.objects.get(pk=document.pk)
        self.assertEqual(document_db.file_name, file_name)
        self.assertEqual(document_db.contact_uuid, contact_uuid)

    def test_document_save_file_type_xls(self):
        file_name = "Test File 1.xls"
        contact_uuid = str(uuid.uuid4())

        document = Document.objects.create(
            file_name=file_name,
            workflowlevel1_uuids=[str(uuid.uuid4())],
            contact_uuid=contact_uuid
        )

        document_db = Document.objects.get(pk=document.pk)
        self.assertEqual(document_db.file_name, file_name)
        self.assertEqual(document_db.contact_uuid, contact_uuid)

    def test_document_save_file_type_xlsx(self):
        file_name = "Test File 1.xlsx"
        contact_uuid = str(uuid.uuid4())

        document = Document.objects.create(
            file_name=file_name,
            workflowlevel1_uuids=[str(uuid.uuid4())],
            contact_uuid=contact_uuid
        )

        document_db = Document.objects.get(pk=document.pk)
        self.assertEqual(document_db.file_name, file_name)
        self.assertEqual(document_db.contact_uuid, contact_uuid)

    def test_document_save_file_type_ppt(self):
        file_name = "Test File 1.ppt"
        contact_uuid = str(uuid.uuid4())

        document = Document.objects.create(
            file_name=file_name,
            workflowlevel1_uuids=[str(uuid.uuid4())],
            contact_uuid=contact_uuid
        )

        document_db = Document.objects.get(pk=document.pk)
        self.assertEqual(document_db.file_name, file_name)
        self.assertEqual(document_db.contact_uuid, contact_uuid)

    def test_document_save_file_type_pptx(self):
        file_name = "Test File 1.pptx"
        contact_uuid = str(uuid.uuid4())

        document = Document.objects.create(
            file_name=file_name,
            workflowlevel1_uuids=[str(uuid.uuid4())],
            contact_uuid=contact_uuid
        )

        document_db = Document.objects.get(pk=document.pk)
        self.assertEqual(document_db.file_name, file_name)
        self.assertEqual(document_db.contact_uuid, contact_uuid)

    @mock_s3
    def test_document_save_generates_thumbnail(self):
        conn = boto3.resource('s3', region_name='us-east-1')
        conn.create_bucket(Bucket=settings.AWS_STORAGE_BUCKET_NAME)

        file_name = "Test.jpg"
        contact_uuid = str(uuid.uuid4())

        image = Image.new('RGB', (400, 500), color='blue')
        temp_thumb = BytesIO()
        image.save(temp_thumb, "JPEG")
        temp_thumb.seek(0)

        file = ContentFile(temp_thumb.read(), name="Testfile.jpg")

        document = Document.objects.create(
            file_name=file_name,
            file=file,
            file_type='jpg',
            workflowlevel1_uuids=[str(uuid.uuid4())],
            contact_uuid=contact_uuid
        )

        document.save()

        document_db = Document.objects.get(pk=document.pk)

        self.assertEqual(document_db.file_name, file_name)
        self.assertEqual(document_db.contact_uuid, contact_uuid)
        thumbnail = Image.open(document_db.thumbnail)
        self.assertEqual(thumbnail.size, (200, 200))
