from odoo import fields, models, _

class SaleOrderBool(models.TransientModel):
    _inherit = 'res.config.settings'
    
    sale_order_bool = fields.Boolean(string='Sale order bool test')

