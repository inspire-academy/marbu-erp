# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from datetime import datetime,date, timedelta
from io import BytesIO,StringIO
from odoo.tools.float_utils import float_compare, float_is_zero, float_round

		


class StockInventoryUpdate(models.Model):
	_inherit = 'stock.inventory'


	def action_validate_custom(self):

		return {
					'view_type': 'form',
					'view_mode': 'form',
					'res_model': 'wizard.inventory.adjustment',
					'type': 'ir.actions.act_window',
					'target': 'new',
					'res_id': False,
					'context': {'default_inventory_id':self.id},
				}

