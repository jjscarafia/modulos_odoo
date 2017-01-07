# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging

from odoo import api, fields, models
from odoo import tools, _
from odoo.exceptions import ValidationError
from odoo.modules.module import get_module_resource


_logger = logging.getLogger(__name__)

class Employee(models.Model):
    _name = "hr.employee"
    _description = "Employee"
    _inherit = ['hr.employee']
    
    vehicle_type = fields.Many2one('hr.vehicle.type', string='Vehicle type')
    
    #vehicle_type = #fields.Selection([
        #('standard', 'Standard'),
        #('business', 'Business'),
        #('premium', 'Premium'),
        #('carrier', 'Carrier'),
        #('mini_van', 'Mini Van'),
    #], string='Vehicle Type', help='Driver license')
    vehicle_model = fields.Char('Vehicle model', help='Vehicle model')
    driver_license = fields.Char('Driver license', help='Driver license')
    vehicle_color = fields.Char('Vehicle color', help='Vehicle color')
    airport_ids = fields.Many2many('hr.airport', 'employee_airport_rel', 'emp_id', 'airport_id', string='Airports')
    language_ids = fields.Many2many('hr.language', 'employee_language_rel', 'emp_id', 'language_id', string='Language')
