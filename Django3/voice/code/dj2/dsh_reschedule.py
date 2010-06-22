#!/usr/bin/python -u
#
# called by /etc/rc.local
# clears the outgoing spool. then reschedules.
#


import sys,logging,os,signal,subprocess,datetime,time
import dsh_agi,dsh_utils,dsh_config,dsh_bizarro,dsh_django2
import dsh_common_selection



#
# django-specific initializations.
#
os.environ['DJANGO_SETTINGS_MODULE'] = dsh_config.lookup(
    'DJANGO_SETTINGS_MODULE')
dsh_utils.add_to_sys_path(dsh_config.lookup('django_sys_paths'))
from dv2.db.models import Person,Organization,Item,Event
import dsh_django_utils,dsh_db_config

    
    
def main():

    dsh_django2.init_log('dv2/dsh_reschedule.py: entered --------------------')
    dsh_common_selection.reschedule_script_call(Person)
    sys.exit(0)
    

    
if __name__ == '__main__':
    main()
