# -*- encoding: utf-8 -*-

{
    'name': 'OSCG Financial Report',
    'version': '1.0',
    "category" : "Generic Modules/Report",
    'description': """
        twt report
     """,
    'author': 'OSCG',
    'depends': ['base','report_aeroo','account'],
    'init_xml': [

    ],
    'update_xml': [
        'group_data.xml',
        'oscg_financial.xml',
        'oscg_financial_report.xml',
        'security/ir.model.access.csv',
        
    ],
    'demo_xml': [],
    'installable': True,
    'active': False
}

