#!./modules/jython2.5.1/jython
import constants_plugin as CP
import LIRCControl, SearchLogic

from org.lirc.util import IRActionListener, SimpleLIRCClient

from java.lang import System	        
from java.net import URL	        
from javax.swing import *	        
from javax.swing.plaf.synth import *	        
from javax.swing.GroupLayout import Alignment	        

class Search():
	def fieldKeyPressed(self, event):
		if event.getSource() == self.nameField.getEditor().getEditorComponent():
			print('kasd')
			oldText = self.nameField.getEditor().getEditorComponent().text
			self.nameField.removeAllItems()
			self.nameField.addItem(oldText)
			self.nameField.addItem('Hello ' + str(event.keyChar))
			self.nameField.setPopupVisible(True)
		elif event.getSource() == self.subjectField.getEditor().getEditorComponent():
			oldText = self.subjectField.getEditor().getEditorComponent().text
			self.subjectField.removeAllItems()
			self.subjectField.addItem(oldText)
			self.subjectField.addItem('Hello ' + str(event.keyChar))
			self.subjectField.setPopupVisible(True)
		elif event.getSource() == self.authorField.getEditor().getEditorComponent():
			oldText = self.authorField.getEditor().getEditorComponent().text
			self.authorField.removeAllItems()
			self.authorField.addItem(oldText)
			self.authorField.addItem('Hello ' + str(event.keyChar))
			self.authorField.setPopupVisible(True)
		elif event.getSource() == self.classField.getEditor().getEditorComponent():
			oldText = self.classField.getEditor().getEditorComponent().text
			self.classField.removeAllItems()
			self.classField.addItem(oldText)
			self.classField.addItem('Hello ' + str(event.keyChar))
			self.classField.setPopupVisible(True)
	
	def buttonPressed(self, event):
		print(event.source.text)
		self.exit()
	
	def exit(self):
		self.client.stopListening()
	        System.exit(0)
	def __init__(self):
		self.client = SimpleLIRCClient('xbmc_code/search.lirc')
		self.client.addIRActionListener(LIRCControl.MoveListener(self));
		
		# Uncomment the following 4 lines to enable custom look and feel.
		#lookAndFeel = SynthLookAndFeel()
		#lookAndFeel.load(URL('file://' + CP.PLUGIN_PATH + '/xbmc_code/laf.xml'))
		#UIManager.setLookAndFeel(lookAndFeel)
		#JFrame.setDefaultLookAndFeelDecorated(True)
		
		self.win = JFrame('Search Videos...', defaultCloseOperation = WindowConstants.EXIT_ON_CLOSE)
		self.win.size = (700, 700)
		self.layout = GroupLayout(self.win.contentPane)
		self.win.contentPane.layout = self.layout
		self.layout.setAutoCreateGaps(True)
		self.layout.setAutoCreateContainerGaps(True)
		
		self.nameField = JComboBox()
		self.nameField.preferredSize = (200, 20)
		self.nameField.editable = True
		self.nameField.getEditor().getEditorComponent().keyPressed = self.fieldKeyPressed
		self.nameField.getEditor().getEditorComponent().actionPerformed = self.fieldKeyPressed
		
		self.subjectField = JComboBox()
		self.subjectField.preferredSize = (200, 20)
		self.subjectField.editable = True
		self.subjectField.getEditor().getEditorComponent().keyPressed = self.fieldKeyPressed
		
		self.authorField = JComboBox()
		self.authorField.preferredSize = (200, 20)
		self.authorField.editable = True
		self.authorField.getEditor().getEditorComponent().keyPressed = self.fieldKeyPressed
		
		self.classField = JComboBox()
		self.classField.preferredSize = (200, 20)
		self.classField.editable = True
		self.classField.getEditor().getEditorComponent().keyPressed = self.fieldKeyPressed
		
		self.searchButton = JButton('Search')
		self.searchButton.preferredSize = (100, 20)
		self.searchButton.actionPerformed = self.buttonPressed
		self.cancelButton = JButton('Cancel')
		self.cancelButton.preferredSize = (100, 20)
		self.cancelButton.actionPerformed = self.buttonPressed
		
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
Search()
