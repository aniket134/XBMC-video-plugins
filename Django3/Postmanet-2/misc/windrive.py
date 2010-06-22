
from watsup.winGuiAuto import findControl,setEditText, findTopWindow,clickButton
from watsup.winGuiAuto import activateMenuItem, getComboboxItems, selectComboboxItem
import os, sys
import os.path
import time

import win32gui
import watsup.winGuiAuto as winGuiAuto

import subprocess
def startGoldwave():
	pid = subprocess.Popen([r'c:\program files\goldwave\goldwave.exe']).pid
	return pid

import win32process
def makePIDFilter(pid):
	def filterFunc(hwnd):
		ignore, ppid = win32process.GetWindowThreadProcessId(hwnd)
		return ppid == pid 
	return filterFunc
		
def findGoldwaveHelpWindow(pid):
	selectionFunc = makePIDFilter(pid)
	return findTopWindow(wantedText="GoldWave Help", wantedClass="MS_WINHELP", selectionFunction = selectionFunc, maxWait = 5, retryInterval = 0.3)

def main(filename):
	pid = startGoldwave()
	print "goldwave started with pid %d to process file %s" % (pid,filename)
	selectionFunc = makePIDFilter(pid)
	hgw = findTopWindow(wantedText="GoldWave", wantedClass="TMainForm", selectionFunction = selectionFunc, maxWait = 5, retryInterval = 0.3)
	activateMenuItem(hgw,("File",1))
	hos = findTopWindow(wantedText="Open Sound", wantedClass="#32770",selectionFunction=selectionFunc,maxWait=5,retryInterval=0.3)
	editArea = findControl(hos,wantedClass="Edit")
	setEditText(editArea,filename)
	selectfunc = lambda x: winGuiAuto._normaliseText(win32gui.GetWindowText(x)) == "open"	
	openButton = findControl(hos,wantedText="&Open",wantedClass="Button", selectionFunction = selectfunc)
	clickButton(openButton)

	time.sleep(5)
	while True:
		try:
			c = findControl(hgw, wantedText = os.path.basename(filename), wantedClass = "TWaveView", maxWait=1, retryInterval=1)
			break
		except winGuiAuto.WinGuiAutoError, err:
			if str(err).startswith("No control found for"):
				print "waiting for file to load.. sleeping for 5 seconds"
				time.sleep(5)
				#make this more robust by making sure the Audio decompression progress bar thingie is still on ?
				pass
			else:
				raise
	selectLeftChannel(hgw)
	doNoiseReduction(hgw)
	saveAsWave(hgw, filename)
	quitGoldwave(hgw)
	combineFiles(filename)

def quitGoldwave(hgw):
	activateMenuItem(hgw,("File",10))
	hc = findTopWindow(wantedText="Confirm",wantedClass="TMessageForm",selectionFunction=makePIDFilter(getPIDfromHandle(hgw)), maxWait=5, retryInterval=0.3)
	noButton = findControl(hc,wantedText="No",wantedClass="TButton",maxWait=5, retryInterval=0.3)
	clickButton(noButton)

def printWindows(windows):
	for win in windows:
		print "%d, %s, %s" % (win, win32gui.GetWindowText(win), win32gui.GetClassName(win))

def selectLeftChannel(hgw):
	activateMenuItem(hgw,("Edit",20,0))

def saveAsWave(hgw,filename):
	activateMenuItem(hgw,("File",7)) # save selection as menu item
	pidFunc = makePIDFilter(getPIDfromHandle(hgw))
	hssa = findTopWindow(wantedText="Save Sound As",wantedClass="#32770",selectionFunction=pidFunc,maxWait = 5, retryInterval=0.3)
	editArea = findControl(hssa,wantedClass="Edit")
	setEditText(editArea,os.path.splitext(filename)[0])
	def selectFunc(x):
		if win32gui.GetClassName(x) != "ComboBox":
			return False
		if getComboboxItems(x) and getComboboxItems(x)[0] == "Wave (*.wav)":
			return True
		return False
	hsat = findControl(hssa,wantedClass="ComboBox",selectionFunction=selectFunc)
	selectComboboxItem(hsat,"Wave (*.wav)")
	htcsf = findControl(hssa,wantedClass="TCustomSaveForm")
	hcb = findControl(htcsf,wantedClass="TComboBox")
	options = getComboboxItems(hcb)
	selectComboboxItem(hcb,"PCM signed 16 bit, mono")
	waveFile = os.path.splitext(filename)[0] + ".wav"
	try:
		if os.path.exists(waveFile):
			os.remove(waveFile)
			print "old wav file removed"
	except:
		print "error in removing file. do error logging/reporting here"
	saveButton = findControl(hssa,wantedClass="Button",wantedText="Save")
	clickButton(saveButton)
	waitToFinish(wantedText="Processing Saving",selectionFunction=pidFunc)
	

def getPIDfromHandle(hwnd):
	ignore, pid = win32process.GetWindowThreadProcessId(hwnd)
	return pid

import re
def doNoiseReduction(hgw):
	activateMenuItem(hgw,("Effect",4,3))
	selectFunc = makePIDFilter(getPIDfromHandle(hgw))
	hnr = findTopWindow(wantedText="Noise Reduction", wantedClass="TEffectWrapper",selectionFunction = selectFunc, maxWait=5, retryInterval=0.3)
	hpr = findControl(hnr,wantedText="Presets",wantedClass="TGroupBox")
	hcb = findControl(hpr,wantedClass="TComboBox")
	cl = getComboboxItems(hcb)
	selectComboboxItem(hcb,"Hiss removal")
	okButton = findControl(hnr,wantedText="OK",wantedClass="TButton")
	clickButton(okButton)
	waitToFinish(wantedText="Processing Noise Reduction",selectionFunction=selectFunc)

def combineFiles(filename):
	d = {}
	d['sourceAvi'] = filename
	d['waveFile']  = os.path.splitext(filename)[0] + ".wav"
	d['destinationAvi'] = os.path.splitext(filename)[0] + "_processed.avi"
	vdubscript = os.path.splitext(filename)[0] + "_vdubjob.txt"
	virtualdub = r"C:\Program Files\Virtualdub-1.6.10\VirtualDub.exe"
	writeVirtualdubScript(vdubscript,d)
	command = [virtualdub]
	command.append("/x")
	command.append("/s")
	command.append(vdubscript)
	subprocess.call(command)
	os.remove(d['waveFile'])
	os.remove(vdubscript)

def writeVirtualdubScript(filename,d):
	e = {}
	for k,v in d.iteritems():
	    e[k] = v.replace("\\","\\\\")
	f = open(filename,"w")
	f.write(virtualdubScript % e)
	f.close()
	
def waitToFinish(wantedText=None,wantedClass="TProgressForm",selectionFunction=None,maxWait=5,retryInterval=0.1):
	htpf = None
	try:
		htpf = findTopWindow(wantedText=wantedText,wantedClass=wantedClass,selectionFunction=selectionFunction,maxWait=maxWait,retryInterval=retryInterval)
	except:
		#assume file was so short that processing is already over. Practically this wont happen for our needs
		pass
	while htpf:
		try:
			htpf = findTopWindow(wantedText=wantedText,wantedClass=wantedClass,selectionFunction=selectionFunction,maxWait=maxWait,retryInterval=retryInterval)
			try:
				htst = findControl(htpf,wantedClass="TStaticText",maxWait=maxWait,retryInterval=retryInterval)
				text = win32gui.GetWindowText(htst)
				m = re.search(r"(?P<hours>\d+):(?P<minutes>\d+):(?P<seconds>\d+)",text)
				if m:
					sleeptime = "%s*3600 + %s*60 + %s" % (m.group("hours"),m.group("minutes"),m.group("seconds"))
					sleeptime = eval(sleeptime)/2 + 1 # random formula as estimates are not always accurate
					if sleeptime > 90:	# random threshold
						sleeptime = 90
					print "waiting for processing to finish... sleeping %d seconds" % (sleeptime,)
					time.sleep(sleeptime)
				else:
					time.sleep(2)
			except:
				time.sleep(2)
		except:
			# processing done.
			htpf = None
			break
			# either one of above should work really.
			


import types
def makeSelectionFunction(*args):
	def filterFunc(hwnd):
		for i in args:
			if i(hwnd):
				continue
			else:
				return False
		return True
	return filterFunc

virtualdubScript = """
// VirtualDub job list (Sylia script format)
// This is a program generated file -- edit at your own risk.

VirtualDub.Open("%(sourceAvi)s","",0);
VirtualDub.audio.SetSource("%(waveFile)s");
VirtualDub.audio.SetMode(1);
VirtualDub.audio.SetInterleave(1,500,1,0,0);
VirtualDub.audio.SetClipMode(1,1);
VirtualDub.audio.SetConversion(0,0,0,0,0);
VirtualDub.audio.SetVolume();
VirtualDub.audio.SetCompression(85,22050,1,0,3000,1,12,"AQACAAAATgABAHEF");
VirtualDub.audio.EnableFilterGraph(0);
VirtualDub.video.SetInputFormat(0);
VirtualDub.video.SetOutputFormat(7);
VirtualDub.video.SetMode(0);
VirtualDub.video.SetFrameRate(0,1);
VirtualDub.video.SetIVTC(0,0,-1,0);
VirtualDub.video.SetRange(0,0);
VirtualDub.video.SetCompression();
VirtualDub.video.filters.Clear();
VirtualDub.audio.filters.Clear();
VirtualDub.project.ClearTextInfo();
VirtualDub.SaveAVI("%(destinationAvi)s");
VirtualDub.audio.SetSource(1);
VirtualDub.Close();

"""

if __name__ == '__main__':
	if len(sys.argv) != 2:
		print "Usage: %s name_of_avi_file_to_process" % (sys.argv[0],)
	filename = os.path.abspath(sys.argv[1])
	if not os.path.exists(filename):
		print "Given filename %s doesn't exist!" % (filename,)
	base, ext = os.path.splitext(filename)
	if ext.lower() != ".avi":
		print "code only handles .avi files for now"
		print "exiting..."
		sys.exit(1)
	main(filename)

