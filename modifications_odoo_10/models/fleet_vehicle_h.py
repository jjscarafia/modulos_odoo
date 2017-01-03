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
    location = fields.Char(string="Location", help='Location of the vehicle (garage, ...)', 
                compute='_get_work_location', search='_search_fleet_vehicle_work_location')
    
    @api.onchange('employee_id') # if these fields are changed, call method
    def check_change(self):
        if self.employee_id:
            self.location = self.employee_id.work_location

    def _get_work_location(self):
        for record in self:
            if record.employee_id:
                record.location = record.employee_id.work_location

    def _search_fleet_vehicle_work_location(self, operator, value):
        res = []
        assert operator in ('=', '!=', '<>', 'ilike', 'not ilike'), 'Operation not supported'
        if operator in ('=', 'ilike'):
            search_operator = 'in'
        elif operator in ('<>', '!=', 'not ilike'):
            search_operator = 'not in'
        
        if value == False:
            string = ''' vehicle.location ''' + operator + ''' NULL ''' + \
                        ''' or vehicle.location ''' + operator + """ '' """
        else:
            string = ''' vehicle.location ''' + operator + ''' %s '''
            if operator in ('ilike', 'not ilike'):
                value = '%' + value + '%'
        
        self.env.cr.execute('''SELECT vehicle.id
                        FROM fleet_vehicle vehicle
                        WHERE ''' + string, (value,))
                        
        print '''SELECT vehicle.id
                        FROM fleet_vehicle vehicle
                        WHERE ''' + string
        res_ids = [x[0] for x in self.env.cr.fetchall()]
        res.append(('id', search_operator, res_ids))
        return res
