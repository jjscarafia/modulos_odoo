# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging

from odoo import api, fields, models
from odoo import tools, _
from odoo.exceptions import ValidationError
from odoo.modules.module import get_module_resource

_logger = logging.getLogger(__name__)

class product_type(models.Model):
    _name = "product.type"
    _description = "Product type"
    _rec_name = "name"
    
    name = fields.Char('Product type', help='Product type', required=True)
    code = fields.Char('Code', compute='_compute_code', help='Code')

    def _compute_code(self):
        for record in self:
            if record.name:
                record.code = "_".join(record.name.lower().split())

    @api.onchange('name') # if these fields are changed, call method
    def check_change_code(self):
        if self.name:
            self.code = "_".join(self.name.lower().split())
