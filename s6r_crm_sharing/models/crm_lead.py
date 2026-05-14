# Copyright 2025 Scalizer (https://www.scalizer.fr)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import logging
import uuid

from odoo import api, fields, models, Command, _
from odoo.exceptions import AccessError

_logger = logging.getLogger(__name__)

CRM_LEAD_READABLE_FIELDS = frozenset({
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
})

# Adding a field here is the only safe way to extend portal write access — intentional allowlist.
SELF_WRITABLE_FIELDS = frozenset({
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
    'team_id',
})

class CrmLead(models.Model):
    _inherit = 'crm.lead'

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
            self.check_access('create')
            for vals in vals_list:
                self._ensure_fields_write(vals)
        leads = super(CrmLead, self.sudo() if is_portal_user else self).create(vals_list)
        return leads

    def write(self, vals):
        if self.env.user.has_group('base.group_portal') and not self.env.su:
            self._ensure_fields_write(vals)
        return super(CrmLead, self).write(vals)

    def _ensure_fields_write(self, vals):
        unauthorized_fields = set(vals.keys()) - self.SELF_WRITABLE_FIELDS
        if unauthorized_fields:
            raise AccessError(_("You cannot write on %s fields in lead.") % ', '.join(unauthorized_fields))
