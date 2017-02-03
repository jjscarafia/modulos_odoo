# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging

from odoo import api, fields, models
from odoo import tools, _
from odoo.exceptions import ValidationError
from odoo.modules.module import get_module_resource


_logger = logging.getLogger(__name__)

class city(models.Model):
    _name = "hr.city"
    _description = "City"
    _rec_name = "name"
    
    name = fields.Char('City name', help='City name', required=True)
    country_id = fields.Many2one('hr.country', string='Country name', required=True)
