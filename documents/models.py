from __future__ import unicode_literals
import uuid
from io import BytesIO

from django.contrib.postgres.fields import ArrayField
from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from django.db import models

from functools import partial
from PIL import Image


try:
    from django.utils import timezone
except ImportError:
    from datetime import datetime as timezone


def get_file_storage():
    try:
        from django_boto.s3.storage import S3Storage
        file_storage = S3Storage()
    except AttributeError:
        from django.core.files.storage import FileSystemStorage
        file_storage = FileSystemStorage('/media/uploads/')
    return file_storage


FILE_TYPE_CHOICES = (
    ('jpg', 'JPG Image'),
    ('jpeg', 'JPEG Image'),
    ('png', 'PNG Image'),
    ('gif', 'GIF File'),
    ('pdf', 'PDF Document'),
    ('txt', 'TXT File'),
    ('doc', 'doc Document'),
    ('docx', 'docx Document'),
    ('xls', 'xls File'),
    ('xlsx', 'xlsx File'),
    ('ppt', 'ppt Document'),
    ('pptx', 'pptx Document'),
)
IMAGE_FILE_TYPES = ['jpg', 'jpeg', 'png', '.gif']
THUMBNAIL_DIMENSIONS = (200, 200)


def make_filepath(field_name, instance, filename):
    now = timezone.now()
    new_filename = "%s.%s" % (uuid.uuid4(), filename.split('.')[-1])
    filepath = "uploads/%s-%s/%s/" % (now.year, now.month, now.day)
    return filepath+new_filename


def make_filepath_thumbnail(field_name, instance, filename):
    now = timezone.now()
    new_filename = "%s.%s" % (uuid.uuid4(), filename.split('.')[-1])
    filepath = "uploads/%s-%s/%s/thumbnails/" % (now.year, now.month, now.day)
    return filepath+new_filename


class Document(models.Model):
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)

    file_description = models.CharField(max_length=50,
                                        help_text='File Description',
                                        null=True, blank=True)
    file_name = models.CharField(max_length=50, help_text='Filename')
    file_type = models.CharField(
        max_length=30, choices=FILE_TYPE_CHOICES,
        null=True, blank=True,
        help_text='Allowed File Types: {}'.format(
            ", ".join([ft[0] for ft in FILE_TYPE_CHOICES])))
    file = models.FileField(upload_to=partial(make_filepath, 'file'),
                            null=True,
                            blank=True,
                            storage=get_file_storage())

    thumbnail = models.FileField(
                            upload_to=partial(make_filepath_thumbnail, 'file'),
                            null=True,
                            blank=True,
                            storage=get_file_storage())

    create_date = models.DateTimeField(null=True, blank=True)
    upload_date = models.DateTimeField(null=True, blank=True,
                                       auto_now_add=True)

    organization_uuid = models.CharField(max_length=36, blank=True, null=True,
                                         verbose_name='Organization UUID')
    user_uuid = models.CharField(max_length=36, blank=True, null=True,
                                 verbose_name='User UUID')

    contact_uuid = models.CharField(max_length=36, blank=True,
                                    null=True, verbose_name='Contact UUID')

    workflowlevel1_uuids = ArrayField(models.CharField(max_length=36),
                                      blank=True, null=True,
                                      help_text='List of Workflowlevel1 UUIDs')
    workflowlevel2_uuids = ArrayField(models.CharField(max_length=36),
                                      blank=True, null=True,
                                      help_text='List of Workflowlevel2 UUIDs')

    def clean_fields(self, exclude=None):
        super(Document, self).clean_fields(exclude=exclude)

        if self.file_type not in [ft[0] for ft in FILE_TYPE_CHOICES]:
            raise ValidationError('Invalid File Type.'
                                  'Allowed File Types: {}'.format(
                                    ', '.join([ft[0] for ft in
                                               FILE_TYPE_CHOICES])))

    def save(self, *args, **kwargs):
        self.file_type = self.file_name.lower().split('.')[-1]
        self.full_clean()

        if self.file_type in IMAGE_FILE_TYPES and self.file:
            self.make_thumbnail()

        super(Document, self).save()

    def make_thumbnail(self):
        if self.file_type in ['jpg', 'jpeg']:
            ftype = 'JPEG'
        elif self.file_type == 'gif':
            ftype = 'GIF'
        elif self.file_type == 'png':
            ftype = 'PNG'
        else:
            return False

        # load image
        image = Image.open(self.file)

        # scale and crop image to maintain ratio
        size = THUMBNAIL_DIMENSIONS
        image_ratio = image.size[0] / image.size[1]

        ratio = size[0] / size[1]

        if ratio > image_ratio:
            image = image.resize(
                (size[0], int(size[0] * image.size[1] / image.size[0])),
                Image.ANTIALIAS)

            box = (0, (image.size[1] - size[1]) / 2,
                   image.size[0], (image.size[1] + size[1]) / 2)

            image = image.crop(box)
        elif ratio < image_ratio:
            image = image.resize(
                (int(size[1] * image.size[0] / image.size[1]), size[1]),
                Image.ANTIALIAS)

            box = (
                int((image.size[0] - size[0]) / 2), 0,
                int((image.size[0] + size[0]) / 2), image.size[1])

            image = image.crop(box)
        else:
            image = image.resize((size[0], size[1]), Image.ANTIALIAS)

        # save temporary image
        temp_thumb = BytesIO()

        image.save(temp_thumb, ftype)
        temp_thumb.seek(0)

        self.thumbnail = ContentFile(temp_thumb.read(),
                                     name=self.file.name)

    def __unicode__(self):
        return u'{} {}'.format(self.file_type, self.file_name)
