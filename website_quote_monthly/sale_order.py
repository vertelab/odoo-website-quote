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
    
    @api.one
    @api.depends('order_line')
    def _compute_amount_month(self):
        month = self.env.ref('website_quote_template.product_uom_month')
        self.order_line_month_ids = self.order_line.filtered(lambda x: x.product_id and x.product_id.uom_id == month)
        self.order_line_fixed_ids = self.order_line.filtered(lambda x: x.product_id and x.product_id.uom_id != month)
    
    amount_month_total = fields.Float(compute='_compute_amount_month')
    amount_fixed_total = fields.Float(compute='_compute_amount_month')
    order_line_month_ids = fields.One2many('sale.order.line', compute='_compute_amount_month')
    order_line_fixed_ids = fields.One2many('sale.order.line', compute='_compute_amount_month')
    
 