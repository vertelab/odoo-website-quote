from odoo import api, fields, tools, models, _
from odoo.exceptions import UserError, ValidationError

import logging
_logger = logging.getLogger(__name__)

class SaleOrdersSettings(models.Model):
    _inherit = "sale.order"
    
    pricelist_id = fields.Many2one()


    def _prepare_contract_vals(self, line):
        

        resdict = {
            'payment_term_id': self.payment_term_id.id,
            'pricelist_id': self.pricelist_id.id,
            'client_order_ref': self.client_order_ref,
            'fiscal_position_id': self.fiscal_position_id.id,
        }
        
        res = super(SaleOrdersSettings, self)._prepare_contract_vals(line)
        
        for key,value in resdict.items():
            res[key]=value
            
        return res
    
