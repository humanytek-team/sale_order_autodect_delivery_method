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

{
    'name': "Autodetect the delivery method cheaper in sale orders.",
    'description': """
    Adds onchange method to the model sale.order to detect changes in lines of
    sale orders and autodetect the delivery method cheaper.
    """,
    'author': "Humanytek",
    'website': "http://www.humanytek.com",
    'category': 'Stock',
    'version': '0.1.0',
    'depends': ['delivery', ],
    'data': [
    ],
    'demo': [
    ],
}
