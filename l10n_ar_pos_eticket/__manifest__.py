# -*- coding: utf-8 -*-
{
    "name": "POS eticket",
    "version": "14.0.1.0.1",
    "license": "LGPL-3",
    "sequence": 14,
    "category": "Point Of Sale",
    "author": "Quilsoft, Juan Manuel De Castro Pronexo.com",
    "website": "https://www.quilsoft.com",
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
