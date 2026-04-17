{
    'name': 'S6R CRM Sharing',
    'version': '19.0.1.0.2',
    'author': 'Scalizer',
    'depends': ['project', 'website_crm_partner_assign'],
    'data': [
        'security/ir.model.access.csv',
        'views/crm_sharing_views.xml',
        'templates/crm_sharing_templates.xml',
    ],
    'assets': {
        'project.webclient': [
            's6r_crm_sharing/static/src/**/**/*',
        ],
    },
    'installable': True,
    'license': 'LGPL-3',
}
