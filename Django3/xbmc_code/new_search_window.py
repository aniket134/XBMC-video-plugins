#!./modules/jython2.5.1/jython
import os, sys

import constants_plugin as CP
import LIRCControl, SearchLogic

from org.lirc.util import IRActionListener, SimpleLIRCClient
from com.swabunga.spell.engine import SpellDictionaryHashMap
from com.swabunga.spell.event import SpellChecker
from info.clearthought.layout import TableLayout

from java.io import File
import java.io.IOException

from java.lang import System	        
from java.net import URL	        
from javax.swing import *	        
from javax.swing.plaf.synth import *	        
from java.awt import GridLayout
from javax.swing.GroupLayout import Alignment	        
from java.awt import KeyboardFocusManager
from java.awt.event import KeyEvent

class Search():
	def fieldKeyReleased(self, event):
		"""
		This function implements suggest feature for keyboard only.
		"""
		eventSourceName = event.source.name
		self.focussedField = self.getFocussedField()
		if self.focussedField != None:
			# A textfield has focus.
			text = self.focussedField.getEditor().getEditorComponent().text
			visible = True
			oldText = self.getOldFieldText(eventSourceName)
			if text != '' and (oldText == None or (oldText != text and \
					event.getKeyCode() != KeyEvent.VK_UP and event.getKeyCode() != KeyEvent.VK_DOWN)):
				self.setOldFieldText(text, eventSourceName)
				visible = self.addSuggestedList(text, self.focussedField)
			elif event.getKeyCode() == KeyEvent.VK_ESCAPE or event.getKeyCode() == KeyEvent.VK_SHIFT:
				visible = False
			self.focussedField.setPopupVisible(visible)
		elif eventSourceName != None and (eventSourceName == 'Search' or \
				eventSourceName == 'Cancel' or eventSourceName == 'Clear') and event.getKeyCode() == KeyEvent.VK_ENTER:
			# When a button has focus.
			self.buttonPressedAction(eventSourceName)
		elif event.getKeyCode() == KeyEvent.VK_ENTER:
			self.buttonPressedAction('Search')
		else:
			self.buttonPressedAction('Null')		# This case may come
	
	def addSuggestedList(self, text, focussedField):
		"""
		This functions gets suggestions to be added for remote and keyboard both.
		"""
		focussedField.removeAllItems()
		items = []
		# Get suggestions from Database.
		if len(text) >= 1:
			items += SearchLogic.suggestSearch(text, focussedField.name)
		else:
			return False
		# Get suggestions from Jazzy.
		lastWord = text.split()[-1]
		if len(lastWord) >= 3:
			phonetic_items = self.getSuggestions(lastWord)
			for p in phonetic_items:
				q = str(p)
				if q not in items and len(q) >= len(lastWord):
					items.append(q)
		# Add suggestions to Drop Down list.
		focussedField.addItem(text)
		for item in items:
			if item != text:
				focussedField.addItem(item)
		focussedField.setPopupVisible(False)
		focussedField.setMaximumRowCount(8)
		focussedField.setPopupVisible(True)
		if len(items) == 0:
			return False
		else:
			return True

	def buttonPressed(self, event):
		"""
		This function takes event from Keyboard and passes required
		data to buttonPressedAction function.
		"""
		self.buttonPressedAction(event.source.name)
	
	def buttonPressedAction(self, buttonName):
		"""
		This function performs functionality for button press,
		for both Keyboard and Remote. For Keyboard it is accessed through
		buttonPressed function and for Remote it is directly accessed.
		It is needed as Remote does not generate an event.
		"""
		if buttonName == 'Search':
			texts = []
			mode = self.tabbedPane.getSelectedIndex()
			if mode == 0:
				texts = [self.defaultField.getEditor().getEditorComponent().text]
			elif mode == 1:
				texts = [self.nameField_1.getEditor().getEditorComponent().text, \
						self.subjectField_1.getEditor().getEditorComponent().text, \
						self.authorField_1.getEditor().getEditorComponent().text, \
						self.classField_1.getEditor().getEditorComponent().text]
			elif mode == 2:
				texts = [self.nameField_2.getEditor().getEditorComponent().text, \
						self.subjectField_2.getEditor().getEditorComponent().text, \
						self.authorField_2.getEditor().getEditorComponent().text, \
						self.classField_2.getEditor().getEditorComponent().text, \
						self.descriptionField.text, \
						self.contentTypeField.text, self.videoResField.text, \
						self.otherMediaTextField.text, self.otherLangField.text, \
						self.subject_list, self.media_list, self.lang_list]
			text = SearchLogic.getValidText(texts)
			print(text, mode)
			self.exit()
			# Can't call SearchLogic.finalSearch in this file. This is Jython that is Python. 
			# It uses MySQLdb which does not work with Jython.
		elif buttonName == 'Cancel':
			print('Cancel', -1)
			self.exit()
		else:
			pass									# This case may come

	def checkboxClicked(self, event):
		"""
		This function takes event from Keyboard and passes required
		data to checkboxClickedAction function.
		"""
		sourceName = event.source.name
		acmd = event.getActionCommand()
		self.checkboxClickedAction(sourceName, acmd)

	def checkboxClickedAction(self, sourceName, acmd):
		"""
		This function performs functionality for checkbox click,
		for both Keyboard and Remote. For Keyboard it is accessed through
		checkboxClicked function and for Remote it is directly accessed.
		It is needed as Remote does not generate an event.
		"""
		if sourceName == 'Subject':
			if acmd in self.subject_list:
				self.subject_list.remove(acmd)
			else:
				self.subject_list.append(acmd)
		elif sourceName == 'Media':
			if acmd in self.media_list:
				self.media_list.remove(acmd)
			else:
				self.media_list.append(acmd)
		elif sourceName == 'Language':
			if acmd in self.lang_list:
				self.lang_list.remove(acmd)
			else:
				self.lang_list.append(acmd)
		else:
			pass								# This case may come, if more checkbox fields are added.
	
	def setOldFieldText(self, text, name):
		"""
		What it uses should be matched with getOldFieldText and getFocussedField.
		Used only for KeyBoard events, so we can use 'event' object's functions.
		We have used 'event' object's function to get the parameter 'name'.
		Remote handles differently. No need of such fields for remote.
		"""
		if name == 'DefaultTextEditor':
			self.oldNameFieldText = text
		elif name == 'NameTextEditor_1' or name == 'NameTextEditor_2':
			self.oldNameFieldText = text
		elif name == 'SubjectTextEditor_1' or name == 'SubjectTextEditor_2':
			self.oldSubjectFieldText = text
		elif name == 'AuthorTextEditor_1' or name == 'AuthorTextEditor_2':
			self.oldAuthorFieldText = text
		elif name == 'ClassTextEditor_1' or name == 'ClassTextEditor_2':
			self.oldClassFieldText = text
		else:
			self.oldNameFieldText = text								# This case may come

	def getOldFieldText(self, name):
		"""
		What it returns should be matched with getFocussedField and setOldFieldText.
		Used only for KeyBoard events, so we can use 'event' object's functions.
		We have used 'event' object's function to get the parameter 'name'.
		Remote handles differently. No need of such fields for remote.
		"""
		pane = self.tabbedPane.getSelectedIndex()
		if self.oldPane != pane:
			# If the pane was changed then return None.
			# Otherwise a little discrepancy comes.
			return None

		if name == 'DefaultTextEditor':
			return self.oldNameFieldText
		elif name == 'NameTextEditor_1' or name == 'NameTextEditor_2':
			return self.oldNameFieldText
		elif name == 'SubjectTextEditor_1' or name == 'SubjectTextEditor_2':
			return self.oldSubjectFieldText
		elif name == 'AuthorTextEditor_1' or name == 'AuthorTextEditor_2':
			return self.oldAuthorFieldText
		elif name == 'ClassTextEditor_1' or name == 'ClassTextEditor_2':
			return self.oldClassFieldText
		else:
			return None								# This case may come

	def getFocussedField(self):
		"""
		It should return those fields that are to have suggest feature.
		It should return only those fields that are also present in
		getOldFieldText and setOldFieldText functions.
		Used in fieldKeyReleased and in LIRCControl.
		Cannot use self.frame.getFocusOwner function here, it returns weird
		things for JComboBox.
		It should return JComboBox, JTextField or JTextArea only.
		Used by Remote too, so can't use event.source.name, 
		as Remote does not pass any event.
		"""
		if self.defaultField.getEditor().getEditorComponent().hasFocus():
			return self.defaultField
		elif self.nameField_1.getEditor().getEditorComponent().hasFocus():
			return self.nameField_1
		elif self.subjectField_1.getEditor().getEditorComponent().hasFocus():
			return self.subjectField_1
		elif self.authorField_1.getEditor().getEditorComponent().hasFocus():
			return self.authorField_1
		elif self.classField_1.getEditor().getEditorComponent().hasFocus():
			return self.classField_1
		elif self.nameField_2.getEditor().getEditorComponent().hasFocus():
			return self.nameField_2
		elif self.subjectField_2.getEditor().getEditorComponent().hasFocus():
			return self.subjectField_2
		elif self.authorField_2.getEditor().getEditorComponent().hasFocus():
			return self.authorField_2
		elif self.classField_2.getEditor().getEditorComponent().hasFocus():
			return self.classField_2
		elif self.descriptionField.hasFocus():
			return self.descriptionField
		elif self.contentTypeField.hasFocus():
			return self.contentTypeField
		elif self.videoResField.hasFocus():
			return self.videoResField
		else:
			return None

	def getFocussedButtonName(self):
		"""
		Used by Remote only, as we can't use event.source.name, 
		we have to use this.
		"""
		if self.searchButton.hasFocus() == True:
			return self.searchButton.name
		elif self.cancelButton.hasFocus() == True:
			return self.cancelButton.name
		elif self.clearButton.hasFocus() == True:
			return self.clearButton.name
		elif self.searchButton_1.hasFocus() == True:
			return self.searchButton_1.name
		elif self.cancelButton_1.hasFocus() == True:
			return self.cancelButton_1.name
		elif self.clearButton_1.hasFocus() == True:
			return self.clearButton_1.name
		elif self.searchButton_2.hasFocus() == True:
			return self.searchButton_2.name
		elif self.cancelButton_2.hasFocus() == True:
			return self.cancelButton_2.name
		elif self.clearButton_2.hasFocus() == True:
			return self.clearButton_2.name
		else:
			return None								# This case may come, if more buttons are added.

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
		self.threshold = 3	# Doesn't do anything, but its needed

		# Useful field to check whether the keyStroke changed the text in field or not.
		# Which is then used to invoke Auto-Suggest feature.
		self.oldNameFieldText = None
		self.oldSubjectFieldText = None
		self.oldAuthorFieldText = None
		self.oldClassFieldText = None

		self.subject_list = []					# These lists are used to keep track of what checkboxes were checked.
		self.media_list = []					# It is used in Advanced Search.
		self.lang_list = []						# There are 3 lists as there are three fields with multiple checkboxes.

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
		# b - border
		# f - FILL
		# p - PREFERRED
		# vs - vertical space between labels and text fields
		# vg - vertical gap between form elements
		# hg - horizontal gap between form elements
		
		self.b = 10;
		self.f = TableLayout.FILL;
		self.p = TableLayout.PREFERRED;
		self.vs = 4;
		self.vg = 8;
		self.hg = 8;

		self.frame = JFrame('Search Videos...', defaultCloseOperation = WindowConstants.EXIT_ON_CLOSE)
		self.frame.size = (700, 700)
		self.frame.setLocationRelativeTo(None)
		self.tabbedPane = JTabbedPane()
		self.tabbedPane.addTab('Default', self.firstSearch())
		self.tabbedPane.addTab('Extra Fields', self.secondSearch())
		self.tabbedPane.addTab('Advanced', self.thirdSearch())
		self.frame.add(self.tabbedPane)
		self.frame.pack()
		self.frame.show()
		self.oldPane = self.tabbedPane.getSelectedIndex()

	def firstSearch(self):
		self.win_1 = JPanel(False)
		size = [[self.b, self.f, self.hg, self.b],
				[self.b, self.p, self.vs, self.p, self.vg, self.p, self.b]]
		self.layout_1 = TableLayout(size)
		self.win_1.setLayout(self.layout_1)
		
		self.defaultField = JComboBox()
		self.defaultField.name = 'Default'													# Important attribute. Used in suggestSearch.
		self.defaultField.getEditor().getEditorComponent().name = 'DefaultTextEditor'
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
		self.clearButton = JButton('Clear')
		self.clearButton.preferredSize = (100, 20)
		self.clearButton.actionPerformed = self.buttonPressed
		self.clearButton.keyReleased = self.fieldKeyReleased
		self.clearButton.name = 'Clear'				# Very important attribute.
		self.panelButton = JPanel()
		self.panelButton.add(self.searchButton)
		self.panelButton.add(self.clearButton)
		self.panelButton.add(self.cancelButton)
		
		self.defaultLabel = JLabel('Search')

		self.win_1.add(self.defaultLabel, '1, 1')
		self.win_1.add(self.defaultField, '1, 3')
		self.win_1.add(self.panelButton, '1, 5')
		return self.win_1

	def secondSearch(self):
		self.win_2 = JPanel(False)
		size = [[self.b, self.f, self.hg, self.b],
				[self.b, self.p, self.vs, self.p, self.vg, self.p, self.vg,
					self.p, self.vg, self.p, self.vg, self.p, self.vg,
					self.p, self.vg, self.p, self.vg, self.p, self.b]]
		self.layout_2 = TableLayout(size)
		self.win_2.setLayout(self.layout_2)
		
		self.nameField_1 = JComboBox()
		self.nameField_1.name = 'Name'												# Important attribute. Used in suggestSearch.
		self.nameField_1.getEditor().getEditorComponent().name = 'NameTextEditor_1'
		self.nameField_1.preferredSize = (200, 20)
		self.nameField_1.editable = True
		self.nameField_1.getEditor().getEditorComponent().keyReleased = self.fieldKeyReleased
		
		self.subjectField_1 = JComboBox()
		self.subjectField_1.name = 'Subject'												# Important attribute. Used in suggestSearch.
		self.subjectField_1.getEditor().getEditorComponent().name = 'SubjectTextEditor_1'
		self.subjectField_1.preferredSize = (200, 20)
		self.subjectField_1.editable = True
		self.subjectField_1.getEditor().getEditorComponent().keyReleased = self.fieldKeyReleased
		
		self.authorField_1 = JComboBox()
		self.authorField_1.name = 'Author'												# Important attribute. Used in suggestSearch.
		self.authorField_1.getEditor().getEditorComponent().name = 'AuthorTextEditor_1'
		self.authorField_1.preferredSize = (200, 20)
		self.authorField_1.editable = True
		self.authorField_1.getEditor().getEditorComponent().keyReleased = self.fieldKeyReleased
		
		self.classField_1 = JComboBox()
		self.classField_1.name = 'Class'												# Important attribute. Used in suggestSearch.
		self.classField_1.getEditor().getEditorComponent().name = 'ClassTextEditor_1'
		self.classField_1.preferredSize = (200, 20)
		self.classField_1.editable = True
		self.classField_1.getEditor().getEditorComponent().keyReleased = self.fieldKeyReleased
		
		self.searchButton_1 = JButton('Search')
		self.searchButton_1.preferredSize = (100, 20)
		self.searchButton_1.actionPerformed = self.buttonPressed
		self.searchButton_1.keyReleased = self.fieldKeyReleased
		self.searchButton_1.name = 'Search'				# Very important attribute.
		self.cancelButton_1 = JButton('Cancel')
		self.cancelButton_1.preferredSize = (100, 20)
		self.cancelButton_1.actionPerformed = self.buttonPressed
		self.cancelButton_1.keyReleased = self.fieldKeyReleased
		self.cancelButton_1.name = 'Cancel'				# Very important attribute.
		self.clearButton_1 = JButton('Clear')
		self.clearButton_1.preferredSize = (100, 20)
		self.clearButton_1.actionPerformed = self.buttonPressed
		self.clearButton_1.keyReleased = self.fieldKeyReleased
		self.clearButton_1.name = 'Clear'				# Very important attribute.
		self.panelButton = JPanel()
		self.panelButton.add(self.searchButton_1)
		self.panelButton.add(self.clearButton_1)
		self.panelButton.add(self.cancelButton_1)
		
		self.nameLabel = JLabel('Name')
		self.subjectLabel = JLabel('Subject')
		self.authorLabel = JLabel('Author')
		self.classLabel = JLabel('Class')
		
		self.win_2.add(self.nameLabel, '1, 1')
		self.win_2.add(self.nameField_1, '1, 3')
		self.win_2.add(self.subjectLabel, '1, 5')
		self.win_2.add(self.subjectField_1, '1, 7')
		self.win_2.add(self.authorLabel, '1, 9')
		self.win_2.add(self.authorField_1, '1, 11')
		self.win_2.add(self.classLabel, '1, 13')
		self.win_2.add(self.classField_1, '1, 15')
		self.win_2.add(self.panelButton, '1, 17')
		return self.win_2

	def thirdSearch(self):
		# A variable to differentiate which search box is currently open.
		# Used in buttonPressedAction.
		self.win_3 = JPanel()
		self.nameField_2 = JComboBox()

		self.nameField_2.name = 'Name'												# Important attribute. Used in suggestSearch.
		self.nameField_2.getEditor().getEditorComponent().name = 'NameTextEditor_2'
		self.nameField_2.preferredSize = (200, 20)
		self.nameField_2.editable = True
		self.nameField_2.getEditor().getEditorComponent().keyReleased = self.fieldKeyReleased
		
		self.subjectField_2 = JComboBox()
		self.subjectField_2.name = 'Subject'												# Important attribute. Used in suggestSearch.
		self.subjectField_2.getEditor().getEditorComponent().name = 'SubjectTextEditor_2'
		self.subjectField_2.preferredSize = (200, 20)
		self.subjectField_2.editable = True
		self.subjectField_2.getEditor().getEditorComponent().keyReleased = self.fieldKeyReleased
		
		self.authorField_2 = JComboBox()
		self.authorField_2.name = 'Author'												# Important attribute. Used in suggestSearch.
		self.authorField_2.getEditor().getEditorComponent().name = 'AuthorTextEditor_2'
		self.authorField_2.preferredSize = (200, 20)
		self.authorField_2.editable = True
		self.authorField_2.getEditor().getEditorComponent().keyReleased = self.fieldKeyReleased
		
		self.classField_2 = JComboBox()
		self.classField_2.name = 'Class'												# Important attribute. Used in suggestSearch.
		self.classField_2.getEditor().getEditorComponent().name = 'ClassTextEditor_2'
		self.classField_2.preferredSize = (200, 20)
		self.classField_2.editable = True
		self.classField_2.getEditor().getEditorComponent().keyReleased = self.fieldKeyReleased
		
		self.contentTypeField = JTextField()
		self.contentTypeField.name = 'ContentType'
		self.contentTypeField.preferredSize = (200, 20)
		
		self.videoResField = JTextField()
		self.videoResField.name = 'VideoRes'
		self.videoResField.preferredSize = (200, 20)
		
		self.descriptionField = JTextArea()
		self.descriptionField.name = 'Description'
		self.descriptionField.preferredSize = (200, 60)
		self.descriptionField.editable = True
		
		p1 = JPanel()
		p1.add(JCheckBox(CP.SUBJECT_CHOICES[0][1], actionPerformed=self.checkboxClicked, name='Subject'))
		p1.add(JCheckBox(CP.SUBJECT_CHOICES[1][1], actionPerformed=self.checkboxClicked, name='Subject'))
		p1.add(JCheckBox(CP.SUBJECT_CHOICES[2][1], actionPerformed=self.checkboxClicked, name='Subject'))
		p1.add(JCheckBox(CP.SUBJECT_CHOICES[12][1], actionPerformed=self.checkboxClicked, name='Subject'))
		p1.add(JCheckBox(CP.SUBJECT_CHOICES[13][1], actionPerformed=self.checkboxClicked, name='Subject'))
		p2 = JPanel()
		p2.add(JCheckBox(CP.SUBJECT_CHOICES[3][1], actionPerformed=self.checkboxClicked, name='Subject'))
		p2.add(JCheckBox(CP.SUBJECT_CHOICES[4][1], actionPerformed=self.checkboxClicked, name='Subject'))
		p2.add(JCheckBox(CP.SUBJECT_CHOICES[5][1], actionPerformed=self.checkboxClicked, name='Subject'))
		p2.add(JCheckBox(CP.SUBJECT_CHOICES[6][1], actionPerformed=self.checkboxClicked, name='Subject'))
		p2.add(JCheckBox(CP.SUBJECT_CHOICES[7][1], actionPerformed=self.checkboxClicked, name='Subject'))
		p3 = JPanel()
		p3.add(JCheckBox(CP.SUBJECT_CHOICES[8][1], actionPerformed=self.checkboxClicked, name='Subject'))
		p3.add(JCheckBox(CP.SUBJECT_CHOICES[9][1], actionPerformed=self.checkboxClicked, name='Subject'))
		p3.add(JCheckBox(CP.SUBJECT_CHOICES[10][1], actionPerformed=self.checkboxClicked, name='Subject'))
		p3.add(JCheckBox(CP.SUBJECT_CHOICES[11][1], actionPerformed=self.checkboxClicked, name='Subject'))
		p4 = JPanel()
		p4.add(JCheckBox(CP.SUBJECT_CHOICES[14][1], actionPerformed=self.checkboxClicked, name='Subject'))
		p4.add(JCheckBox(CP.SUBJECT_CHOICES[15][1], actionPerformed=self.checkboxClicked, name='Subject'))
		p4.add(JCheckBox(CP.SUBJECT_CHOICES[16][1], actionPerformed=self.checkboxClicked, name='Subject'))
		p4.add(JCheckBox(CP.SUBJECT_CHOICES[17][1], actionPerformed=self.checkboxClicked, name='Subject'))
		p4.add(JCheckBox(CP.SUBJECT_CHOICES[18][1], actionPerformed=self.checkboxClicked, name='Subject'))
		p4.add(JCheckBox(CP.SUBJECT_CHOICES[35][1], actionPerformed=self.checkboxClicked, name='Subject'))
		p6 = JPanel()
		p6.add(JCheckBox(CP.SUBJECT_CHOICES[19][1], actionPerformed=self.checkboxClicked, name='Subject'))
		p6.add(JCheckBox(CP.SUBJECT_CHOICES[20][1], actionPerformed=self.checkboxClicked, name='Subject'))
		p6.add(JCheckBox(CP.SUBJECT_CHOICES[36][1], actionPerformed=self.checkboxClicked, name='Subject'))
		p6.add(JCheckBox(CP.SUBJECT_CHOICES[37][1], actionPerformed=self.checkboxClicked, name='Subject'))
		p6.add(JCheckBox(CP.SUBJECT_CHOICES[30][1], actionPerformed=self.checkboxClicked, name='Subject'))
		p6.add(JCheckBox(CP.SUBJECT_CHOICES[39][1], actionPerformed=self.checkboxClicked, name='Subject'))
		p7 = JPanel()
		p7.add(JCheckBox(CP.SUBJECT_CHOICES[21][1], actionPerformed=self.checkboxClicked, name='Subject'))
		p7.add(JCheckBox(CP.SUBJECT_CHOICES[22][1], actionPerformed=self.checkboxClicked, name='Subject'))
		p7.add(JCheckBox(CP.SUBJECT_CHOICES[23][1], actionPerformed=self.checkboxClicked, name='Subject'))
		p7.add(JCheckBox(CP.SUBJECT_CHOICES[40][1], actionPerformed=self.checkboxClicked, name='Subject'))
		p7.add(JCheckBox(CP.SUBJECT_CHOICES[38][1], actionPerformed=self.checkboxClicked, name='Subject'))
		p8 = JPanel()
		p8.add(JCheckBox(CP.SUBJECT_CHOICES[24][1], actionPerformed=self.checkboxClicked, name='Subject'))
		p8.add(JCheckBox(CP.SUBJECT_CHOICES[25][1], actionPerformed=self.checkboxClicked, name='Subject'))
		p8.add(JCheckBox(CP.SUBJECT_CHOICES[26][1], actionPerformed=self.checkboxClicked, name='Subject'))
		p8.add(JCheckBox(CP.SUBJECT_CHOICES[27][1], actionPerformed=self.checkboxClicked, name='Subject'))
		p8.add(JCheckBox(CP.SUBJECT_CHOICES[28][1], actionPerformed=self.checkboxClicked, name='Subject'))
		p8.add(JCheckBox(CP.SUBJECT_CHOICES[29][1], actionPerformed=self.checkboxClicked, name='Subject'))
		p9 = JPanel()
		p9.add(JCheckBox(CP.SUBJECT_CHOICES[31][1], actionPerformed=self.checkboxClicked, name='Subject'))
		p9.add(JCheckBox(CP.SUBJECT_CHOICES[32][1], actionPerformed=self.checkboxClicked, name='Subject'))
		p9.add(JCheckBox(CP.SUBJECT_CHOICES[33][1], actionPerformed=self.checkboxClicked, name='Subject'))
		p9.add(JCheckBox(CP.SUBJECT_CHOICES[34][1], actionPerformed=self.checkboxClicked, name='Subject'))
		p10 = JPanel()
		p10.add(JLabel('Other', name='Subject'))
		p10.add(self.subjectField_2)
		self.subjectCheckboxes = [
				p1, p2, p3, p4, p6, p7, p8, p9, p10
				]

		m1 = JPanel()
		m1.add(JCheckBox(CP.MEDIA_TYPE[0][1], actionPerformed=self.checkboxClicked, name='Media'))
		m1.add(JCheckBox(CP.MEDIA_TYPE[1][1], actionPerformed=self.checkboxClicked, name='Media'))
		m1.add(JCheckBox(CP.MEDIA_TYPE[2][1], actionPerformed=self.checkboxClicked, name='Media'))
		m1.add(JCheckBox(CP.MEDIA_TYPE[3][1], actionPerformed=self.checkboxClicked, name='Media'))
		m1.add(JCheckBox(CP.MEDIA_TYPE[4][1], actionPerformed=self.checkboxClicked, name='Media'))
		m1.add(JCheckBox(CP.MEDIA_TYPE[5][1], actionPerformed=self.checkboxClicked, name='Media'))
		m2 = JPanel()
		m2.add(JCheckBox(CP.MEDIA_TYPE[6][1], actionPerformed=self.checkboxClicked, name='Media'))
		m2.add(JCheckBox(CP.MEDIA_TYPE[7][1], actionPerformed=self.checkboxClicked, name='Media'))
		m2.add(JCheckBox(CP.MEDIA_TYPE[8][1], actionPerformed=self.checkboxClicked, name='Media'))
		m2.add(JCheckBox(CP.MEDIA_TYPE[9][1], actionPerformed=self.checkboxClicked, name='Media'))
		m2.add(JCheckBox(CP.MEDIA_TYPE[10][1], actionPerformed=self.checkboxClicked, name='Media'))
		m3 = JPanel()
		m3.add(JCheckBox(CP.MEDIA_TYPE[11][1], actionPerformed=self.checkboxClicked, name='Media'))
		m3.add(JCheckBox(CP.MEDIA_TYPE[12][1], actionPerformed=self.checkboxClicked, name='Media'))
		m3.add(JCheckBox(CP.MEDIA_TYPE[13][1], actionPerformed=self.checkboxClicked, name='Media'))
		m3.add(JCheckBox(CP.MEDIA_TYPE[14][1], actionPerformed=self.checkboxClicked, name='Media'))
		m3.add(JCheckBox(CP.MEDIA_TYPE[15][1], actionPerformed=self.checkboxClicked, name='Media'))
		m4 = JPanel()
		m4.add(JCheckBox(CP.MEDIA_TYPE[16][1], actionPerformed=self.checkboxClicked, name='Media'))
		m4.add(JCheckBox(CP.MEDIA_TYPE[17][1], actionPerformed=self.checkboxClicked, name='Media'))
		m4.add(JCheckBox(CP.MEDIA_TYPE[18][1], actionPerformed=self.checkboxClicked, name='Media'))
		m4.add(JCheckBox(CP.MEDIA_TYPE[19][1], actionPerformed=self.checkboxClicked, name='Media'))
		m4.add(JCheckBox(CP.MEDIA_TYPE[20][1], actionPerformed=self.checkboxClicked, name='Media'))
		m5 = JPanel()
		m5.add(JLabel('Other', name='Media'))
		self.otherMediaTextField = JTextField(50, name='Media')
		m5.add(self.otherMediaTextField)
		self.mediaTypeCheckboxes = [
				m1, m2, m3, m4, m5
				]

		l1 = JPanel()
		l1.add(JCheckBox(CP.LANGUAGES[0][1], actionPerformed=self.checkboxClicked, name='Language'))
		l1.add(JCheckBox(CP.LANGUAGES[1][1], actionPerformed=self.checkboxClicked, name='Language'))
		l1.add(JCheckBox(CP.LANGUAGES[2][1], actionPerformed=self.checkboxClicked, name='Language'))
		l1.add(JCheckBox(CP.LANGUAGES[3][1], actionPerformed=self.checkboxClicked, name='Language'))
		l1.add(JCheckBox(CP.LANGUAGES[4][1], actionPerformed=self.checkboxClicked, name='Language'))
		l2 = JPanel()
		l2.add(JCheckBox(CP.LANGUAGES[5][1], actionPerformed=self.checkboxClicked, name='Language'))
		l2.add(JCheckBox(CP.LANGUAGES[6][1], actionPerformed=self.checkboxClicked, name='Language'))
		l2.add(JCheckBox(CP.LANGUAGES[7][1], actionPerformed=self.checkboxClicked, name='Language'))
		l2.add(JCheckBox(CP.LANGUAGES[8][1], actionPerformed=self.checkboxClicked, name='Language'))
		l3 = JPanel()
		l3.add(JLabel('Other', name='Language'))
		self.otherLangField = JTextField(50, name='Language')
		l3.add(self.otherLangField)
		self.languageCheckboxes = [
				l1, l2, l3
				]

		self.searchButton_2 = JButton('Search')
		self.searchButton_2.preferredSize = (100, 20)
		self.searchButton_2.actionPerformed = self.buttonPressed
		self.searchButton_2.keyReleased = self.fieldKeyReleased
		self.searchButton_2.name = 'Search'				# Very important attribute.
		self.cancelButton_2 = JButton('Cancel')
		self.cancelButton_2.preferredSize = (100, 20)
		self.cancelButton_2.actionPerformed = self.buttonPressed
		self.cancelButton_2.keyReleased = self.fieldKeyReleased
		self.cancelButton_2.name = 'Cancel'				# Very important attribute.
		self.clearButton_2 = JButton('Clear')
		self.clearButton_2.preferredSize = (100, 20)
		self.clearButton_2.actionPerformed = self.buttonPressed
		self.clearButton_2.keyReleased = self.fieldKeyReleased
		self.clearButton_2.name = 'Clear'				# Very important attribute.
		self.panelButton = JPanel()
		self.panelButton.add(self.searchButton_2)
		self.panelButton.add(self.clearButton_2)
		self.panelButton.add(self.cancelButton_2)

		self.nameLabel = JLabel('Name')
		self.subjectLabel = JLabel('Subject')
		self.authorLabel = JLabel('Author')
		self.classLabel = JLabel('Class')
		self.descriptionLabel = JLabel('Description')
		self.mediaTypeLabel = JLabel('Media Type')
		self.languageLabel = JLabel('Language')
		self.contentTypeLabel = JLabel('Content Type')
		self.videoResLabel = JLabel('Video Resolution')

		subList = []
		for i in range(len(self.subjectCheckboxes)):
			subList.append(self.p)

		medList = []
		for i in range(len(self.mediaTypeCheckboxes)):
			medList.append(self.p)

		langList = []
		for i in range(len(self.languageCheckboxes)):
			langList.append(self.p)

		size = [[self.b, self.f, self.hg, self.b],
				[self.b, self.p, self.vs, self.p, self.vg,						
					self.p, self.vs] + subList + [self.vg,						
					self.p, self.vs, self.p, self.vg,							# This is the place that is 
					self.p, self.vs, self.p, self.vg,							# hard coded and needs to be 
					self.p, self.vs, self.p, self.vg,							# modified when change is made in
					self.p, self.vs, self.p, self.vg,							# ordering of fields.
					self.p, self.vs] + langList + [self.vg,							
					self.p, self.vs] + medList + [self.vg,							
					self.p, self.vs, self.p, self.vg,							
					self.p, self.vs, self.p, self.vg,							
					self.p, self.vs, self.p, self.vg,							
					self.p, self.vs, self.p, self.vg,							
					self.p, self.vs, self.p, self.vg,							
					self.p, self.vs, self.p, self.vg,							
					self.p, self.vs, self.p, self.b]]
		self.layout_3 = TableLayout(size)
		self.win_3.setLayout(self.layout_3)
		
		self.win_3.add(self.nameLabel, '1, 1')
		self.win_3.add(self.nameField_2, '1, 3')
		self.win_3.add(self.subjectLabel, '1, 5')
		count = 7
		for i in range(len(self.subjectCheckboxes)):
			self.win_3.add(self.subjectCheckboxes[i], '1, ' + str(count))
			count += 1
		count += 1
		self.win_3.add(self.authorLabel, '1, ' + str(count))
		count += 2
		self.win_3.add(self.authorField_2, '1, ' + str(count))
		count += 2
		self.win_3.add(self.classLabel, '1, ' + str(count))
		count += 2
		self.win_3.add(self.classField_2, '1, ' + str(count))
		count += 2
		self.win_3.add(self.descriptionLabel, '1, ' + str(count))
		count += 2
		self.win_3.add(self.descriptionField, '1, ' + str(count))
		count += 2
		self.win_3.add(self.contentTypeLabel, '1, ' + str(count))
		count += 2
		self.win_3.add(self.contentTypeField, '1, ' + str(count))
		count += 2
		self.win_3.add(self.languageLabel, '1, ' + str(count))
		count += 2
		for i in range(len(self.languageCheckboxes)):
			self.win_3.add(self.languageCheckboxes[i], '1, ' + str(count))
			count += 1
		count += 1
		self.win_3.add(self.mediaTypeLabel, '1, ' + str(count))
		count += 2
		for i in range(len(self.mediaTypeCheckboxes)):
			self.win_3.add(self.mediaTypeCheckboxes[i], '1, ' + str(count))
			count += 1
		count += 1
		self.win_3.add(self.videoResLabel, '1, ' + str(count))
		count += 2
		self.win_3.add(self.videoResField, '1, ' + str(count))
		count += 2
		self.win_3.add(self.panelButton, '1, ' + str(count))
		
		self.scrollPane = JScrollPane(self.win_3)
		self.scrollPane.setVerticalScrollBarPolicy(JScrollPane.VERTICAL_SCROLLBAR_ALWAYS)
		return self.scrollPane
		
if __name__ == '__main__':
	Search()
