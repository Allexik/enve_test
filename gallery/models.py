import os

from django.conf import settings
from django.db import models

from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import ValidationError


class Album(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=90)

    class Meta:
        unique_together = ('owner', 'name')

    def __str__(self):
        return '%s - %s' % (self.owner, self.name)


def get_photo_upload_path(instance, filename):
    return os.path.join('photos/', filename)


class Photo(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to=get_photo_upload_path)
    description = models.CharField(max_length=200, blank=True)
    album = models.ForeignKey(Album, on_delete=models.CASCADE)

    def __str__(self):
        return '%s - %s - %s' % (self.owner, self.album.name, os.path.basename(self.photo.name))

    def clean(self):
        if self.owner != self.album.owner:
            raise ValidationError({'album': _('This album does not belong to you')})

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)


class Comment(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.CharField(max_length=500)
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE)

    def __str__(self):
        return '%s - %s - %s' % (self.owner, self.photo, self.text[:15])


class Bookmark(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('owner', 'photo')

    def __str__(self):
        return '%s - %s' % (self.owner, self.photo)

    def clean(self):
        if self.owner == self.photo.owner:
            raise ValidationError({'photo': _('You cannot bookmark own photos')})

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)


