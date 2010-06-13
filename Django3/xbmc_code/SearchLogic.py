import re
import constants_plugin as CP

def suggestSearch(text):
	suggestions = []
	suggestions += [text, text + 'a']
	return suggestions

def stripColons(text):
	print(text)
	SD = CP.SEARCH_DELIMITER
	if text[-1] == SD:
		text = text[:-1]
	if text[0] == SD:
		text = text[1:]
	text = ' '.join(re.split(SD, text))
	return text

def getValidText(texts):
	return 'Hello there...'
