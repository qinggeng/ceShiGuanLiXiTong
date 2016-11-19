#-*- coding: utf-8 -*-
from models import *
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt

from decorators import jsonResp
import os.path
import json
from prettyprint import pp

def getUriPrefixByRequest(request):
    prefix = u'{scheme}://{host}{path}'.format(scheme = request.scheme, host = request.get_host(), path = request.path)
    return prefix

def getTestObjects(uriPrefix):
    allObjects = TestObject.objects.all()
    return map(lambda x: {'uri': uriPrefix + '/' + unicode(x.id), 'id': unicode(x.id), 'title': x.title, 'description': x.description}, allObjects)

@csrf_exempt 
@require_http_methods(['GET'])
def testObjects(request):
    prefix = u'{scheme}://{host}{path}'.format(scheme = request.scheme, host = request.get_host(), path = request.path)
    # TODO handle permissions by request
    retStr = json.dumps(getTestObjects(prefix))
    resp = HttpResponse(retStr, content_type = 'application/json')
    return resp

"""
@restful(dispatcher, method)
"""
def testObject(request, objectid):
    if request.method == 'GET':
        return getTestObject(request, objectid)
    pass

def getTestObject(request, objectid):
    testObject = TestObject.objects.filter(id = objectid)[0]
    ret = {
        'uri': getUriPrefixByRequest(request),
        'title': testObject.title,
        'id': unicode(testObject.id),
        'description': testObject.description,
        'categoryLevels': getUriPrefixByRequest(request) + '/' + 'category-levels',
        'categories': getUriPrefixByRequest(request) + '/' + 'categories',
        'reports': getUriPrefixByRequest(request) + '/' + 'reports',
        'testcases': getUriPrefixByRequest(request) + '/' + 'testcases',
        'testPlans': getUriPrefixByRequest(request) + '/' + 'test-plans',
    }
    retStr = json.dumps(ret)
    resp = HttpResponse(retStr, content_type = 'application/json')
    return resp

@csrf_exempt
def testCategoryManage(request, objectid, propName):
    if request.method == 'GET':
        return getTestObjectCategoryProp(request, objectid, propName)

def getTestObjectCategoryProp(request, objectid, propName):
    level = Level.objects.filter(id = objectid)[0]
    if propName == 'sub-categories':
        ret = map(lambda x: {
            'uri': getUriPrefixByRequest(request) + '/' + unicode(x.id),
            'title': x.title,
            'id': unicode(x.id),
            'subCategories': getUriPrefixByRequest(request) + '/' + unicode(x.id) + '/sub-categories',
            #level type uri
            'levelType': '',
        }, level.children.all())
        retStr = json.dumps(ret)
        resp = HttpResponse(retStr, content_type = 'application/json')
        return resp


@csrf_exempt
def testObjectCategories(request, objectid):
    if request.method == 'GET':
        return getTestObjectCategories(request, objectid)
    if request.method == 'PUT':
        return putTestObjectCategories(request, objectid)

def getTestObjectCategories(request, objectid):
    testObject = TestObject.objects.filter(id = objectid)[0]
    try:
        ret = map(lambda x: dict({
                    'uri': getUriPrefixByRequest(request) + '/' + unicode(x.id),
                },
                **categoryJsonify(getUriPrefixByRequest(request), x)),
            testObject.testLevels.all())
    except Exception, e:
        ret = []
    retStr = json.dumps(ret)
    resp = HttpResponse(retStr, content_type = 'application/json')
    return resp

def putTestObjectCategories(request, objectid):
    categoryIds = json.loads(request.body)
    categories = Level.objects.filter(testObjects = None).filter(id__in = categoryIds)
    testObject = TestObject.objects.filter(id = objectid)[0]
    for category in categories:
        testObject.testLevels.add(category)
        testObject.save()
    return getTestObjectCategories(request, objectid)

def testCategories(request, categoryId):
    if request.method == 'GET':
        return getTestCategories(request, categoryId)

def getTestCategories(request, categoryId):
    if u'orphans' == categoryId:
        categories = Level.objects.filter(parent = None).filter(testObjects = None)
        categories = map(lambda x: {}, categories)
        ret = HttpResponse(json.dumps(categories))
        return ret
    else:
        pass

def categoryJsonify(uriPrefix, x):
    return {
            'id': unicode(x.id),
            'title': x.title,
            'id': unicode(x.id),
            'subCategories':uriPrefix + '/' + unicode(x.id) + '/sub-categories',
            #level type uri
            'levelType': '',
    }

