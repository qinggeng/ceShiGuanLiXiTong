# -*- coding: utf-8 -*-
"""
json序列化框架的设计:
|------------------|-----------------------------------|----------------------|
|    OBJECT        | CLASS                             | USE                  |
|------------------|-----------------------------------|----------------------|
|    converterDict | dict                              | store kv for         |
|                  |                                   | (instance / type)->  |    
|                  |                                   | dictConvertFunction  |
|------------------|-----------------------------------|----------------------|
|    encoder       | Encoder, subclass of JSON.Encoder | use converterDict to |
|                  |                                   | generate jsoned      |
|                  |                                   | string               |     
|------------------|-----------------------------------|----------------------|
"""
import functools
from models import *
def jsonifyTestObject(x):
    return {
#        'uri': uriPrefix + '/' + unicode(x.id), 
        'id': unicode(x.id), 
        'title': x.title, 
        'description': x.description,
        'categoryLevels': 'categoryLevels',
        'categories': 'categories',
        'reports': 'reports',
        'testcases': 'testcases',
        'testPlans': 'test-plans',
        }

def jsonifyCategory(x):
    return {
            'id'            : unicode(x.id),
            'title'         : x.title,
            'id'            : unicode(x.id),
            'subCategories' : 'sub-categories',
            'levelType'     : '',
    }

def mgr2json(x):
    convs = JsonConvertors
    return map(lambda y: convs[type(y)](y), x.all())


JsonConvertors = {
    TestObject: jsonifyTestObject,
    TestObject.objects: (lambda x: map(JsonConvertors[TestObject], x.all())),
    #TestObject.testLevels.related_manager_cls: (lambda x: map(JsonConvertors[type(x)], x.all())),
    TestObject.testLevels.related_manager_cls: mgr2json,
    Level: jsonifyCategory,
}

def obj2jsonFunc(converters, obj):
    objType = type(obj)
    if obj in converters:
        return converters[obj](obj)
    elif objType in converters:
        return converters[objType](obj)
    return ""

obj2json = functools.partial(obj2jsonFunc, JsonConvertors)


def test():
    from prettyprint import pp
    pp(obj2json(TestObject.objects))
if __name__ == '__main__':
    test()
    
