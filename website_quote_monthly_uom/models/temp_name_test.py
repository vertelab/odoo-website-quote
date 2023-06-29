from odoo import fields, models, _

class SaleOrderBool(models.Model):
    _inherit = 'uom.category'
    
    sale_order_bool = fields.Boolean(string='Exist inside monthly sums')
    
    # def _action_confirm(self):
    
    #     res = super(SaleOrderBool,self)._action_confirm()

    #     return res