# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging

from odoo import api, fields, models
from odoo import tools, _
from odoo.exceptions import ValidationError
from odoo.modules.module import get_module_resource


_logger = logging.getLogger(__name__)

class language(models.Model):
    _name = "hr.language"
    _description = "Language"
    _rec_name = "name"
    
    name = fields.Char('Language name', help='Language name')
    employee_ids = fields.Many2many('hr.employee', 'employee_language_rel', 'language_id', 'emp_id', string='Employees')
