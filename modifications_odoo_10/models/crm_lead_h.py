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
    def _get_data_booking_number_generate(self, year_in, month_in, supplier_code, id_book_number):
		year = year_in
		month = month_in
		#booking_search = self.search([('booking_number', '>', 0),
		#								('year_book_number','=',year),
		#								('month_book_number','=',month)], limit=1, order="booking_number_compute DESC")
        
		return {'year_book_number':year,'month_book_number':month}
    """
        string = '''
			booking_number != '' and
			year_book_number = '%s' and month_book_number = '%s'
		'''
		self.env.cr.execute('''SELECT booking_number_compute
						FROM crm_lead
						WHERE ''' + string + 
						''' 
                            order by booking_number_compute DESC limit 1
						''', (year,month))
		
		booking_search = self.env.cr.fetchall()
		
		if len(booking_search) == 0:
			return {'booking_number':1,'year_book_number':year,'month_book_number':month,
                    'booking_number_compute':1,'year_book_number_compute':year,'month_book_number_compute':month,}
		else:
			if booking_search[0][0] == 0 or booking_search[0][0] == None:
				return {'booking_number':1,'year_book_number':year,'month_book_number':month,
                        'booking_number_compute':1,'year_book_number_compute':year,'month_book_number_compute':month,}
			else:
				return {'booking_number':Decimal(str(booking_search[0][0])[:-2]) + Decimal(1),
						'year_book_number':year,'month_book_number':month,
                        'booking_number_compute':Decimal(str(booking_search[0][0])[:-2]) + Decimal(1),
						'year_book_number_compute':year,'month_book_number_compute':month}
    """
				
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
    
    date_and_time = fields.Datetime('Date and Time')#, related='partner_id.date_time', store=False)
    
    journey = fields.Text('Destination address')
    
    employee_id = fields.Many2one('hr.employee', string='Driver assigned')
    
    #customer_id = fields.Many2one('res.partner', string='Customer')
    partner_id_name = fields.Char("Booking name", related='partner_id.name', store=False)
    partner_id_book_number = fields.Char("Booking ID Number", related='partner_id.id_book_number', store=False)
    #user_id = fields.Many2one(related='partner_id.user_id', store=False)
    supplier_id = fields.Many2one(related='partner_id.supplier_id', store=False)
    flight_number = fields.Char("Flight number", related='partner_id.flight_number', store=False)
    customer_email = fields.Char('Booking email', compute='_get_data_customer')
    customer_mobile = fields.Char('Booking mobile', compute='_get_data_customer')
    
    priority = fields.Selection(PRIORITIES, string='Rating', index=True, default=PRIORITIES[0][0])
    
    id_number = fields.Char('ID number', compute='_get_data_id_number', search='_search_data_id_number', store=False)
    id_number_type = fields.Selection([
					('book', 'Booking (BOOK)'),],
					string='ID number type', default='book')
    
    #booking_number = fields.Char('Booking number')#, digits=(19,0)) #default=_get_data_booking_number)
    
    year_book_number = fields.Char('Year', default=_get_current_year)
    
    month_book_number = fields.Char('Month', default=_get_current_month)
    
    supplier_code_compute = fields.Char(related='partner_id.supplier_code_compute')
    
    id_book_number_compute = fields.Char(related='partner_id.id_book_number')
    
    #booking_number_compute = fields.Float('Booking number', digits=(19,0), compute="_get_data_crm_h", store=True)
    #year_book_number_compute = fields.Integer('Year', compute="_get_data_crm_h", store=True)
    #month_book_number_compute = fields.Integer('Month', compute="_get_data_crm_h", store=True)
    
    #flight_number = fields.Char('Flight number')
    
    #products_text = fields.Text('Products')

    #_sql_constraints = {
	#	('booking_month_year_number_supplier_uniq', 'unique(id_number_type,year_book_number,month_book_number,supplier_code_compute,id_book_number_compute)', "The booking number can't be repeated, try again please!.")
	#}
	
    @api.model
    def create(self, vals):
        
        res_id = super(Lead, self).create(vals)
        return res_id
    
    @api.multi
    def write(self, vals):

        return super(Lead, self).write(vals)
	
    @api.one
    def button_generate_booking_number(self):
        book_search = self.search([('id', '=', self.id)], limit=1)
        if book_search.booking_number == False or book_search.booking_number == 0:
            book_search.write(self._get_data_booking_number_generate(
                datetime.datetime.now().year,
                datetime.datetime.now().month))
        return True
    
    def _get_data_id_number(self):
        for record in self:
            if record.supplier_code_compute and record.id_book_number_compute and record.year_book_number and record.month_book_number:
				#CEROPLACES = Decimal(21) ** 0
				if record.id_number_type == "book":
					booking = "BOOK-"
				else:
					booking = "ID-"
				
				record.id_number = booking + str(record.year_book_number) + "-" + str(record.month_book_number) + "-" + str(record.supplier_code_compute) + "-" + str(record.id_book_number_compute)
            elif record.year_book_number in [False, ''] or \
                    record.month_book_number in [False, '']:
				record.id_number = "Without booking number"
                
    def _search_data_id_number(self, operator, value):
		#if value[:5] == 'BOOK-':
		book_type = ''
		year = ''
		month = ''
		number = ''
		if len(value) > 3:
			all_the_other = value
			all_the_other = all_the_other.split('-')
			
			count = len(all_the_other)
			
			if operator == "ilike":
				operator = "=ilike"
			elif operator == "like":
				operator = "=like"
			
			list_cond = []
			if count < 5:
				if count > 0:
					book_type = all_the_other[0]
					if operator == "=ilike" or operator == "=like":
						book_type = book_type+"%"
					list_cond.append(('id_number_type', operator, book_type))
				if count > 1:
					year = all_the_other[1]
					if operator == "=ilike" or operator == "=like":
						year = year+"%"
					list_cond.append(('year_book_number', operator, year))
				if count > 2:
					month = all_the_other[2]
					if operator == "=ilike" or operator == "=like":
						month = month+"%"
					list_cond.append(('month_book_number', operator, month))
				if count > 3:
					number = all_the_other[3]
					if operator == "=ilike" or operator == "=like":
						number = number+"%"
					list_cond.append(('booking_number', operator, number))
                    
				crm_lead_ids = self.env['crm.lead'].search(
					list_cond
				)
				list_cond = crm_lead_ids.ids
			return [('id', 'in', list_cond)]
		else:
			return [('id', 'in', [])]
				
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
    
    """def _get_data_crm_h(self):
        for record in self:
            record.booking_number = record.partner_id.supplier_id.supplier_code + "-" + record.partner_id.id_book_number
            #record.booking_number_compute = Decimal(record.booking_number)
            #record.year_book_number_compute = int(record.year_book_number)
            #record.month_book_number_compute = int(record.month_book_number)
    """
    
    def _get_data_customer(self):
        for record in self:
            if record.partner_id:
                record.customer_email = record.partner_id.email
                record.customer_mobile = record.partner_id.mobile
                #record.user_id = record.partner_id.user_id
                record.supplier_id = record.partner_id.supplier_id
    
    @api.onchange('partner_id') # if these fields are changed, call method
    def check_change_customer(self):
        if self.partner_id:
            self.customer_email = self.partner_id.email
            self.customer_mobile = self.partner_id.mobile
            self.partner_id_name = self.partner_id.name
            self.partner_id_book_number = self.partner_id.id_book_number
            #self.partner_id_supplier = self.partner_id.supplier_id.name
            self.partner_id_flight_number = self.partner_id.flight_number
            #self.user_id = self.partner_id.user_id
            self.supplier_id = self.partner_id.supplier_id
            #self.date_and_time = self.partner_id.date_time
            self.supplier_code_compute = self.partner_id.supplier_code_compute
            self.id_book_number_compute = self.partner_id.id_book_number

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
