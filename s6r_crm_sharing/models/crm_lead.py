# Copyright 2025 Scalizer (https://www.scalizer.fr)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import logging
import uuid

from odoo import api, fields, models, Command, _

_logger = logging.getLogger(__name__)

CRM_LEAD_READABLE_FIELDS = {
    'message_follower_ids',
    'access_token',
}

SELF_WRITABLE_FIELDS = {
    'message_follower_ids',
}

class CrmLead(models.Model):
    _inherit = 'crm.lead'

    access_token = fields.Char('Security Token', copy=False)

    def _portal_ensure_token(self):
        """ Get the current record access token """
        if not self.access_token:
            # we use a `sudo` here because the user may not have the rights to write on the record
            # but we need a token for the portal chatter to work
            self.sudo().write({'access_token': str(uuid.uuid4())})
        return self.access_token

    @property
    def SELF_READABLE_FIELDS(self):
        return super().SELF_READABLE_FIELDS | CRM_LEAD_READABLE_FIELDS | self.SELF_WRITABLE_FIELDS
