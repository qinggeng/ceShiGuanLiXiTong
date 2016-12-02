# -*- coding: utf-8
import requests
from prettyprint import pp
import json

def importLevelsFromXslx():
    url = 'http://192.168.99.100:8081/test-man/import-xlsx'
    path = u'ceShiGuanLiSite/test.xlsx'
    f = open(path, 'r')
    formData = {
        'ltlt': 'B6',
        'ltrb': 'D7',
        'llt': 'B8',
        'lrb': 'D419'
    }
    resp = requests.post(url, data = formData, files = {'file': f})
    print resp

def createNewLevel():
    url = 'http://192.168.99.100:8081/test-man/new-test-object'
    formData = {
        'name': u'满意云',
        'description': u'医患关系管理系统(鼓楼)',
    }
    resp = requests.post(url, data = formData)
    print resp

def getTestObjectsByApi():
    url = 'http://192.168.99.100:8081/test-man/api/v0/testObjects?filter=abc'
    resp = requests.get(url)
    pp(resp.text)

def getTestObjectByApi(log = False):
    url = 'http://192.168.99.100:8081/test-man/api/v0/testObjects?filter=abc'
    resp = requests.get(url)
    testObjects = json.loads(resp.text)
    testObjectUri = testObjects[0]['uri']
    resp = requests.get(testObjectUri)
    testObject = json.loads(resp.text)
    if log:
        pp(testObject)
    return testObject

def getTestObjectCategories():
    testObject = getTestObjectByApi()
    url = testObject['categories']
    resp = requests.get(url)
    return json.loads(resp.text)

def getOrphanTestCategories():
    url = 'http://192.168.99.100:8081/test-man/api/v0/testCategories/orphans'
    resp = requests.get(url)
    return (json.loads(resp.text))

def putTestObjectCategory():
    testObject = getTestObjectByApi()
    category = getOrphanTestCategories()[0]
    url = testObject['categories']
    resp = requests.put(url, json = [category['id']])
    return (json.loads(resp.text))

#pp(putTestObjectCategory())
#pp(getTestObjectCategories())
#pp(getOrphanTestCategories())
#pp(getTestObjectCategories())
pp(getTestObjectsByApi())
