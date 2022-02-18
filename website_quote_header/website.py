# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models
from odoo.tools.translate import html_translate
import logging
_logger = logging.getLogger(__name__)
from odoo.http import request
from lxml import etree

class Website(models.Model):
    _inherit = 'website'

    def render_from_field(self,template,website_description,value):
        view_id = self.env['ir.ui.view'].get_view_id(template)
        template = self.env['ir.ui.view'].sudo()._read_template(view_id)
        template = template.replace('<span>\n','<span>\n'+website_description)
        view = etree.fromstring(template)
        res = self.env['ir.qweb']._render(view,{'sale_order':value})
        return res


# ~ <!-- addition -->
# ~ <!--
    # ~ <div t-raw="request.env['website'].render_from_field('website_quote_header.website_description',sale_order.website_description,sale_order)">
# ~ -->
# ~ <!-- addition -->   
