# Copyright 2024 Scalizer (<https://www.scalizer.fr>)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
{
    'name': 'Scalizer CRM Tag Partner Category',
    'version': '16.0.1.0.0',
    'author': 'Scalizer',
    'website': 'https://www.scalizer.fr',
    'summary': "Synchronize partner category and crm tag",
    'sequence': 0,
    'license': 'LGPL-3',
    'depends': [
        'sales_team',
        'crm',
    ],
    'category': 'Generic Modules/Scalizer',
    'complexity': 'easy',
    'description': '''
This module allows to synchronize partner category and crm tag
    ''',
    'qweb': [
    ],
    'demo': [
    ],
    'images': [
    ],
    'data': [
        'views/crm_tag_views.xml',
        'views/partner_category_views.xml',
    ],
    'auto_install': False,
    'installable': True,
    'application': False,
}
