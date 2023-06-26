from odoo import api, fields, tools, models, _
from odoo.exceptions import UserError, ValidationError

import logging
_logger = logging.getLogger(__name__)

class ContractExtraInvoiceFields(models.Model):
    _inherit = "contract.contract"

    client_order_ref = fields.Char(string='Customer Reference', copy=False, store=True)
    