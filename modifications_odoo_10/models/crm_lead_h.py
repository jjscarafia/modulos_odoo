# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging

from odoo import api, fields, models
from odoo import tools, _
from odoo.exceptions import ValidationError
from odoo.modules.module import get_module_resource

from decimal import *

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
    
    @api.model
    def _get_data_booking_number(self):
		booking_search = self.search([('booking_number', '>', 0)], limit=1, order="booking_number DESC")
		
		if len(booking_search) == 0:
			return 1
		else:
			if booking_search.booking_number == 0:
				return 1
			else:
				return Decimal(str(booking_search.booking_number)) + Decimal(1)
    
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
    
    date_and_time = fields.Datetime('Date and Time')
    
    journey = fields.Char('Journey')
    
    employee_id = fields.Many2one('hr.employee', string='Driver')
    
    #customer_id = fields.Many2one('res.partner', string='Customer')
    customer_email = fields.Char('Customer email', compute='_get_data_customer')
    customer_mobile = fields.Char('Customer mobile', compute='_get_data_customer')
    
    priority = fields.Selection(PRIORITIES, string='Rating', index=True, default=PRIORITIES[0][0])
    
    id_number = fields.Char('ID number', compute='_get_data_id_number', search='_search_data_id_number', store=False)
    
    booking_number = fields.Float('Booking number', digits=(19,0), 
								default=_get_data_booking_number)
    
    flight_number = fields.Char('Flight number')
    
    destination_address = fields.Text('Destination address')
    
    dest_date_and_time = fields.Datetime('Destination date and time')
    
    products_text = fields.Text('Products')
    
    _sql_constraints = {
		('booking_number_uniq', 'unique(booking_number)', "The booking number can't be repeated, try again please!.")
	}
	
    @api.one
    def button_generate_booking_number(self):
		book_search = self.search([('id', '=', self.id)], limit=1)
		if book_search.booking_number == False or book_search.booking_number == 0:
			book_search.write({'booking_number': self._get_data_booking_number()})
		return True
    
    def _get_data_id_number(self):
        for record in self:
            if record.booking_number:
				CEROPLACES = Decimal(21) ** 0
				record.id_number = "ID-" + str(Decimal(record.booking_number).quantize(CEROPLACES))
            else:
				record.id_number = "Without booking number"
                
    def _search_data_id_number(self, operator, value):
		if value[:3] == 'ID-':
			if len(value) > 3:
				return [('booking_number', operator, value[3:])]
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
                record.vehicle_type = record.employee_id.vehicle_type
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
            self.vehicle_type = self.employee_id.vehicle_type.name
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
