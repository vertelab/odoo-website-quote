from odoo import api, fields, tools, models, _
from odoo.exceptions import UserError, ValidationError


class ProductCategoryBool(models.Model):
    _inherit = 'uom.category'

    monthly_bool = fields.Boolean("Exist inside monthly sums")
    