# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging

from odoo import api, fields, models
from odoo import tools, _
from odoo.exceptions import ValidationError
from odoo.modules.module import get_module_resource

_logger = logging.getLogger(__name__)

class career_origin_destiny(models.Model):
    _name = "career.origin.destiny"
    _description = "Origin"
    _rec_name = "name"
    
    name = fields.Char('Name', help='Name', required=True)
    city_id = fields.Many2one('hr.city', string='City', help='City', required=True)
    is_origin = fields.Boolean('Is origin', help='Is origin')
    is_destiny = fields.Boolean('Is destiny', help='Is destiny')
    is_airport = fields.Boolean('Is airport', help='Is airport')
