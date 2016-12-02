# -*- coding: utf-8 -*-
from models import *
JsonConvertors = {
    TestObject: (lambda x: {
#        'uri': uriPrefix + '/' + unicode(x.id), 
        'id': unicode(x.id), 
        'title': x.title, 
        'description': x.description}),
}

def test():
    from prettyprint import pp
    pp(map(JsonConvertors[TestObject], TestObject.objects.all()))
if __name__ == '__main__':
    test()
    
