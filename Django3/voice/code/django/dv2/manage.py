#!/usr/bin/env python

#import os
#os.environ['DJANGO_SETTINGS_MODULE'] = 'dv2.settings'

import sys


from django.core.management import execute_manager
try:
    import settings # Assumed to be in the same directory.
except ImportError:
    import sys
    sys.stderr.write("Error: Can't find the file 'settings.py' in the directory containing %r. It appears you've customized things.\nYou'll have to run django-admin.py, passing it your settings module.\n(If the file settings.py does indeed exist, it's causing an ImportError somehow.)\n" % __file__)
    sys.exit(1)

if __name__ == "__main__":
#    print '---------- in dv2/manage.py ' + os.environ['DJANGO_SETTINGS_MODULE']
#    print '---------- in dv2/manage.py before ' + repr(sys.path)
    execute_manager(settings)
#    print '---------- in dv2/manage.py after ' + repr(sys.path)
