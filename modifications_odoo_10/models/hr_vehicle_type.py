# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging

from odoo import api, fields, models
from odoo import tools, _
from odoo.exceptions import ValidationError
from odoo.modules.module import get_module_resource


_logger = logging.getLogger(__name__)

class VehicleType(models.Model):
    _name = "hr.vehicle.type"
    _description = "Vehicle Type"
    _rec_name = "vehicle_type_name"
    
    vehicle_type_name = fields.Char('Vehicle type name', help='Vehicle type name')
    vehicle_type_code = fields.Char('Vehicle type code', help='Vehicle type code')
    vehicle_type_description = fields.Text('Vehicle type description', help='Vehicle type description')
