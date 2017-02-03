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
    
    country_origin_id = fields.Many2one('hr.country', string='Country origin')
    country_destiny_id = fields.Many2one('hr.country', string='Country destiny')
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

    @api.onchange('city_origin_id', 'city_destiny_id', 'career_origin', 'career_destiny', 'career_zone', 'career_type') # if these fields are changed, call method
    def check_change_code(self):
        if self.is_mpc_product:
            product_name = self.name
            if self.city_origin_id:
                product_name = "Service from city " + self.city_origin_id.name
                if self.country_origin_id:
                    product_name = product_name + " in " + self.country_destiny_id.name
                    if self.city_destiny_id:
                        product_name = product_name + " to city " + self.city_destiny_id.name
                        if self.country_destiny_id:
                            product_name = product_name + " in " + self.country_destiny_id.name
                            if self.career_origin:
                                product_name = product_name + ". Origin: " + self.career_origin.name
                                if self.career_destiny:
                                    product_name = product_name + ", Destiny: " + self.career_destiny.name
                                    if self.career_zone:
                                        product_name = product_name + " " + self.career_zone.name + "."
                                        if self.career_type:
                                            product_name = product_name + " Career type: " + self.career_type.name + "."
            
            self.name = product_name
