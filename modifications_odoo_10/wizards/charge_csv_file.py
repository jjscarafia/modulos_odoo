# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging

from odoo import api, fields, models
from odoo import tools, _
from odoo.exceptions import ValidationError
from odoo.modules.module import get_module_resource

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


    def charge_csv_file(self):
        print self.csv_file
        #raise Warning('Here is the message')
        raise except_orm('Warning','Here is the message')
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
