# Django settings for mysite project.
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'dv2.settings'

import os.path


import dsh_django_config
dshDjangoDataRoot = dsh_django_config.lookup('PHONE_DATA_DJANGO_PATH')
dshTemplateDir = dsh_django_config.lookup('TEMPLATE_DIR')
#dshDjangoDataRoot += 'haha'
#dshDjangoDataRoot = '/home/rywang/phone_data/db2/'
#import sys
#dshDjangoDataRoot = repr(sys.path)
#dshTemplateDir = '/home/rywang/voice/code/django/dv2/templates'

import dsh_django_utils2
dsh_django_utils2.add_to_sys_path(dsh_django_config.lookup('COMMON_CODE_DIR'))


#print '---------- in dv2/settings.py'

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

DATABASE_ENGINE = 'sqlite3'           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
#DATABASE_NAME = os.path.join(os.path.dirname(__file__), 'database/datarepo.db').replace('\\','/')            # Or path to database file if using sqlite3.

DATABASE_NAME = os.path.join(dshDjangoDataRoot, 'database')

DATABASE_USER = ''             # Not used with sqlite3.
DATABASE_PASSWORD = ''         # Not used with sqlite3.
DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

#
# 10/02/27:
# "OperationalError: database is locked"
#
DATABASE_OPTIONS = {'timeout': 30} 


# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
#TIME_ZONE = 'Asia/Kolkata'
TIME_ZONE = 'Asia/Calcutta'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 2

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
#MEDIA_ROOT = os.path.join(os.path.dirname(__file__), 'repository').replace('\\','/')

MEDIA_ROOT = os.path.join(dshDjangoDataRoot, 'media')


# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/media/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

# Make this unique, and don't share it with anybody.
#SECRET_KEY = ')znyp916_(2uciu%cimhp@%1ojbybxi3&-*pu*@v*u-8jq=5h0'
SECRET_KEY = 'dv2yp916_(2uciu%cimhp@%1ojbybxi3&-*pu*@v*u-8jq=5h0'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)

ROOT_URLCONF = 'dv2.urls'

TEMPLATE_DIRS = (
	os.path.join(os.path.dirname(__file__), 'templates').replace('\\','/'),
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    dshTemplateDir,
)

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'dv2.db',
)

#import sys
#print '---------- in dv2/settings.py: ' + repr(sys.path)

#
# need to be different for the two different sites so they
# don't conflict with each other.
#
# must access this site, dv2, at pnet1.vpn.dsh.mooo.com
# while the other one, dvoice, is at 10.8.0.14
# similarly,
# it's 128.208.4.220 vs. dsh.cs.washington.edu on dsh.cs
#
#SESSION_COOKIE_DOMAIN = 'pnet1.vpn.dsh.mooo.com'
#SESSION_COOKIE_DOMAIN = '10.7.0.14'
SESSION_COOKIE_NAME = 'dv2sess'
