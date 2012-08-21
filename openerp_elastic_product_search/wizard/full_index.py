from osv import osv


class search_full_index(osv.osv_memory):

    _name = 'openerp_elastic_product_search.full_index'
    _description = 'Elastic Search Index'

    def index_data(self, cr, uid, ids, context=None):
        products = self.pool.get('product.product')
        import pdb; pdb.set_trace()
        return { 'type': 'ir.actions.act_window_close' }


search_full_index()

