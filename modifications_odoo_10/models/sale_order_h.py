# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging

from odoo import api, fields, models
from odoo import tools, _
from odoo.exceptions import ValidationError
from odoo.modules.module import get_module_resource


_logger = logging.getLogger(__name__)

class SaleOrder(models.Model):
    _name = "sale.order"
    _description = "Sales Order"
    _inherit = ['sale.order']

	
