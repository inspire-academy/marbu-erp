# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2015 DevIntelle Consulting Service Pvt.Ltd (<http://www.devintellecs.com>).
#
#    For Module Support : devintelle@gmail.com  or Skype : devintelle
#
##############################################################################

{
    'name': 'Purchase Revision Number & history',
    'version': '14.0.1.0',
    'sequence': 1,
    'category': 'Purchases',
    'description':
        """
        This Module add below functionality into odoo

        1.Create multiple copies of purchase orders as revision and link revisions with main purchase order\n
        2.Navigate to revisions of purchase orders from main purchase order\n
Merge purchase order 
Odoo merge purchase order
Manage merge purchase order 
Odoo manage merge purchase order 
Odoo Merge Purchase Order application helps you to merge two or more Purchase Quotations of same vendor in new single Quotation.

Merge two or more Purchase Quotations, as new Purchase Quotation
odoo Merge two or more Purchase Quotations, as new Purchase Quotation

Once new Purchase Quotation is created, previously selected Quotations will be cancelled
Odoo 
Once new Purchase Quotation is created, previously selected Quotations will be cancelled
Merge PO 
Odoo Merge PO 
Manage merge PO
Odoo Managae merge PO 


    """,
    'summary': 'Odoo app will help to add Purchase Revision order of Purchase order, Purchase Revision,Purchase revision history, revision history, revise Purchase order, revise Purchase number, Purchase revision history, revision history',
    'depends': ['purchase'],
    'data': ['security/ir.model.access.csv',
             'views/purchase_views.xml'],
    'demo': [],
    'test': [],
    'css': [],
    'qweb': [],
    'js': [],
    'images': ['images/main_screenshot.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
    
    # author and support Details =============#
    'author': 'DevIntelle Consulting Service Pvt.Ltd',
    'website': 'http://www.devintellecs.com',    
    'maintainer': 'DevIntelle Consulting Service Pvt.Ltd', 
    'support': 'devintelle@gmail.com',
    'price':15.0,
    'currency':'EUR',
    #'live_test_url':'https://youtu.be/A5kEBboAh_k',
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
