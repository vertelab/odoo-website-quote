# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models
from odoo.tools.translate import html_translate


class SaleOrderTemplate(models.Model):
    _inherit = "sale.order.template"

    website_description_footer = fields.Html('Website Description Footer', sanitize_attributes=False, translate=html_translate)
    terms_page = fields.Char('Terms Page')
    
    header_template_description = fields.Html('Website Description Dynamical Header', sanitize_attributes=False, translate=html_translate, default="<p></p>") ####### WHAT IM GOING TO USE TO CALL THE T RAW WITH
    footer_template_description = fields.Html('Website Description Dynamical Footer', sanitize_attributes=False, translate=html_translate, default="<p></p>") ####### WHAT IM GOING TO USE TO CALL THE T RAW WITH


