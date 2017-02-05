# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging

from odoo import api, fields, models
from odoo import tools, _
from odoo.exceptions import ValidationError, AccessError
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
        print(row['country_origin'], row['country_destiny'], row['city_origin'], 
                    row['city_destiny'], row['origin'], row['is_origin_airport'],
                    row['zone'], row['destiny'], row['is_destiny_airport'], row['mpc_price'],
                    row['km'], row['mpc_price_km'], row['career_type'],
                    row['pax'], row['product_type'])
        
        country_ids = self.env['hr.country'].search(
            [('name', '=ilike', row['country_origin'].strip())], limit=1, order="id ASC"
        )
        country_origin_id = 0
        if len(country_ids) > 0:
            country_origin_id = country_ids
        else:
            country_origin_id = self.env['hr.country'].create({'name': row['country_origin'].strip()})
        
        country_ids = self.env['hr.country'].search(
            [('name', '=ilike', row['country_destiny'].strip())], limit=1, order="id ASC"
        )
        country_destiny_id = 0
        if len(country_ids) > 0:
            country_destiny_id = country_ids
        else:
            country_destiny_id = self.env['hr.country'].create({'name': row['country_destiny'].strip()})
        
        city_ids = self.env['hr.city'].search(
            [('name', '=ilike', row['city_origin'].strip()),
            ('country_id', '=', country_origin_id.id)], limit=1, order="id ASC"
        )
        city_origin_id = 0
        if len(city_ids) > 0:
            city_origin_id = city_ids
        else:
            city_origin_id = self.env['hr.city'].create({'name': row['city_origin'].strip(), 'country_id': country_origin_id.id})
        
        city_ids = self.env['hr.city'].search(
            [('name', '=ilike', row['city_destiny'].strip()),
            ('country_id', '=', country_destiny_id.id)], limit=1, order="id ASC"
        )
        city_destiny_id = 0
        if len(city_ids) > 0:
            city_destiny_id = city_ids
        else:
            city_destiny_id = self.env['hr.city'].create({'name': row['city_destiny'].strip(), 'country_id': country_destiny_id.id})
        
        if row['is_origin_airport'].strip().upper() == "YES":
            is_airport = True
        else:
            is_airport = False
        career_origin_destiny_ids = self.env['career.origin.destiny'].search(
            [('name', '=ilike', row['origin'].strip()),
                ('city_id','=',city_origin_id.id),
                ('country_id', '=', country_origin_id.id),
                ('is_origin','=',True),
                ('is_airport','=',is_airport)], limit=1, order="id ASC")
        career_origin_id = 0
        if len(career_origin_destiny_ids) > 0:
            career_origin_id = career_origin_destiny_ids
        else:
            career_origin_id = self.env['career.origin.destiny'].create({'name': row['origin'].strip(), 
                                                                        'city_id': city_origin_id.id,
                                                                        'country_id': country_origin_id.id, 
                                                                        'is_origin': True, 'is_airport': is_airport})
        
        if row['is_destiny_airport'].strip().upper() == "YES":
            is_airport = True
        else:
            is_airport = False
        career_origin_destiny_ids = self.env['career.origin.destiny'].search(
            [('name', '=ilike', row['destiny'].strip()),
                ('city_id','=',city_destiny_id.id),
                ('country_id', '=', country_destiny_id.id),
                ('is_destiny','=',True),
                ('is_airport','=',is_airport)], limit=1, order="id ASC")
        career_destiny_id = 0
        if len(career_origin_destiny_ids) > 0:
            career_destiny_id = career_origin_destiny_ids
        else:
            career_destiny_id = self.env['career.origin.destiny'].create({'name': row['destiny'].strip(), 'city_id': city_destiny_id.id, 
                                                                            'country_id': country_destiny_id.id, 
                                                                            'is_destiny': True, 
                                                                            'is_airport': is_airport})
        
        if row['zone'].strip() == "":
            career_zone_id = False
        else:
            zone_ids = self.env['career.zone'].search(
                [('name', '=ilike', row['zone'].strip()),
                    ('country_id', '=', country_origin_id.id),
                    ('city_id','=',city_origin_id.id)], limit=1, order="id ASC")
            career_zone_id = 0
            if len(zone_ids) > 0:
                career_zone_id = zone_ids
            else:
                career_zone_id = self.env['career.zone'].create({'name': row['zone'].strip(), 'city_id': city_origin_id.id, 'country_id': country_origin_id.id})
        
        career_type_ids = self.env['hr.vehicle.type'].search(
            [('code', '=', "_".join(row['career_type'].lower().split()))
                ], limit=1, order="id ASC")
        career_type_id = 0
        if len(career_type_ids) > 0:
            career_type_id = career_type_ids
        else:
            career_type_id = self.env['hr.vehicle.type'].create({'code': "_".join(row['career_type'].lower().split()), 'name': row['career_type'].strip(), 'description': row['career_type'].strip()})
        
        if row['pax'].strip() == "":
            career_pax_id = False
        else:
            career_pax_ids = self.env['career.pax'].search(
                [('code', '=', "_".join(row['pax'].lower().split()))
                    ], limit=1, order="id ASC")
            career_pax_id = 0
            if len(career_pax_ids) > 0:
                career_pax_id = career_pax_ids
            else:
                career_pax_id = self.env['career.pax'].create({'code': "_".join(row['pax'].lower().split()), 'name': row['pax'].strip()})
            
        #row['city_origin'], row['city_destiny'], row['origin'], row['is_origin_airport'],
        #            row['zone'], row['destiny'], row['is_destiny_airport'], row['mpc_price'],
        #            row['km'], row['mpc_price_km'], row['career_type'],
        #            row['pax'], row['product_type']
        
        row['mpc_price'] = row['mpc_price'].replace(",", ".")
        
        conditions = [('country_origin_id', '=', country_origin_id.id),
                            ('country_destiny_id', '=', country_destiny_id.id),
                            ('city_origin_id', '=', city_origin_id.id),
                            ('city_destiny_id', '=', city_destiny_id.id),
                            ('career_origin', '=', career_origin_id.id),
                            ('career_destiny', '=', career_destiny_id.id),
                            ('list_price', '=', row['mpc_price'].strip()),
                            ('career_type', '=', career_type_id.id),
                            ('is_mpc_product', '=', True),
                        ]
                        
        if career_zone_id:
            conditions.append(('career_zone', '=', career_zone_id.id))
        if career_pax_id:
            conditions.append(('career_pax', '=', career_pax_id.id))
        if row['km'].strip() != "":
            row['km'] = row['km'].replace(",", ".")
            conditions.append(('km', '=', row['km'].strip()))
        if row['mpc_price_km'].strip() != "":
            row['mpc_price_km'] = row['mpc_price_km'].replace(",", ".")
            conditions.append(('mpc_price_km', '=', row['mpc_price_km'].strip()))

        product_template_ids = self.env['product.template'].search(
            conditions, limit=1, order="id ASC")

        product_name = "Service from city " + city_origin_id.name + " in " + country_origin_id.name + \
            " to city " + city_destiny_id.name + " in " + country_destiny_id.name + \
            ". Origin: " + career_origin_id.name + \
            ", Destiny: " + career_destiny_id.name + "."

        if career_pax_id:
            product_name = product_name + " " + career_pax_id.name + "."
            
        if career_zone_id:
            product_name = product_name + " " + career_zone_id.name + "."
        
        product_name = product_name + " Career type: " + career_type_id.name + "."
            
        if len(product_template_ids) > 0:
            raise AccessError('ERROR: ' + product_name)
        
        dictionary = {'name': product_name,
                            'country_origin_id': country_origin_id.id,
                            'country_destiny_id': country_destiny_id.id,
                            'city_origin_id': city_origin_id.id,
                            'city_destiny_id': city_destiny_id.id,
                            'career_origin': career_origin_id.id,
                            'career_destiny': career_destiny_id.id,
                            'list_price': row['mpc_price'].strip(),
                            'standard_price': row['mpc_price'].strip(),
                            'career_type': career_type_id.id,
                            'is_mpc_product': True}
        
        if career_zone_id:
            dictionary['career_zone'] = career_zone_id.id
        if career_pax_id:
            dictionary['career_pax'] = career_pax_id.id
        if row['km'].strip() != "":
            row['km'] = row['km'].replace(",", ".")
            dictionary['km'] = row['km'].strip()
        if row['mpc_price_km'].strip() != "":
            row['mpc_price_km'] = row['mpc_price_km'].replace(",", ".")
            dictionary['mpc_price_km'] = row['mpc_price_km'].strip()
            
        print str(dictionary)
    
        self.env['product.template'].create(dictionary)
        
        #print(city_origin_id.id, city_destiny_id.id, career_origin_id.id, career_destiny_id.id, career_zone_id.id, career_type_id.id, career_pax_id.id)

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
                string = string + row['country_origin'] + "; " + row['country_destiny'] + "; " + row['city_origin'] + "; " + row['city_destiny'] + "; " + row['origin'] + "; " + row['is_origin_airport'] + \
                    "; " + row['zone'] + "; " + row['destiny'] + "; " + row['is_destiny_airport'] + "; " + row['mpc_price'] + \
                    "; " + row['km'] + "; " + row['mpc_price_km'] + "; " + row['career_type'] + \
                    "; " + row['pax'] + "; " + row['product_type'] + "\n"
        
        #print csvfile_path
        
        remove(csvfile_path)
        
        #raise AccessError('Here is the message: ' + string)
        
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
