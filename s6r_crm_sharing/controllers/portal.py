import datetime
from collections import OrderedDict

from odoo import fields, http, conf
from odoo.http import request
from odoo.addons.website_crm_partner_assign.controllers.main import WebsiteAccount

from odoo.tools.translate import _

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
    def portal_my_opportunities(self, page=1, date_begin=None, date_end=None, sortby=None, filterby=None, **kw):
        values = self._prepare_portal_layout_values()
        CrmLead = request.env['crm.lead']
        domain = self.get_domain_my_opp(request.env.user)

        today = fields.Date.today()
        this_week_end_date = fields.Date.to_string(fields.Date.from_string(today) + datetime.timedelta(days=7))

        searchbar_filters = {
            'all': {'label': _('Active'), 'domain': []},
            'today': {'label': _('Today Activities'), 'domain': [('activity_date_deadline', '=', today)]},
            'week': {'label': _('This Week Activities'),
                     'domain': [('activity_date_deadline', '>=', today), ('activity_date_deadline', '<=', this_week_end_date)]},
            'overdue': {'label': _('Overdue Activities'), 'domain': [('activity_date_deadline', '<', today)]},
            'won': {'label': _('Won'), 'domain': [('stage_id.is_won', '=', True)]},
            'lost': {'label': _('Lost'), 'domain': [('active', '=', False), ('probability', '=', 0)]},
        }
        searchbar_sortings = {
            'date': {'label': _('Newest'), 'order': 'create_date desc'},
            'name': {'label': _('Name'), 'order': 'name'},
            'contact_name': {'label': _('Contact Name'), 'order': 'contact_name'},
            'revenue': {'label': _('Expected Revenue'), 'order': 'expected_revenue desc'},
            'probability': {'label': _('Probability'), 'order': 'probability desc'},
            'stage': {'label': _('Stage'), 'order': 'stage_id'},
        }

        if not sortby:
            sortby = 'date'
        order = searchbar_sortings[sortby]['order']
        if not filterby:
            filterby = 'all'
        domain += searchbar_filters[filterby]['domain']
        if filterby == 'lost':
            CrmLead = CrmLead.with_context(active_test=False)

        if date_begin and date_end:
            domain += [('create_date', '>', date_begin), ('create_date', '<=', date_end)]
        opp_count = CrmLead.search_count(domain)
        pager = request.website.pager(
            url="/my/opportunities",
            url_args={'date_begin': date_begin, 'date_end': date_end, 'sortby': sortby, 'filterby': filterby},
            total=opp_count,
            page=page,
            step=self._items_per_page
        )
        opportunities = CrmLead.search(domain, order=order, limit=self._items_per_page, offset=pager['offset'])

        values.update({
            'date': date_begin,
            'opportunities': opportunities,
            'page_name': 'opportunity',
            'default_url': '/my/opportunities',
            'pager': pager,
            'searchbar_sortings': searchbar_sortings,
            'sortby': sortby,
            'searchbar_filters': OrderedDict(sorted(searchbar_filters.items())),
            'filterby': filterby,
            'session_info': self._prepare_crm_sharing_session_info()
        })
        return request.render("s6r_crm_sharing.crm_sharing_embed", values)
