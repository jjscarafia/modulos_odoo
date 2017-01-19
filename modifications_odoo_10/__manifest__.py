# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Modifications Odoo 10',
    'depends': ['base','hr','fleet','crm','sale','account'],
    'description': """
Assets management
=================
Manage assets owned by a company or a person.
Keeps track of depreciations, and creates corresponding journal entries.

    """,
    'website': 'Custom webpage',
    'category': 'Modifications',
    'sequence': 32,
    'demo': [
    ],
    'data': [
        'views/hr_employee_h.xml',
        'views/fleet_vehicle_h.xml',
        'views/menu_h.xml',
        'views/vehicle_type_view.xml',
        'views/airport_view.xml',
        'views/languages_view.xml',
        'views/city_view.xml',
        'views/supplier_view.xml',
        'views/resource_calendar_view.xml',
        'views/res_partner_h.xml',
        'views/crm_lead_h.xml',
        'views/sale_h.xml',
        'views/account_invoice_h.xml',
        'security/ir.model.access.csv',
    ],
    'qweb': [
    ],
}
