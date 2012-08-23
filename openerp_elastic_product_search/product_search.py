# -*- coding: utf-8 -*-

from osv import fields, osv
from pyes import ES
import pyes.exceptions
import tools

# this seems ugly but it kinda seems
# consistent with the way OpenERP is currently architected??
# TODO: perhaps add debug logging to indicate
# which server we've connected to?
server = tools.config.get('elasticsearch', None)
conn = ES(server or '127.0.0.1:9200')

# TODO: at some point a lot of this code could probably be
# refactored out into a trait.

# FIXME: I need to do something to ensure the index is created
# I probably also want to do an index instead of an update
# if the object doesn't exist yet too.


class product_search(osv.osv):
    _name = "product.product"
    _inherit = "product.product"

    # FIXME: ought to figure out what fields we care about.
    _columns_to_search = ['description', 'description_sale',
                            'name']

    def write(self, cr, user, ids, vals, context=None):
        success = super(product_search, self).write(cr, user, ids, vals, context)
        if success:
            data = self._filter_values(vals)
            if len(data) > 0:
                for prod_id in ids:
                    try:
                        conn.update(data, "openerp_" + cr.dbname, "product", prod_id)
                    except pyes.exceptions.IndexMissingException:
                        # may as well just index what we have.
                        conn.index(data, "openerp_" + cr.dbname, "product", prod_id)
                    except pyes.exceptions.NotFoundException:
                        # may as well just index what we have.
                        conn.index(data, "openerp_" + cr.dbname, "product", prod_id)
                    
        return success

    def create(self, cr, user, vals, context=None):
        o = super(product_search, self).create(cr, user, vals, context)
        if o:
            data = self._filter_values(vals)
            # FIXME how safe is the dbname for this purpose?
            conn.index(data, "openerp_" + cr.dbname, "product", o)
        return o

    def _filter_values(self, vals):
        # FIXME: need to filter out nulls
        # also need to look at stuff that does _source stuff.
        return dict([v for v in vals.items()
                            if v[0] in self._columns_to_search])

    def reindex(self, cr, uid):
        prod_ids = self.search(cr, uid, [])
        # FIXME: is reading all the products in one go a good idea?
        # perhaps break it into chunks?
        prods = self.read(cr, uid, prod_ids)
        # FIXME: also think about making use of the elastic search
        # bulk operations
        for product in prods:
            data = self._filter_values(product)
            conn.index(data, "openerp_" + cr.dbname, "product", product['id'])


product_search()
