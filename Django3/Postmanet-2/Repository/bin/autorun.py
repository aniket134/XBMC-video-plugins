#
# python autorun.py --overwrite
#

import os,sys
import os.path
import urllib
import traceback
import socket
import urllib2
import ConfigParser

def findDriveLetter():
	try:
		#return os.path.splitdrive(os.path.abspath(sys.argv[0]))[0]
		#use above if autorun.py can be anywhere and not in the root dir of
		#the dvd. Using below one currently as it is also convenient for testing.
		return (True,os.path.dirname(os.path.abspath(sys.argv[0])))
	except:
		return (False, "Error in finding root dir: Trace: " + traceback.format_exc())

redirectWeb = "redirectWebIndicator"
redirectDisk = "redirectDiskIndicator"
redirectFoo = "redirectFoo"

def verifyRepository():
	try:
		url = urllib2.urlopen("http://localhost/postmanetWhoAmI.txt")
		# for now we just check that the page exists. we can add more
		# content inside it later to get more info out of it like which
		# url to use to do the merging etc.
		parser = ConfigParser.RawConfigParser()
		parser.readfp(url)
		return dict(parser.items("MergeIncoming"))
	except:
		return None
	
def verifyVillage():
	try:
		url = urllib2.urlopen("http://localhost:8000/postmanetWhoAmI.txt")
		parser = ConfigParser.RawConfigParser()
		parser.readfp(url)
		return dict(parser.items("MergeIncoming"))
	except:
		return None

def askUserToPick(repository, village):
	while(True):
		print
		print "Found both repository and village services running.\n"
		print "Pick where to merge. Enter 1 for repository, 2 for village side: ",
		choice = sys.stdin.readline().strip()
		if choice == "1":
			return (repository, None)
		elif choice == "2":
			return (None, village)
		else:
			print "\nInvalid choice. Please enter 1 or 2."

	
def mergeTarget():
	repositoryRunning = None
	villageRunning = None
	try:
		s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		s.connect(("localhost",80))
		repositoryRunning = verifyRepository()
		s.close()
	except: pass # nothing on port 80.
	
	try:
		s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		s.connect(("localhost",8000))
		villageRunning = verifyVillage()
		s.close()
	except: pass # nothing on port 8000

	if repositoryRunning and villageRunning:
		repositoryRunning, villageRunning = askUserToPick(repositoryRunning, villageRunning)
	
	return (repositoryRunning,villageRunning)



def requestMergeIncoming():
    wait_to_exit("Press any key to begin merge. Ctl-C or close this window if u dont want to merge")
    repository, village = mergeTarget()
    if repository:

        ovw = False
        if '--overwrite' in sys.argv:
	    ovw = True
	    
        mergeRepository(repository, overWrite = ovw)
    else:
	mergeVillage(village)



def mergeVillage(village):
	# url = "http://localhost:8000/cgi-bin/repository/repository_start_ryw.py?"
	success,path = findDriveLetter()
	if not success:
		print path
		wait_to_exit()
		return
	try:
		# paramsdict = {'driveroot':path, 'redirectDisk':redirectDisk, 'redirectWeb':redirectWeb, 'redirectFoo':redirectFoo}
		# params = urllib.urlencode(paramsdict)
		f = urllib.urlopen(village["url"] % {"path":path})
		for line in f:
			if line.startswith(redirectDisk):
				# ignore url for disk browsing suggested by line
				print "Got error returned from server."
				wait_to_exit("Press any key to launch browser for disc...")
				launchBrowser("file:///" + path + "/repository/html/index.html")
				break
			elif line.startswith(redirectWeb):
				ignore, url = line.split(":",1)
				print "merging of disc done"
				wait_to_exit("Press any key to close this window and launch browser...")
				if url.startswith("http"):
					launchBrowser(url)
					break
				elif url.startswith("/"):
					launchBrowser("http://localhost:8000" + url)
					break
				else:
					baseurl = village['url'].split("?",1)[0].rsplit("/",1)[0]
					launchBrowser(baseurl + "/" + url)
					break
			elif line.startswith(redirectFoo):
				print
				print
				print line[len(redirectFoo)+1:]
				wait_to_exit("Press any key to exit...")
				break
			else:
				print line

		if not line:
			wait_to_exit("merge failed without returning error type. Press any key to browse incoming disk directly...")
			launchBrowser("file:///" + path + "/repository/html/index.html")

	except:
		print "Error in requestMergeIncoming: Trace: " + traceback.format_exc()
		wait_to_exit("Press any key. Browser for incoming disc will start...")
		launchBrowser("file:///" + path + "/repository/html/index.html")
	return
		
def getAuthInfo():
	print "Enter Login name: ",
	login = sys.stdin.readline().strip()
	import getpass
	password = getpass.getpass()
	return (login, password)

def setupHTTPAuth(login,password):
	passman = urllib2.HTTPPasswordMgrWithDefaultRealm()
	passman.add_password(None,"http://localhost/",login,password)
	authhandler = urllib2.HTTPBasicAuthHandler(passman)
	opener = urllib2.build_opener(authhandler)
	urllib2.install_opener(opener)


def mergeRepository(repository, overWrite = False):
	success,path = findDriveLetter()
	if not success:
		print path
		wait_to_exit()
		return

	path = urllib.quote(path)
	print 'source data located at: ' + path + '\n'
	
	print "Merging into repository requires auth info.\n"
	login,password = getAuthInfo()
	setupHTTPAuth(login,password)

	try:
		urlStr = repository["url"] % {"path":path}
		if overWrite:
			urlStr += '&overwrite=true'
			print 'overwrite flag is on.'

		f = urllib2.urlopen(urlStr)
		for line in f:
			if line.startswith(redirectDisk):
				# ignore url for disk browsing suggested by line
				print "Got error returned from server."
				wait_to_exit("Press any key to launch browser for disc...")
				launchBrowser("file:///" + path + "/repository/html/index.html")
				break
			elif line.startswith(redirectWeb):
				ignore, url = line.split(":",1)
				print "merging of disc done"
				wait_to_exit("Press any key to close this window and launch browser...")
				if url.startswith("http"):
					launchBrowser(url)
					break
				elif url.startswith("/"):
					launchBrowser("http://localhost" + url)
					break
				else:
					baseurl = repository['url'].split("?",1)[0].rsplit("/",1)[0]
					launchBrowser(baseurl + "/" + url)
					break
			elif line.startswith(redirectFoo):
				print
				print
				print line[len(redirectFoo)+1:]
				wait_to_exit("Press any key to exit...")
				break
			else:
				print line

		if not line:
			wait_to_exit("merge failed without returning error type. Press any key to browse incoming disk directly...")
			launchBrowser("file:///" + path + "/repository/html/index.html")

	except:
		print "Error in requestMergeIncoming: Trace: " + traceback.format_exc()
		wait_to_exit("Press any key. Browser for incoming disc will start...")
		launchBrowser("file:///" + path + "/repository/html/index.html")
	return
		


def launchBrowser(url):
	import webbrowser
	print "Launching webbrowser..."
	webbrowser.open(url,new=True,autoraise=True)


def wait_to_exit(msg = "Press any key to exit..."):
	print
	print msg
	sys.stdin.read(1)


if __name__ == "__main__":
	requestMergeIncoming()
