# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging

from odoo import api, fields, models
from odoo import tools, _
from odoo.exceptions import ValidationError
from odoo.modules.module import get_module_resource

_logger = logging.getLogger(__name__)

class career_zone(models.Model):
    _name = "career.zone"
    _description = "Zone"
    _rec_name = "name"
    
    name = fields.Char('Zone', help='Zone name', required=True)
    city_id = fields.Many2one('hr.city', string='City', help='City', required=True)
