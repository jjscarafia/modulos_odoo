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
    supplier_id = fields.Many2one('res.partner', string='Booking Supplier')
    pick_up_address = fields.Text('Pick Up Address')
    dest_address = fields.Text('Destinations Address')
    date_time = fields.Datetime('Date and Time')
    flight_number = fields.Char('Flight Number')
    contact = fields.Boolean('Is Contact')
    is_booking = fields.Boolean('Is a Booking')
    supplier_code = fields.Char('Supplier code')
    supplier_code_compute = fields.Char('Supplier code', compute='_get_supplier_data')
    
    def _get_supplier_data(self):
        for record in self:
            if record.supplier_id:
                record.supplier_code_compute = record.supplier_id.supplier_code
                
    @api.onchange('supplier_id') # if these fields are changed, call method
    def check_change_supplier(self):
        if self.supplier_id:
            self.supplier_code_compute = self.supplier_id.supplier_code
            
    @api.onchange('id_book_number') # if these fields are changed, call method
    def check_change_id_book_number(self):
        if self.id_book_number:
            code_stripped = self.id_book_number.strip()
            self.id_book_number = "".join(code_stripped.split())
            
    @api.onchange('supplier_code') # if these fields are changed, call method
    def check_change_supplier_code(self):
        if self.supplier_code:
            code_stripped = self.supplier_code.strip()
            self.supplier_code = "".join(code_stripped.split())
    
    def name_get(self):
        res = []
        for partner in self:
            name = partner.name or ''

            if partner.company_name or partner.parent_id:
                if not name and partner.type in ['invoice', 'delivery', 'other']:
                    name = dict(self.fields_get(['type'])['type']['selection'])[partner.type]
                if not partner.is_company and not partner.is_booking:
                    name = "%s, %s" % (partner.commercial_company_name or partner.parent_id.name, name)
            if self._context.get('show_address_only'):
                name = partner._display_address(without_company=True)
            if self._context.get('show_address'):
                name = name + "\n" + partner._display_address(without_company=True)
            name = name.replace('\n\n', '\n')
            name = name.replace('\n\n', '\n')
            if self._context.get('show_email') and partner.email:
                name = "%s <%s>" % (name, partner.email)
            if partner.id_book_number and partner.is_booking:
                name = "%s %s" % (partner.id_book_number, name)
            elif partner.supplier_code and partner.supplier:
                name = "%s %s" % (partner.supplier_code, name)
            if self._context.get('html_format'):
                name = name.replace('\n', '<br/>')
            res.append((partner.id, name))
        return res
    
    @api.depends('id_book_number')
    def _compute_display_name(self):
        diff = dict(show_address=None, show_address_only=None, show_email=None)
        names = dict(self.with_context(**diff).name_get())
        for partner in self:
            partner.display_name = names.get(partner.id)

    _sql_constraints = {
		('booking_id_number_uniq', 'unique(supplier_id,id_book_number)', "The booking number can't be repeated, try again please!."),
        ('supplier_code_uniq', 'unique(supplier_code)', "The supplier code can't be repeated, try again please!."),
	}
    
    @api.multi
    def write(self, vals):
        
        result = super(Partner, self).write(vals)
        
        diff = dict(show_address=None, show_address_only=None, show_email=None)
        names = dict(self.with_context(**diff).name_get())
        
        for partner in self:
            super(Partner, partner).write({'display_name': names.get(partner.id)})

        return result
