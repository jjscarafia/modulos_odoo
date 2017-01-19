# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging

from odoo import api, fields, models
from odoo import tools, _
from odoo.exceptions import ValidationError
from odoo.modules.module import get_module_resource

from decimal import *

import time

import datetime

_logger = logging.getLogger(__name__)

PRIORITIES = [
    ('0', 'Normal'),
    ('1', 'Low'),
    ('2', 'High'),
    ('3', 'Very High'),
    ('4', 'So High'),
    ('5', 'Completely High'),
]

class Lead(models.Model):
    _name = "crm.lead"
    _description = "Lead/Opportunity"
    _inherit = ['crm.lead']
    
    """
    @api.model
    def _get_data_booking_number(self):
		booking_search = self.search([('booking_number', '>', 0),
										('year_book_number','=',datetime.datetime.now().year),
										('month_book_number','=',datetime.datetime.now().month)], limit=1, order="booking_number DESC")
		
		if len(booking_search) == 0:
			return 1
		else:
			if booking_search.booking_number == 0:
				return 1
			else:
				return Decimal(str(booking_search.booking_number)) + Decimal(1)
	"""
				
    @api.model
    def _get_data_booking_number_generate(self):
		year = datetime.datetime.now().year
		month = datetime.datetime.now().month
		booking_search = self.search([('booking_number', '>', 0),
										('year_book_number','=',year),
										('month_book_number','=',month)], limit=1, order="booking_number DESC")
		
		if len(booking_search) == 0:
			return {'booking_number':1,'year_book_number':year,'month_book_number':month}
		else:
			if booking_search.booking_number == 0:
				return {'booking_number':1,'year_book_number':year,'month_book_number':month}
			else:
				return {'booking_number':Decimal(str(booking_search.booking_number)) + Decimal(1),
						'year_book_number':year,'month_book_number':month}
				
    @api.model
    def _get_current_year(self):
        now = datetime.datetime.now()
        return str(now.year)
        
    @api.model
    def _get_current_month(self):
        now = datetime.datetime.now()
        return str(now.month)
    
    mobile_number = fields.Char('Mobile number', compute='_get_data_employee')
    email_address = fields.Char('Email address', compute='_get_data_employee')
    landline_number = fields.Char('Landline number', compute='_get_data_employee')
    whatsapp_number = fields.Char('WhatsApp number', compute='_get_data_employee')
    driver_license = fields.Char('Driver license', compute='_get_data_employee')
    vehicle_type = fields.Char('Vehicle type', compute='_get_data_employee')
    vehicle_model = fields.Char('Vehicle model', compute='_get_data_employee')
    vehicle_color = fields.Char('Vehicle color', compute='_get_data_employee')
    plate_number = fields.Char('Plate number', compute='_get_data_employee')
    car_insurance_number = fields.Char('Car insurance number', compute='_get_data_employee')
    #name = fields.Char('Product', required=True, index=True)
    
    product_id = fields.Many2one('product.template', string='Product')
    
    price = fields.Float('Price')
    #product_ids = fields.Many2many('product.template', 'crm_product_template_rel', 'crm_id', 'product_id', string='Products')

    
    date_and_time = fields.Datetime('Date and Time')
    
    journey = fields.Text('Destination address')
    
    employee_id = fields.Many2one('hr.employee', string='Driver assigned')
    
    #customer_id = fields.Many2one('res.partner', string='Customer')
    partner_id_name = fields.Char("Customer name", related='partner_id.name', store=False)
    partner_id_book_number = fields.Char("Customer ID Number", related='partner_id.id_book_number', store=False)
    partner_id_supplier = fields.Char("Booking Supplier", related='partner_id.supplier_id.name', store=False)
    flight_number = fields.Char("Flight number", related='partner_id.flight_number', store=False)
    customer_email = fields.Char('Customer email', compute='_get_data_customer')
    customer_mobile = fields.Char('Customer mobile', compute='_get_data_customer')
    
    priority = fields.Selection(PRIORITIES, string='Rating', index=True, default=PRIORITIES[0][0])
    
    id_number = fields.Char('ID number', compute='_get_data_id_number', search='_search_data_id_number', store=False)
    id_number_type = fields.Selection([
					('book', 'Booking (BOOK-)'),],
					string='ID number type', default='book')
    
    booking_number = fields.Float('Booking number', digits=(19,0)) #default=_get_data_booking_number)
								
    year_book_number = fields.Integer('Year', default=_get_current_year)
    
    month_book_number = fields.Integer('Month', default=_get_current_month)
    
    #flight_number = fields.Char('Flight number')
    
    destination_address = fields.Text('Destination address')
    
    dest_date_and_time = fields.Datetime('Destination date and time')
    
    #products_text = fields.Text('Products')

    _sql_constraints = {
		('booking_number_uniq', 'unique(year_book_number,month_book_number,booking_number)', "The booking number can't be repeated, try again please!.")
	}
	
    @api.model
    def create(self, vals):
        vals.update(self._get_data_booking_number_generate())
        res_id = super(Lead, self).create(vals)
        return res_id
	
    @api.one
    def button_generate_booking_number(self):
		book_search = self.search([('id', '=', self.id)], limit=1)
		if book_search.booking_number == False or book_search.booking_number == 0:
			book_search.write(self._get_data_booking_number_generate())
		return True
    
    def _get_data_id_number(self):
        for record in self:
            if record.booking_number:
				#CEROPLACES = Decimal(21) ** 0
				if record.id_number_type == "book":
					booking = "BOOK-"
				else:
					booking = "ID-"
				
				record.id_number = booking + str(record.year_book_number) + str(record.month_book_number) + "-" + str(record.booking_number)[:-2]
            elif record.booking_number == False or record.booking_number == 0:
				record.id_number = "Without booking number"
                
    def _search_data_id_number(self, operator, value):
		if value[:5] == 'BOOK-':
			if len(value) > 3:
				return [('booking_number', operator, value[5:])]
			else:
				return [('booking_number', operator, '')]
				
    """
		res = []
		assert operator in ('=', '!=', '<>', 'ilike', 'not ilike'), 'Operation not supported'
		if operator in ('=', 'ilike'):
			search_operator = 'in'
		elif operator in ('<>', '!=', 'not ilike'):
			search_operator = 'not in'
		
		if value == False:
			string = ''' crm.id_number ''' + operator + ''' NULL ''' + \
						''' or crm.id_number ''' + operator + """ '' """
		else:
			string = ''' crm.id_number ''' + operator + ''' %s '''
			if operator in ('ilike', 'not ilike'):
				value = '%' + value + '%'
		
		self.env.cr.execute('''SELECT crm.id
						FROM crm_lead crm
						WHERE ''' + string, (value,))
						
		res_ids = [x[0] for x in self.env.cr.fetchall()]
		res.append(('id', search_operator, res_ids))
		return res
    """
    
    def _get_data_employee(self):
        for record in self:
            if record.employee_id:
                record.mobile_number = record.employee_id.mobile_phone
                record.email_address = record.employee_id.work_email
                record.landline_number = record.employee_id.landline_number
                record.whatsapp_number = record.employee_id.whatsapp_number
                record.driver_license = record.employee_id.driver_license
                record.vehicle_type = record.employee_id.vehicle_type_id.name
                record.vehicle_model = record.employee_id.vehicle_model
                record.vehicle_color = record.employee_id.vehicle_color
                record.plate_number = record.employee_id.plate_number
                record.car_insurance_number = record.employee_id.car_insurance_number
    
    @api.onchange('employee_id') # if these fields are changed, call method
    def check_change_employee(self):
        if self.employee_id:
            self.mobile_number = self.employee_id.mobile_phone
            self.email_address = self.employee_id.work_email
            self.landline_number = self.employee_id.landline_number
            self.whatsapp_number = self.employee_id.whatsapp_number
            self.driver_license = self.employee_id.driver_license
            self.vehicle_type = self.employee_id.vehicle_type_id.name
            self.vehicle_model = self.employee_id.vehicle_model
            self.vehicle_color = self.employee_id.vehicle_color
            self.plate_number = self.employee_id.plate_number
            self.car_insurance_number = self.employee_id.car_insurance_number
            
    def _get_data_customer(self):
        for record in self:
            if record.partner_id:
                record.customer_email = record.partner_id.email
                record.customer_mobile = record.partner_id.mobile
    
    @api.onchange('partner_id') # if these fields are changed, call method
    def check_change_customer(self):
        if self.partner_id:
            self.customer_email = self.partner_id.email
            self.customer_mobile = self.partner_id.mobile
            self.partner_id_name = self.partner_id.name
            self.partner_id_book_number = self.partner_id.id_book_number
            self.partner_id_supplier = self.partner_id.supplier_id.name
            self.partner_id_flight_number = self.partner_id.flight_number

    """
    location = fields.Char(string="Location", help='Location of the vehicle (garage, ...)', 
                compute='_get_work_location', search='_search_fleet_vehicle_work_location')
    
    @api.onchange('employee_id') # if these fields are changed, call method
    def check_change(self):
        if self.employee_id:
            self.location = self.employee_id.work_location

    def _get_work_location(self):
        for record in self:
            if record.employee_id:
                record.location = record.employee_id.work_location
    """
