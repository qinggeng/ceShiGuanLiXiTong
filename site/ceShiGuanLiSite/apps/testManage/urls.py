# -*- coding: utf-8 -*-
from django.conf.urls import include, url
import views
import apiViews
import restfulUrls

"""
testObjectsUrl = [
]
"""
urlpatterns = [
    url('^import-xlsx$', views.importXslx),
    url('^new-test-object$', views.newTestObject),
    url('^allTestCases$', views.allTestcases),
    url('^allTestObjects$', views.allTestObjects),
    url('^allTestLevelTypes$', views.allTestLevelTypes),
    url('^api/v0/(.*)$', apiViews.apiRoot),
#    url('^api/v0/testObjects$', apiViews.testObjects),
#    url('^api/v0/testObjects/([^/]+)$', apiViews.testObject),
#    url('^api/v0/testObjects/([^/]+)/categories$', apiViews.testObjectCategories),
#    url('^api/v0/testCategories/([^/]+)$', apiViews.testCategories),
#    url('^api/v0/testCategories/([^/]+)/([^/]+)$', apiViews.testCategoryManage),
]
