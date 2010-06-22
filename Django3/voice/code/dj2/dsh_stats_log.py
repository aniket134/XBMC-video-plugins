#!/usr/bin/python -u
#
# called by /etc/rc.local
# clears the outgoing spool. then reschedules.
#


import sys,logging,os,signal,subprocess,datetime,time
import dsh_agi,dsh_utils,dsh_config,dsh_bizarro,dsh_django2



#
# django-specific initializations.
#
os.environ['DJANGO_SETTINGS_MODULE'] = dsh_config.lookup(
    'DJANGO_SETTINGS_MODULE')
dsh_utils.add_to_sys_path(dsh_config.lookup('django_sys_paths'))
from dv2.db.models import Person,Organization,Item,Event
import dsh_django_utils,dsh_db_config,dsh_stats

    
    
def main():

    dsh_django2.init_log('dsh_stats_log.py: entered --------------------')
    sortBy = dsh_config.lookup('STATS_SORT_BY')

    success,response,totals = dsh_stats.stats_calculate(
        sortBy=sortBy, logAction='STT1', textLog=True)
    
    sys.exit(0)
    

    
if __name__ == '__main__':
    main()
