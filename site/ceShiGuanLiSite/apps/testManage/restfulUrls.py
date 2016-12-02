#-*- encoding: utf-8 -*-

kPattern = 'pattern'
kHandler = 'handler'
kChildren = 'children'

urlChain = [
    {
        kPattern: 'testObjects',
        kHandler: None,
    }
]

def getObjectByRequest(request):
    path = request.path()    
    return uriProcessingChain(path, urlChain)

