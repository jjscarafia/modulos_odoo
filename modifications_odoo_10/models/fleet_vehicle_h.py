# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging

from odoo import api, fields, models
from odoo import tools, _
from odoo.exceptions import ValidationError
from odoo.modules.module import get_module_resource


_logger = logging.getLogger(__name__)

class FleetVehicle(models.Model):
    _name = "fleet.vehicle"
    _description = "Information on a vehicle"
    _inherit = ['fleet.vehicle']
    
    employee_id = fields.Many2one('hr.employee', 'Driver employee')
    
    @api.onchange('employee_id') # if these fields are changed, call method
    def check_change(self):
        if self.employee_id:
            self.location = self.employee_id.work_location
