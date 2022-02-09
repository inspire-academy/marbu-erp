# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from datetime import datetime,date, timedelta
from io import BytesIO,StringIO
from odoo.tools.float_utils import float_compare, float_is_zero, float_round



class LineInventoryUpdate(models.Model):
	_inherit = 'stock.inventory.line'

	invline_remark = fields.Char('Remark')


