# Copyright 2024 Scalizer (<https://www.scalizer.fr>)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0.html).

from odoo import api, models, fields


class PartnerCategory(models.Model):
    _inherit = 'res.partner.category'

    synchronize_with_lead = fields.Boolean('Synchronize with Lead', default=False)
