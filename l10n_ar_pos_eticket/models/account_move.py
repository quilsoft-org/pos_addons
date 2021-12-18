# -*- coding: utf-8 -*-
import base64

from odoo import fields, models
import logging
_logger = logging.getLogger(__name__)


class accountMove(models.Model):
    _inherit = "account.move"

    l10n_ar_afip_qr_image = fields.Binary(
        string='image',
        compute="compute_qr_image"
    )

    def compute_qr_image(self):
        for move_id in self:
            if move_id.l10n_ar_afip_qr_code:
                barcode = self.env['ir.actions.report'].barcode(
                    'QR',
                    move_id.l10n_ar_afip_qr_code,
                    width=180,
                    height=180
                )
                move_id.l10n_ar_afip_qr_image = base64.b64encode(barcode)
            else:
                move_id.l10n_ar_afip_qr_image = False
