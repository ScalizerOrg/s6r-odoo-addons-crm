# Copyright 2024 Scalizer (<https://www.scalizer.fr>)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0.html).

from odoo import api, models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'

    def write(self, vals):
        if self.env.context.get('synchronize_partner_tag'):
            return super(ResPartner, self).write(vals)
        res = False
        for rec in self:
            remove_ids = []
            if vals.get('category_id'):
                val_tag_ids = vals.get('category_id', [])
                for val_tag_id in val_tag_ids:
                    if val_tag_id[0] == 3:
                        remove_ids.append(val_tag_id[1])
                    elif val_tag_id[0] == 5:
                        remove_ids.extend(rec.category_id.ids)
                    elif val_tag_id[0] == 6:
                        remove_ids.extend([tag_id for tag_id in rec.category_id.ids if tag_id not in val_tag_id[2]])
                    if remove_ids:
                        rec.remove_leads_tags(remove_ids)
            res = super(ResPartner, rec).write(vals)
            rec.update_leads_tags(remove_ids)
        return res

    @api.model_create_multi
    def create(self, vals_list):
        res = super(ResPartner, self).create(vals_list)
        res.update_leads_tags()
        return res

    def update_leads_tags(self, removed_ids=[]):
        for partner in self:
            lead_ids = self.env['crm.lead'].search([('partner_id', '=', partner.id)])
            if not lead_ids:
                continue
            category_ids = partner.category_id.filtered(lambda t: t.synchronize_with_lead)
            for category_id in [c for c in category_ids if c.id not in removed_ids]:
                crm_tag_id = self.env['crm.tag'].search([('name', '=', category_id.name)], limit=1)
                if not crm_tag_id:
                    crm_tag_id = self.env['crm.tag'].create({'name': category_id.name,
                                                            'color': category_id.color})

                for lead_id in lead_ids:
                    if crm_tag_id not in lead_id.tag_ids:
                        lead_id.with_context(synchronize_lead_tag=True).write({'tag_ids': [(4, crm_tag_id.id)]})

    def remove_leads_tags(self, ids):
        lead_ids = self.env['crm.lead'].search([('partner_id', '=', self.id)])
        if not lead_ids:
            return
        for tag_id in self.env['res.partner.category'].browse(ids):
            if tag_id.synchronize_with_lead:
                crm_tag_id = self.env['crm.tag'].search([('name', '=', tag_id.name)], limit=1)
                for lead_id in lead_ids:
                    if crm_tag_id in lead_id.tag_ids:
                        lead_id.with_context(synchronize_lead_tag=True).write({'tag_ids': [(3, crm_tag_id.id)]})
