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
from datetime import datetime

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

parameter = {
    # Folder:
    'folder_log': config.get('log', 'folder'),
    'folder_history': config.get('log', 'history'),
    'folder_temp': config.get('log', 'temp'),
    
    # Constant:
    'log_extension': 'log', # TODO put in cfg file?
    'tot_items': 4, #TODO put in cfg file?
    }

activity_file = config.get('log', 'activity')
activity_log = open(activity_file, 'a') 

# -----------------------------------------------------------------------------
# Utility:
# -----------------------------------------------------------------------------
def log_event(activity_log, event, mode='info'):
    ''' Log event on file
    '''
    activity_log.write('[%s] %s: %s\n' % (
        mode.lower(),
        datetime.now(),
        event,
        ))
    return True
    
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

def insert_odoo_record(erp_pool, f, parameter, temp=False):
    ''' Get file name (and mode: temp or not) and import as ODOO event, after
        put in history folder
        erp_pool: object ODOO on web
        f: filename (not full name)
        folder: dict of folder for manage: log, temp and history path
        temp: if f is yet a temp file
    ''' 
    # Check if is a .log file:
    if '.' not in f or f.split('.')[-1].lower() != parameter['log_extension']:
        return False # not a log file

    if temp:
        import_id = f        
        fulltemp = os.path.join(parameter['folder_temp'], import_id)

        # Delete import_id previous imported line:
        event_ids = erp_pool.search([
            ('import_id', '=', import_id),
            ])
        if event_ids:
            erp_pool.unlink(event_ids)
    else: # normale:
        import_ts_id = datetime.now().strftime('%Y%m%d.%H%M%S.%f')    
        fullname = os.path.join(parameter['folder_log'], f)    
        import_id = '%s.%s' % (import_ts_id, f)        
        fulltemp = os.path.join(parameter['folder_temp'], import_id)
        os.rename(fullname, fulltemp)
        
    # Read all temp file line:
    for line in open(fulltemp, 'r'):
        field_list = line.split(';')
        if len(field_list) != parameter['tot_items']:
            continue #TODO log
            
        # Read columns:            
        user_name = field_list[0].strip()
        host_name = field_list[1].strip()
        timestamp = field_list[2].strip() # GG/MM/AAAA HH:MM:SS
        mode = field_list[3].strip()
                    
        timestamp = '%s-%s-%s %s:%s:%s' % (
            timestamp[6:10],
            timestamp[3:5],
            timestamp[:2],
            timestamp[11:13],   
            timestamp[14:16],   
            timestamp[17:19],   
            )
        
        # Create ODOO record:
        erp_pool.create({
            'timestamp': timestamp, 
            'user_name': user_name, 
            'host_name' : host_name, 
            'mode' : mode,
            'import_id': import_id,
            })    
            
    # History the temp file:        
    fullhistory = os.path.join(parameter['folder_history'], import_id)
    os.rename(fulltemp, fullhistory)
    return True
    
# -----------------------------------------------------------------------------
# ERPPEEK Client connection:
# -----------------------------------------------------------------------------
URL = 'http://%s:%s' % (hostname, port) 
erp_pool = get_erp_pool(URL, database, username, password)

log_event(
    activity_log,
    'Start publish log event on %s' % URL,
    )
    
# -----------------------------------------------------------------------------
# Read temp folder
# -----------------------------------------------------------------------------
for root, folders, files in os.walk(parameter['folder_temp']):
    for f in files:
        insert_odoo_record(erp_pool, f, parameter, temp=True)
        log_event(
            activity_log,
            'Found temp files: %s' % f,
            'warning',
            )    
    break # only once!

# -----------------------------------------------------------------------------
# Read log folder
# -----------------------------------------------------------------------------
for root, folders, files in os.walk(parameter['folder_log']):
    for f in files:
        insert_odoo_record(erp_pool, f, parameter)
        log_event(
            activity_log,
            'Import log file: %s' % f,
            )    
    break # only once!

log_event(
    activity_log,
    'End publish log event on %s\n' % URL,
    )

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
