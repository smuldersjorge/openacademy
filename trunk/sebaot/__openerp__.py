# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
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
##############################################################################
{
    'name' : 'Sebaot',
    'version' : '1.0',
    'author' : 'Cubic ERP SAC',
    'category' : 'Insurance',
    'description' : """
Modulo de Integración con SEBAOT
====================================

Modulo de integación de polizas y siniestros
    """,
    'website': 'https://www.regionalseguros.com.py',
    'images' : [],
    'depends' : ['crm','sale','project_issue'],
    'data': ["sebaot_view.xml",'security/groups.xml','security/ir.model.access.csv',
    ],
    'qweb' : [
    ],
    'demo': [
    ],
    'test': [
    ],
    'installable': True,
    'auto_install': False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: