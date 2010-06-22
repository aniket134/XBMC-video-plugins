import Search,ryw_view,ryw,logging
import Browse

logDir = os.path.join(RepositoryRoot, 'WWW', 'logs')
logFile = 'upload.log'

ryw.check_logging(logDir, logFile)
logging.info('search_su: entered...')

searchFile = os.path.join(RepositoryRoot, 'SearchFile')

#
# 02/20/08
# moved to inside Search.py
# this breaks the village side,
# which probably has been long broken.
# should be easy to fix if I want to.
#
#displayObject = ryw_view.DisplayObject(RepositoryRoot,
#                                       calledByVillageSide = False,
#                                       missingFileFunc=Browse.reqDownloadFunc)

scriptName = '/cgi-bin/search_su.py'

resourcesPath = os.path.join(RepositoryRoot, 'Resources.txt')
repResources = ryw.get_resources(resourcesPath)

Search.main(logDir, logFile, searchFile, scriptName, resources = repResources)

print Browse.script_str(calledByVillageSide = False)

