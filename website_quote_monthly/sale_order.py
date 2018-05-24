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


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    show_description_on_quotation = fields.Boolean('Q', help='Show this product description in online quotation.')


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    website_description_quotation = fields.Html(string='Website Description for Quotation')

    @api.multi
    def edit_website_description_quotation(self):
        return {
            'name': 'Go to website',
            'res_model': 'ir.actions.act_url',
            'type': 'ir.actions.act_url',
            'url': '/shop/product/%s/quotation/' %self.id,
            'target': 'self',
        }


class Controller(http.Controller):

    @http.route(['/shop/product/<model("product.template"):product>/quotation/'], type='http', auth='user', website=True)
    def website_description_quotation(self, product, **post):
        return request.render('website_quote_monthly.product_description_quotation', {'product': product})
