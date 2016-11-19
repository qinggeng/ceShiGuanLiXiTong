# -*- coding: utf-8 -*-
from django.http import HttpResponse
import json
def jsonResp(func):
    def makeResp(*args, **kwargs):
        obj = func(*args, **kwargs)
        return HttpResponse(json.dumps(obj), 'application/json')
    return makeResp
