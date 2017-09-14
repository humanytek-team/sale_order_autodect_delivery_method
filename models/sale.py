# -*- coding: utf-8 -*-
###############################################################################
#
#    Odoo, Open Source Management Solution
#    Copyright (C) 2017 Humanytek (<www.humanytek.com>).
#    Manuel Márquez <manuel@humanytek.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################

import operator

from openerp import api, models

OPERATORS = {
    '==': operator.eq,
    '<=': operator.le,
    '<': operator.lt,
    '>=': operator.ge,
    '>': operator.gt,
}


class SaleOrder(models.Model):
    _inherit='sale.order'

    @api.onchange('order_line')
    def onchange_lines(self):
        total_weight = 0
        total_volume = 0
        for line in self.order_line:
            total_weight += line.product_id.weight * line.product_uom_qty
            total_volume += line.product_id.volume * line.product_uom_qty

        DeliveryCarrier = self.env['delivery.carrier']
        all_carriers = DeliveryCarrier.search([])

        order = self
        order_free_carriers = all_carriers.filtered(
            lambda carrier: carrier.free_if_more_than and
            order.amount_total >= carrier.amount and
            (order.partner_id.country_id in carrier.country_ids
            if carrier.country_ids else True) and
            (order.partner_id.state_id in carrier.state_ids
            if carrier.state_ids else True))

        if order_free_carriers:
            self.carrier_id = order_free_carriers[0]

        else:
            valids_carriers = all_carriers
            for carrier in valids_carriers:
                if carrier.delivery_type == 'base_on_rule':

                    apply_to_weight = False
                    apply_to_volume = False

                    carrier_has_rule_to_weight = any([
                        rule
                        for rule in carrier.price_rule_ids
                        if rule.variable == 'weight'])

                    carrier_has_rule_to_volume = any([
                        rule
                        for rule in carrier.price_rule_ids
                        if rule.variable == 'volume'])

                    if not carrier_has_rule_to_weight:
                        apply_to_weight = True

                    if not carrier_has_rule_to_volume:
                        apply_to_volume = True

                    if carrier_has_rule_to_volume or carrier_has_rule_to_weight:

                        for rule in carrier.price_rule_ids:

                            if rule.variable == 'weight':
                                if OPERATORS[rule.operator](
                                    total_weight, rule.max_value):
                                    apply_to_weight = True

                            if rule.variable == 'volume':
                                if OPERATORS[rule.operator](
                                    total_volume, rule.max_value):
                                    apply_to_volume = True

                    if not apply_to_weight or not apply_to_volume:
                        valids_carriers -= carrier

            if self.partner_id:
                customer_country = self.partner_id.country_id
                customer_state = self.partner_id.state_id

                for carrier in valids_carriers:

                    if carrier.country_ids:
                        if customer_country not in carrier.country_ids:
                            valids_carriers -= carrier

                    if carrier.state_ids:
                        if customer_state not in carrier.state_ids:
                            valids_carriers -= carrier

            if valids_carriers:

                valids_carriers_sorted =  valids_carriers.sorted(
                    key=lambda carrier: carrier.get_shipping_price_from_so(self)[0]
                    if carrier.delivery_type not in ['fixed', 'base_on_rule']
                    else carrier.get_price_available(self)
                    if self.company_id.currency_id.id ==
                    self.pricelist_id.currency_id.id
                    else self.company_id.currency_id.with_context(
                    date=self.date_order).compute(
                    carrier.get_price_available(self), self.pricelist_id.currency_id)
                )

                self.carrier_id = valids_carriers_sorted[0]
        
