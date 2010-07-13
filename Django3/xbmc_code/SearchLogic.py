#!/usr/bin/python
import re, os, sys
import constants_plugin as CP

# Used to load 'django' in SearchLogic.
sys.path.append(os.getcwd() + '/modules/')
# Enables this script to be run as a standalone script
sys.path.append(os.getcwd())
# Used to set DJANGO_SETTINGS_MODULE.
sys.path.append(CP.PLUGIN_PATH)

# Remember, it must be set before any Django model is imported.
os.environ['DJANGO_SETTINGS_MODULE'] = CP.DJANGO_SETTINGS_MODULE

import django

SD = CP.SEARCH_DELIMITER
# Used as a link between database tables/columns and Search box fields. Case-sensitive.
fields = ['Name', 'Subject', 'Author', 'Class', 'Description', \
		'ContentType', 'VideoRes', 'Media', 'Language', \
		'checkboxSubject', 'checkboxMedia', 'checkboxLanguage']
textNotCatched = []

def suggestSearch(text, type):
	# Important environment variable. Used in settings.py to use JDBC driver for Jython.
#	os.environ['JYTHON_RUNNING'] = 'YES'
#	from video_lec.models import object, person, organization
#	import db_interaction as DB
	#print('Suggesting Search for text: ' + text + 'and type: ' + type)
	suggestions = []

	if type == fields[0]:
		f = open('xbmc_code/suggestions/name.txt', 'rU')
	elif type == fields[1]:
		f = open('xbmc_code/suggestions/subject.txt', 'rU')
	elif type == fields[2]:
		f = open('xbmc_code/suggestions/person.txt', 'rU')
	elif type == fields[3]:
		f = open('xbmc_code/suggestions/class.txt', 'rU')
	elif type == 'Default':
		f = open('xbmc_code/suggestions/name.txt', 'rU')
		dbString = f.read()
		f.seek(0)
		dbLines = f.readlines()
		f.close()
		dbWords = dbString.split()
		getMatch(dbLines, text, suggestions)
		suggestions = suggestions[:2]
		if len(suggestions) == 0:
			getMatch(dbWords, text.split()[-1], suggestions)
		lenSug = len(suggestions)

		f = open('xbmc_code/suggestions/subject.txt', 'rU')
		dbString = f.read()
		f.seek(0)
		dbLines = f.readlines()
		f.close()
		dbWords = dbString.split()
		getMatch(dbLines, text, suggestions)
		suggestions = suggestions[:3]
		if lenSug == len(suggestions):
			getMatch(dbWords, text.split()[-1], suggestions)
		lenSug = len(suggestions)

		f = open('xbmc_code/suggestions/person.txt', 'rU')
		dbString = f.read()
		f.seek(0)
		dbLines = f.readlines()
		f.close()
		dbWords = dbString.split()
		getMatch(dbLines, text, suggestions)
		suggestions = suggestions[:4]
		if lenSug == len(suggestions):
			getMatch(dbWords, text.split()[-1], suggestions)
		lenSug = len(suggestions)

		f = open('xbmc_code/suggestions/class.txt', 'rU')
		dbString = f.read()
		f.seek(0)
		dbLines = f.readlines()
		f.close()
		dbWords = dbString.split()
		getMatch(dbLines, text, suggestions)
		suggestions = suggestions[:5]
		if lenSug == len(suggestions):
			getMatch(dbWords, text.split()[-1], suggestions)
		lenSug = len(suggestions)

		f = open('xbmc_code/suggestions/en_US.dic', 'rU')
		engWords = f.readlines()
		f.close()
	
		suggestions = suggestions[:6]
		getMatch(engWords, text.split()[-1], suggestions)

		return suggestions[:7]
	else:
		return []
	
	dbString = f.read()
	f.seek(0)
	dbLines = f.readlines()
	f.close()
	dbWords = dbString.split()
	f = open('xbmc_code/suggestions/en_US.dic', 'rU')
	engWords = f.readlines()
	f.close()
	
	getMatch(dbLines, text, suggestions)
	# This condition is implied because if match is found in dbLines then
	# its atleast one part will again occur in dbWords.
	if len(suggestions) == 0:
		getMatch(dbWords, text.split()[-1], suggestions)
	getMatch(engWords, text.split()[-1], suggestions)

#	os.environ['JYTHON_RUNNING'] = 'NO'
	return suggestions[:6]

def populateSuggest():
	"""
	Used to populate suggestions. Reads database and fills files with data, which is used to suggest results.
	"""
	from video_lec.models import object, person, organization
	import db_interaction as DB
	obos = object.objects.all()					# object objects
	pos = person.objects.all()					# person objects
	orgos = organization.objects.all()			# organization objects
	nf = open('xbmc_code/suggestions/name.txt', 'w')
	sf = open('xbmc_code/suggestions/subject.txt', 'w')
	cf = open('xbmc_code/suggestions/class.txt', 'w')
	pf = open('xbmc_code/suggestions/person.txt', 'w')
	orgf = open('xbmc_code/suggestions/organization.txt', 'w')
	string_1 = ''; string_2 = ''; string_3 = ''; string_4 = ''; string_5 = ''; string_6 = ''
	for o in obos:
		string_1 += str(o.title) + '\n'
		string_4 += str(o.subject) + '\n' + str(o.other_subject) + '\n'
		string_5 += str(o.for_class) + '\n'
	for o in pos:
		string_2 += str(o.name) + '\n'
	for o in orgos:
		string_3 += str(o.name) + '\n' + str(o.address) + '\n'
	string_1 = string_1.replace('None', '').replace('  ', ' ').replace('   ', ' ')
	string_2 = string_2.replace('None', '').replace('  ', ' ').replace('   ', ' ')
	string_3 = string_3.replace('None', '').replace('  ', ' ').replace('   ', ' ')
	string_4 = string_3.replace('None', '').replace('  ', ' ').replace('   ', ' ')
	string_5 = string_3.replace('None', '').replace('  ', ' ').replace('   ', ' ')
	nf.write(string_1)
	pf.write(string_2)
	orgf.write(string_3)
	sf.write(string_2)
	cf.write(string_2)
	nf.close()
	pf.close()
	orgf.close()
	sf.close()
	cf.close()

def finalSearch(string):
	"""
	Main Search function. All search boxes call this function.
	string: String - The search query entered by user.
	mode: Integer - 0 means Default search will take place. 1 means second (with four fields). 2 means advanced search.
	"""
	tup = ()
	try:
		tup = eval(string)
	except Exception, e:
		sys.stderr.write('==================================' + str(e))
		return None
	if not type(tup) == tuple:
		return None
	hashtable = getHashtable(tup[0])
	if hashtable == None or hashtable == {}:
		return None
	# At this point we have a hashtable, which contains keys=one of the value in
	# fields list and the value corresponding to that key is the search string.
	# Thus no need to check for valid key.
	# More methods to get valid search string can be included in getHashtable.
	# Do not manipulate hashtable here. Only database queries go here.
	os.environ['JYTHON_RUNNING'] = 'NO'
	from video_lec.models import object, person, organization
	import db_interaction as DB
	obos = object.objects					# object objects QuerySet
	pos = person.objects					# person objects QuerySet
	orgos = organization.objects			# organization objects QuerySet
	objects = []
	mode = tup[1]
	if mode == 0:
		# Default Search with one search fields
		objects = firstObjectSearch(hashtable[fields[0]], obos, pos, orgos)
	elif mode == 1:
		# Second Search box with four search fields
		objects = secondObjectSearch(hashtable, obos, pos, orgos)
	elif mode == 2:
		# Advanced Search box
		objects = thirdObjectSearch(hashtable, obos, pos, orgos)
	print(objects)
	return objects

def thirdObjectSearch(hashtable, obos, pos, orgos):
	return secondObjectSearch(hashtable, obos, pos, orgos)

def secondObjectSearch(hashtable, obos, pos, orgos):
	objects = []
	list = []

	value = hashtable.get(fields[0])
	list_1 = []
	tmp = []
	if value != None and value != '':
		addObject(list_1, obos.filter(title__search=value))
		addObject(list_1, obos.filter(title__contains=value))
		for v in value.split():
			addObject(tmp, obos.filter(title__regex='\w*' + v + '\w*'))
			addObject(tmp, obos.filter(title__iregex='\w*' + v + '\w*'))
	list += list_1
	list_1 = getOrderedList(list_1)
	list_1 += getOrderedList(tmp)

	value = hashtable.get(fields[1])
	list_2 = []
	tmp = []
	if value != None and value != '':
		addObject(list_2, obos.filter(subject__search=value))
		addObject(list_2, obos.filter(subject__contains=value))
		for v in value.split():
			addObject(tmp, obos.filter(subject__regex='\w*' + v + '\w*'))
			addObject(tmp, obos.filter(subject__iregex='\w*' + v + '\w*'))
	list += list_2
	list_2 = getOrderedList(list_2)
	list_2 += getOrderedList(tmp)

	value = hashtable.get(fields[2])
	list_3 = []
	tmp = []
	if value != None and value != '':
		addObjectViaPerson(list_3, pos.filter(name__search=value))
		addObjectViaPerson(list_3, pos.filter(name__contains=value))
		for v in value.split():
			addObjectViaPerson(tmp, pos.filter(name__regex='\w*' + v + '\w*'))
			addObjectViaPerson(tmp, pos.filter(name__iregex='\w*' + v + '\w*'))
	list += list_3
	list_3 = getOrderedList(list_3)
	list_3 += getOrderedList(tmp)

	value = hashtable.get(fields[3])
	list_4 = []
	tmp = []
	if value != None and value != '':
		addObject(list_4, obos.filter(for_class__search=value))
		addObject(list_4, obos.filter(for_class__contains=value))
		for v in value.split():
			addObject(tmp, obos.filter(for_class__regex='\w*' + v + '\w*'))
			addObject(tmp, obos.filter(for_class__iregex='\w*' + v + '\w*'))
	list += list_4
	list_4 = getOrderedList(list_4)
	list_4 += getOrderedList(tmp)

	list = getOrderedList(list)
	list += getOrderedList(list_1 + list_2 + list_3 + list_4)
	list = getOrderedList(list)
	for l in list:
		objects.append(l)
	return objects

def firstObjectSearch(value, obos, pos, orgos):
	"""
	Used to search and return 'object' list for the Simple Search box.
	"""
	list = []
	objects = []

	list_1 = []
	addObject(list_1, obos.filter(title__search=value))
	addObject(list_1, obos.filter(subject__search=value))
	addObject(list_1, obos.filter(for_class__search=value))
	addObject(list_1, obos.filter(other_subject__search=value))
	addObjectViaPerson(list_1, pos.filter(name__search=value))
	addObjectViaPerson(list_1, pos.filter(sex__search=value))
	addObjectViaOrg(list_1, orgos.filter(name__search=value))
	addObjectViaOrg(list_1, orgos.filter(address__search=value))
	list_1 = getOrderedList(list_1)
	list += list_1

	list_2 = []
	addObject(list_2, obos.filter(title__contains=value))
	addObject(list_2, obos.filter(subject__contains=value))
	addObject(list_2, obos.filter(for_class__contains=value))
	addObject(list_2, obos.filter(other_subject__contains=value))
	addObject(list_2, obos.filter(person__name__contains=value))
	addObject(list_2, obos.filter(person__sex__contains=value))
	addObject(list_2, obos.filter(person__organization__name__contains=value))
	addObject(list_2, obos.filter(person__organization__address__contains=value))
	addObject(list_2, obos.filter(title__icontains=value))
	addObject(list_2, obos.filter(subject__icontains=value))
	addObject(list_2, obos.filter(for_class__icontains=value))
	addObject(list_2, obos.filter(other_subject__icontains=value))
	addObjectViaPerson(list_2, pos.filter(name__icontains=value))
	addObjectViaPerson(list_2, pos.filter(sex__icontains=value))
	addObjectViaOrg(list_2, orgos.filter(name__icontains=value))
	addObjectViaOrg(list_2, orgos.filter(address__icontains=value))
	list_2 = getOrderedList(list_2)
	list += list_2
	
	list_3 = []
	values = value.split()
	for v in values:
		addObject(list_3, obos.filter(title__regex='\w*' + v + '\w*'))
		addObject(list_3, obos.filter(subject__regex='\w*' + v + '\w*'))
		addObject(list_3, obos.filter(for_class__regex='\w*' + v + '\w*'))
		addObject(list_3, obos.filter(other_subject__regex='\w*' + v + '\w*'))
		addObject(list_3, obos.filter(person__name__regex='\w*' + v + '\w*'))
		addObject(list_3, obos.filter(person__sex__regex='\w*' + v + '\w*'))
		addObject(list_3, obos.filter(person__organization__name__regex='\w*' + v + '\w*'))
		addObject(list_3, obos.filter(person__organization__address__regex='\w*' + v + '\w*'))
		addObject(list_3, obos.filter(title__iregex='\w*' + v + '\w*'))
		addObject(list_3, obos.filter(subject__iregex='\w*' + v + '\w*'))
		addObject(list_3, obos.filter(for_class__iregex='\w*' + v + '\w*'))
		addObject(list_3, obos.filter(other_subject__iregex='\w*' + v + '\w*'))
		addObjectViaPerson(list_3, pos.filter(name__iregex='\w*' + v + '\w*'))
		addObjectViaPerson(list_3, pos.filter(sex__iregex='\w*' + v + '\w*'))
		addObjectViaOrg(list_3, orgos.filter(name__iregex='\w*' + v + '\w*'))
		addObjectViaOrg(list_3, orgos.filter(address__iregex='\w*' + v + '\w*'))
	list_3 = getOrderedList(list_3)
	list += list_3
	list = getOrderedList(list)

	for l in list:
		objects.append(l)
	return objects

def addObjectViaOrg(list1, list2):
	"""
	Retreives 'object' objects from a QuerySet on orgos.
	"""
	for i in list2.all():
		for j in i.person_set.all():
			for k in j.object_set.all():
				list1.append(k)

def addObjectViaPerson(list1, list2):
	"""
	Retreives 'object' objects from a QuerySet on pos.
	"""
	for i in list2.all():
		for j in i.object_set.all():
			list1.append(j)

def addObject(list1, list2):
	"""
	Retreives 'object' objects from a QuerySet on obos.
	"""
	for i in list2.all():
		list1.append(i)


######################## NO DATABASE QUERIES BELOW ###########################


def getMatch(listOfStrings, string, list):
	"""
	Adds all the strings of 'listOfStrings' that start with 'string' into 'list'.
	Case sensitive match is given higher priority and is placed higher in 'list' than case insensitive.
	Duplication of data is avoided.
	"""
	# Case sensitive search
	for s in listOfStrings:
		if s.startswith(string):
			if s[-1] == '\n':
				if s[:-1] not in list:
					list.append(s[:-1])
			else:
				if s[:] not in list:
					list.append(s[:])
	# Case insensitive search
	for s in listOfStrings:
		if s.upper().startswith(string.upper()):
			if s[-1] == '\n':
				if s[:-1] not in list:
					list.append(s[:-1])
			else:
				if s[:] not in list:
					list.append(s[:])

def getOrderedList(list):
	"""
	Returns a list with all unique elements ordered on the basis of relevence.
	The more number of times an element is present in list, the higher it is placed in the returning list.
	"""
	hash = {}
	for l in list:
		if l in hash.keys():
			value = hash.pop(l)
			hash[l] = value + 1
		else:
			hash[l] = 1
	return sorted(hash, key=lambda key: hash[key], reverse=True)

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
	strings = string.split(SD + SD)
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
	updated to match the list argument, ie, 'len(texts) = len(fields)'.
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
	if (type(text)) == list:
		return str(text)
	if text == None or len(text) < 2:
		return text
	text = text.replace(SD, ' ')
	text = text.strip()
	return text

# To run is as a standalone script for testing.
if __name__ == '__main__':
	# This imitates the actual list that is passed for Search.
	list = ['u', '', '', '']
	print('----------------------Searching-----------------------')
	# Function that searches.
	tup = (getValidText(list), 1)
	finalSearch(str(tup))

	print('----------------------Suggesting-----------------------')
	# This imitates Suggest.
	text = 'how'
	populateSuggest()
	suggestSearch(text, 'Name')
