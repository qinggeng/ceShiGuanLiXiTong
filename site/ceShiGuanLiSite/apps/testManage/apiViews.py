#-*- coding: utf-8 -*-
from models import *
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt

from decorators import jsonResp
import os.path
import json
from prettyprint import pp

from libs.resturl import uriProcessingChain

def getUriPrefixByRequest(request):
    prefix = u'{scheme}://{host}{path}'.format(scheme = request.scheme, host = request.get_host(), path = request.path)
    return prefix

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


def testObjectListing(useless):
    objects = TestObject.objects
    return objects

def getTestObjectById(objects, oid):
    ret =  objects.get(id = oid)
    return ret

def getTestObjectCategories(testObject, dummy):
    ret = testObject.testLevels
    return ret

kPattern  = 'pattern'
kChildren = 'children'
kHandler  = 'handler'

uriChain = [{
    kPattern: 'testObjects',
    kHandler: testObjectListing,
    kChildren: [{
        kPattern  : '[0-9a-f-]{36}',
        kHandler  : getTestObjectById,
        kChildren : [{
            kPattern  : 'categories',
            kHandler  : getTestObjectCategories,
            kChildren : []},
            ],},],
}]


def testUriChain():
    from serializers import obj2json
    uri = "testObjects/67a01e17-9e8e-4d99-973b-170d74110a4b"
    ret = uriProcessingChain(uri, uriChain)
    ret = obj2json(ret)
    pp(ret)
    ret = type(ret)

from serializers import obj2json

def injectUriForTestObject(prefix, x):
    def ap(key):
        x[key] = prefix + '/' + x[key]
    x['uri'] = prefix
    ap('categories')
    ap('categoryLevels')
    ap('reports')
    ap('testcases')
    ap('testPlans')

def injectUriForTestObjects(prefix, objects):
    return map(lambda x: injectUriForTestObject(prefix + '/' + x['id'], x), objects)

def injectUriForTestLevel(prefix, x):
    def ap(key):
        x[key] = prefix + '/' + x[key]
    x['uri'] = prefix
    ap('subCategories')

def injectUriForTestLevels(prefix, objects):
    return map(lambda x: injectUriForTestLevel(prefix + '/' + x['id'], x), objects)

uriInjectors = {
    TestObject         : injectUriForTestObject,
    TestObject.objects : injectUriForTestObjects,
    TestObject.testLevels.related_manager_cls: injectUriForTestLevels,
    Level: injectUriForTestLevel,
}

def injectUri(injector, targets, prefix):
    if None == injector:
        return targets
    injector(prefix, targets)
    return targets


def apiRoot(request, uri):
    obj = uriProcessingChain(uri, uriChain)
    print obj
    if (None == obj):
        response = HttpResponse()
        response.status_code = 404
        return response

    ret = obj2json(obj)
    objType = type(obj)
    print 'objType', objType
    pp(ret)
    injector = None
    if obj in uriInjectors:
        injector = uriInjectors[obj]
    elif objType in uriInjectors:
        injector = uriInjectors[objType]
    ret = injectUri(injector, ret, getUriPrefixByRequest(request))
    ret = json.dumps(ret, ensure_ascii = False)
    response = HttpResponse(ret)
    return response

