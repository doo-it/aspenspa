# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

#-*- coding:utf-8 -*-
##############################################################################
#
#    SnippetBucket, MidSized Business Application Solution
#    Copyright (C) 2013-2014 http://snippetbucket.com/. All Rights Reserved.
#    Email: snippetbucket@gmail.com, Skype: live.snippetbucket
#
#
##############################################################################
{
    'name': "SB - Due Invoice Alerts",
    'summary': """SnippetBucket Due Invoice Alerts.""",
    'description': """
                    Due Invoice Alerts by snippetbucket
                    
                    Support: business@snipppetbucket.com
                    
                    Powered by: snippetbucket technologies, snippetbucket.com
                   """,
    'depends' : ['calendar','account','account_accountant'],
    'author': "SnippetBucket",
    'website': "https://snippetbucket.com/",
    'category': 'SnippetBucket',
    'version': '0.1',
    'data': [
            'sb_views/sb_views.xml',
    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
    'images': [],
   
    "license": 'Other proprietary',
}
