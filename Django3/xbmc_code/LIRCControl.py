#!./modules/jython2.5.1/jython
import time, sys, traceback

from org.lirc.util import IRActionListener, SimpleLIRCClient
from java.awt import KeyboardFocusManager
from javax.swing import *
import SearchLogic

class MoveListener(IRActionListener):
	def __init__(self, searchObject):
		self.searchObject = searchObject
		self.times = []
		self.prevKey = None
		self.onTime = False
		self.allCaps = False

	def action(self, command):
		# ok, enter and exit do not work with XBMC. They are managed by XBMC as its own events.
		self.focussedField = self.searchObject.getFocussedField()
		self.focussedButtonName = self.searchObject.getFocussedButtonName()
		try:
			if command == 'chanUp':
				# A common command to get next component in focus. 
				# We have checkboxes, buttons, textfields etc. so a common command is required.
				KeyboardFocusManager.getCurrentKeyboardFocusManager().focusNextComponent()
			elif command == 'chanDown':
				# A common command to get previous component in focus. 
				KeyboardFocusManager.getCurrentKeyboardFocusManager().focusPreviousComponent()
			elif command == 'play':
				# A common command to search.
				self.searchObject.buttonPressedAction('Search')
			elif self.focussedField != None:
				# When some textfield has focus.
				if command == 'moveUp':
					self.searchObject.nameLabel.text = 'MoveUp'
				elif command == 'moveDown':
					if type(self.focussedField) == JComboBox:
						self.focussedField.setPopupVisible(True)
				elif command == 'moveRight':
					self.clearTime()
				elif command == 'moveLeft':
					self.searchObject.nameLabel.text = 'MoveUp'
				elif command == 'exit':
					self.searchObject.exit()
				elif command == 'ok':
					self.searchObject.buttonPressedAction('Search')
				elif command == 'mute':
					self.searchObject.buttonPressedAction('Search')
				elif command == 'enter':
					KeyboardFocusManager.getCurrentKeyboardFocusManager().focusNextComponent()
				elif command == 'clear':
					if type(self.focussedField) == JComboBox:
						self.focussedField.getEditor().getEditorComponent().text = ''
					elif type(self.focussedField) == JTextField or type(self.focussedField) == JTextArea:
						self.focussedField.text = ''
				elif command == 'one' or command == 'two' or command == 'three' or \
						command == 'four' or command == 'five' or command == 'six' or \
						command == 'seven' or command == 'eight' or command == 'nine' or \
						command == 'zero' or command == 'star' or command == 'hash':
							newKey = self.checkPrevKey(command)
							oldText = ''
							if type(self.focussedField) == JComboBox:
								oldText = self.focussedField.getEditor().getEditorComponent().text
							elif type(self.focussedField) == JTextField or type(self.focussedField) == JTextArea:
								oldText = self.focussedField.text
							if self.onTime:
								newText = oldText[:-1]
							else:
								newText = oldText
							if self.allCaps:
								newKey = newKey.capitalize()
							if len(newKey):
								newText += newKey
								if type(self.focussedField) == JComboBox:
									visible = self.searchObject.addSuggestedList(newText, self.focussedField)
									self.focussedField.setPopupVisible(visible)
								elif type(self.focussedField) == JTextField or type(self.focussedField) == JTextArea:
									self.focussedField.text = newText
				elif command == 'back':
					self.clearTime()
					if type(self.focussedField) == JComboBox:
						newText = self.focussedField.getEditor().getEditorComponent().text
						newText = newText[:-1]
						visible = self.searchObject.addSuggestedList(newText, self.focussedField)
						self.focussedField.setPopupVisible(visible)
					elif type(self.focussedField) == JTextField or type(self.focussedField) == JTextArea:
						newText = self.focussedField.text
						newText = newText[:-1]
						self.focussedField.text = newText
			elif self.focussedButtonName != None:
				# When a button has focus.
				if command == 'moveUp':
					KeyboardFocusManager.getCurrentKeyboardFocusManager().focusPreviousComponent()
				elif command == 'moveDown':
					KeyboardFocusManager.getCurrentKeyboardFocusManager().focusNextComponent()
				elif command == 'moveRight':
					KeyboardFocusManager.getCurrentKeyboardFocusManager().focusNextComponent()
				elif command == 'moveLeft':
					KeyboardFocusManager.getCurrentKeyboardFocusManager().focusPreviousComponent()
				elif command == 'exit':
					self.searchObject.exit()
				elif command == 'ok':
					self.searchObject.buttonPressedAction(self.focussedButtonName)
				elif command == 'mute':
					self.searchObject.buttonPressedAction(self.focussedButtonName)
				elif command == 'back':
					KeyboardFocusManager.getCurrentKeyboardFocusManager().focusPreviousComponent()
			elif command == 'enter':
				# If other JComponent like JCheckbox, JRadioButton is selected.
				otherComponent = self.searchObject.frame.getFocusOwner()
				if type(otherComponent) == JCheckBox:
					self.searchObject.checkboxClickedAction(otherComponent)
				elif type(otherComponent) == JRadioButton:
					otherComponent.setSelected(True)
			elif command == 'moveUp':
				# If non-editable JComboBox is selected moveUp.
				otherComponent = self.searchObject.frame.getFocusOwner()
				if type(otherComponent) == JComboBox:
					otherComponent.setPopupVisible(True)
					nextIndex = otherComponent.getSelectedIndex() - 1
					if nextIndex < 0:
						nextIndex = 0
					otherComponent.setSelectedIndex(nextIndex)
			elif command == 'moveDown':
				# If non-editable JComboBox is selected moveDown.
				otherComponent = self.searchObject.frame.getFocusOwner()
				if type(otherComponent) == JComboBox:
					otherComponent.setPopupVisible(True)
					nextIndex = otherComponent.getSelectedIndex() + 1
					if nextIndex >= otherComponent.getItemCount():
						nextIndex = otherComponent.getItemCount() - 1
					otherComponent.setSelectedIndex(nextIndex)
			elif command == 'moveRight':
				# When neither any textfield, button, checkbox etc has focus. 
				# Switch between tabs. Get next tab in focus.
				index = self.searchObject.tabbedPane.getSelectedIndex() + 1
				if index >= self.searchObject.tabbedPane.getTabCount():
					index = 0
				self.searchObject.tabbedPane.setSelectedIndex(index)
				#KeyboardFocusManager.getCurrentKeyboardFocusManager().focusNextComponent()
			elif command == 'moveLeft':
				# When neither any textfield, button, checkbox etc has focus. 
				# Switch between tabs. Get previous tab in focus.
				index = self.searchObject.tabbedPane.getSelectedIndex() - 1
				if index <= -1:
					index = self.searchObject.tabbedPane.getTabCount() - 1
				self.searchObject.tabbedPane.setSelectedIndex(index)
				#KeyboardFocusManager.getCurrentKeyboardFocusManager().focusNextComponent()
		except Exception, e:
			sys.stderr.write((str(e)))
			traceback.print_exc(file=sys.stderr)

	def checkPrevKey(self, key):
		self.onTime = False
		if self.prevKey != None and key == self.prevKey:
			t1 = time.clock()
			if t1 - self.times[-1] <= 1.0:
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
		else:
			return ''
