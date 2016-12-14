# -*- coding: utf-8 -*-
kPattern  = 'pattern'
kChildren = 'children'
kHandler  = 'handler'

categoriesNode = {
            kPattern  : 'categories',
            kHandler  : getTestObjectCategories,
            kChildren : []},
            ],}

testObjectNode = {
        kPattern  : '[0-9a-f-]{36}',
        kHandler  : getTestObjectById,
        kChildren : [categoriesNode],
}

testObjectListNode = {
    kPattern: 'testObjects',
    kHandler: testObjectListing,
    kChildren: [testObjectNode]}

uriChain = [testObjectListNode]
