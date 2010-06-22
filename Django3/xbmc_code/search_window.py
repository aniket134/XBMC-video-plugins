#!./modules/jython2.5.1/jython
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
				self.addSuggestedList(text, self.focussedField)
			elif event.getKeyCode() == KeyEvent.VK_ESCAPE or event.getKeyCode() == KeyEvent.VK_SHIFT:
				visible = False
			self.focussedField.setPopupVisible(visible)
		elif eventSourceName != None and (eventSourceName == 'Search' or \
				eventSourceName == 'Cancel') and event.getKeyCode() == KeyEvent.VK_ENTER:
			self.buttonPressedAction(eventSourceName)
		elif event.getKeyCode() == KeyEvent.VK_ENTER:
			self.buttonPressedAction('Search')
		else:
			self.buttonPressedAction('Null')		# This case may come
	
	def addSuggestedList(self, text, focussedField):
		lastWord = text.split()[-1]
		items = []
		if len(lastWord) > 3:
			items = self.getSuggestions(lastWord)
		if items == None:
			items = []
		items += SearchLogic.suggestSearch(text, focussedField.name)
		for item in items:
			self.focussedField.addItem(item)

	def buttonPressed(self, event):
		self.buttonPressedAction(event.source.name)
	
	def buttonPressedAction(self, buttonName):
		if buttonName == 'Search':
			texts = [self.nameField.getEditor().getEditorComponent().text, \
					self.subjectField.getEditor().getEditorComponent().text, \
					self.authorField.getEditor().getEditorComponent().text, \
					self.classField.getEditor().getEditorComponent().text]
			text = SearchLogic.getValidText(texts)
			print(text)
			self.exit()
		elif buttonName == 'Cancel':
			print('Cancel')
			self.exit()
		else:
			pass									# This case may come
	
	def setOldFieldText(self, text):
		if self.nameField.getEditor().getEditorComponent().hasFocus() == True:
			self.oldNameFieldText = text
		elif self.subjectField.getEditor().getEditorComponent().hasFocus() == True:
			self.oldSubjectFieldText = text
		elif self.authorField.getEditor().getEditorComponent().hasFocus() == True:
			self.oldAuthorFieldText = text
		elif self.classField.getEditor().getEditorComponent().hasFocus() == True:
			self.oldClassFieldText = text
		else:
			pass									# This case never comes

	def getOldFieldText(self):
		if self.nameField.getEditor().getEditorComponent().hasFocus() == True:
			return self.oldNameFieldText
		elif self.subjectField.getEditor().getEditorComponent().hasFocus() == True:
			return self.oldSubjectFieldText
		elif self.authorField.getEditor().getEditorComponent().hasFocus() == True:
			return self.oldAuthorFieldText
		elif self.classField.getEditor().getEditorComponent().hasFocus() == True:
			return self.oldClassFieldText
		else:
			return None								# This case never comes

	def getFocussedButtonName(self):
		if self.searchButton.hasFocus() == True:
			return self.searchButton.name
		elif self.cancelButton.hasFocus() == True:
			return self.cancelButton.name
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
		else:
			return None								# This case may come

	def getSuggestions(self, word):
		return self.spellChecker.getSuggestions(word, self.threshold)

	def exit(self):
		try:
			self.client.stopListening()
		except:
			pass
		os.environ['JYTHON_RUNNING'] = 'NO'
		System.exit(0)

	def __init__(self):
		self.dictionary = SpellDictionaryHashMap(File(os.getcwd() + '/xbmc_code/en-US.dic'))
		self.spellChecker = SpellChecker(self.dictionary)
		self.threshold = 0

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
		
		# The UI part begins now. This JFrame is used to paint everythong.
		self.win = JFrame('Search Videos...', defaultCloseOperation = WindowConstants.EXIT_ON_CLOSE)
		self.win.size = (700, 700)
		# GroupLayout is used to decide the positions of JButtons and JComboBoxes.
		self.layout = GroupLayout(self.win.contentPane)
		self.win.contentPane.layout = self.layout
		self.layout.setAutoCreateGaps(True)
		self.layout.setAutoCreateContainerGaps(True)
		
		self.nameField = JComboBox()
		self.nameField.name = 'Name'
		self.nameField.getEditor().getEditorComponent().name = 'NameTextEditor'
		self.nameField.preferredSize = (200, 20)
		self.nameField.editable = True
		self.nameField.getEditor().getEditorComponent().keyReleased = self.fieldKeyReleased
		
		self.subjectField = JComboBox()
		self.subjectField.name = 'Subject'
		self.subjectField.getEditor().getEditorComponent().name = 'SubjectTextEditor'
		self.subjectField.preferredSize = (200, 20)
		self.subjectField.editable = True
		self.subjectField.getEditor().getEditorComponent().keyReleased = self.fieldKeyReleased
		
		self.authorField = JComboBox()
		self.authorField.name = 'Author'
		self.authorField.getEditor().getEditorComponent().name = 'AuthorTextEditor'
		self.authorField.preferredSize = (200, 20)
		self.authorField.editable = True
		self.authorField.getEditor().getEditorComponent().keyReleased = self.fieldKeyReleased
		
		self.classField = JComboBox()
		self.classField.name = 'Class'					# Important attribute. Used in suggestSearch.
		self.classField.getEditor().getEditorComponent().name = 'ClassTextEditor'	# Important attribute. Used in getFocussedField
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
		
		self.nameLabel = JLabel('Name')
		self.subjectLabel = JLabel('Subject')
		self.authorLabel = JLabel('Author')
		self.classLabel = JLabel('Class')
		
		self.layout.setHorizontalGroup(self.layout.createSequentialGroup()
		        .addGroup(self.layout.createParallelGroup(Alignment.LEADING)
				.addComponent(self.nameLabel)
				.addComponent(self.subjectLabel)
				.addComponent(self.authorLabel)
				.addComponent(self.classLabel)
				.addComponent(self.cancelButton))
		        .addGroup(self.layout.createParallelGroup(Alignment.LEADING)
		        	.addComponent(self.nameField)
				.addComponent(self.subjectField)
				.addComponent(self.authorField)
				.addComponent(self.classField)
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
		                .addComponent(self.authorField))
			.addGroup(self.layout.createParallelGroup(Alignment.BASELINE)
		                .addComponent(self.classLabel)
		                .addComponent(self.classField))
			.addGroup(self.layout.createParallelGroup(Alignment.BASELINE)
			        .addComponent(self.cancelButton)
		        	.addComponent(self.searchButton))
		)
		
		self.win.pack()
		self.win.show()
if __name__ == '__main__':
	Search()
