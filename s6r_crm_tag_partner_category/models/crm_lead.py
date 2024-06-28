# Copyright 2024 Scalizer (<https://www.scalizer.fr>)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0.html).

from odoo import api, models, fields
from odoo.fields import Command


def get_command(values):
    if isinstance(values[0], int):
        cmd = Command(values[0]).name
    else:
        cmd = values[0].name
    return cmd


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    def write(self, vals):
        if self.env.context.get('synchronize_lead_tag'):
            return super(CrmLead, self).write(vals)
        remove_ids = []
        for rec in self:
            remove_ids = []
            if vals.get('tag_ids') or vals.get('partner_id'):
                val_tag_ids = vals.get('tag_ids', [])
                for val_tag_id in val_tag_ids:
                    if get_command(val_tag_id) == 'UNLINK':
                        remove_ids.append(val_tag_id[1])
                    elif get_command(val_tag_id) == 'CLEAR':
                        remove_ids.extend(rec.tag_ids.ids)
                    elif get_command(val_tag_id) == 'SET':
                        remove_ids.extend([tag_id for tag_id in rec.tag_ids.ids if tag_id not in val_tag_id[2]])
                    if remove_ids:
                        rec.remove_partner_tags(remove_ids)
        res = super(CrmLead, self).write(vals)
        for rec in self:
            if vals.get('tag_ids'):
                if rec.partner_id:
                    rec.update_partner_tags(remove_ids)
                    rec.partner_id.update_leads_tags()
            if vals.get('partner_id'):
                if rec.partner_id and rec.partner_id.category_id:
                    rec.partner_id.update_leads_tags()
        return res

    @api.model_create_multi
    def create(self, vals_list):
        res = super(CrmLead, self).create(vals_list)
        res.update_partner_tags()
        if res.partner_id and res.partner_id.category_id:
            res.partner_id.update_leads_tags()
        return res

    def update_partner_tags(self, removed_ids=None):
        if not removed_ids:
            removed_ids = []
        for lead in self:
            if not lead.partner_id:
                continue
            tag_ids = lead.tag_ids.filtered(lambda t: t.synchronize_with_partner)
            for tag_id in [t for t in tag_ids if t.id not in removed_ids]:
                partner_category_id = self.env['res.partner.category'].search([('name', '=', tag_id.name)], limit=1)
                if not partner_category_id:
                    partner_category_id = self.env['res.partner.category'].create({'name': tag_id.name,
                                                                                   'color': tag_id.color})
                if partner_category_id not in lead.partner_id.category_id:
                    values = {'category_id': [(4, partner_category_id.id)]}
                    lead.partner_id.with_context(synchronize_partner_tag=True).write(values)

    def remove_partner_tags(self, ids):
        if not self.partner_id:
            return
        for tag_id in self.env['crm.tag'].browse(ids):
            if tag_id.synchronize_with_partner:
                partner_category_id = self.env['res.partner.category'].search([('name', '=', tag_id.name)], limit=1)
                if partner_category_id in self.partner_id.category_id:
                    values = {'category_id': [(3, partner_category_id.id)]}
                    self.partner_id.with_context(synchronize_partner_tag=True).write(values)
