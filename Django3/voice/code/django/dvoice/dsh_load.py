#!/usr/bin/python -u
#
# usage: dsh_load.py [--overwrite]
#
# this file will look for a file named 'dumpfile.py'
# in the current directory.
# this dumpfile is generated by the http://localhost:8080/dump/ script.
# this dump script may also generated a .tar file of the /media files.
# the .tar file must be untarred first before dsh_load.py is run.
#



import sys,os,subprocess,logging
import dsh_django_config,dsh_django_utils2
dsh_django_utils2.append_to_sys_path(
    dsh_django_config.lookup('DSH_VOICE_CODE_DIR'))
import dsh_utils,dsh_config,dsh_agi

os.environ['DJANGO_SETTINGS_MODULE'] = dsh_config.lookup(
    'DJANGO_SETTINGS_MODULE')
dsh_django_utils2.add_to_sys_path(dsh_config.lookup('django_sys_paths'))
from dvoice.db.models import Person,Organization,Item,Event,KeyWord
import dsh_django_utils,dsh_dump_models,dsh_dump



try:
    import dumpfile
except:
    print 'failed to find dumpfile.py'
    sys.exit(1)



def init_log():
    """set up logging."""
    logdir = dsh_config.lookup('log_file_dir')
    logName = dsh_config.lookup('log_file_name')
    dsh_utils.check_logging(logdir, logName)
    dsh_utils.give_news('dsh_load: entered --------------------',
                        logging.info)



def main():
    init_log()

    overWrite = False
    if '--overwrite' in sys.argv:
        overWrite = True
        dsh_utils.give_news('overwrite flag on.')

    dsh_utils.db_print('dsh_load: entered...', 104)
    dsh_dump.load_all(dumpfile.SelectedKeyWords,
                      dumpfile.SelectedOrgs,
                      dumpfile.SelectedPersons,
                      dumpfile.SelectedItems,
                      dumpfile.SelectedEvents,
                      overWrite)

    

if __name__ == '__main__':
    main()