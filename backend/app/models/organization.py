from django.conf import settings
from django.db import models

import os
import shutil
import typing

if typing.TYPE_CHECKING:
    from app.models.member import Member


class Organization(models.Model):
    name = models.CharField('Name', max_length=100)
    slug = models.SlugField('URL Slug', unique=True, max_length=50)
    exportBaseUrl = models.URLField('Export Base-URL', max_length=200)
    members: 'models.QuerySet[Member]'

    class Meta:
        verbose_name = 'Organisation'
        verbose_name_plural = 'Organisationen'

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        if self.pk:
            try:
                prev = Organization.objects.get(pk=self.pk)
                if prev.slug != self.slug:
                    renameSlug(prev.slug, self.slug)
            except Organization.DoesNotExist:
                pass
        return super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        deleteSlug(self.slug)
        return super().delete(*args, **kwargs)


def renameSlug(oldSlug: str, newSlug: str):
    if newSlug == oldSlug:
        return
    oldExportPath = settings.EXPORT_PATH / oldSlug
    oldMediaPath = settings.MEDIA_ROOT / oldSlug
    if os.path.exists(oldExportPath):
        os.rename(oldExportPath, settings.EXPORT_PATH / newSlug)
    if os.path.exists(oldMediaPath):
        os.rename(oldMediaPath, settings.MEDIA_ROOT / newSlug)


def deleteSlug(oldSlug: str):
    shutil.rmtree(settings.EXPORT_PATH / oldSlug, ignore_errors=True)
    shutil.rmtree(settings.MEDIA_ROOT / oldSlug, ignore_errors=True)
