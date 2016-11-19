# -*- coding: utf-8 -*-
from openpyxl import load_workbook
from libs.xlsxInterface import getLevelTypes, travesalLevels
import models
from prettyprint import pp
from functools import partial
from django.db import transaction

def generateLevels(levelDict, levelTypes, cellAndValues):
    currentDict = levelDict
    parentLevel = None
    for index, (cell, value) in zip(range(len(cellAndValues)), cellAndValues):
        levelType = levelTypes[index]
        if value not in currentDict:
            currentDict[value] = {}
            level = models.Level()
            level.title = value
            currentDict[value]['levelObject'] = level
            if parentLevel != None:
                level.parent = parentLevel
            else:
                pass
            level.levelType = levelType
            level.save()
            parentLevel = level
        else:
            parentLevel = currentDict[value]['levelObject']
        currentDict = currentDict[value]
    pass

@transaction.atomic
def generateLevelsFromExcelFile(xlsxFile, **args):
    ltlt = args.pop('leftTopLevelTypeCell')
    ltrb = args.pop('rightBottomLevelTypeCell')
    lt = args.pop('leftTopLevelCell')
    rb = args.pop('rightBottomLevelCell')
    ws = load_workbook(xlsxFile, read_only = False).worksheets[0]
    levelTypes = getLevelTypes(ws, ltlt, ltrb)
    levelTypes = map(lambda x: models.LevelType(x), levelTypes)
    levelDict = {}
    travesalLevels(ws, lt, rb, partial(generateLevels, levelDict, levelTypes))
    for levelType in levelTypes:
        levelType.save()
        pass
    return levelDict

@transaction.atomic
def test():
#    levelDict = generateLevelsFromExcelFile('test.xlsx',
#        leftTopLevelTypeCell = 'B6',
#        rightBottomLevelTypeCell = 'D7',
#        leftTopLevelCell = 'B8',
#        rightBottomLevelCell = 'D419')
#    levels = models.Level.objects.all()
    traversalLevels()
    pass

@transaction.atomic
def clearAll():
    map(lambda x: x.delete(), models.Level.objects.all())
    map(lambda x: x.delete(), models.LevelType.objects.all())

def traversalLevels():
    roots = models.Level.objects.filter(parent = None)
    tableTemplate = u"""
<table>
    <tbody>
    {content}
    </tbody>
</table>
    """
    content = u""
    for level in roots:
        content += u"<TR>" + makeLevelsTable(level)[1]
    print tableTemplate.format(content = content)

def makeLevelsTable(level):
    children = models.Level.objects.filter(parent = level)
    rowSpan = len(children)
    if rowSpan == 0:
        return (1, u"<td>{title}</td></tr>\n".format(title = level.title))
    rowSpan = 0
    ret = u"<TD rowspan='{{rowspan}}'>{title}</TD>".format(title = level.title)
    for i, child in zip(range(len(children)), children):
        childRowCount, childRows = makeLevelsTable(child)
        rowSpan += childRowCount
        if i == 0:
            ret += childRows
        else:
            ret += u"<tr>" + childRows
    ret = ret.format(rowspan = rowSpan)
    return (rowSpan, ret)

def createTestObject(**args):
    title = args.pop('title')
    description = args.pop('description', u'')
    testObject = models.TestObject.objects.create()
    testObject.title = title
    testObject.description = description
    testObject.save()
    return testObject

def getAllTestObjects():
    return models.TestObject.objects.all()

def getAllTestLevelTypes():
    return models.LevelType.objects.all()

def addLevelTypeToTestObject(levelTypeId, testObjectId):
    try:
        lt = models.LevelType.objects.get(id = levelTypeId)
        to = models.TestObject.objects.get(id = testObjectId)
        to.add(lt)
    except Exception, e:
        print e
        raise
