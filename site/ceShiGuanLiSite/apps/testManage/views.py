# -*- coding: utf-8 -*-
import apps
from django.shortcuts import render
from django.http import HttpResponse
from utils import                \
    traversalLevels,             \
    generateLevelsFromExcelFile, \
    createTestObject,            \
    getAllTestObjects,           \
    getAllTestLevelTypes,        \
    addLevelTypeToTestObject


from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt                                          
import os.path
from tables import modelTables, TestObjectTable, TestLevelTypeTable
from django_tables2 import RequestConfig

# Create your views here.
templatesDir = os.path.join(os.path.dirname(apps.__file__), 'templates')

@csrf_exempt 
@require_http_methods(['POST'])
def importXslx(request):
    f = request.FILES['file']
    generateLevelsFromExcelFile(
        f,
        leftTopLevelTypeCell     = request.POST['ltlt'],
        rightBottomLevelTypeCell = request.POST['ltrb'],
        leftTopLevelCell         = request.POST['llt'],
        rightBottomLevelCell     = request.POST['lrb'])
    resp = HttpResponse()
    resp.status = 200
    return resp

@csrf_exempt 
@require_http_methods(['POST'])
def newTestObject(request):
    name         = request.POST['name']
    description  = request.POST['description']
    testObject = createTestObject(title = name, description = description)
    resp = HttpResponse()
    resp.status = 200
    return resp

@csrf_exempt 
@require_http_methods(['POST'])
def addLevelTypeToTestObject(request):
    ltid = request.POST['lt']
    toid = requestPOST['to']
    resp = HttpResponse()
    resp.status = 200
    return resp

@csrf_exempt
def allTestObjects(request):
    theTable = TestObjectTable(getAllTestObjects())
    RequestConfig(request).configure(theTable)
#    context = {'testObjects': getAllTestObjects()}
    context = {'testObjectTable': theTable}
    return render(request, os.path.join(templatesDir, 'testObjects.html'), context)

@csrf_exempt
def allTestLevelTypes(request):
    theTable = TestLevelTypeTable(getAllTestLevelTypes())
    RequestConfig(request).configure(theTable)
    context = {'testLevelTypeTable': theTable}
    return render(request, os.path.join(templatesDir, 'testLevelTypes.html'), context)

def allTestcases(request):
    resp = HttpResponse()
    resp.status = 200
    return resp
