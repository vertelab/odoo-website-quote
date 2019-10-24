# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo, Open Source Enterprise Management Solution, third party addon
#    Copyright (C) 2018 Vertel AB (<http://vertel.se>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from odoo import models, fields, api, _
from odoo import http
from odoo.http import request
import werkzeug
from odoo.exceptions import except_orm, Warning, RedirectWarning

import logging
_logger = logging.getLogger(__name__)

class SaleOrder(models.Model):
    _inherit='sale.order'
    
    @api.depends('order_line.price_total')
    def _compute_amount_month(self):
        month = self.env.ref('website_quote_template.product_uom_month')
        for order in self:
            order.order_line_month_ids = order.order_line.filtered(lambda x: x.product_id and x.product_id.uom_id == month)
            order.order_line_fixed_ids = order.order_line.filtered(lambda x: x.product_id and x.product_id.uom_id != month)
            amount_untaxed = amount_tax = 0.0   
            for line in order.order_line:
                if line.product_id and line.product_id.uom_id == month:
                    amount_untaxed_month += line.price_subtotal
                    amount_tax_month += line.price_tax
                else:
                    amount_untaxed_fixed += line.price_subtotal
                    amount_tax_fixed += line.price_tax
            order.update({
                'amount_month_total': amount_untaxed_month,
                'amount_fixed_total': amount_untaxed_fixed,
            })
        
    
    amount_month_total = fields.Float(compute='_compute_amount_month')
    amount_fixed_total = fields.Float(compute='_compute_amount_month')
    order_line_month_ids = fields.One2many('sale.order.line', compute='_compute_amount_month')
    order_line_fixed_ids = fields.One2many('sale.order.line', compute='_compute_amount_month')
    
 