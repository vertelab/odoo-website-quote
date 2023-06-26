import logging, datetime
from odoo import api, fields, models
from odoo.tools.translate import _
from collections import Iterable
import json
from datetime import date
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

class ContractContract(models.Model):
    _name = "contract.contract"
    _inherit = [
        'contract.contract',
        'mail.render.mixin'
    ]
    """
    Overrides function in contract.contract, 
    so that we can use jinja when you create an invoice from a contract
    """
    
    def _prepare_recurring_invoices_values(self, date_ref=False):
        invoices_values = super()._prepare_recurring_invoices_values(date_ref)
        invoices_values_json=""
        try:

            invoices_values_json = json.dumps(invoices_values, cls=DateEncoder)
        except TypeError:
            raise UserError('At least one of the values in the form can not be parsed with '\
                            'json.stringify check "website_quote_jinja_description" for more')

        invoices_values_json = self._render_template_jinja(

            invoices_values_json,
            "contract.line", 
            self.contract_line_fixed_ids.ids
            )
        
        invoices_values_json = invoices_values_json[self.contract_line_fixed_ids.id]

        invoices_values = json.loads(invoices_values_json, 
            object_hook=DateEncoder.date_decoder)        
        
        return invoices_values

"""
JSON stringify does not work on the original date format, 
so we convert it to a date format that works for json stringify, 
and then convers it back
"""
class DateEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, date):
            return obj.isoformat()  
        return super().default(obj)

    @staticmethod
    def date_decoder(dct):
        for key, value in dct.items():
            if isinstance(value, str) and value.startswith("DATE:"):
                date_string = value.split("DATE:")[1]
                dct[key] = datetime.datetime.strptime(date_string, "%Y-%m-%d").date()
        return dct
