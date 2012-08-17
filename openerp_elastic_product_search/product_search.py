# -*- coding: utf-8 -*-

from osv import fields, osv
from pyes import ES

# FIXME: where do I want to create the connection
# how do I deal with the connection settings?
conn = ES('127.0.0.1:9200')

class product_search(osv.osv):
    _name = "product.product"
    _inherit = "product.product"

    def write(self, cr, user, ids, vals, context=None):
        import pdb; pdb.set_trace()
        #conn.update(vals, "openerp", "product", ids)
        super(product_search, self).write(cr, user, ids, vals, context)

    def create(self, cr, user, vals, context=None):
        import pdb; pdb.set_trace()
        #conn.index(vals, "openerp", "product", ids)
        super(product_search, self).create(cr, user, vals, context)


product_search()


