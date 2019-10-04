# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models
from odoo.tools.translate import html_translate


class SaleOrderTemplate(models.Model):
    _inherit = "sale.order.template"

    website_description_footer = fields.Html('Website Description Footer', translate=html_translate, sanitize_attributes=False)
    terms_page = fields.Char('Terms Page')


