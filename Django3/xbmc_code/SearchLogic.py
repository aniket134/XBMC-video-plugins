#!/usr/bin/python
import re, os, sys
import constants_plugin as CP

# Used to load 'django' in SearchLogic.
sys.path.append(os.getcwd() + '/modules/')
sys.path.append(os.getcwd())
# Used to set DJANGO_SETTINGS_MODULE.
sys.path.append(CP.PLUGIN_PATH)

# Remember, it must be set before any Django model is imported.
os.environ['DJANGO_SETTINGS_MODULE'] = CP.DJANGO_SETTINGS_MODULE

import django

SD = CP.SEARCH_DELIMITER
fields = ['Name', 'Subject', 'Author', 'Class']
textNotCatched = []

def suggestSearch(text, type):
	# Important environment variable. Used in settings.py to use JDBC driver for Jython.
	os.environ['JYTHON_RUNNING'] = 'YES'
	from video_lec.models import course, course_video, random_video
	import db_interaction as DB
	#print('Suggesting Search for text: ' + text + 'and type: ' + type)
	oldText = text
	suggestions = []
	suggestions.append(oldText)
	course_objects = DB.get_course_objects()
	info_labels = {}
	for course in course_objects:
		info_labels = DB.get_course_info_labels(course)
		#print(str(info_labels))
	suggestions = []
	suggestions += [text, text + 'a']
	os.environ['JYTHON_RUNNING'] = 'NO'
	return suggestions

def finalSearch(string):
	"""
	Database query only in this function.
	"""
	print('Inside finalSearch: ' + string)
	hashtable = getHashtable(string)
	if hashtable == None or hashtable == {}:
		return None
	# At this point we have a hashtable, which contains keys=one of the value in
	# fields list and the value corresponding to that key is the search string.
	# Thus no need to check for valid key.
	# More methods to get valid search string can be included in getHashtable.
	# Do not manipulate hashtable here. Only database queries go here.
	os.environ['JYTHON_RUNNING'] = 'NO'
	from video_lec.models import course, course_video, random_video
	import db_interaction as DB
	cos = course.objects				# course objects
	cvos = course_video.objects			# course_video objects
	rvos = random_video.objects			# random_video objects
	links = []
	for key in hashtable.keys():
		# No need to check:: if key in fields:: This is checked in getHashtable
		links += linkSearch_1(key, hashtable[key], rvos)
		#links += linkSearch_2(key, hashtable[key], rvos)
		#links += linkSearch_3(key, hashtable[key], rvos)
	for link in links:
		print(links)

def linkSearch_1(key, value, dbos):
	list = []
	links = []
	if key == fields[0]:
		list += dbos.filter(title__search=value)
	for l in list:
		links.append(l.file.path)
	return links

def getHashtable(string):
	"""
	No Database query in this function. Only String manipulation.
	Incoming string argument is the valid string. 
	Its size does not matter as long as 'fields' list is 
	updated to match the text argument.
	Returns hashtable which contains mapping of each
	field item to a text. Or returns none if Cancel was pressed.
	"""
	if not string.startswith('Search'):
		return None
	strings = string.split(SD+SD)
	# Alternate code for above line, might come useful in future
	#x = re.compile(SD + SD + '(.+)' + SD + SD)
	#strings = x.findall(string)
	hashtable = {}
	for s in strings:
		match = re.search('(\w+)' + SD + '(.+)', s)
		if match:
			if match.group(1) in fields:
				hashtable[match.group(1)] = match.group(2)
			else:
				textNotCatched.append(match.group())
	#sys.stderr.write((str(hashtable)))
	if(len(textNotCatched)) > 0:
		#sys.stderr(('Text Not Catched: ' + str(textNotCatched)))
		pass
	return hashtable

def getValidText(texts):
	"""
	No Database query in this function. Only String manipulation.
	The size of text argument does not matter as long as 'fields' list is 
	updated to match the text argument.
	Returns a string that is valid to be processed for DB interactions.
	"""
	validText = 'Search'
	i = 0
	for text in texts:
		if text != None and text != '':
			validText += SD + SD
			validText += fields[i]
			validText += SD
			validText += stripDelimiter(text)
		i += 1
	return validText

def stripDelimiter(text):
	"""
	No Database query in this function. Only String manipulation.
	The size of text argument does not matter.
	This function will replace SEARCH_DELIMITER with ' ' and strip 
	leading and trailing spaces no matter what, and return the resulting string.
	"""
	if text == None or len(text) < 2:
		return text
	text = text.replace(SD, ' ')
	text = text.strip()
	return text

if __name__ == '__main__':
	list = ['love', '', '::', 'asdsf']
	finalSearch(getValidText(list))

