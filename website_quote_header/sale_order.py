# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models
from odoo.tools.translate import html_translate
import logging
_logger = logging.getLogger(__name__)

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    website_description_footer = fields.Html('Website Description Footer', sanitize_attributes=False, translate=html_translate)

    # ~ @api.onchange('sale_order_template_id')
    def onchange_sale_order_template_id(self):
        ret = super(SaleOrder, self).onchange_sale_order_template_id()
        if self.sale_order_template_id:
            template = self.sale_order_template_id.with_context(lang=self.partner_id.lang)
            self.website_description_footer = template.website_description_footer
            self.terms_page = template.terms_page
        return ret
        
        
    terms_page = fields.Char('Terms Page')
