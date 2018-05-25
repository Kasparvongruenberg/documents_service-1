from __future__ import unicode_literals
import uuid

from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.core.exceptions import ValidationError

from django_boto.s3.storage import S3Storage
from functools import partial

try:
    from django.utils import timezone
except ImportError:
    from datetime import datetime as timezone


FILE_TYPE_CHOICES = (
    ('jpg', 'JPG Image'),
    ('png', 'PNG Image'),
    ('pdf', 'PDF File'),
)

s3 = S3Storage()


def make_filepath(field_name, instance, filename):
    now = timezone.now()
    new_filename = "%s.%s" % (uuid.uuid4(), filename.split('.')[-1])
    filepath = "uploads/%s-%s/%s/" % (now.year, now.month, now.day)
    return filepath+new_filename


class Document(models.Model):
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)

    file_name = models.CharField(max_length=50, help_text='Filename')
    file_type = models.CharField(
        max_length=30, choices=FILE_TYPE_CHOICES,
        null=True, blank=True,
        help_text='Allowed File Types: {}'.format(
            ", ".join([ft[0] for ft in FILE_TYPE_CHOICES])))
    file = models.FileField(upload_to=partial(make_filepath, 'file'),
                            null=True,
                            blank=True,
                            storage=s3)

    create_date = models.DateTimeField(null=True, blank=True)
    upload_date = models.DateTimeField(null=True, blank=True,
                                       auto_now_add=True)

    organization_uuid = models.CharField(max_length=36, blank=True, null=True,
                                         verbose_name='Organization UUID')
    user_uuid = models.CharField(max_length=36, blank=True, null=True,
                                 verbose_name='User UUID')

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
        super(Document, self).save()

    def __unicode__(self):
        return u'{} {}'.format(self.file_type, self.file_name)
