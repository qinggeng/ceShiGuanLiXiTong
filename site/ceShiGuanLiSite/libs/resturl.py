# -*- coding: utf-8 -*-
"""
这个小框架用于解决restful api中, uri的层级处理问题。
在restful架构中，uri至关重要。一般而言， uri以一种层次性的方式来体现：
/[objectlist]/[objectid]
objreclist ::= type | propName
这实际上形成了一种递进关系：
# 获得object
# 获得object-list
# 获得下一个object

其中， object-list可能是以类型或者属性来表达的。

这种uri的风格和对象的访问很类似:
objects().filter(id = id).props.filter(id = id)

所以对uri的处理也就变成了类似的链条:
# uri由若干部分组成, 
# 每部分对应一个处理函数, 
# 这个处理函数的返回值作为下部分的处理函数的输入
# uri处理的最终结果是这个处理链条上的最后一个函数的输出

目前, django的url dispatcher这个机制并不能满足上述的处理结构, 
因此才会有这个小框架。

"""

from inspect import getargspec
from prettyprint import pp
import re

kPattern = 'pattern'
kChildren = 'children'
kHandler = 'handler'

def uriProcessingChain(uri, chain, prevResult = None):
    uri = canonicalUri(uri)
    for head in chain:
        uriPattern = re.compile(head[kPattern])
        m = uriPattern.match(uri)
        if None == m or m.pos != 0:
            continue
        handler = head[kHandler]
        try:
            if None == prevResult:
                result = handler(*(list(m.groups())))
            else:
                result = handler(*([prevResult] + list(m.groups())))
            if kChildren in head:
                return uriProcessingChain(uri[m.end():], head[kChildren], result)
            else:
                return result
        except Exception, e:
            raise

def canonicalUri(uri):
    if uri[0] == '/':
        uri = uri[1:]
    if uri[-1] == '/':
        uri = uri[:-1]
    return uri


if __name__ == '__main__':
    def genTestStup():
        def getObjects():
            return [
                {
                    'id': 1,
                },
            ]

        def getObject(objects, objectId):
            return filter(lambda x: x['id'] == int(objectId), objects)[0]

        return [
            {
                'pattern': 'objects',
                'handler': getObjects,
                'children': 
                [
                    {
                        'pattern': '(\d+)',
                        'handler': getObject
                    }
                ]
            },
        ]
    uri = ur"objects/1/"
    uri = ur"objects/1"
    uri = ur"/objects/1"
    #uri = /objects/1/
    #uri = /objects/1
    print uriProcessingChain(uri, genTestStup())
    pass
