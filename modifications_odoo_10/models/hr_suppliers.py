# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging

from odoo import api, fields, models
from odoo import tools, _
from odoo.exceptions import ValidationError
from odoo.modules.module import get_module_resource


_logger = logging.getLogger(__name__)

class Supplier(models.Model):
    _name = "hr.supplier"
    _description = "Supplier"
    _rec_name = "name"
    
    name = fields.Char('Supplier name', help='Airport name', required=True)
    supplier_code = fields.Char('Supplier code', help='Airport code', required=True)
    supplier_location = fields.Text('Supplier location', help='Airport location')
