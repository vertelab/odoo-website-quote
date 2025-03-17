# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models
from odoo.tools.translate import html_translate
import logging
_logger = logging.getLogger(__name__)
from odoo.http import request
from lxml import etree

# class Website(models.Model):
#     _inherit = 'website'
#
#     @api.model
#     def render_from_field(self, template, website_description=None,value=None):
#
#         view_id = self.env['ir.ui.view'].get_view_id(template)
#         template = self.env['ir.ui.view'].sudo()._read_template(view_id)
#         if website_description:
#             # ~ template = template.replace('<span>\n','<span>\n'+website_description)
#             template = template.replace('</span>',website_description+'</span>')
#             template = template.replace('<br>','<br/>')#_render can't hande <br>
#             #template = template.replace('<br/>','')#_render can't hande </br>
#         view = etree.fromstring(template)
#         value_dict = {}
#         if value:
#             value_dict = {'sale_order':value}
#             res = self.env['ir.qweb']._render(view,value_dict)
#         else:
#             try:
#                 res = self.env['ir.qweb']._render(view)
#             except:
#                 return
#
#         return res

