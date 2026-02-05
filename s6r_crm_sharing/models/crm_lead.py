# Copyright 2025 Scalizer (https://www.scalizer.fr)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import logging
import uuid

from odoo import api, fields, models, Command, _
from odoo.exceptions import AccessError

_logger = logging.getLogger(__name__)

CRM_LEAD_READABLE_FIELDS = {
    'message_follower_ids',
    'access_token',
    'active',
    'campaign_id',
    'company_id',
    'contact_name',
    'description',
    'email_cc',
    'email_from',
    'expected_revenue',
    'kanban_state',
    'medium_id',
    'mobile',
    'name',
    'partner_id',
    'phone',
    'priority',
    'probability',
    'source_id',
    'stage_id',
    'tag_ids',
    'team_id',
    'type',
    'user_id',
    'user_company_ids',
}

SELF_WRITABLE_FIELDS = {
    'message_follower_ids',
    'description',
    'email_from',
    'expected_revenue',
    'kanban_state',
    'name',
    'partner_id',
    'phone',
    'priority',
    'probability',
    'tag_ids',
    'user_id',
}

class CrmLead(models.Model):
    _inherit = 'crm.lead'

    access_token = fields.Char('Security Token', copy=False)

    _mail_post_token_field = 'access_token'

    def _portal_ensure_token(self):
        """ Get the current record access token """
        if not self.access_token:
            # we use a `sudo` here because the user may not have the rights to write on the record
            # but we need a token for the portal chatter to work
            self.sudo().write({'access_token': str(uuid.uuid4())})
        return self.access_token

    @property
    def SELF_READABLE_FIELDS(self):
        try:
            base_fields = super().SELF_READABLE_FIELDS
        except AttributeError:
            base_fields = set()
        return base_fields | CRM_LEAD_READABLE_FIELDS | self.SELF_WRITABLE_FIELDS

    @property
    def SELF_WRITABLE_FIELDS(self):
        try:
            base_fields = super().SELF_WRITABLE_FIELDS
        except AttributeError:
            base_fields = set()
        return base_fields | SELF_WRITABLE_FIELDS

    @api.model_create_multi
    def create(self, vals_list):
        is_portal_user = self.env.user.has_group('base.group_portal')
        if is_portal_user:
            self.check_access_rights('create')
            for vals in vals_list:
                self._ensure_fields_write(vals)
        # We use sudo() here because the portal user might not have rights to all fields
        # or related records required during create (like project sharing does)
        # But we must check access rule after creation.
        leads = super(CrmLead, self.sudo() if is_portal_user else self).create(vals_list)
        if is_portal_user:
            leads.with_user(self.env.user).check_access_rule('create')
            for lead in leads:
                lead._portal_ensure_token()
        return leads

    def write(self, vals):
        if self.env.user.has_group('base.group_portal') and not self.env.su:
            self._ensure_fields_write(vals)
            self.check_access_rights('write')
            self.check_access_rule('write')
        return super(CrmLead, self).write(vals)

    def _ensure_fields_write(self, vals):
        unauthorized_fields = set(vals.keys()) - self.SELF_WRITABLE_FIELDS
        if unauthorized_fields:
            raise AccessError(_("You cannot write on %s fields in lead.") % ', '.join(unauthorized_fields))
