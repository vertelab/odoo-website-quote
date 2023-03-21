# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo SA, Open Source Management Solution, third party addon
#    Copyright (C) 2022- Vertel AB (<https://vertel.se>).
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
#    along with this program. If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

{
    'name': 'Website Quote: Monthly, Template',
    'version': '14.0.1.1.0',
    # Version ledger: 14.0 = Odoo version. 1 = Major. Non regressionable code. 2 = Minor. New features that are regressionable. 3 = Bug fixes
    'summary': 'More features for online quotation.',
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Sales',
    'description': """
More features for online quotation
==================================

* Product image in pricing
* Product detail description for quotation
* New unit of measure month
* Additional table for monthly cost products

*14.0.1.1.0
========================
- Split the order line for customer preview, so that the customer sees products with the
  UOM "month"
- Also ensured that the notes and sections are visible where applicable. 
NoTE: For the notes and sections to show well, you need to add the word "Monthly:"
      to the beginning of any section or note that is added to the line e.g Monthly: Subscriptions
    """,
    #'sequence': '1',
    'author': 'Vertel AB',
    'website': 'https://vertel.se/apps/odoo-website-quote/website_quote_monthly',
    'images': ['static/description/banner.png'],  # 560x280 px.
    'license': 'AGPL-3',
    'contributor': '',
    'maintainer': 'Vertel AB',
    'repository': 'https://github.com/vertelab/odoo-website-quote',
    # Any module necessary for this one to work correctly

    'depends': ['sale_quotation_builder'],
    'data': [
        'data/data.xml',
        'views/template.xml',
        # 'views/sale_order_view.xml',
    ],
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
