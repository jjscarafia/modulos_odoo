# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging

from odoo import api, fields, models
from odoo import tools, _
from odoo.exceptions import ValidationError
from odoo.modules.module import get_module_resource

import odoo.addons.decimal_precision as dp

_logger = logging.getLogger(__name__)

class SaleOrderLine(models.Model):
    _inherit = ['sale.order.line']
    
    journey = fields.Char('Journey', help='Journey')
    price_unit = fields.Float('Unit Price', required=True, digits=dp.get_precision('Product Price'), default=0.0)
    price_unit_to_show = fields.Float('Unit Price', required=True, digits=dp.get_precision('Product Price'), default=0.0, compute='_get_price_unit_alt')
    
    def _get_price_unit_alt(self):
		for record in self:
			if record.product_id:
				record.price_unit_to_show = record.product_id.list_price
    
    @api.onchange('product_id') # if these fields are changed, call method
    def check_change_price_unit_alt(self):
		if self.product_id:
			self.price_unit = self.product_id.list_price
			self.price_unit_to_show = self.product_id.list_price
