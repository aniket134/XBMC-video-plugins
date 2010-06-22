
import sys, os

import pickle, cgi, cgitb, xmlrpclib
cgitb.enable()

import su, tempfile, mmap, re, ryw, logging
import subprocess
import time
import ryw_view,ryw_upload

name = os.getenv("REMOTE_USER")

def get_resources():
	logging.debug('get_resources: entered...')
	try:
		resources = su.parseKeyValueFile(os.path.join(RepositoryRoot,
                                                      'Resources.txt'))
		robotJobsDir = resources['robotsjobdir']
	except:
		ryw.give_bad_news("get_resources failed.",logging.critical)
		return ""
	return robotJobsDir

def write_job_file(count, robotJobsDir):
	try:
		ryw.give_news("Trying to write job file...",None)
		fd, filename = tempfile.mkstemp(prefix = "eraseDiscs_", dir = robotJobsDir)
	except:
		ryw.give_bad_news("failed to make temp jrq file",logging.critical)
		return ""
	try:
		f = os.fdopen(fd,"w")
		jobDesc = """
JobID=%s
ClientID=DiscEraser
Copies=%d
LoadUnloadOverride=YES
""" % (os.path.basename(filename),count)
		f.write(jobDesc)
		f.close()
		os.rename(filename, filename + ".JRQ")
		return filename
	except:
		ryw.give_bad_news("failed to write to jrq file",logging.critical)
		clean_up(filename, f)
		return ""

def clean_up(filename, f = None):
	try:
		ryw.give_news("cleaning up files...",None)
		if f and not f.closed:
			f.close()
		if os.path.exists(filename):
			os.remove(filename)
		if os.path.exists(filename + ".JRQ"):
			os.remove(filename + ".JRQ")
		if os.path.exists(filename + ".ERR"):
			os.remove(filename + ".ERR")
		if os.path.exists(filename + ".DON"):
			os.remove(filename + ".DON")
			
	except:
		ryw.give_bad_news("Error cleaning up files used",logging.critical)

def wait_till_job_starts(filename, robotJobsDir):
	try:
		ryw.give_news("Waiting for robot to pick up the job...",None)
		time.sleep(20)
		while not os.path.exists(filename + ".INP"):
			ryw.give_news2(" * ",None)
			time.sleep(5)
	except:
		ryw.give_bad_news("Bad things happened while waiting for job to be processed",logging.critical)
		return False
	return True


def load_section(filename, robotJobsDir,rexp):
	section = {}
	statusFile = os.path.join(robotJobsDir, "Status", "PTStatus.txt")
	if not os.path.exists(statusFile):
		ryw.give_bad_news("cant find robot server's log file", logging.critical)
		section['ABORT'] = True
		return section

	try:
		f = open(statusFile)
	        mm = mmap.mmap(f.fileno(),0,access=mmap.ACCESS_READ)	
		m = rexp.search(mm)
		if not m:
			# search for section in status file failed.
			if os.path.exists(filename + ".INP"):
				# file exists... race occurance: inp file created
				# but section in log not created yet. try again in
				# some time.
				section['CONTINUE'] = True
				return section
			else:
				# what happened ? no file and no section...
				section['ABORT'] = True
				ryw.give_bad_news("job's .INP file doesnt exist. Nor is there a section for the job in status file", logging.critical)
				if os.path.exists(filename + ".DON"):
					ryw.give_bad_news("unexpectedly found .DON file for the job",logging.critical)
				if os.path.exists(filename + ".ERR"):
					ryw.give_bad_news("unexpectedly found .ERR file for the job", logging.critical)
				return section
		r = m.group(0)
		#r = re.sub(r"(?m)^\s*$","",r)
		l = r.splitlines()
		l2 = [x.split("=",1) for x in l if x.find("=") != -1]
		section.update(l2)
		mm.close()
		return section
	except:
		ryw.give_bad_news("Error in parsing PTStatus.txt file",logging.critical)
		section['ABORT'] = True
		return section

def wait_to_end_and_cleanup(filename, count, robotJobsDir):
	rexp = re.compile(regexp % (os.path.basename(filename),))
	try:	
		ryw.give_news("Waiting for job to end...",None)
		while True:
			section = load_section(filename, robotJobsDir, rexp)
			if section.has_key("TimeCompleted") and \
				section["TimeCompleted"].strip() != "":
					break
			ryw.give_news2(" * ",None)
			time.sleep(10)

		section['TimeCompleted'] = section['TimeCompleted'].strip()
		mesg = "Job finished at %(TimeCompleted)s. %(GoodDiscs)s good discs and %(BadDiscs)s bad discs were produced.\n"
		if "JobErrorNumber" in section and section['JobErrorNumber'] != "16":
			mesg += "Job ended with error. Error code = %(JobErrorNumber)s. Error String = %(JobErrorString)s.\n"
		for i in range(0,10):
			if not "DiscErrorIndex%d" % (i,) in section:
				break
			index = section["DiscErrorIndex%d" % (i,)]
			number = section["DiscErrorNumber%d" % (i,)]
			errstr = section["DiscErrorString%d" % (i,)]
			mesg += "Disc %s had error. Error code = %s. Error Message = %s\n" % (index, number, errstr)

		ryw.give_news("<PRE>" + mesg % section + "</PRE>", None)
		if ("JobErrorNumber" in section and section['JobErrorNumber'] != "16") or \
			section['BadDiscs'] != "0" or "DiscErrorIndex0" in section:
			logging.warning("Erase job ended with errors. Job's status dict: " + str(section))
		else:
			logging.debug("Erase job ended with no errors. Job's status dict: " + str(section)) 
		clean_up(filename)
	except:
		ryw.give_bad_news("Error while waiting for job to finish",logging.warning)
		clean_up(filename)
		
def check_if_disc_loaded(section, discNumber):
	try:
		loadingDiscMSg = "Loading Disc %d" % (discNumber,)
		if not section['CurrentStatus'].startswith(loadingDiscMSg):
			# its not loading the next disc currenly. any LoadDiscState info will be out of date
			return (None, None)
		loaded = [k for (k,v) in section.iteritems() if k.startswith("LoadDiscState") and v == "1"]
		if loaded == []:
			return (None, None)
		if len(loaded) > 1:
			ryw.give_bad_news("Found multiple discs in hold state. Can only happen if robot has multiple drives",logging.critical)
			ryw.give_bad_news("returning 1st hold disc to be erased",logging.critical)
		k = loaded[0]
		discID = k[len("LoadDiscState"):]
		drive = section["LoadDiscDrive"+discID]
		return (discID, drive)
	except:
		ryw.give_bad_news("Unable to locate which discID and drive of loaded disc",logging.critical)
		return (None, None)

		
regexp = r"(?ms)(?<=^\[%s\]\r\n)(.*?)(?=^\[)"
def do_erase(filename,count,robotJobsDir):
	if not wait_till_job_starts(filename, robotJobsDir):
		return False
	ryw.give_news("Job is now being processed",None)
	i = 1
	rexp = re.compile(regexp % (os.path.basename(filename),))
	while i <= count:
		section = load_section(filename,robotJobsDir,rexp)
		if "ABORT" in section:
			ryw.give_news("Aborting...",None)
			return False
		if "CONTINUE" in section:
			ryw.give_news("job status not yet in file..continuing...",None)
			time.sleep(5)
			continue
		if was_aborted(section):
			if "ABORT" in section:
				return False
			else:
				return True

		discID, drive = check_if_disc_loaded(section, i)
		if discID:
			ryw.give_news("disc loaded... attempting to erase...",None)
			if eraseDiscInDrive(drive):
				unloadDisc(discID,filename,robotJobsDir)
				i += 1
			else:
				rejectDisc(discID,filename, robotJobsDir)
			time.sleep(20)
			# sleep to let .ptm file be processed and disc unloaded
		else:
			ryw.give_news(section['CurrentStatus'].strip(),None)
			time.sleep(5)
			continue
	return True

def was_aborted(section):
	try:
		status = section['JobState']
		if status == "1":
			return False
		if status == "2":
			ryw.give_bad_news("Job shows up as being finished when its not...",logging.warning)
			return True
		if status == "3":
			# job failed.. check if it was user abort
			if section['JobErrorNumber'] == "16":
				return True
			else:
				ryw.give_bad_news("Job ended with error code %s and error string %s" % ( \
					section['JobErrorNumber'], section['JobErrorString']), logging.critical)
				section['ABORT'] = True
				return True
	except:
		ryw.give_bad_news("section had key missing",logging.critical)
		section['ABORT'] = True
		return True

def unloadDisc(discID, filename, robotJobsDir):
	try:
		ryw.give_news("Writing req to unload disc...",None)
		f = open(filename,"w")
		f.write("""Message=UNLOAD_DISC
DiscID=%s
""" % (discID,))
		f.close()
		os.rename(filename, filename + ".PTM")
	except:
		ryw.give_bad_news("Error writing command to unload disc",logging.critical)
		return False
	return True

def rejectDisc(discID, filename, robotJobsDir):
	try:
		ryw.give_news("Writing req to reject disc...",None)
		f = open(filename,"w")
		f.write("""Message=REJECT_DISC
DiscID=%s
""" % (discID,))
		f.close()
		os.rename(filename, filename + ".PTM")
	except:
		ryw.give_bad_news("Error writing command to reject disc",logging.critical)
		return False
	return True

import exceptions

def eraseDiscInDrive(driveLetter):
	
	count = 0
	while count < 12:
		try:
			os.listdir(driveLetter + ":\\")
		except Exception, err:
			if err.__class__ == exceptions.WindowsError:
				if err.errno == 1 or err.errno == 1005:
					return True
				if err.errno == 21:
					ryw.give_news("waiting for drive to become ready", None)
					time.sleep(5)
					count += 1
			else:
				ryw.give_bad_news("eraseDiscInDrive failed",logging.critical)
				return False

	erasedisc = r"C:\Program Files\BatchDisc\EraseDisc.exe"
	options = [r"/ID="+scsi_string,r"/NOEJECT",r"/NOCONFIRM"]
	try:
		ryw.give_news("Invoking erasedisc to erase...",None)
		pipe = subprocess.Popen([erasedisc] + options, shell=True, stdout=subprocess.PIPE)
		r = pipe.communicate()[0]
		returncode = pipe.returncode
		ryw.give_news("<PRE>" + r + "</PRE>", None)
		if returncode != 0:
			ryw.give_bad_news("erasing of disc failed. return code = %d. Erase Disc output:\n" + r % (returncode,), logging.critical)
			return False
		else:
			return True
	except:
		ryw.give_bad_news("Exception while trying to erase disc",logging.critical)
		return False

def find_dvdwriter_id_from_server(robotJobsDir):
	statusFile = os.path.join(robotJobsDir,"Status","PTStatus.txt")
	if not os.path.exists(statusFile):
		ryw.give_bad_news("DVD robot's status file not found",logging.critical)
		return None
	try:
		f = open(statusFile)
		for line in f:
			if line.startswith("DriveDesc"):
				break
		f.close()
		writerid = line.strip().split("=",1)[1]
		logging.debug("dvd robot drive desc: " + writerid)
		return writerid
	except StopIteration:
		ryw.give_bad_news("No DriveDesc line found in status file",logging.critical)
		return None # EOF reached before DriveDesc found
	except:
		ryw.give_bad_news("find_dvdwriter_id failed",logging.critical)
		return  None

def find_scsi_string(writer):
	try:
		scanbus = r"c:\program files\batchdisc\scanbus.exe"
		pipe = subprocess.Popen([scanbus], shell=True, stdout=subprocess.PIPE)
		r = pipe.communicate()[0]
		m = re.findall(r"(?m)^\d+:\d+:\d+.*$",r)
		if not m:
			ryw.give_bad_news("Scanbus couldnt find any writers",logging.critical)
			return None
		m = [x.strip() for x in m]
		l = [re.split("\s+",x) for x in m]
		l2 = re.split("\s+",writer)
		logging.debug("drives returned by scanbus are: " + str(l))
		logging.debug("robot drive is: " + str(l2)) 
		dvdwriter = [x for x in l if set(l2).issubset(set(x))]
		if not dvdwriter:
			ryw.give_bad_news("no match found in writers returned by scanbus and by robot server",logging.critical)
			return None
		logging.debug("dvdwriter scsi info that matches robot's desc: " + str(dvdwriter))
		return dvdwriter[0][0]
	except:
		ryw.give_bad_news("find_scsci_string failed",logging.critical)
		return None
	
scsi_string = ""
def find_scsi_string_for_eraser(robotJobsDir):
	writer = find_dvdwriter_id_from_server(robotJobsDir)	
	if not writer:
		return False
	global scsi_string
	scsi_string = find_scsi_string(writer)
	if not scsi_string:
		return False
	return True

def main():
	ryw.check_logging(os.path.join(RepositoryRoot, 'WWW', 'logs'),
                      'upload.log')
	logging.debug('eraseDisc.py: attempted...')
	robotJobsDir = get_resources()

	ryw_view.print_header_logo()
	
	if not robotJobsDir:
		ryw_upload.quick_exit(1)
	
	if not find_scsi_string_for_eraser(robotJobsDir):
		ryw_upload.quick_exit(1)
		
	count = 100
	filename = write_job_file(count, robotJobsDir)
	if not filename:
		ryw_upload.quick_exit(1)
	
	do_erase(filename, count, robotJobsDir)
	wait_to_end_and_cleanup(filename, count, robotJobsDir)
	
	ryw_view.print_footer()
	
	
main()
#rexp = re.compile(regexp % ("testid",))
#section = load_section("","Y:\\",rexp)
#print section
#print check_if_disc_loaded(section)
