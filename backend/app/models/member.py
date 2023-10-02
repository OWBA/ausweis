from pathlib import PosixPath
from django.conf import settings
from django.db import models

from app.form.file_with_img_preview import FileWithImagePreview, ImageValidator
from app.utils import encrypt, overwrite_upload, random_secret

import os
import uuid
import json
import base64


class Member(models.Model):
    # auto-generated ids
    uuid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    secret = models.CharField(
        max_length=20, default=random_secret, editable=False)

    # member info
    organization = models.ForeignKey(
        'Organization', on_delete=models.CASCADE, related_name='members')
    member_id = models.CharField('Mitglieder-Nr.', max_length=20)
    name = models.CharField('Name', max_length=100)
    valid_since = models.DateField('Mitglied seit')
    valid_until = models.DateField('Mitglied bis', blank=True, null=True)
    image = FileWithImagePreview(
        'Bild', blank=True, null=True,
        upload_to=overwrite_upload, validators=[ImageValidator.validate],
        help_text=ImageValidator.help_text)
    additional = models.JSONField(
        'Zusätzliche Daten (JSON)', blank=True, null=True)

    class Meta:
        verbose_name = 'Mitglied'
        verbose_name_plural = 'Mitglieder'

    def __str__(self) -> str:
        return self.name

    @property
    def export_url(self) -> str:
        return self.organization.exportBaseUrl + \
            f"#{self.organization.slug}/{self.uuid}/{self.secret}"

    @property
    def export_os_path(self) -> PosixPath:
        return settings.EXPORT_PATH / self.organization.slug / str(self.uuid)

    @property
    def image_save_url(self) -> str:
        return f'{self.organization.slug}/{self.uuid}'

    @property
    def image_os_path(self) -> PosixPath:
        return settings.MEDIA_ROOT / self.organization.slug / str(self.uuid)

    @property
    def json(self):
        return json.dumps({
            'name': self.name,
            'org': self.organization.name,
            'id': self.member_id,
            'valid_since': str(self.valid_since or ''),
            'valid_until': str(self.valid_until or ''),
            'data': self.additional or '',
            'img': base64.b64encode(self.image.read()).decode(
                'utf-8') if self.image else None,
        })

    @property
    def json_encrypted(self) -> bytes:
        return encrypt(self.json, self.secret)

    def export(self):
        os.makedirs(self.export_os_path.parent, exist_ok=True)
        with open(self.export_os_path, 'wb') as fp:
            fp.write(self.json_encrypted)

    def save(self, *args, **kwargs):
        if self.pk:
            try:
                prev = Member.objects.get(pk=self.pk)
                if prev.image != self.image:
                    prev.image.delete(save=False)
            except Member.DoesNotExist:
                pass
        self.export()
        return super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.image:
            self.image.delete(save=False)
        if os.path.isfile(self.export_os_path):
            os.remove(self.export_os_path)
        return super().delete(*args, **kwargs)
