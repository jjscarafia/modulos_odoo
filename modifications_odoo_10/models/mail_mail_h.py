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

_logger = logging.getLogger(__name__)

class MailMail(models.Model):
    """ Model holding RFC2822 email messages to send. This model also provides
        facilities to queue and send new email messages.  """
    _inherit = 'mail.mail'
    
    is_user_uid = fields.Boolean('Is user UID', compute='_get_user_uid', search="_search_user_uid")
    
    def _get_user_uid(self):
        for record in self:
			res_user_ids = self.env['res.users'].search(
				[('id', '=', self.env.uid)]
			)
			if self.author_id == res_user_ids.partner_id.id:
				self.is_user_uid = True
			else:
				self.is_user_uid = False

    def _search_user_uid(self, operator, value):
		res_user_ids = self.env['res.users'].search(
			[('id', '=', self.env.uid)]
		)
		mail_mail_ids = self.env['mail.mail'].search(
			[('author_id', '=', res_user_ids.partner_id.id)]
		)
		return [('id', 'in', mail_mail_ids.ids)]
