import logging
from lxml import etree

from odoo import api, fields, models, _
from odoo.tools.translate import html_translate
from odoo.addons.base.models.ir_qweb import QWebException

_logger = logging.getLogger(__name__)

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    header_template_description = fields.Html(
        'Website Description Header', sanitize_attributes=False, translate=html_translate, default="<p></p>")

    footer_template_description = fields.Html(
        'Website Description Footer', sanitize_attributes=False, translate=html_translate, default="<p></p>")

    website_description = fields.Html(
        'Website Description', sanitize_attributes=False, translate=html_translate, default="<p></p>")


    @api.onchange('sale_order_template_id')
    def _onchange_sale_order_template_id(self):
        ret = super(SaleOrder, self)._onchange_sale_order_template_id()
        if self.sale_order_template_id:
            template = self.sale_order_template_id.with_context(lang=self.partner_id.lang)
            self.website_description = template.website_description
            self.header_template_description = template.header_template_description
            self.footer_template_description = template.footer_template_description
        return ret

    def render_template_field(self, template_html, template_type="template"):
        if not template_html:
            return "<p></p>"

        values = {'sale_order': self}
        template = str(template_html).replace("<br>", "<br/>")

        try:
            parsed_template = etree.fromstring(f"<div>{template}</div>")
            rendered = self.env["ir.qweb"]._render(parsed_template, values)
            return rendered
        except etree.XMLSyntaxError as e:
            _logger.error(f"XML parse error in {template_type}: {e}")
            return f"<p>Error: Malformed HTML in {template_type}</p>"
        except QWebException as e:
            _logger.error(f"QWeb render error in {template_type}: {e}")
            return f"<p>Error: QWeb rendering failed - {e}</p>"
        except Exception as e:
            _logger.error(f"Unknown error rendering {template_type}: {e}")
            return f"<p>Error: {e}</p>"
        
