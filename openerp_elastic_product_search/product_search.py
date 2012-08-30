# -*- coding: utf-8 -*-

from osv import fields, osv
from pyes import ES
import pyes.exceptions
import tools
import logging

_logger = logging.getLogger(__name__)

server = tools.config.get('elasticsearch', '127.0.0.1:9200')
conn = ES(server)
_logger.info('Connecting to ElasticSearch server %s' % server)

# TODO: at some point a lot of this code could probably be
# refactored out into a trait.
# FIXME: it would be ideal if we could configure the 
# classes and fields we're interested in.


class product_search(osv.osv):
    _name = "product.product"
    _inherit = "product.product"

    # FIXME: ought to figure out what fields we care about.
    _columns_to_search = ['description', 'description_sale',
                            'name']

    def write(self, cr, user, ids, vals, context=None):
        success = super(product_search, self).write(cr, user, ids,
                                                    vals, context)
        if success and ids:
            data = self._filter_values(vals)
            if len(data) > 0:
                if isinstance(ids, (int, long)):
                    ids = [ids]
                index = self._index_name(cr)
                for prod_id in ids:
                    try:
                        conn.update(data, index, "product", prod_id)
                    except pyes.exceptions.IndexMissingException:
                        # may as well just index what we have.
                        # NOTE: this isn't the only time we might create
                        # the index, it's just the only time we explicitly
                        # notice we are.
                        _logger.info('Creating index %s in ElasticSearch'
                                        % index)
                        conn.index(data, index, "product", prod_id)
                    except pyes.exceptions.NotFoundException:
                        # may as well just index what we have.
                        _logger.debug('Product %d not found in index'
                                        % prod_id)
                        conn.index(data, index, "product", prod_id)

        return success

    def create(self, cr, user, vals, context=None):
        o = super(product_search, self).create(cr, user, vals, context)
        if o:
            data = self._filter_values(vals)
            if len(data) > 0:
                index = self._index_name(cr)
                conn.index(data, index, "product", o)
        return o

    def unlink(self, cr, uid, ids, context=None):
        success = super(product_search, self).unlink(cr, uid, ids, context)
        if success and ids:
            if isinstance(ids, (int, long)):
                ids = [ids]
            index = self._index_name(cr)
            for prod_id in ids:
                conn.delete(index, "product", prod_id)
        return success

    def _filter_values(self, vals):
        return dict([v for v in vals.items()
                            if v[0] in self._columns_to_search])

    def _index_name(self, cr):
        # FIXME how safe is the dbname for this purpose?
        index = "openerp_" + cr.dbname
        return index

    def reindex(self, cr, uid):
        prod_ids = self.search(cr, uid, [])
        # FIXME: is reading all the products in one go a good idea?
        # perhaps break it into chunks?
        prods = self.read(cr, uid, prod_ids)
        # FIXME: also think about making use of the elastic search
        # bulk operations
        index = self._index_name(cr)
        for product in prods:
            data = self._filter_values(product)
            if len(data) > 0:
                _logger.debug("%s: Indexing product %d" % (index, product['id']))
                _logger.debug(data)
                conn.index(data, index, "product", product['id'])


product_search()
