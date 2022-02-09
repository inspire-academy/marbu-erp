# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from datetime import datetime,date, timedelta
from io import BytesIO,StringIO
from odoo.tools.float_utils import float_compare, float_is_zero, float_round


class WizardInventoryAdjustment(models.TransientModel):
	_name = 'wizard.inventory.adjustment'

	inventory_date = fields.Date('Inventory BackDate',required=True)
	inventory_remark = fields.Char('Remark',required=True)
	inventory_id = fields.Many2one('stock.inventory',string="Inventory")



	def custom_backdateorder_button_inventoryadjust(self):
		if self.inventory_date >= date.today():
			raise UserError(_('Please Enter Correct Back Date'))

		custom_stock_inventory_ids = self.env['stock.inventory'].browse(self._context.get('active_id'))

		if custom_stock_inventory_ids:
			custom_stock_inventory_ids = custom_stock_inventory_ids
		else:
			custom_stock_inventory_ids = self.inventory_id

		custom_stock_inventory_ids.action_validate()

		jornal_id = self.env['account.journal'].search([('code', '=', 'MISC')])

		for custom_stock_inventory_ids1 in custom_stock_inventory_ids:
			custom_stock_inventory_ids1.write({'accounting_date':self.inventory_date})

			for custom_stock_inventory_ids3 in custom_stock_inventory_ids1.line_ids:
				custom_stock_inventory_ids3.write({'invline_remark':self.inventory_remark})

			for custom_stock_inventory_ids2 in custom_stock_inventory_ids1.move_ids:
				custom_stock_inventory_ids2.write({'date':custom_stock_inventory_ids1.accounting_date,
					'move_remark':self.inventory_remark})

				for custom_stock_inventory_ids4 in custom_stock_inventory_ids2.move_line_ids:
					custom_stock_inventory_ids4.write({'date':custom_stock_inventory_ids2.date,
						'move_remarks_line':self.inventory_remark})

					custom_accountmove = self.env['account.move'].create({'date':self.inventory_date,
						'journal_id':jornal_id.id,'stock_move_id':custom_stock_inventory_ids2.id})

					self.env['account.move.line'].create({'partner_id':3,'account_id':1,
						'name':'Transfer','move_id':custom_accountmove.id})

					custom_accountmove.post()

		return {
					'view_type': 'form',
					'view_mode': 'form',
					'res_model': 'stock.inventory',
					'type': 'ir.actions.act_window',
					'target': 'main',
					'res_id': custom_stock_inventory_ids1.id,
				}

