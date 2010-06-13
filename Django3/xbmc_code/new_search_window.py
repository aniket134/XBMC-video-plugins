#!./modules/jython2.5.1/jython
import sys

import constants_plugin as CP
import LIRCControl, SearchLogic

from org.lirc.util import IRActionListener, SimpleLIRCClient

from java.lang import System	        
from java.net import URL	        
from javax.swing import *	        
from javax.swing.plaf.synth import *	        
from javax.swing.GroupLayout import Alignment	        
from java.awt import KeyboardFocusManager
from java.awt.event import KeyEvent

class Search():
	def fieldKeyReleased(self, event):
		self.focussedField = self.getFocussedField()
		self.focussedButtonName = self.getFocussedButtonName()
		if self.focussedField != None:
			text = self.focussedField.getEditor().getEditorComponent().text
			visible = True
			oldText = self.getOldFieldText()
			if oldText == None or (oldText != text and event.getKeyCode() != KeyEvent.VK_UP and event.getKeyCode() != KeyEvent.VK_DOWN):
				self.setOldFieldText(text)
				self.focussedField.removeAllItems()
				items = SearchLogic.suggestSearch(self.stripColons(text))
				for item in items:
					self.focussedField.addItem(item)
			elif event.getKeyCode() == KeyEvent.VK_ESCAPE or event.getKeyCode() == KeyEvent.VK_SHIFT:
				visible = False
			self.focussedField.setPopupVisible(visible)
		elif (event.source.name == 'Search' or event.source.name == 'Cancel') and event.getKeyCode() == KeyEvent.VK_ENTER:
			self.buttonPressedAction(event.source.name)
		elif event.getKeyCode() == KeyEvent.VK_ENTER:
			self.buttonPressedAction('Search')
		else:
			self.buttonPressedAction('Null')		# This case may come
	
	def buttonPressed(self, event):
		self.buttonPressedAction(event.source.name)
	
	def buttonPressedAction(self, name):
		if name == 'Search':
			text = self.getValidText()
			print('Search::' + text)
		elif name == 'Cancel':
			print('Cancel::')
		else:
			pass			# This case may come
		self.exit()
	
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
			pass			# This case never comes

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
			return None		# This case never comes

	def getFocussedButtonName(self):
		if self.searchButton.hasFocus() == True:
			return self.searchButton.name
		elif self.cancelButton.hasFocus() == True:
			return self.cancelButton.name
		else:
			return None		# This case may come

	def getFocussedField(self):
		if self.nameField.getEditor().getEditorComponent().hasFocus() == True:
			return self.nameField
		elif self.subjectField.getEditor().getEditorComponent().hasFocus() == True:
			return self.subjectField
		elif self.authorField.getEditor().getEditorComponent().hasFocus() == True:
			return self.authorField
		elif self.classField.getEditor().getEditorComponent().hasFocus() == True:
			return self.classField
		else:
			return None		# This case may come

	def stripColons(self, text):
			return text

	def getValidText(self):
			return 'Hello there...'

	def exit(self):
		self.client.stopListening()
		System.exit(0)

	def __init__(self):
		# Usefull field to check whether the keyStroke changed the text in field or not.
		# Which is then used to invoke Auto-Suggest feature.
		self.oldNameFieldText = None
		self.oldSubjectFieldText = None
		self.oldAuthorFieldText = None
		self.oldClassFieldText = None

		# The following 2 lines handle LIRC remote events.
		self.client = SimpleLIRCClient('xbmc_code/search.lirc')
		self.client.addIRActionListener(LIRCControl.MoveListener(self));
		
		# The following 4 lines enable custom look and feel.
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
		self.nameField.preferredSize = (200, 20)
		self.nameField.editable = True
		self.nameField.getEditor().getEditorComponent().keyReleased = self.fieldKeyReleased
		
		self.subjectField = JComboBox()
		self.subjectField.preferredSize = (200, 20)
		self.subjectField.editable = True
		self.subjectField.getEditor().getEditorComponent().keyReleased = self.fieldKeyReleased
		
		self.authorField = JComboBox()
		self.authorField.preferredSize = (200, 20)
		self.authorField.editable = True
		self.authorField.getEditor().getEditorComponent().keyReleased = self.fieldKeyReleased
		
		self.classField = JComboBox()
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
