# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2015 DevIntelle Consulting Service Pvt.Ltd (<http://www.devintellecs.com>).
#
#    For Module Support : devintelle@gmail.com  or Skype : devintelle
#
##############################################################################

from odoo import models, fields, api


class PurchaseOrderRevision(models.Model):
    _name = 'purchase.order.revision'
    _description = 'Link between Purchase Order and Purchase Revisions'

    parent_purchase_id = fields.Many2one('purchase.order', string='Purchase')
    revision_id = fields.Many2one('purchase.order', string='Name')
    user_id = fields.Many2one('res.users', string='Revision User')


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    purchase_revision_ids = fields.One2many('purchase.order.revision', 'parent_purchase_id', string="Order History")
    purchase_revision_count = fields.Integer(compute='_find_len')

    def _find_len(self):
        self.purchase_revision_count = len(self.purchase_revision_ids.ids)

    def create_purchase_order_revision(self):
        new_purchase_id = self.copy()
        uid_id = self.env.user.id
        self.env['purchase.order.revision'].create(
            {'revision_id': new_purchase_id.id,
             'user_id': uid_id,
             'parent_purchase_id': self.ids[0]
             })
        new_purchase_id.name = self.name + ' - R' + str(len(self.purchase_revision_ids.ids))
        new_purchase_id.origin = self.name

        action = self.env.ref('purchase.purchase_form_action').read()[0]
        if new_purchase_id:
            action['views'] = [(self.env.ref('purchase.purchase_order_form').id, 'form')]
            action['res_id'] = new_purchase_id.ids[0]
        else:
            action = {'type': 'ir.actions.act_window_close'}
        return action

    def view_purchase_order_revision(self):
        action = self.env.ref('purchase.purchase_form_action').read()[0]
        purchase_revision_ids = self.mapped('purchase_revision_ids.revision_id')
        if len(purchase_revision_ids) > 1:
            action['domain'] = [('id', 'in', purchase_revision_ids.ids)]
        elif purchase_revision_ids:
            action['views'] = [
                (self.env.ref('purchase.purchase_order_form').id, 'form')]
            action['res_id'] = purchase_revision_ids.id
        return action

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
