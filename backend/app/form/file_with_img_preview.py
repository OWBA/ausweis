from django.conf import settings
# from django.contrib.admin.widgets import AdminFileWidget
# from django.core.exceptions import ValidationError
from django.db import models
from django.forms import ValidationError
from django.forms.widgets import ClearableFileInput

# class ImageFileWidget(AdminFileWidget):


class ImageFileWidget(ClearableFileInput):
    template_name = 'forms/img-file.html'

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['MEDIA_URL'] = settings.MEDIA_URL
        return context


class FileWithImagePreview(models.FileField):
    def formfield(self, **kwargs):
        # if 'widget' not in kwargs:  # only if no other is set (admin UI)
        kwargs['widget'] = ImageFileWidget
        return super().formfield(**kwargs)


class ImageValidator:
    help_text = 'Ideal: 250 x 320 px (JPEG oder PNG)'

    @staticmethod
    def validate(value: 'models.FieldFile') -> None:
        # TODO: make configurable
        if value.size > 512 * 1024:
            raise ValidationError('Datei darf maximal 512 KB groß sein.')

        content_type = getattr(value.file, 'content_type', None)
        if content_type not in ['image/png', 'image/jpeg', None]:
            raise ValidationError('Nur JPEG und PNG Bilder werden unterstützt')
