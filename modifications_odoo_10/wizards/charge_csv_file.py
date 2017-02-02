# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging

from odoo import api, fields, models
from odoo import tools, _
from odoo.exceptions import ValidationError
from odoo.modules.module import get_module_resource

from os import path, mkdir, remove

import csv
import base64
#https://docs.python.org/2/library/csv.html

from openerp.exceptions import except_orm, Warning, RedirectWarning

_logger = logging.getLogger(__name__)

class ChargeCSVFile(models.Model):
    """
     Este wizard es utilizado para la carga de zip con los certificados(PDF's)
     de las cooperativas.
    """
    _name = "charge.csv.file"
    _description = "Charge CSV File"
    
    state = fields.Selection([
        ('start', 'Start'),
        ('charged', 'Charged'),], string='State')
    
    csv_file = fields.Binary("CSV File", required=True)

    def insert_row(self, row):
        print(row['city'], row['origin'], row['is_origin_airport'],
                    row['zone'], row['destiny'], row['mpc_price'],
                    row['km'], row['mpc_price_km'], row['career_type'],
                    row['pax'], row['product_type'])

    def charge_csv_file(self):
        csv_decoded = base64.b64decode(self.csv_file)
        csv_path = path.join(path.dirname(__file__), '')
        csvfile_name = 'csv-%s.csv' % str(self.id)
        csvfile_path = csv_path + csvfile_name

        with open(csvfile_path, 'w') as csvfile:
            csvfile.write(csv_decoded)
        
        string = ""
        with open(csvfile_path) as csvfile:
            reader = csv.DictReader(csvfile, delimiter=';', quotechar='"')
            for row in reader:
                self.insert_row(row)
                string = string + row['city'] + "; " + row['origin'] + "; " + row['is_origin_airport'] + \
                    "; " + row['zone'] + "; " + row['destiny'] + "; " + row['mpc_price'] + \
                    "; " + row['km'] + "; " + row['mpc_price_km'] + "; " + row['career_type'] + \
                    "; " + row['pax'] + "; " + row['product_type'] + "\n"
        
        #print csvfile_path
        
        remove(csvfile_path)
        
        #raise Warning('Here is the message')
        raise except_orm('Warning','Here is the message: ' + string)
        #raise except_orm('FOO','Lorem ipsum dolor sit amet')
        
    """
    def create(self, cr, uid, vals, context=None):
        if vals.get('zip'):
            zip_decoded = base64.b64decode(vals['zip'])
            agreements_path = path.join(path.dirname(__file__), '../report/certificados/')
            zipfile_name = 'CERTIFICADOS-SINCOOP-%s.zip' % datetime.now(timezone('America/Caracas')).strftime('%d-%m-%Y %H:%M:%S')
            zipfile_path = agreements_path + zipfile_name

            with open(zipfile_path, 'w') as zipfile:
                zipfile.write(zip_decoded)

            if is_zipfile(zipfile_path):
                del(vals['zip'])
                vals['name'] = zipfile_name
                return super(carga_certificado, self).create(cr, uid, vals, context)
            else:
                raise osv.except_osv(
                    _('Alerta!'),
                    _('El archivo no es un zip valido!'))
        else:
            raise osv.except_osv(
                _('Alerta!'),
                _('Su archivo zip debe contener los certificados firmados electronicamente!'))
    """
