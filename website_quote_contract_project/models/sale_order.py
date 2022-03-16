# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models
from odoo.tools.translate import html_translate
import logging
_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = 'sale.order'
    sale_created_project_id = fields.Many2one(comodel_name="project.project", string="Uppdrag") ############ Project created by a line is set to this one

    
class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'  

    def _timesheet_create_task_prepare_values(self, project):
            res = super(SaleOrderLine, self)._timesheet_create_task_prepare_values(project)
            self.order_id.sale_created_project_id = project
            return res
