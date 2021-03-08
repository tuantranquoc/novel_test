from django.db import models
from manga import choices
from django.utils import timezone
from django import forms
from django_ace import AceWidget

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name


class Author(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name


class Manga(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    created = models.DateTimeField(default=timezone.now)
    last_update = models.DateTimeField(auto_now_add=True)
    slug = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    status = models.IntegerField(choices=choices.STATUS_CHOICES, default=1)
    category = models.ManyToManyField(Category)
    source = models.IntegerField(choices=choices.SOURCE_CHOICES, default=1)

    def __str__(self):
        return self.title


class Chapter(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    chapter = models.IntegerField(default=0)
    content = models.TextField()
    manga = models.ForeignKey(
        Manga, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.title
