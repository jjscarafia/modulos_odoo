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
    
    airport_name = fields.Char('Airport name', help='Airport name')
    airport_address = fields.Char('Airport address', help='Airport address')
    airport_location = fields.Char('Airport location', help='Airport location')
