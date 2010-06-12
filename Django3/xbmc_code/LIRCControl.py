#!./modules/jython2.5.1/jython
import time

from org.lirc.util import IRActionListener, SimpleLIRCClient
import SearchLogic

class MoveListener(IRActionListener):
	def __init__(self, searchObject):
		self.searchObject = searchObject
		self.times = []
		self.prevKey = None
		self.onTime = False
		self.allCaps = False

	def action(self, command):
		self.focussedField = self.getFocusedField()
		try:
			if command == 'moveUp':
				self.searchObject.nameLabel.text = 'MoveUp'
			elif command == 'moveDown':
				self.focussedField.setPopupVisible(True)
			elif command == 'moveRight':
				self.clearTime()
			elif command == 'moveLeft':
				self.searchObject.nameLabel.text = 'MoveUp'
			elif command == 'exit':
				self.searchObject.exit()
			elif command == 'one' or command == 'two' or command == 'three' or \
					command == 'four' or command == 'five' or command == 'six' or \
					command == 'seven' or command == 'eight' or command == 'nine' or \
					command == 'zero' or command == 'star' or command == 'hash':
						newKey = self.checkPrevKey(command)
						oldText = self.focussedField.getEditor().getEditorComponent().text
						if self.onTime:
							newText = oldText[:-1]
						else:
							newText = oldText
						if self.allCaps:
							newKey = newKey.capitalize()
						if len(newKey):
							newText += newKey
						self.focussedField.removeAllItems()
						items = SearchLogic.suggestSearch(newText)
						for item in items:
							self.focussedField.addItem(item)
						self.focussedField.setPopupVisible(True)
		except Exception, e:
			print(str(e))

	def getFocusedField(self):
		if self.searchObject.nameField.getEditor().getEditorComponent().hasFocus() == True:
			return self.searchObject.nameField
		elif self.searchObject.subjectField.getEditor().getEditorComponent().hasFocus() == True:
			return self.searchObject.subjectField
		elif self.searchObject.authorField.getEditor().getEditorComponent().hasFocus() == True:
			return self.searchObject.authorField
		elif self.searchObject.classField.getEditor().getEditorComponent().hasFocus() == True:
			return self.searchObject.classField

	def checkPrevKey(self, key):
		self.onTime = False
		if self.prevKey != None and key == self.prevKey:
			t1 = time.clock()
			if t1 - self.times[-1] <= 3.0:
				tempKey = self.getNextKey(key, len(self.times))
				self.setTime(key)
				self.onTime = True
				return tempKey
			else:
				self.clearTime()
				self.setTime(key)
		elif self.prevKey == None:
			self.clearTime()
			self.setTime(key)
		elif key != self.prevKey:
			self.clearTime()
			self.setTime(key)
		return self.getNextKey(key, 0)
			
	def setTime(self, key):
		t0 = time.clock()
		self.times.append(t0)
		self.prevKey = key

	def clearTime(self):
		self.times = []
		self.prevKey = None

	def getNextKey(self, key, count):
		lettersOnTwo = 7
		lettersOnThree = 7
		lettersOnFour = 7
		lettersOnFive = 7
		lettersOnSix = 7
		lettersOnSeven = 9
		letterOnEight = 7
		lettersOnNine = 9
		lettersOnZero = 2
		lettersOnOne = 21
		lettersOnStar = 0
		lettersOnHash = 1

		if key == 'two':
			if count%lettersOnTwo == 0:
				return 'a'
			elif count%lettersOnTwo == 1:
				return 'b'
			elif count%lettersOnTwo == 2:
				return 'c'
			elif count%lettersOnTwo == 3:
				return '2'
			elif count%lettersOnTwo == 4:
				return 'A'
			elif count%lettersOnTwo == 5:
				return 'B'
			elif count%lettersOnTwo == 6:
				return 'C'
			else:	
				return 'a'
		elif key == 'three':
			if count%lettersOnThree == 0:
				return 'd'
			elif count%lettersOnThree == 1:
				return 'e'
			elif count%lettersOnThree == 2:
				return 'f'
			elif count%lettersOnThree == 3:
				return '3'
			elif count%lettersOnThree == 4:
				return 'D'
			elif count%lettersOnThree == 5:
				return 'E'
			elif count%lettersOnThree == 6:
				return 'F'
			else:	
				return 'd'
		elif key == 'four':
			if count%lettersOnFour == 0:
				return 'g'
			elif count%lettersOnFour == 1:
				return 'h'
			elif count%lettersOnFour == 2:
				return 'i'
			elif count%lettersOnFour == 3:
				return '4'
			elif count%lettersOnFour == 4:
				return 'G'
			elif count%lettersOnFour == 5:
				return 'H'
			elif count%lettersOnFour == 6:
				return 'I'
			else:	
				return 'g'
		elif key == 'five':
			if count%lettersOnFive == 0:
				return 'j'
			elif count%lettersOnFive == 1:
				return 'k'
			elif count%lettersOnFive == 2:
				return 'l'
			elif count%lettersOnFive == 3:
				return '5'
			elif count%lettersOnFive == 4:
				return 'J'
			elif count%lettersOnFive == 5:
				return 'K'
			elif count%lettersOnFive == 6:
				return 'L'
			else:	
				return 'j'
		elif key == 'six':
			if count%lettersOnSix == 0:
				return 'm'
			elif count%lettersOnSix == 1:
				return 'n'
			elif count%lettersOnSix == 2:
				return 'o'
			elif count%lettersOnSix == 3:
				return '6'
			elif count%lettersOnSix == 4:
				return 'M'
			elif count%lettersOnSix == 5:
				return 'N'
			elif count%lettersOnSix == 6:
				return 'O'
			else:	
				return 'm'
		elif key == 'seven':
			if count%lettersOnSeven == 0:
				return 'p'
			elif count%lettersOnSeven == 1:
				return 'q'
			elif count%lettersOnSeven == 2:
				return 'r'
			elif count%lettersOnSeven == 3:
				return 's'
			elif count%lettersOnSeven == 4:
				return '7'
			elif count%lettersOnSeven == 5:
				return 'P'
			elif count%lettersOnSeven == 6:
				return 'Q'
			elif count%lettersOnSeven == 7:
				return 'R'
			elif count%lettersOnSeven == 8:
				return 'S'
			else:	
				return 'p'
		elif key == 'eight':
			if count%letterOnEight == 0:
				return 't'
			elif count%letterOnEight == 1:
				return 'u'
			elif count%letterOnEight == 2:
				return 'v'
			elif count%letterOnEight == 3:
				return '8'
			elif count%letterOnEight == 4:
				return 'T'
			elif count%letterOnEight == 5:
				return 'U'
			elif count%letterOnEight == 6:
				return 'V'
			else:	
				return 't'
		elif key == 'nine':
			if count%lettersOnNine == 0:
				return 'w'
			elif count%lettersOnNine == 1:
				return 'x'
			elif count%lettersOnNine == 2:
				return 'y'
			elif count%lettersOnNine == 3:
				return 'z'
			elif count%lettersOnNine == 4:
				return '9'
			elif count%lettersOnNine == 5:
				return 'W'
			elif count%lettersOnNine == 6:
				return 'X'
			elif count%lettersOnNine == 7:
				return 'Y'
			elif count%lettersOnNine == 8:
				return 'Z'
			else:	
				return 'w'
		elif key == 'zero':
			if count%lettersOnZero == 0:
				return ' '
			elif count%lettersOnZero == 1:
				return '0'
			else:	
				return 'a'
		elif key == 'one':
			if count%lettersOnOne == 0:
				return '1'
			elif count%lettersOnOne == 1:
				return '"'
			elif count%lettersOnOne == 2:
				return ','
			elif count%lettersOnOne == 3:
				return '.'
			elif count%lettersOnOne == 4:
				return '-'
			elif count%lettersOnOne == 5:
				return '?'
			elif count%lettersOnOne == 6:
				return '!'
			elif count%lettersOnOne == 7:
				return '@'
			elif count%lettersOnOne == 8:
				return '#'
			elif count%lettersOnOne == 9:
				return '$'
			elif count%lettersOnOne == 10:
				return '%'
			elif count%lettersOnOne == 11:
				return '^'
			elif count%lettersOnOne == 12:
				return '&'
			elif count%lettersOnOne == 13:
				return '*'
			elif count%lettersOnOne == 14:
				return '('
			elif count%lettersOnOne == 15:
				return ')'
			elif count%lettersOnOne == 16:
				return '+'
			elif count%lettersOnOne == 17:
				return '='
			elif count%lettersOnOne == 18:
				return '|'
			elif count%lettersOnOne == 19:
				return ':'
			elif count%lettersOnOne == 20:
				return ';'
			else:	
				return '1'
		elif key == 'star':
			return ''
		elif key == 'hash':
			if count%lettersOnHash == 0:
				if self.allCaps:
					self.allCaps = False
				else:
					self.allCaps = True
				return ''
