#!./modules/jython2.5.1/jython
# This works!
import os, sys

import constants_plugin as CP
import LIRCControl, SearchLogic

from org.lirc.util import IRActionListener, SimpleLIRCClient
from com.swabunga.spell.engine import SpellDictionaryHashMap
from com.swabunga.spell.event import SpellChecker

from java.io import File
import java.io.IOException

from java.lang import System	        
from java.net import URL	        
from javax.swing import *	        
from javax.swing.plaf.synth import *	        
from javax.swing.GroupLayout import Alignment	        
from java.awt import KeyboardFocusManager
from java.awt.event import KeyEvent

class Search():
	def fieldKeyReleased(self, event):
		eventSourceName = event.source.name
		self.focussedField = self.getFocussedField(eventSourceName)
		if self.focussedField != None:
			text = self.focussedField.getEditor().getEditorComponent().text
			visible = True
			oldText = self.getOldFieldText()
			if text != '' and (oldText == None or (oldText != text and \
					event.getKeyCode() != KeyEvent.VK_UP and event.getKeyCode() != KeyEvent.VK_DOWN)):
				self.setOldFieldText(text)
				self.focussedField.removeAllItems()
				visible = self.addSuggestedList(text, self.focussedField)
			elif event.getKeyCode() == KeyEvent.VK_ESCAPE or event.getKeyCode() == KeyEvent.VK_SHIFT:
				visible = False
			self.focussedField.setPopupVisible(visible)
		elif eventSourceName != None and (eventSourceName == 'Search' or \
				eventSourceName == 'Cancel' or eventSourceName == 'Advanced') and event.getKeyCode() == KeyEvent.VK_ENTER:
			self.buttonPressedAction(eventSourceName)
		elif event.getKeyCode() == KeyEvent.VK_ENTER:
			self.buttonPressedAction('Search')
		else:
			self.buttonPressedAction('Null')		# This case may come
	
	def addSuggestedList(self, text, focussedField):
		items = []
		# Get suggestions from Database.
		if len(text) >= 3:
			items += SearchLogic.suggestSearch(text, focussedField.name)
		print(items)
		# Get suggestions from Jazzy.
		lastWord = text.split()[-1]
		if len(lastWord) >= 3:
			phonetic_items = self.getSuggestions(lastWord)
			print(phonetic_items)
			for p in phonetic_items:
				q = str(p)
				if q not in items and len(q) >= len(lastWord):
					items.append(q)
		# Add suggestions to Drop Down list.
		self.focussedField.addItem(text)
		for item in items:
			if item != text:
				self.focussedField.addItem(item)
		self.focussedField.setPopupVisible(False)
		self.focussedField.setMaximumRowCount(8)
		self.focussedField.setPopupVisible(True)
		if len(items) == 0:
			return False
		else:
			return True

	def buttonPressed(self, event):
		self.buttonPressedAction(event.source.name)
	
	def buttonPressedAction(self, buttonName):
		if buttonName == 'Search':
			if self.mode == 0:
				texts = [self.defaultField.getEditor().getEditorComponent().text]
			elif self.mode == 1:
				texts = [self.nameField.getEditor().getEditorComponent().text, \
						self.subjectField.getEditor().getEditorComponent().text, \
						self.authorField.getEditor().getEditorComponent().text, \
						self.classField.getEditor().getEditorComponent().text]
			text = SearchLogic.getValidText(texts)
			print(text)
			# Can't call SearchLogic.finalSearch in this file. This is Jython that is Python. 
			# It uses MySQLdb which does not work with Jython.
			self.exit()
		elif buttonName == 'Cancel':
			print('Cancel')
			self.exit()
		elif buttonName == 'Advanced':
			print('Advanced')
			if self.mode == 0:
				self.win.visible = False
				self.secondSearch()
			elif self.mode == 1:
				self.win.visible = False
				self.thirdSearch()
			elif self.mode == 2:
				self.win.visible = False
				self.firstSearch()
		else:
			pass									# This case may come
	
	def setOldFieldText(self, text):
		try:
			if self.nameField.getEditor().getEditorComponent().hasFocus() == True:
				self.oldNameFieldText = text
				return
		except:
			pass
		try:
			if self.subjectField.getEditor().getEditorComponent().hasFocus() == True:
				self.oldSubjectFieldText = text
				return
		except:
			pass
		try:
			if self.authorField.getEditor().getEditorComponent().hasFocus() == True:
				self.oldAuthorFieldText = text
				return
		except:
			pass
		try:
			if self.classField.getEditor().getEditorComponent().hasFocus() == True:
				self.oldClassFieldText = text
				return
		except:
			pass
		self.oldNameFieldText = text

	def getOldFieldText(self):
		try:
			if self.nameField.getEditor().getEditorComponent().hasFocus() == True:
				return self.oldNameFieldText
		except:
			pass
		try:
			if self.subjectField.getEditor().getEditorComponent().hasFocus() == True:
				return self.oldSubjectFieldText
		except:
			pass
		try:
			if self.authorField.getEditor().getEditorComponent().hasFocus() == True:
				return self.oldAuthorFieldText
		except:
			pass
		try:
			if self.classField.getEditor().getEditorComponent().hasFocus() == True:
				return self.oldClassFieldText
		except:
			pass
		return self.oldNameFieldText

	def getFocussedButtonName(self):
		if self.searchButton.hasFocus() == True:
			return self.searchButton.name
		elif self.cancelButton.hasFocus() == True:
			return self.cancelButton.name
		elif self.advancedButton.hasFocus() == True:
			return self.advancedButton.name
		else:
			return None								# This case may come

	def getFocussedField(self, name):
		if name == 'NameTextEditor':
			return self.nameField
		elif name == 'SubjectTextEditor':
			return self.subjectField
		elif name == 'AuthorTextEditor':
			return self.authorField
		elif name == 'ClassTextEditor':
			return self.classField
		elif name == 'DefaultTextEditor':
			return self.defaultField
		else:
			return None								# This case may come

	def getSuggestions(self, word):
		"""
		Returns suggested words form Jazzy.
		"""
		return self.spellChecker.getSuggestions(word, self.threshold)

	def exit(self):
		try:
			self.client.stopListening()
		except:
			pass
		os.environ['JYTHON_RUNNING'] = 'NO'
		System.exit(0)


######################################################## INIT ########################################################


	def __init__(self):
		# The following lines initialize Jazzy. It is an auto-completion Java library.
		# It provides spell-checking and suggests phonetically similar words.
		self.dictionary = SpellDictionaryHashMap(File(os.getcwd() + '/xbmc_code/suggestions/en-US.dic'))
		self.spellChecker = SpellChecker(self.dictionary)
		self.threshold = 3	# Doesn't do anything

		# Useful field to check whether the keyStroke changed the text in field or not.
		# Which is then used to invoke Auto-Suggest feature.
		self.oldNameFieldText = None
		self.oldSubjectFieldText = None
		self.oldAuthorFieldText = None
		self.oldClassFieldText = None

		# The following lines handle LIRC remote events.
		try:
			self.client = SimpleLIRCClient('xbmc_code/search.lirc')
			self.client.addIRActionListener(LIRCControl.MoveListener(self));
		except:
			pass
		
		# The following lines enable custom look and feel.
		#lookAndFeel = SynthLookAndFeel()
		#lookAndFeel.load(URL('file://' + CP.PLUGIN_PATH + '/xbmc_code/laf.xml'))
		#UIManager.setLookAndFeel(lookAndFeel)
		#JFrame.setDefaultLookAndFeelDecorated(True)
		self.firstSearch()

	def firstSearch(self):
		self.mode = 0
		self.win = JFrame('Search Videos...', defaultCloseOperation = WindowConstants.EXIT_ON_CLOSE)
		self.win.size = (700, 700)
		self.win.setLocationRelativeTo(None)
		# GroupLayout is used to decide the positions of JButtons and JComboBoxes.
		self.layout = GroupLayout(self.win.contentPane)
		self.win.contentPane.layout = self.layout
		self.layout.setAutoCreateGaps(True)
		self.layout.setAutoCreateContainerGaps(True)
		
		self.defaultField = JComboBox()
		self.defaultField.name = 'Default'													# Important attribute. Used in suggestSearch.
		self.defaultField.getEditor().getEditorComponent().name = 'DefaultTextEditor'		# Important attribute. Used in getFocussedField.
		self.defaultField.preferredSize = (200, 20)
		self.defaultField.editable = True
		self.defaultField.getEditor().getEditorComponent().keyReleased = self.fieldKeyReleased
		
		self.searchButton = JButton('Search')
		self.searchButton.preferredSize = (100, 20)
		self.searchButton.actionPerformed = self.buttonPressed
		self.searchButton.keyReleased = self.fieldKeyReleased
		self.searchButton.name = 'Search'				# Very important attribute.
		self.cancelButton = JButton('Cancel')
		self.cancelButton.preferredSize = (100, 20)
		self.cancelButton.actionPerformed = self.buttonPressed
		self.cancelButton.keyReleased = self.fieldKeyReleased
		self.cancelButton.name = 'Cancel'				# Very important attribute.
		self.advancedButton = JButton('Advanced')
		self.advancedButton.preferredSize = (100, 20)
		self.advancedButton.actionPerformed = self.buttonPressed
		self.advancedButton.keyReleased = self.fieldKeyReleased
		self.advancedButton.name = 'Advanced'				# Very important attribute.
		
		self.defaultLabel = JLabel('Search')
		self.layout.setHorizontalGroup(self.layout.createSequentialGroup()
		        .addGroup(self.layout.createParallelGroup(Alignment.LEADING)
					.addComponent(self.defaultLabel))
		        .addGroup(self.layout.createParallelGroup(Alignment.TRAILING)
			        .addComponent(self.defaultField)
					.addComponent(self.cancelButton))
		       	.addGroup(self.layout.createParallelGroup(Alignment.LEADING)
					.addComponent(self.advancedButton)
					.addComponent(self.searchButton))
		)
		self.layout.setVerticalGroup(self.layout.createSequentialGroup()
			.addGroup(self.layout.createParallelGroup(Alignment.BASELINE)
		                .addComponent(self.defaultLabel)
		                .addComponent(self.defaultField)
						.addComponent(self.advancedButton))
			.addGroup(self.layout.createParallelGroup(Alignment.BASELINE)
			        .addComponent(self.cancelButton)
		        	.addComponent(self.searchButton))
		)
		
		self.win.pack()
		self.win.show()

	def secondSearch(self):
		self.mode = 1
		# The UI part begins now. This JFrame is used to paint everythong.
		self.win = JFrame('Search Videos...', defaultCloseOperation = WindowConstants.EXIT_ON_CLOSE)
		self.win.size = (700, 700)
		self.win.setLocationRelativeTo(None)
		# GroupLayout is used to decide the positions of JButtons and JComboBoxes.
		self.layout = GroupLayout(self.win.contentPane)
		self.win.contentPane.layout = self.layout
		self.layout.setAutoCreateGaps(True)
		self.layout.setAutoCreateContainerGaps(True)
		
		self.nameField = JComboBox()
		self.nameField.name = 'Name'												# Important attribute. Used in suggestSearch.
		self.nameField.getEditor().getEditorComponent().name = 'NameTextEditor'		# Important attribute. Used in getFocussedField.
		self.nameField.preferredSize = (200, 20)
		self.nameField.editable = True
		self.nameField.getEditor().getEditorComponent().keyReleased = self.fieldKeyReleased
		
		self.subjectField = JComboBox()
		self.subjectField.name = 'Subject'												# Important attribute. Used in suggestSearch.
		self.subjectField.getEditor().getEditorComponent().name = 'SubjectTextEditor'	# Important attribute. Used in getFocussedField.
		self.subjectField.preferredSize = (200, 20)
		self.subjectField.editable = True
		self.subjectField.getEditor().getEditorComponent().keyReleased = self.fieldKeyReleased
		
		self.authorField = JComboBox()
		self.authorField.name = 'Author'												# Important attribute. Used in suggestSearch.
		self.authorField.getEditor().getEditorComponent().name = 'AuthorTextEditor'		# Important attribute. Used in getFocussedField.
		self.authorField.preferredSize = (200, 20)
		self.authorField.editable = True
		self.authorField.getEditor().getEditorComponent().keyReleased = self.fieldKeyReleased
		
		self.classField = JComboBox()
		self.classField.name = 'Class'												# Important attribute. Used in suggestSearch.
		self.classField.getEditor().getEditorComponent().name = 'ClassTextEditor'	# Important attribute. Used in getFocussedField.
		self.classField.preferredSize = (200, 20)
		self.classField.editable = True
		self.classField.getEditor().getEditorComponent().keyReleased = self.fieldKeyReleased
		
		self.searchButton = JButton('Search')
		self.searchButton.preferredSize = (100, 20)
		self.searchButton.actionPerformed = self.buttonPressed
		self.searchButton.keyReleased = self.fieldKeyReleased
		self.searchButton.name = 'Search'				# Very important attribute.
		self.cancelButton = JButton('Cancel')
		self.cancelButton.preferredSize = (100, 20)
		self.cancelButton.actionPerformed = self.buttonPressed
		self.cancelButton.keyReleased = self.fieldKeyReleased
		self.cancelButton.name = 'Cancel'				# Very important attribute.
		self.advancedButton = JButton('Advanced')
		self.advancedButton.preferredSize = (100, 20)
		self.advancedButton.actionPerformed = self.buttonPressed
		self.advancedButton.keyReleased = self.fieldKeyReleased
		self.advancedButton.name = 'Advanced'				# Very important attribute.
		
		self.nameLabel = JLabel('Name')
		self.subjectLabel = JLabel('Subject')
		self.authorLabel = JLabel('Author')
		self.classLabel = JLabel('Class')
		
		self.layout.setHorizontalGroup(self.layout.createSequentialGroup()
		        .addGroup(self.layout.createParallelGroup(Alignment.LEADING)
					.addComponent(self.nameLabel)
					.addComponent(self.subjectLabel)
					.addComponent(self.authorLabel)
					.addComponent(self.classLabel))
		        .addGroup(self.layout.createParallelGroup(Alignment.TRAILING)
			        .addComponent(self.nameField)
					.addComponent(self.subjectField)
					.addComponent(self.authorField)
					.addComponent(self.classField)
					.addComponent(self.cancelButton))
		       	.addGroup(self.layout.createParallelGroup(Alignment.LEADING)
					.addComponent(self.advancedButton)
					.addComponent(self.searchButton))
		)
		self.layout.setVerticalGroup(self.layout.createSequentialGroup()
			.addGroup(self.layout.createParallelGroup(Alignment.BASELINE)
		                .addComponent(self.nameLabel)
		                .addComponent(self.nameField))
			.addGroup(self.layout.createParallelGroup(Alignment.BASELINE)
		                .addComponent(self.subjectLabel)
		                .addComponent(self.subjectField))
			.addGroup(self.layout.createParallelGroup(Alignment.BASELINE)
		                .addComponent(self.authorLabel)
		                .addComponent(self.authorField)
						.addComponent(self.advancedButton))
			.addGroup(self.layout.createParallelGroup(Alignment.BASELINE)
		                .addComponent(self.classLabel)
		                .addComponent(self.classField))
			.addGroup(self.layout.createParallelGroup(Alignment.BASELINE)
			        .addComponent(self.cancelButton)
		        	.addComponent(self.searchButton))
		)
		
		self.win.pack()
		self.win.show()

	def thirdSearch(self):
		# A variable to differentiate which search box is currently open.
		# Used in buttonPressedAction.
		self.mode = 2
		# The UI part begins now. This JFrame is used to paint everythong.
		self.win = JFrame('Search Videos...', defaultCloseOperation = WindowConstants.EXIT_ON_CLOSE)
		self.win.size = (700, 700)
		self.win.setLocationRelativeTo(None)
		# GroupLayout is used to decide the positions of JButtons and JComboBoxes.
		self.layout = GroupLayout(self.win.contentPane)
		self.win.contentPane.layout = self.layout
		self.layout.setAutoCreateGaps(True)
		self.layout.setAutoCreateContainerGaps(True)
		
		self.nameField = JComboBox()
		self.nameField.name = 'Name'												# Important attribute. Used in suggestSearch.
		self.nameField.getEditor().getEditorComponent().name = 'NameTextEditor'		# Important attribute. Used in getFocussedField.
		self.nameField.preferredSize = (200, 20)
		self.nameField.editable = True
		self.nameField.getEditor().getEditorComponent().keyReleased = self.fieldKeyReleased
		
		self.subjectField = JComboBox()
		self.subjectField.name = 'Subject'												# Important attribute. Used in suggestSearch.
		self.subjectField.getEditor().getEditorComponent().name = 'SubjectTextEditor'	# Important attribute. Used in getFocussedField.
		self.subjectField.preferredSize = (200, 20)
		self.subjectField.editable = True
		self.subjectField.getEditor().getEditorComponent().keyReleased = self.fieldKeyReleased
		
		self.authorField = JComboBox()
		self.authorField.name = 'Author'												# Important attribute. Used in suggestSearch.
		self.authorField.getEditor().getEditorComponent().name = 'AuthorTextEditor'		# Important attribute. Used in getFocussedField.
		self.authorField.preferredSize = (200, 20)
		self.authorField.editable = True
		self.authorField.getEditor().getEditorComponent().keyReleased = self.fieldKeyReleased
		
		self.classField = JComboBox()
		self.classField.name = 'Class'												# Important attribute. Used in suggestSearch.
		self.classField.getEditor().getEditorComponent().name = 'ClassTextEditor'	# Important attribute. Used in getFocussedField.
		self.classField.preferredSize = (200, 20)
		self.classField.editable = True
		self.classField.getEditor().getEditorComponent().keyReleased = self.fieldKeyReleased
		
		self.descriptionField = JTextArea()
		self.descriptionField.name = 'Description'
		self.descriptionField.preferredSize = (200, 60)
		self.descriptionField.editable = True
		
		self.searchButton = JButton('Search')
		self.searchButton.preferredSize = (100, 20)
		self.searchButton.actionPerformed = self.buttonPressed
		self.searchButton.keyReleased = self.fieldKeyReleased
		self.searchButton.name = 'Search'				# Very important attribute.
		self.cancelButton = JButton('Cancel')
		self.cancelButton.preferredSize = (100, 20)
		self.cancelButton.actionPerformed = self.buttonPressed
		self.cancelButton.keyReleased = self.fieldKeyReleased
		self.cancelButton.name = 'Cancel'				# Very important attribute.
		self.advancedButton = JButton('Advanced')
		self.advancedButton.preferredSize = (100, 20)
		self.advancedButton.actionPerformed = self.buttonPressed
		self.advancedButton.keyReleased = self.fieldKeyReleased
		self.advancedButton.name = 'Advanced'				# Very important attribute.
		
		self.nameLabel = JLabel('Name')
		self.subjectLabel = JLabel('Subject')
		self.authorLabel = JLabel('Author')
		self.classLabel = JLabel('Class')
		self.descriptionLabel = JLabel('Description')
		
		self.layout.setHorizontalGroup(self.layout.createSequentialGroup()
		        .addGroup(self.layout.createParallelGroup(Alignment.LEADING)
					.addComponent(self.nameLabel)
					.addComponent(self.subjectLabel)
					.addComponent(self.authorLabel)
					.addComponent(self.classLabel)
					.addComponent(self.descriptionLabel))
		        .addGroup(self.layout.createParallelGroup(Alignment.TRAILING)
			        .addComponent(self.nameField)
					.addComponent(self.subjectField)
					.addComponent(self.authorField)
					.addComponent(self.classField)
					.addComponent(self.descriptionField)
					.addComponent(self.cancelButton))
		       	.addGroup(self.layout.createParallelGroup(Alignment.LEADING)
					.addComponent(self.advancedButton)
					.addComponent(self.searchButton))
		)
		self.layout.setVerticalGroup(self.layout.createSequentialGroup()
			.addGroup(self.layout.createParallelGroup(Alignment.BASELINE)
		                .addComponent(self.nameLabel)
		                .addComponent(self.nameField))
			.addGroup(self.layout.createParallelGroup(Alignment.BASELINE)
		                .addComponent(self.subjectLabel)
		                .addComponent(self.subjectField))
			.addGroup(self.layout.createParallelGroup(Alignment.BASELINE)
		                .addComponent(self.authorLabel)
		                .addComponent(self.authorField)
						.addComponent(self.advancedButton))
			.addGroup(self.layout.createParallelGroup(Alignment.BASELINE)
		                .addComponent(self.classLabel)
		                .addComponent(self.classField))
			.addGroup(self.layout.createParallelGroup(Alignment.BASELINE)
		                .addComponent(self.descriptionLabel)
		                .addComponent(self.descriptionField))
			.addGroup(self.layout.createParallelGroup(Alignment.BASELINE)
			        .addComponent(self.cancelButton)
		        	.addComponent(self.searchButton))
		)
		
		self.win.pack()
		self.win.show()
if __name__ == '__main__':
	Search()
