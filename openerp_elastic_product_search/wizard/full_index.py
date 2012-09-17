from osv import osv


class search_full_index(osv.osv_memory):

    _name = 'openerp_elastic_product_search.full_index'
    _description = 'Elastic Search Index'

    def index_data(self, cr, uid, ids, context=None):
        # FIXME: it would be neat to detect all
        # the classes that have full text search.
        products = self.pool.get('product.product')
        products.reindex(cr, uid)
        templates = self.pool.get('product.template')
        templates.reindex(cr, uid)
        categories = self.pool.get('product.category')
        categories.reindex(cr, uid)
        return { 'type': 'ir.actions.act_window_close' }


search_full_index()

