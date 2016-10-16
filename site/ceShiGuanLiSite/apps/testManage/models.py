from __future__ import unicode_literals

from django.db import models
import uuid

# Create your models here.

class Level(models.Model):
    title = models.CharField(max_length = 200)
    id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    parent = models.UUIDField()

class LevelTypes(models.Model):
    title = models.CharField(max_length = 200)
    id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    parent = models.UUIDField()

class TestObject(models.Model):
    id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)

class TestCase(models.Model):
    id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)

class TestSet(models.Model):
    id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)

