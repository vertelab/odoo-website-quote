import logging
from lxml import etree

from odoo import api, fields, models, _
from odoo.tools.translate import html_translate
from odoo.addons.base.models.ir_qweb import QWebException
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    header_template_description = fields.Html(
        'Website Description Header', sanitize_attributes=False, translate=html_translate, default="<p></p>")
    website_description_footer = fields.Html(
        'Website Description', sanitize_attributes=False, translate=html_translate, default="<p></p>")
    footer_template_description = fields.Html(
        'Website Description Footer', sanitize_attributes=False, translate=html_translate, default="<p></p>")   
    header_template_description_rendered = fields.Html('Website Description Dynamical Header', sanitize_attributes=False, compute="compute_template_description_rendered", store=True)
    website_description_footer_rendered = fields.Html('Website Description Dynamical', sanitize_attributes=False, compute="compute_template_description_rendered", store=True)   
    footer_template_description_rendered = fields.Html('Website Description Dynamical Footer', sanitize_attributes=False, compute="compute_template_description_rendered", store=True)   
    terms_page = fields.Char('Terms Page')

    @api.onchange('sale_order_template_id')
    def _onchange_sale_order_template_id(self):
        ret = super(SaleOrder, self)._onchange_sale_order_template_id()
        if self.sale_order_template_id:
            template = self.sale_order_template_id.with_context(lang=self.partner_id.lang)
            self.website_description_footer = template.website_description_footer
            self.terms_page = template.terms_page
            self.header_template_description = template.header_template_description
            self.footer_template_description = template.footer_template_description
        return ret
        
    @api.depends("header_template_description","footer_template_description")
    def compute_template_description_rendered(self):
        for record in self:
            if record.header_template_description:
                record.header_template_description_rendered = self.template_description_rendererer(record,record.header_template_description,"header")
            else:
                record.header_template_description_rendered = "<p></p>"

            if record.website_description_footer:
                record.website_description_footer_rendered = self.template_description_rendererer(record,record.website_description_footer,"website description")
            else:
                record.website_description_footer_rendered = "<p></p>"
                
            if record.footer_template_description:
                record.footer_template_description_rendered = self.template_description_rendererer(record,record.footer_template_description,"footer")
            else:
                record.footer_template_description_rendered = "<p></p>"
    
    def template_description_rendererer(self,record,template,template_type):
        values = {'sale_order':record}
        template = str(template).replace("<br>","<br/>")
        try:
            parsed_template = etree.fromstring(template)
            renderd_template = self.env["ir.qweb"]._render(parsed_template,values)
        except etree.XMLSyntaxError as e:
            _logger.error(f"Got this error while trying to parse the sale order template for the {template_type}: {e}. The qweb/html is probably malformed for the template {record.sale_order_template_id.name}.")
            renderd_template = f"<p>Got this error while trying to parse the sale order template for the {template_type}: {e}. The qweb/html is probably malformed for the template {record.sale_order_template_id.name}.</p>"
        except QWebException as e:
            _logger.error(f"Got this error while trying to render the sale order template for the {template_type} with Qweb: {e}. A field is most likely missing in order for the Qweb rendering to work for the template {record.sale_order_template_id.name}.")
            renderd_template = f"<p>Got this error while trying to render the sale order template for the {template_type} with Qweb: {e}. A field is most likely missing in order for the Qweb rendering to work for the template {record.sale_order_template_id.name}.</p>"
        except Exception as e:
            _logger.error(f"Got this unknow error while trying to render the sale order template for the {template_type} with Qweb: {e}")
            renderd_template = f"<p>Got this unknow error while trying to render the sale order template for the {template_type} with Qweb: {e}</p>"
        return renderd_template
