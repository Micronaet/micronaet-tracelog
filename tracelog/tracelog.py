# -*- coding: utf-8 -*-
###############################################################################
#
#    Copyright (C) 2001-2014 Micronaet SRL (<http://www.micronaet.it>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
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
import os
import sys
import logging
import odoo
from odoo.osv import fields, osv, expression, api
from datetime import timedelta
from odoo import tools


_logger = logging.getLogger(__name__)

class TracelogEvent(orm.Model):
    """ Model name: TracelogEvent
    """
    
    _name = 'tracelog.event'
    _description = 'Tracelog event'
    _rec_name = 'timestamp'
    _order = 'timestamp desc'
    
    # -------------------------------------------------------------------------
    # Columns:
    # -------------------------------------------------------------------------
    timestamp = fields.Datetime('Timestamp', required=True)
    user_name = fields.Char('Username', size=64, required=True)
    host_name = fields.Char('Hostname', size=64, required=True)
    import_id = fields.Char('Import ID', size=100, required=True)
    mode = fields.selection([
        ('in', 'Log in'),
        ('out', 'Log out'),
        ('err', 'Error'),
        ], 'Mode', required=True, default='err'),
        }
    
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
