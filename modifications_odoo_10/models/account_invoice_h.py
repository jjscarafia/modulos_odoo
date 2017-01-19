# -*- coding: utf-8 -*-

import json
from lxml import etree
from datetime import datetime
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models, _
from odoo.tools import float_is_zero, float_compare
from odoo.tools.misc import formatLang

from odoo.exceptions import UserError, RedirectWarning, ValidationError

import odoo.addons.decimal_precision as dp
import logging

_logger = logging.getLogger(__name__)

class AccountInvoice(models.Model):
    _inherit = ['account.invoice']
    
    supplier_id = fields.Many2one(related='partner_id.supplier_id', store=False)
    
    user_related_id = fields.Many2one(string="Salesperson related to Booking", related='partner_id.user_id', store=False)

    @api.onchange('partner_id') # if these fields are changed, call method
    def check_change_customer(self):
        if self.partner_id:
            self.supplier_id = self.partner_id.supplier_id
            self.user_related_id = self.partner_id.user_id
