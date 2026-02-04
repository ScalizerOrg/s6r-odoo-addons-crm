{
    'name': 'S6R CRM Sharing',
    'version': '16.0.1.0.0',
    'author': 'Scalizer',
    'depends': ['project', 'crm', 'portal'],
    'data': [
        'views/crm_sharing_views.xml',
        'templates/crm_sharing_templates.xml',
    ],
    'assets': {
        'project.webclient': [
            's6r_crm_sharing/static/src/crm_sharing/**/*',
        ],
    },
    'installable': True,
    'license': 'LGPL-3',
}
