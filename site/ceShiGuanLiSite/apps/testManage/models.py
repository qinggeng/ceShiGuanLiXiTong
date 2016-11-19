from __future__ import unicode_literals

from django.db import models
import uuid

# Create your models here.

class Level(models.Model):
    title       = models.CharField(max_length = 200)
    id          = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    parent      = models.ForeignKey('self', on_delete = models.CASCADE, null = True, related_name = 'children')
    levelType   = models.ForeignKey('LevelType', on_delete = models.PROTECT, null = True)
    def __str__(self):
        return str({'id': self.id, 'parent': self.parent, 'levelType': self.levelType, 'testObjects': self.testObjects})

class LevelType(models.Model):
    title       = models.CharField(max_length = 200)
    id          = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    prevLevel   = models.ForeignKey('self', on_delete = models.PROTECT, null = True)
    def __init__(self, title, id = None, prevLevel = None):
        models.Model.__init__(self)
        self.title = title
        if id == None:
            id = uuid.uuid4()
        self.id = id
        self.prevLevel = prevLevel

    def __repr__(self):
        return str({'id': self.id, 'title': self.title})

    def __str__(self):
        return str({'id': self.id, 'title': self.title})

class TestObject(models.Model):
    id              = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    title           = models.CharField(max_length = 200, default = u'')
    description     = models.CharField(max_length = 4000, default = u'')
    testLevelTypes  = models.ManyToManyField('LevelType')
    testLevels      = models.ManyToManyField('Level', related_name = 'testObjects')
    def levelTypes(self):
        return LevelType.objects.filter(testObject = self)

class TestCase(models.Model):
    id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)

class TestSet(models.Model):
    id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)

class TestPlan(models.Model):
    id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)

class Comment(models.Model):
    id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)

class Transaction(models.Model):
    id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)

