# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging

from odoo import api, fields, models
from odoo import tools, _
from odoo.exceptions import ValidationError
from odoo.modules.module import get_module_resource


_logger = logging.getLogger(__name__)

class ProductTemplate(models.Model):
    _inherit = ['product.template']
    
    city_origin_id = fields.Many2one('hr.city', string='City origin')
    city_destiny_id = fields.Many2one('hr.city', string='City destiny')
    career_origin = fields.Many2one('career.origin.destiny', string='Career origin')
    career_destiny = fields.Many2one('career.origin.destiny', string='Career destiny')
    career_zone = fields.Many2one('career.zone', string='Career zone')
    #mpc_price is list_price and standard_price
    km = fields.Float('KMs', help='KMs')
    mpc_price_km = fields.Float('MPC price per KM', help='MPC price per KM')
    career_type = fields.Many2one('hr.vehicle.type', string='Career type')
    career_pax = fields.Many2one('career.pax', string='Career pax')
    is_mpc_product = fields.Boolean('Is a MPC Product')
