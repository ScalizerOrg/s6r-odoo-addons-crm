from odoo import http
from odoo.http import request
from odoo.addons.website_crm_partner_assign.controllers.main import WebsiteAccount
from odoo import conf

class CrmSharingPortal(WebsiteAccount):

    def _prepare_crm_sharing_session_info(self):
        session_info = request.env['ir.http'].session_info()
        user_context = dict(request.env.context) if request.session.uid else {}
        mods = conf.server_wide_modules or []
        lang = user_context.get("lang")
        translation_hash = request.env['ir.http'].get_web_translations_hash(mods, lang)
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
            currencies=request.env['ir.http'].get_currencies(),
        )
        return session_info

    @http.route(['/my/opportunities', '/my/opportunities/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_opportunities(self, **kw):
        values = self._prepare_portal_layout_values()
        values['session_info'] = self._prepare_crm_sharing_session_info()
        return request.render("s6r_crm_sharing.crm_sharing_embed", values)
