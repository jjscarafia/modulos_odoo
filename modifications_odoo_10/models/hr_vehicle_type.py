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
    _rec_name = "name"
    
    name = fields.Char('Name', help='Vehicle type name', required=True)
    description = fields.Text('Description', help='Vehicle type description')
    code = fields.Char('Code', compute='_compute_code', help='Vehicle type code', store=True)
    
    @api.depends('name')
    def _compute_code(self):
        for record in self:
            if record.name:
                record.code = "_".join(record.name.lower().split())

    @api.onchange('name') # if these fields are changed, call method
    def check_change_code(self):
        if self.name:
            self.code = "_".join(self.name.lower().split())

    _sql_constraints = {
       ('hr_vehicle_type_uniq', 'unique(code)', 'Code can not be repeated')
    }
