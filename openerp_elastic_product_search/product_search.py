# -*- coding: utf-8 -*-

from osv import fields, osv
from pyes import ES
import tools

# this seems ugly but it kinda seems
# consistent with the way OpenERP is currently architected??
# TODO: perhaps add debug logging to indicate 
# which server we've connected to?
server = tools.config.get('elasticsearch', None)
conn = ES(server or '127.0.0.1:9200')

# TODO: at some point a lot of this code could probably be
# refactored out into a trait.


class product_search(osv.osv):
    _name = "product.product"
    _inherit = "product.product"

    # FIXME: ought to figure out what fields we care about.
    _columns_to_search = ['description', 'description_sale',
                            'name']

    def write(self, cr, user, ids, vals, context=None):
        data = self._filter_values(vals)
        if len(data) > 0:
            # TODO: perhaps add debug logging?
            for prod_id in ids:
                conn.update(data, "openerp_" + cr.dbname, "product", prod_id)
        return super(product_search, self).write(cr, user, ids, vals, context)

    def create(self, cr, user, vals, context=None):
        o = super(product_search, self).create(cr, user, vals, context)
        data = self._filter_values(vals)
        # FIXME how safe is the dbname for this purpose?
        conn.index(data, "openerp_" + cr.dbname, "product", o)
        return o

    def _filter_values(self, vals):
        return dict([v for v in vals.items()
                            if v[0] in self._columns_to_search])


product_search()
