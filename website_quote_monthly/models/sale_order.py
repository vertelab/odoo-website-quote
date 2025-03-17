# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo, Open Source Enterprise Management Solution, third party addon
#    Copyright (C) 2018 Vertel AB (<http://vertel.se>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from odoo import models, fields, api, _
from odoo import http
from odoo.http import request
import werkzeug
from odoo.exceptions import  UserError

import logging

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.depends('order_line.price_total')
    def _compute_amount_month(self):
        month = self.env.ref('website_quote_monthly.product_uom_month')
        for order in self:
            amount_untaxed = amount_untaxed_fixed = amount_untaxed_month = amount_tax = \
                amount_tax_month = amount_tax_fixed = 0.0
            for line in order.order_line:
                if line.product_id and line.product_id.uom_id == month:
                    amount_untaxed_month += line.price_subtotal
                    amount_tax_month += line.price_tax
                else:
                    amount_untaxed_fixed += line.price_subtotal
                    amount_tax_fixed += line.price_tax
            order.update({
                'amount_tax_fixed': amount_tax_fixed,
                'amount_month_total': amount_untaxed_month,
                'amount_fixed_total': amount_untaxed_fixed,
                'amount_month_total_tax': amount_untaxed_month + amount_tax_month,
                'amount_fixed_total_tax': amount_untaxed_fixed + amount_tax_fixed,
                'amount_tax_month': amount_tax_month
            })

    amount_tax_fixed = fields.Monetary(compute='_compute_amount_month')
    amount_tax_month = fields.Monetary(compute='_compute_amount_month')
    amount_month_total = fields.Monetary(compute='_compute_amount_month')
    amount_month_total_tax = fields.Monetary(compute='_compute_amount_month')
    amount_fixed_total = fields.Monetary(compute='_compute_amount_month')
    amount_fixed_total_tax = fields.Monetary(compute='_compute_amount_month')

    def _find_order_line_sequence(self, sequence):
        return self.order_line.filtered(lambda line: line.sequence == sequence and line.display_type == 'line_section')

    @api.depends('order_line')
    def _month_uom_order_lines_ids(self):
        month = self.env.ref('website_quote_monthly.product_uom_month')
        for order in self:
            line_ids = self.env['sale.order.line']

            for order_line in order.order_line:
                if (not order_line.display_type and order_line.product_id.uom_id == month) or \
                        (order_line.display_type and order_line.name.startswith('Monthly:')):
                    line_ids += order_line
                    # if self._find_order_line_sequence(order_line.sequence - 1):
                    #     line_ids += self._find_order_line_sequence(order_line.sequence - 1)

            order.order_line_month_ids = line_ids.sorted(key=lambda line: line.sequence)

    @api.depends('order_line')
    def _fixed_uom_order_lines_ids(self):
        month = self.env.ref('website_quote_monthly.product_uom_month')
        for order in self:
            line_ids = self.env['sale.order.line']

            for order_line in order.order_line:
                if (not order_line.display_type and order_line.product_id.uom_id != month) or \
                        (order_line.display_type and not order_line.name.startswith('Monthly:')):
                    line_ids += order_line
                    # if self._find_order_line_sequence(order_line.sequence - 1):
                    #     line_ids += self._find_order_line_sequence(order_line.sequence - 1)

            order.order_line_fixed_ids = line_ids.sorted(key=lambda line: line.sequence)

    order_line_month_ids = fields.One2many('sale.order.line', compute='_month_uom_order_lines_ids')
    order_line_fixed_ids = fields.One2many('sale.order.line', compute='_fixed_uom_order_lines_ids')

    monthly_tax_totals = fields.Binary(compute='_compute_monthly_tax_totals', exportable=False)
    fixed_tax_totals = fields.Binary(compute='_compute_fixed_tax_totals', exportable=False)

    @api.depends_context('lang')
    @api.depends('order_line.price_subtotal', 'currency_id', 'company_id')
    def _compute_monthly_tax_totals(self):
        AccountTax = self.env['account.tax']
        for order in self:
            order_lines = order.order_line_month_ids.filtered(lambda x: not x.display_type)
            base_lines = [line._prepare_base_line_for_taxes_computation() for line in order_lines]
            AccountTax._add_tax_details_in_base_lines(base_lines, order.company_id)
            AccountTax._round_base_lines_tax_details(base_lines, order.company_id)
            order.monthly_tax_totals = AccountTax._get_tax_totals_summary(
                base_lines=base_lines,
                currency=order.currency_id or order.company_id.currency_id,
                company=order.company_id,
            )

    @api.depends_context('lang')
    @api.depends('order_line.price_subtotal', 'currency_id', 'company_id')
    def _compute_fixed_tax_totals(self):
        AccountTax = self.env['account.tax']
        for order in self:
            order_lines = order.order_line_fixed_ids.filtered(lambda x: not x.display_type)
            base_lines = [line._prepare_base_line_for_taxes_computation() for line in order_lines]
            AccountTax._add_tax_details_in_base_lines(base_lines, order.company_id)
            AccountTax._round_base_lines_tax_details(base_lines, order.company_id)
            order.fixed_tax_totals = AccountTax._get_tax_totals_summary(
                base_lines=base_lines,
                currency=order.currency_id or order.company_id.currency_id,
                company=order.company_id,
            )

    def _get_fixed_order_lines_to_report(self):
        month = self.env.ref('website_quote_monthly.product_uom_month')
        down_payment_lines = self.order_line.filtered(lambda line:
            line.is_downpayment
            and not line.display_type
            and not line._get_downpayment_state()
        )

        def show_line(line):
            if not line.is_downpayment:
                return True
            elif line.display_type and down_payment_lines:
                return True  # Only show the down payment section if down payments were posted
            elif line in down_payment_lines:
                return True  # Only show posted down payments
            else:
                return False

        return self.order_line.filtered(
            lambda fixed_line: (not fixed_line.display_type and fixed_line.product_id.uom_id != month)
                               or (fixed_line.display_type and not fixed_line.name.startswith('Monthly:'))
            ).filtered(show_line)

