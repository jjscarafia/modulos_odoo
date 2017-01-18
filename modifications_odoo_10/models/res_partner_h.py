# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging

from odoo import api, fields, models
from odoo import tools, _
from odoo.exceptions import ValidationError
from odoo.modules.module import get_module_resource

from decimal import *

import time

_logger = logging.getLogger(__name__)

class Partner(models.Model):
    _name = "res.partner"
    _description = 'Partner'
    _inherit = ['res.partner']
    
    id_book_number = fields.Char('ID number', required=True)
    display_name = fields.Char("Name", store=True, index=True)
