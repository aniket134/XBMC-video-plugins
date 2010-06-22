import sys, os

import cgi, cgitb
cgitb.enable()

import ryw, logging
import ryw_bizarro



def launchExplorer(path):
    ryw.db_print2('launchExplorer: path is: ' + path, 59)
    try:
        return ryw_bizarro.launch_explorer(path)
    except:
        ryw.give_bad_news("Failed to launch Explorer",logging.warning)
	return False



def local():
	if os.environ['SERVER_ADDR'] == os.environ['REMOTE_ADDR']:
		return True
	else:
		return False
			
def get_url():
	form = cgi.FieldStorage()
	url = form.getfirst('url','')
	if not url:
		return (False, url)
	else:
		return (True, url)



def get_pdrive():
	"""on a LAN, this is invoked with the p flag on in
	ryw_view.make_explorer_popup_string() as so:
        target = "/cgi-bin/launchExplorer.py?p=True&url="
"""
	form = cgi.FieldStorage()
	pflag = form.getfirst('pdrive', '')
	if not pflag:
		return False
	return True



def url2path(url, pdrive):
	path = os.environ['DOCUMENT_ROOT'] + "/" + url
	path = path.replace("%23","#")
	path = os.path.normpath(path)
	if pdrive:
		path = 'P:' + path[2:]
		ryw.db_print('url2path: is pdrive, path is: ' + path, 46)
	else:
		ryw.db_print('url2path: is not pdrive, path is: ' + path, 46)
	if not os.path.exists(path):
		#sys.stdout.write('explorer.py: path does not exist: ' +
		#		 path + ' \n')
		pass
	return path



def main():
	ryw.print_header()

	pdrive = get_pdrive()
	if not pdrive:
		if not local():
			ryw.give_news("Request is not local",logging.debug)
			sys.stdout.write("False")
			sys.exit(0)
	
	success, url = get_url()
	if not success:
		sys.stdout.write("False")
		sys.exit(1)
		
	path = url2path(url, pdrive)
	
	if launchExplorer(path):
		sys.stdout.write("True")
	else:
		sys.stdout.write("False")

	sys.exit(0)

