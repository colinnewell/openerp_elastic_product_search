# -*- coding: utf-8 -*-

from osv import fields, osv
from pyes import ES

# FIXME: where do I want to create the connection
# how do I deal with the connection settings?
conn = ES('127.0.0.1:9200')


class product_search(osv.osv):
    _name = "product.product"
    _inherit = "product.product"

    # FIXME: ought to figure out what fields we care about.
    _columns_to_search = ['description', 'description_sale',
                            'name']

    def write(self, cr, user, ids, vals, context=None):
        import pdb; pdb.set_trace()
        data = self._filter_values(vals)
        if len(data) > 0:
            #conn.update(vals, "openerp", "product", ids)
            pass
        return super(product_search, self).write(cr, user, ids, vals, context)

    def create(self, cr, user, vals, context=None):
        import pdb; pdb.set_trace()
        o = super(product_search, self).create(cr, user, vals, context)
        # o is the id
        # vals is the data structure
        data = self._filter_values(vals)
        conn.index(data, "openerp", "product", o)
        return o

    def _filter_values(self, vals):
        return dict([v for v in vals.items()
                            if v[0] in self._columns_to_search])


product_search()
