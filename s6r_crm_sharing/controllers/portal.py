import datetime
from collections import OrderedDict

from odoo import fields, http
from odoo.tools import config  # [MIG]: odoo.conf module removed in v19, server_wide_modules now via config
from odoo.http import request
from odoo.addons.website_crm_partner_assign.controllers.main import WebsiteAccount

from odoo.tools.translate import _

class CrmSharingPortal(WebsiteAccount):

    def _prepare_crm_sharing_session_info(self):
        session_info = request.env['ir.http'].session_info()
        user_context = request.env.context
        mods = config['server_wide_modules'] or []
        lang = user_context.get("lang")
        translation_hash = request.env['ir.http']._get_web_translations_hash(mods, lang)
        cache_hashes = {
            "translations": translation_hash,
        }

        company = request.env.company

        session_info.update(
            cache_hashes=cache_hashes,
            active_id=False,
            active_model='crm.lead',
            action_name='s6r_crm_sharing.crm_lead_action_sharing',
            user_companies={
                'current_company': company.id,
                'allowed_companies': {
                    company.id: {
                        'id': company.id,
                        'name': company.name,
                    },
                },
            },
            currencies=request.env['res.currency'].get_all_currencies(),
        )
        return session_info

    @http.route(['/my/opportunities', '/my/opportunities/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_opportunities(self, page=1, date_begin=None, date_end=None, sortby=None, filterby=None, **kw):
        return request.render("s6r_crm_sharing.crm_sharing_portal", {'page_name': 'opportunity'})

    @http.route("/my/opportunities/crm_sharing", type="http", auth="user", methods=['GET'])
    def render_crm_backend_view(self):
        return request.render(
            's6r_crm_sharing.crm_sharing_embed',
            {'session_info': self._prepare_crm_sharing_session_info()},
        )
