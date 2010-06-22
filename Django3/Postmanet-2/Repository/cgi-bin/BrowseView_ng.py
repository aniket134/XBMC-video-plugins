
import sys, os, Browse

searchfile = os.path.join(RepositoryRoot,"SearchFile")
logDir = os.path.join(RepositoryRoot,"WWW","logs")
logFile = "upload.log"

browse = Browse.BrowseForm("/cgi-bin/AddToQueue.py","Request",searchfile,logDir, logFile)
browse.generate()
