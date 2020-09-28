# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Account Invoice Timesheet Date',
    'version': '13.0.1.0.0',
    'category': 'Sales/Sales',
    'summary': 'Invoice Helper',
    'description': """
This module contains modifications to the common features of Sales Management and eCommerce.
    """,
    'depends': ['sale'],
    'data': [

        'wizard/sale_make_invoice_advance_views.xml',

    ],
    'demo': [],
    'qweb': [],
    'installable': True,
    'auto_install': False
}
