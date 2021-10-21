# -*- coding: utf-8 -*-
#    Copyright (C) 2007  pronexo.com  (https://www.pronexo.com)
#    All Rights Reserved.
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
############################################################################## # 
from odoo import models, api, fields
from odoo.exceptions import UserError


import logging
_logger = logging.getLogger(__name__)


class PosOrderReturn(models.Model):
    _inherit = 'pos.order'

    refund_from_order_id = fields.Many2one(
        'pos.order',
        string='Field Label',
    )
    return_ref = fields.Char(string='Return Ref', readonly=True, copy=False)
    return_status = fields.Selection([
        ('nothing_return', 'Nothing Returned'),
        ('partialy_return', 'Partialy Returned'),
        ('fully_return', 'Fully Returned')
    ], string="Return Status", default='nothing_return',
        readonly=True, copy=False, help="Return status of Order")

    @api.model
    def get_lines(self, ref):
        result = []
        order_id = self.search([('pos_reference', '=', ref)], limit=1)
        if order_id:
            lines = self.env['pos.order.line'].search([('order_id', '=', order_id.id)])
            for line in lines:
                if line.qty - line.returned_qty > 0:
                    new_vals = {
                        'product_id': line.product_id.id,
                        'product': line.product_id.name,
                        'qty': line.qty - line.returned_qty,
                        'price_unit': line.price_unit,
                        'discount': line.discount,
                        'line_id': line.id,
                    }
                    result.append(new_vals)

        return [result]

    def _order_fields(self, ui_order):
        order = super(PosOrderReturn, self)._order_fields(ui_order)
        if 'return_ref' in ui_order.keys() and ui_order['return_ref']:
            order['return_ref'] = ui_order['return_ref']
            for line in ui_order['lines']:
                if 'line_id' not in line[2] or not line[2]['line_id']: 
                    raise UserError("No puede mezclar devoluciones y ventas")
            parent_order = self.search([('pos_reference', '=', ui_order['return_ref'])], limit=1)

            updated_lines = ui_order['lines']
            ret = 0
            qty = 0
            for uptd in updated_lines:
                line = self.env['pos.order.line'].search([('order_id', '=', parent_order.id),
                                                          ('id', '=', uptd[2]['line_id'])], limit=1)
                if line:
                    line.returned_qty += -(uptd[2]['qty'])
            for line in parent_order.lines:
                qty += line.qty
                ret += line.returned_qty
            if qty-ret == 0:
                if parent_order:
                    parent_order.return_status = 'fully_return'
            elif ret:
                if qty > ret:
                    if parent_order:
                        parent_order.return_status = 'partialy_return'

        return order

    def _prepare_invoice_vals(self):
        vals = super()._prepare_invoice_vals()
        order = self.env['pos.order']
        if self.return_ref:
            order = self.search([('pos_reference', '=', self.return_ref)])

        if len(order) and order.account_move:
            vals['reversed_entry_id'] = order.account_move.id
        return vals

    """def _create_invoice(self, move_vals):

        # TODO: si quiero validar sin factura uso return self.env['account.move']

        new_move = super()._create_invoice(move_vals)

        return new_move"""


class PosOrderLineReturn(models.Model):
    _inherit = 'pos.order.line'

    returned_qty = fields.Integer(string='Returned Qty', digits=0, readonly=True)
