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
import csv
import erppeek
import ConfigParser

# ----------------
# Read parameters:
# ----------------
config = ConfigParser.ConfigParser()
config.read(['odoo.mic.cfg'])

# -----------------------------------------------------------------------------
# Erpeek client ODOO:
# -----------------------------------------------------------------------------
erp = {}
for mode in ['in', 'out']:
    server = config.get(mode, 'server')
    port = config.get(mode, 'port')
    dbname = config.get(mode, 'dbname')
    user = config.get(mode, 'user')
    password = config.get(mode, 'pwd')
    
    erp[mode] = erppeek.Client(
        'http://%s:%s' % (
            server, port),
        db=dbname,
        user=user,
        password=password,
        )
    print 'Connect with ODOO %s: %s' % (mode, erp[mode])    

# -----------------------------------------------------------------------------
#                             Manual importation:
# -----------------------------------------------------------------------------
company_id = 1 # Micronaet

# -----------------------------------------------------------------------------
#                             Automatic migration:
# -----------------------------------------------------------------------------
# ------
# Event:
# ------
print 'Import Event'
pool_in = erp['in'].TracelogEvent
pool_out = erp['out'].TracelogEvent
record_ids = pool_in.search([])
print 'Tot selected %s' % len(record_ids)
update = False

i = 0
for record in pool_in.browse(record_ids):
    i += 1
    
    # Input:
    #timestamp = record.timestamp
    #host_name = record.host_name
    
    #item_ids = pool_out.search([
    #    ('timestamp', '=', timestamp),
    #    ('host_name', '=', host_name),
    #    ])
        
    data = {
        'timestamp': record.timestamp,
        'host_name': record.host_name,
        'user_name': record.user_name,
        'import_id': record.import_id,
        'mode': record.mode,
        }

    #if item_ids:
    #    item_id = item_ids[0]
    #    if update:
    #        pool_out.write(item_id, data)
    #    print '%s. Update record: %s' % (i, timestamp)
    #else:        
    item_id = pool_out.create(data).id
    print '%s. Create record' % i

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
