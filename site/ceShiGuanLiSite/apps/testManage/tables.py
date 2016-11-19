# -*- encoding: utf-8 -*-
from models import *
import django_tables2 as tables
class TestObjectTable(tables.Table):
    class Meta:
        model = TestObject
        attrs = {'class': 'paleblue'}
    id           = tables.Column(visible = False, accessor = 'id', verbose_name = u'GUID')
    title        = tables.Column(visible = True, accessor = 'title', verbose_name = u'标题')
    description  = tables.Column(visible = True, accessor = 'description', verbose_name = u'描述')

class TestLevelTypeTable(tables.Table):
    class Meta:
        model = LevelType
        attrs = {'class': 'paleblue'}
    id           = tables.Column(visible = False, accessor = 'id', verbose_name = u'GUID')
    title        = tables.Column(visible = True, accessor = 'title', verbose_name = u'标题')
    description  = tables.Column(visible = True, accessor = 'description', verbose_name = u'描述')
    description = tables.Column(visible = True, accessor = 'testObjects', verbose_name = u'所属测试对象')

modelTables = {
    TestObject: TestObjectTable,
    LevelType: TestLevelTypeTable,
}


