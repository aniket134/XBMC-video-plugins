import xbmc, xbmcgui,xbmcplugin,sys,os

# This is used to import plugin specific modules
sys.path.append(os.getcwd() + '/modules/')
# This is used to import plugin related code
sys.path.append(os.getcwd() + '/xbmc_code/')

import constants_plugin as CP
# Used by django to set DJANGO_SETTINGS_MODULE environment variable.
# See xbmc_code.db_interaction
sys.path.append(CP.PLUGIN_PATH)

import db_interaction as db
print('-----------')
print(sys.path)

xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )
