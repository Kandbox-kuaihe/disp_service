# -*- coding: utf-8 -*-
{
    "name": "Disp Service",
    "summary": "To improve efficiency in retail and service delivery, we provide AI solution in inventory optimization, service dispatching.",
    "version": "18.0.1.0.0",
    "category": "Industries",
    "website": "https://www.kuaihe.tech/",
    "author": "kuai he",
    "license": "LGPL-3",
    'support': 'sales@kuaihe.tech',
    "depends": [
        'base',
        'web',
        'auth_signup',
        'hr',
    ],
    'auto_install': False,
    'application': True,
    'images': ['static/description/banner.png'],
    "data": [
        'security/ir.model.access.csv',
        'views/disp_menuitem.xml',
        'views/disp_config_views.xml',
        'views/disp_user_views.xml',
        'views/disp_iframe_action.xml',
    ],



}
