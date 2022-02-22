# -*- coding: utf-8 -*-
##############################################################################
#
#    Global Creative Concepts Tech Co Ltd.
#    Copyright (C) 2018-TODAY iWesabe (<http://www.iwesabe.com>).
#    You can modify it under the terms of the GNU LESSER
#    GENERAL PUBLIC LICENSE (LGPL v3), Version 3.
#
#    It is forbidden to publish, distribute, sublicense, or sell copies
#    of the Software or modified copies of the Software.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU LESSER GENERAL PUBLIC LICENSE (LGPL v3) for more details.
#
#    You should have received a copy of the GNU LESSER GENERAL PUBLIC LICENSE
#    GENERAL PUBLIC LICENSE (LGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    sl_no = fields.Integer(string='Sl. No.', compute='_compute_serial_number', store=True)

    @api.depends('sequence', 'order_id')
    def _compute_serial_number(self):
        for order_line in self:
            if not order_line.sl_no:
                serial_no = 1
                for line in order_line.mapped('order_id').order_line:
                    if line.product_id:
                        line.sl_no = serial_no
                        serial_no += 1

class OrdinalNumber(models.Model):

    _inherit = 'account.move.line'

    number_sequence = fields.Integer(
        compute='_compute_get_number',
        store=True,
    )

    @api.depends('sequence', 'move_id')
    def _compute_get_number(self):
        for line_id in self:
            if not line_id.number_sequence:
                number_sequence = 1
                for invoice in self.mapped('move_id'):
                    for line in invoice.line_ids:
                        if line.product_id:
                            line.number_sequence = number_sequence
                            number_sequence += 1