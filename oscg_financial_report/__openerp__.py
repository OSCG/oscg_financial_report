# -*- encoding: utf-8 -*-

{
    'name': 'OSCG Financial Report',
    'version': '1.0',
    "category" : "Accounting & Finance",
    'description': """
OSCG Financial Report -Aeroo
==========================

This module is specially designed Excel or PDF Financial report for odoo.
It uses the existing PDF version of the odoo function, and it's more flexible than original PDF version.
There are all kinds of report format, single statements may only support a particular printing format, brought enterprise restriction and inconvenience.
OSCG designed this report in order to solve this problem.
The aim of this project is to provide a professional, the financial statements of the official way of printing.

It supports:
------------
System will generate an Excel version of the reports.

User Instructions
------------
If you want to use the report module, users should install Aeroo module in the server and OpenERP as well as Openoffice related plug-in.
If you need some helps, contact us(http://www.oscg.com.hk/).

* If you installed this module, the next step is that you should be go to Settings for the configuration of Aeroo.
  --Settings-->Technical(Aeroo reports).

* If the module install successful, it will show the report name on the report list view.
  There are two ways to adds the print button
  --Method 1 (list View): Tick the report name what you want to print, and click 'More' button to add.
  --Method 2 (Form View): Click the report name and enter into form view, you also can directly click 'More' to add print button  

* After the above procedures, the print button will be shown in the Accounting module.
  --Accounting-->Reporting-->Legal Reports-->Accounting Reports-->OSCG Financial Report.

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

