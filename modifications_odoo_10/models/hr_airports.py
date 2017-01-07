# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging

from odoo import api, fields, models
from odoo import tools, _
from odoo.exceptions import ValidationError
from odoo.modules.module import get_module_resource


_logger = logging.getLogger(__name__)

class Airport(models.Model):
    _name = "hr.airport"
    _description = "Airports"
    _rec_name = "name"
    
    name = fields.Char('Airport name', help='Airport name')
    airport_code = fields.Char('Airport code', help='Airport code')
    airport_location = fields.Char('Airport location', help='Airport location')
    employee_ids = fields.Many2many('hr.employee', 'employee_airport_rel', 'airport_id', 'emp_id', string='Employees')
