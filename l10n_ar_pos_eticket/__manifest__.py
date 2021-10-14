# -*- coding: utf-8 -*-
{
    "name": "POS eticket",
    "version": "14.0.1.0.0",
    "author": "Juan Manuel De Castro Pronexo.com",
    "license": "LGPL-3",
    "sequence": 14,
    "category": "Point Of Sale",
    "website": "https://www.pronexo.com",
    "depends": ["point_of_sale", "l10n_ar"],
    "data": [
        "views/pos_eticket_ar.xml",
        "views/pos_config.xml",
    ],
    "qweb": [
        "static/src/xml/pos_ticket.xml",
    ],
    "installable": True,
}
