# -*- coding: utf-8 -*-

{
    'name': 'Elastic Search for Products',
    'version': '0.01',
    'category': 'Search',
    'description': """
    This hooks up the products into elastic search.

    """,
    'author': 'Colin Newell',
    'website': 'http://colinnewell.wordpress.com',
    'depends': [ 'purchase', 'sale'],
    'init_xml': [],
    'update_xml': [
        'wizard/full_index.xml'
    ],
    'demo_xml': [],
    'test': [],
    'installable': True,
    'active': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
