#!/usr/bin/python
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
import ConfigParser
import erppeek

# -----------------------------------------------------------------------------
#                                Parameters
# -----------------------------------------------------------------------------
# Extract config file name from current name
fullname = './openerp.cfg'
config = ConfigParser.ConfigParser()
config.read([fullname])

# -----------------------------------------------------------------------------
# Read from config file:
# -----------------------------------------------------------------------------
# XMLRPC connection data:
hostname = config.get('XMLRPC', 'host') 
port = eval(config.get('XMLRPC', 'port'))
database = config.get('XMLRPC', 'database')
username = config.get('XMLRPC', 'username')
password = config.get('XMLRPC', 'password')

log_folder = config.get('log', 'folder')
log_history = config.get('log', 'history')
activity_folder = config.get('log', 'activity')

log_extension = 'log' # TODO put in cfg file?
tot_items = 4 #TODO put in cfg file?
# -----------------------------------------------------------------------------
# Utility:
# -----------------------------------------------------------------------------
def get_erp_pool(URL, database, username, password):
    ''' Connect to log table in ODOO
    '''
    erp = erppeek.Client(
        URL,
        db=database,
        user=username,
        password=password,
        )   
    return erp.TracelogEvent

# -----------------------------------------------------------------------------
# ERPPEEK Client connection:
# -----------------------------------------------------------------------------
URL = 'http://%s:%s' % (hostname, port) 
erp_pool = get_erp_pool(URL, database, username, password)

# -----------------------------------------------------------------------------
# Read log folder
# -----------------------------------------------------------------------------
for root, folders, files in os.walk(log_folder): 
    for f in files:
        if '.' not in f or f.split('.')[-1].lower() != log_extension:
            continue #TODO log
        fullname = os.path.join(log_folder, f)    
        for line in open(fullname, 'r'):
            field_list = line.split(';')
            if len(field_list) != tot_items:
                continue #TODO log
            # Read columns:            
            user_name = field_list[0].strip()
            host_name = field_list[1].strip()
            timestamp = field_list[2].strip() # GG/MM/AAAA HH:MM:SS
            mode = field_list[3].strip()
            
            timestamp = '%s/%s/%s%s' % (
                timestamp[6:10],
                timestamp[3:5],
                timestamp[:2],
                timestamp[10:],              
                )
            
            erp_pool.create({
                'timestamp': timestamp, 
                'user_name': username, 
                'host_name' : host_name, 
                'mode' : mode,
                })
    break # only once!
                
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
