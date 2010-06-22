import ProcessDownloadReq
import cgi, cgitb, os
cgitb.enable()

#resources = ParseResources.parseResources()

name = os.getenv("REMOTE_USER")

if name == "" or name == None:
	print "Unknown REMOTE_USER. Need to know who is requesting download"
else:
	logDir = os.path.join(RepositoryRoot,'WWW','logs')
	logFile = 'upload.log'
	queue = os.path.join(RepositoryRoot,'QUEUES',name)
	ProcessDownloadReq.main(queue,logDir,logFile)

