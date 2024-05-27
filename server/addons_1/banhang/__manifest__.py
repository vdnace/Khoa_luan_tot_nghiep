# -*- coding: utf-8 -*-
{
    'name': "banhang",
    'summary': """ban hang""",
    'description': """bán hàng""",
    'author': "Nhat",
    'website': "hhttps://www.google.com.vn/?hl=vi",
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': [
        'sale', 'product'
    ],
    'data': [
        'views/farming_product.xml',
        'views/farming_purchase.xml',
        'views/farming_inventory.xml',
    ],
    # 'qweb': ['static/src/xml/*.xml'],
    'installable': True,
    'application': True,
}