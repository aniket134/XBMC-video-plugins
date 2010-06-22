import cgi, cgitb
cgitb.enable()
import sys, os, ryw_view, ryw, su
import logging


def burnAllReq(form):
	all = form.getfirst("all","false")
	if all == "true":
		return True
	return False

def burnRequested(form):
	image = form.getfirst("Img","")
	if not image:
		print "No Image specified to burn"
		sys.exit(1)
	withRobot = form.getfirst('withRobot', '')
		
	success, resources = get_resources()
	if not success:
		ryw.give_bad_news("Error parsing resource file",logging.error)
		sys.exit(1)
	tmpout = resources['tmpout']
	image = os.path.join(tmpout,image)
	if not os.path.exists(image):
		ryw.give_bad_news("specified image doesnt exist",logging.info)
		sys.exit(1)

	robotPresent = ryw.has_robot(resources)
	if robotPresent and withRobot:
		submitRobotRequest(image,resources['robotsjobdir'])
		sys.stdout.write("True")
	else:
		burnWithCopyToDVD(image,resources['robotsjobdir'])
	
def locate_burner_prog():
    import _winreg
    a = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, "software\\vso")
    pathDir = _winreg.QueryValueEx(a,"copytodvd")[0]
    exefile = os.path.join(pathDir, "copytocd.exe")
    if (os.path.exists(exefile)):
        return exefile
    if (os.path.exists(r"c:/program files/vso/copytodvd/copytocd.exe")):
        return r"c:/program files/vso/copytodvd/copytocd.exe"
    ryw.give_news("copytodvd program not found",logging.error)
    return ""

def prepare_datafl(datafl,root):
    try:
        f = open(datafl,"w")
        dirlist = [os.path.join(root,i) for i in os.listdir(root)]
	f.write("\n".join(dirlist)+"\n")
        f.close()
    except:
        return False
    return True
 
def burnerProgRunning():
	import wmi
	if wmi.WMI().Win32_Process(name="copytocd.exe"):
		return True
	else:
		return False
    
def burnWithCopyToDVD(image,robotdir):
	imgname = os.path.basename(image)
	datafl = os.path.join(robotdir,imgname)

	copytodvdExe = locate_burner_prog()
	if not copytodvdExe:
		ryw.give_bad_news("couldnt locate copytodvd program",logging.critical)
		sys.exit(1)
	
	if burnerProgRunning():
		ryw.give_bad_news("Copytodvd already running. Wait for it to exit/Quit it and try again",logging.info)
		sys.exit(1)

	if not prepare_datafl(datafl,image):
		ryw.give_bad_news("error writing data list file for copytodvd",logging.critical)
		ryw.give_bad_news(datafl, logging.critical)
		sys.exit(1)
	try:
		#returnVal = os.spawnl(os.P_NOWAIT|os.P_DETACH,copytodvdExe,copytodvdExe,'/datafl="%s"' % (datafl,))
		import subprocess
		pid = subprocess.Popen([copytodvdExe, '/datafl=%s' % (datafl,)]).pid
	except:
		ryw.give_bad_news('invoke_burner: failed to burn DVD...',logging.error)
		sys.exit(1)
	sys.stdout.write("True")
	sys.exit(0)

def main():
	ryw.check_logging(os.path.join(RepositoryRoot, 'WWW', 'logs'),
                      'upload.log')
	 
	logging.debug("burn outgoing image entered")
	ryw.print_header()
	form = cgi.FieldStorage()
	if burnAllReq(form):
		burnAll()
	else:
		burnRequested(form)
	logging.debug("burn image done")
	
def get_resources():
    logging.debug('get_resources: entered...')
    try:
        resources = su.parseKeyValueFile(os.path.join(RepositoryRoot,
                                                      'Resources.txt'))
    except:
        ryw.give_bad_news('get_resources failed.', logging.critical)
        return (False, None)
    
    logging.debug('get_resources succeeded.')
    return (True, resources)
        
def submitRobotRequest(imgdir,robotdir):
	imgname = os.path.basename(imgdir)
	jrqFilename = os.path.join(robotdir,imgname)

	if os.path.exists(jrqFilename + '.JRQ'):
		ryw.give_bad_news('robot job already initiated.',
				  logging.error)
		ryw.give_bad_news(
			'submitRobotRequest: job file already exists: '+
			jrqFilename + '.JRQ', logging.error)
		return (False, None)
	
	try:
		f = open(jrqFilename, 'w')
		logging.debug('write_robot_job_file: opened jrq file: ' + jrqFilename)
		f.write('ClientID=localhost\n')
		f.write('JobID=Job-' + imgname + '\n')
		f.write('Copies=1\n')
		f.write('CloseDisc=YES\n')
		f.write('VerifyDisc=YES\n')
		f.write('RejectIfNotBlank=YES\n')
		logging.debug('write_robot_job_file: wrote initial content.')

		tmpdirname = imgdir
		if tmpdirname[-1] == os.sep:
			tmpdirname = tmpdirname[:-1]
		f.write('Data=' + tmpdirname + '\n')
		logging.debug('write_robot_job_file: wrote tmp dir.')

		f.close()
		logging.debug('write_robot_job_file: closed.')
    
		jrq = jrqFilename + '.JRQ'
		os.rename(jrqFilename, jrq)
		logging.debug('write_robot_job_file: finished rename.')
	except:
		ryw.give_bad_news('write_robot_job_file: failed to create robot job file: ' + jrqFilename,
				logging.critical)
		return (False, None)
	return (True, jrqFilename)


def burnAll():

	print '<TITLE>Burning All Outing Disc Images</TITLE>'
	ryw_view.print_logo()

	success,resources = get_resources()
	if not success:
		ryw.give_bad_news("main: error parsing resource file",logging.error)
		sys.exit(1)

	robotPresent = ryw.has_robot(resources)
	
	if not robotPresent:
		ryw.give_bad_news("burning all in one go only works with robot. Resource file indicates robot is not present",logging.info)
		sys.exit(1)
		
	outdir = resources['tmpout']
	robotsjobdir = resources['robotsjobdir']

	for i in [os.path.join(outdir,k) for k in os.listdir(outdir)]:
		submitRobotRequest(i,robotsjobdir)
	
	ryw.give_good_news("Successfully submitted write request to robot for all outgoing images",logging.debug)
	ryw_view.print_footer()

if __name__ == "__main__":
	main()
