

from odoo import api, fields, models
from odoo.tools.translate import html_translate

class SaleOrderTemplate(models.Model):
    _inherit = "sale.order.template"

    website_description = fields.Html(
        'Website Description', sanitize_attributes=False, translate=html_translate, default="<p></p>")
    header_template_description = fields.Html(
        'Website Description Dynamical Header',
        sanitize_attributes=False, translate=html_translate, default="<p></p>")
    footer_template_description = fields.Html(
        'Website Description Dynamical Footer',
        sanitize_attributes=False, translate=html_translate, default="<p></p>")
