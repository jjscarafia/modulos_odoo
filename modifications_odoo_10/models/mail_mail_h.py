# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import base64
import datetime
import logging
import psycopg2
import threading

from email.utils import formataddr

from odoo import _, api, fields, models
from odoo import tools
from odoo.addons.base.ir.ir_mail_server import MailDeliveryException
from odoo.tools.safe_eval import safe_eval

from openerp import SUPERUSER_ID

_logger = logging.getLogger(__name__)

class MailMail(models.Model):
    """ Model holding RFC2822 email messages to send. This model also provides
        facilities to queue and send new email messages.  """
    _inherit = 'mail.mail'
    
    is_user_my_emails_uid = fields.Boolean('My emails', compute='_get_user_received_uid', search="_search_user_received_uid")
    
    is_other_user_emails_uid = fields.Boolean('Other Emails', compute='_get_user_sent_uid', search="_search_user_sent_uid")
    
    def _get_user_received_uid(self):
        for record in self:
			res_user_ids = self.env['res.users'].search(
				[('id', '=', self.env.uid)]
			)
			emails_to = str(self.email_to).split()
			emails_cc = str(self.email_cc).split()
			
			if (res_user_ids.partner_id.email in emails_to or \
				res_user_ids.partner_id.email in emails_cc or \
				res_user_ids.partner_id.id in self.recipient_ids) and \
				self.state in ['received','sent']:
				self.is_user_uid = True
			else:
				self.is_user_uid = False

    def _search_user_received_uid(self, operator, value):
        ids=[]

        res_user_ids = self.env['res.users'].search(
            [('id', '=', self.env.uid)]
        )

        if self.env.uid == SUPERUSER_ID:
            if self.env.context.get("my_emails",False) == True:
                mail_mail_ids = self.env['mail.mail'].search(
                    ['|','|',('email_to', 'ilike', res_user_ids.partner_id.email),
                    ('email_cc', 'ilike', res_user_ids.partner_id.email),
                    ('recipient_ids', '=', res_user_ids.partner_id.id),
                    ('state', 'in', ['received','sent'])]
                )
            else:
                mail_mail_ids = self.env['mail.mail'].search(
                    [('state', 'in', ['received','sent'])]
                )
        else:
            mail_mail_ids = self.env['mail.mail'].search(
                ['|','|',('email_to', 'ilike', res_user_ids.partner_id.email),
                ('email_cc', 'ilike', res_user_ids.partner_id.email),
                ('recipient_ids', '=', res_user_ids.partner_id.id),
                ('state', 'in', ['received','sent'])]
            )
        
        ids = ids + mail_mail_ids.ids

        return [('id', 'in', ids)]
		
    def _get_user_sent_uid(self):
        for record in self:
			res_user_ids = self.env['res.users'].search(
				[('id', '=', self.env.uid)]
			)
			emails_to = str(self.email_to).split()
			emails_cc = str(self.email_cc).split()
			
			if (self.author_id.id == res_user_ids.partner_id.id or \
				self.email_from == res_user_ids.partner_id.email) and \
				self.state in ['outgoing','sent','exception','cancel']:
				self.is_user_uid = True
			else:
				self.is_user_uid = False

    def _search_user_sent_uid(self, operator, value):
        ids=[]

        res_user_ids = self.env['res.users'].search(
            [('id', '=', self.env.uid)]
        )

        if self.env.uid == SUPERUSER_ID:
            if self.env.context.get("my_emails",False) == True:
                mail_mail_ids = self.env['mail.mail'].search(
                    ['|',('author_id', '=', res_user_ids.partner_id.id),
                    ('email_from', '=', res_user_ids.partner_id.email),
                    ('state','in',['outgoing','sent','exception','cancel'])]
                )
            else:
                mail_mail_ids = self.env['mail.mail'].search(
                    [('state','in',['outgoing','sent','exception','cancel'])]
                )
        else:
            mail_mail_ids = self.env['mail.mail'].search(
                ['|',('author_id', '=', res_user_ids.partner_id.id),
                ('email_from', '=', res_user_ids.partner_id.email),
                ('state','in',['outgoing','sent','exception','cancel'])]
            )

        ids = ids + mail_mail_ids.ids

        return [('id', 'in', ids)]
		
    @api.onchange('author_id') # if these fields are changed, call method
    def check_change_employee(self):
        if self.author_id:
            self.email_from = self.author_id.email
