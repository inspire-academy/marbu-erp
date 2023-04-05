# Fixed/Percentage discount on Purchase Order Lines
# Copyright (c) 2021 Sayed Hassan (sh-odoo@hotmail.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)

from odoo import api, fields, models


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    fixed_discount = fields.Float(string="Fixed Disc.", digits="Product Price", default=0.000)

    discount = fields.Float(string='% Disc.', digits='Discount', default=0.000)
    
    @api.onchange("fixed_discount")
    def _onchange_fixed_discount(self):
        for line in self:
            if line.fixed_discount != 0:
                self.discount = 0.0
                discount = ((self.product_qty * self.price_unit) - ((self.product_qty * self.price_unit) - self.fixed_discount)) / (self.product_qty * self.price_unit) * 100 or 0.0
                line.update({"discount": discount})
            if line.fixed_discount == 0:
                discount = 0.0
                line.update({"discount": discount})

    @api.onchange("discount")
    def _onchange_discount(self):
        for line in self:
            if line.discount != 0:
                self.fixed_discount = 0.0
                fixed_discount = round((line.price_unit * line.product_qty) * (line.discount / 100.0))
                line.update({"fixed_discount": fixed_discount})
            if line.discount == 0:
                fixed_discount = 0.000
                line.update({"fixed_discount": fixed_discount})

    def _prepare_compute_all_values(self):
        # Hook method to returns the different argument values for the
        # compute_all method, due to the fact that discounts mechanism
        # is not implemented yet on the purchase orders.
        # This method should disappear as soon as this feature is
        # also introduced like in the sales module.
        self.ensure_one()
        price_unit_w_discount = self.price_unit
        if self.discount != 0:
            #price_unit_w_discount = self.price_unit * (1 - (self.discount / 100.0))
            price_unit_w_discount = self.price_unit - (self.fixed_discount /self.product_qty)

        return {
            'price_unit': price_unit_w_discount,
            'currency_id': self.order_id.currency_id,
            'product_qty': self.product_qty,
            'product': self.product_id,
            'partner': self.order_id.partner_id,
        }

class PurchaseMonetaryInherit(models.Model):
    _inherit = 'purchase.order'

    discounts = fields.Monetary(string='Total Product Discount Fixed Amount', readonly=True)
    discount_in_percentage = fields.Monetary(string='DiscIn(%) ', readonly=True)
    discs_price = fields.Float(string='Total Product Discount Percentage Equal Price', readonly=True)
    amount_total = fields.Float(String='Total', compute='_get_sum')
    discounted_price = fields.Float(string='Discounted Price')
    amount_untaxed = fields.Monetary(string='Untaxed_Amount')
    amount_tax = fields.Monetary(string='Taxes')
    extra_discount_in_price = fields.Monetary(string='Order Discount Fixed Amount')
    extra_discount_percentage = fields.Float(string='Order Discount Fixed Percentage', readonly=False)
    ex_disc_price = fields.Monetary(string='Order Discount Fixed Amount')
    ex_disc_perc = fields.Monetary(string='Order Discount Fixed percentage')
    ex_dis_perc_eql_price = fields.Monetary(string='Order Discount Fixed Percentage Equal Amount')

    def _get_sum(self):
        for disc in self:
            disc.discounted_price = disc.amount_untaxed * (disc.discount_in_percentage / 100) * 100

        for rec in self:
            rec.amount_total = rec.amount_untaxed + rec.amount_tax - rec.discounts - rec.ex_disc_price - rec.ex_dis_perc_eql_price

    @api.depends('order_line.fixed_discount', 'order_line.discount', 'order_line')
    @api.onchange('order_line')
    def set_discount(self):
        self.discounts = 0
        self.discount_in_percentage = 0
        self.discs_price = 0

        for rec in self.order_line:
            self.discounts += rec.fixed_discount
            self.discount_in_percentage += rec.discount / 100
            self.discs_price += rec.fixed_discount

    @api.onchange('extra_discount_in_price')
    def _onchange_extra_discount_in_price(self):
        for rec in self:
            if rec.extra_discount_in_price != 0:
                rec.extra_discount_percentage = ((rec.amount_untaxed - (rec.amount_untaxed- rec.extra_discount_in_price)) / rec.amount_untaxed) * 100
            if rec.extra_discount_in_price == 0:
                rec.extra_discount_percentage = 0.0
            rec.ex_disc_perc = rec.extra_discount_percentage
            rec.ex_disc_price = rec.extra_discount_in_price            
            rec.amount_total = rec.amount_untaxed + rec.amount_tax - rec.ex_disc_price - rec.ex_dis_perc_eql_price

    @api.onchange("extra_discount_percentage")
    def _onchange_extra_discount_percentage(self):
       for rec in self:
            if rec.extra_discount_percentage != 0:
                rec.extra_discount_in_price = rec.amount_untaxed * rec.extra_discount_percentage/100
            if rec.extra_discount_percentage == 0:
                rec.extra_discount_in_price= 0.0
            rec.ex_disc_perc = rec.extra_discount_percentage
            rec.ex_disc_price = rec.extra_discount_in_price            
            rec.amount_total = rec.amount_untaxed + rec.amount_tax - rec.ex_disc_price - rec.ex_dis_perc_eql_price
    """@api.depends('extra_discount_in_price', 'extra_discount_percentage')
    @api.onchange('extra_discount_in_price', 'extra_discount_percentage')
    def get_extra(self):
        for rec in self:
            rec.ex_disc_perc = rec.extra_discount_percentage / 100
            rec.ex_disc_price = rec.extra_discount_in_price
            rec.ex_dis_perc_eql_price = (rec.amount_untaxed -rec.discs_price - rec.discounts) * (
                    rec.extra_discount_percentage / 100)
            rec.amount_total = rec.amount_untaxed + rec.amount_tax - rec.ex_disc_price - rec.ex_dis_perc_eql_price

    def _set_extra_disc(self):
        for ext in self:
            ext.ex_dis_perc_eql_price = (ext.amount_untaxed - ext.discs_price - ext.discounts) * (
                    ext.extra_discount_percentage / 100)
    """