from odoo import models, fields, api, _
from odoo import http
from odoo.http import request
import werkzeug
from odoo.exceptions import except_orm, Warning, RedirectWarning

import logging
_logger = logging.getLogger(__name__)

class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    @api.depends('order_line.price_total')
    def _compute_amount_month(self):
        for order in self:
            order.order_line_month_ids = order.order_line.filtered(lambda x: x.product_id and x.product_id.uom_id.monthly_bool == True)
            order.order_line_fixed_ids = order.order_line.filtered(lambda x: x.product_id and x.product_id.uom_id.monthly_bool == False)
            amount_untaxed = amount_untaxed_fixed = amount_untaxed_month = amount_tax = amount_tax_month = amount_tax_fixed = 0.0 
            for line in order.order_line:
                if line.product_id and line.product_id.uom_id.monthly_bool == True:
                    amount_untaxed_month += line.price_subtotal
                    amount_tax_month += line.price_tax
                else:
                    amount_untaxed_fixed += line.price_subtotal
                    amount_tax_fixed += line.price_tax
            order.update({
                'amount_tax_fixed':amount_tax_fixed,
                'amount_month_total': amount_untaxed_month,
                'amount_fixed_total': amount_untaxed_fixed,
                'amount_month_total_tax': amount_untaxed_month + amount_tax_month,
                'amount_fixed_total_tax': amount_untaxed_fixed + amount_tax_fixed,
                'amount_tax_month':amount_tax_month
            })
            
            
            
            
            