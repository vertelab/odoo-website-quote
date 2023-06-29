from odoo import api, fields, tools, models, _
from odoo.exceptions import UserError, ValidationError


class UoM_add_field(models.Model):
    _inherit = 'uom.uom'

    monthly_bool = fields.Boolean("Exist inside monthly sums")
    
    def _action_confirm(self):
    
        res = super(UoM_add_field,self)._action_confirm()

        return res
    
    