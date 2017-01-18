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
    
    id_book_number = fields.Char('ID number')
    display_name = fields.Char(compute='_compute_display_name', store=True, index=True)
    supplier_id = fields.Many2one('hr.supplier', string='Supplier')
    pick_up_address = fields.Text('Pick Up Address')
    dest_address = fields.Text('Destinations Address')
    date_time = fields.Datetime('Date and Time')
    flight_number = fields.Char('Flight Number')
   
    def name_get(self):
        res = []
        for record in self:
            if record.id_book_number == False:
				number = ""
            else:
				number = record.id_book_number
            name = number + " " + record.name
            res.append((record.id, name))
        return res
    
    @api.depends('id_book_number')
    def _compute_display_name(self):
        diff = dict(show_address=None, show_address_only=None, show_email=None)
        names = dict(self.with_context(**diff).name_get())
        for partner in self:
            partner.display_name = names.get(partner.id)
