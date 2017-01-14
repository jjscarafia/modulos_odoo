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
    
    @api.onchange('product_id') # if these fields are changed, call method
    def check_change_price_unit_alt(self):
		if self.product_id:
			self.price_unit = self.product_id.list_price
			#self.price_unit_to_show = self.product_id.list_price

    '''
    @api.depends('product_uom_qty', 'discount', 'price_unit', 'tax_id')
    def _compute_amount(self):
        """
        Compute the amounts of the SO line.
        """
        #print "HELLO"
        print "HELLO1 " + str(self)
        for line in self:
            price = line.price_unit_to_show * (1 - (line.discount or 0.0) / 100.0)
            taxes = line.tax_id.compute_all(price, line.order_id.currency_id, line.product_uom_qty, product=line.product_id, partner=line.order_id.partner_id)
            line.update({
                'price_tax': taxes['total_included'] - taxes['total_excluded'],
                'price_total': taxes['total_included'],
                'price_subtotal': taxes['total_excluded'],
            })
            
            print "HELLO2 " + str(line.price_unit_to_show)
	'''
