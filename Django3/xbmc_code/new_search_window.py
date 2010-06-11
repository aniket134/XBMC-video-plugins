#!./modules/jython2.5.1/jython
import os

from org.lirc import *
from org.lirc.util import *
from org.lirc.ui import *

from java.lang import *
from java.awt import *
from java.io import *
from java.net import URL
from javax.swing import *
from javax.swing.plaf.synth import *
from javax.swing.GroupLayout.Alignment import *

class MoveListener(IRActionListener):
	def action(self, command):
		try:
			if command == 'moveUp':
				label.text = 'MoveUp'
			elif command == 'exit':
				exit()
		except Exception, e:
			print(str(e))

def nameFieldKeyPressed(event):
	oldText = nameField.getEditor().getEditorComponent().text
	nameField.removeAllItems()
	nameField.addItem(oldText)
	nameField.addItem('Hello ' + str(event.keyChar))
	nameField.setPopupVisible(True)

def subjectFieldKeyPressed(event):
	oldText = subjectField.getEditor().getEditorComponent().text
	subjectField.removeAllItems()
	subjectField.addItem(oldText)
	subjectField.addItem('Hello ' + str(event.keyChar))
	subjectField.setPopupVisible(True)

def authorFieldKeyPressed(event):
	oldText = authorField.getEditor().getEditorComponent().text
	authorField.removeAllItems()
	authorField.addItem(oldText)
	authorField.addItem('Hello ' + str(event.keyChar))
	authorField.setPopupVisible(True)

def classFieldKeyPressed(event):
	oldText = classField.getEditor().getEditorComponent().text
	classField.removeAllItems()
	classField.addItem(oldText)
	classField.addItem('Hello ' + str(event.keyChar))
	classField.setPopupVisible(True)

def buttonPressed(event):
	print(event.source.text)
	exit()

def exit():
	client.stopListening()
        System.exit(0)

# Uncomment the following 4 lines to enable custom look and feel.
#lookAndFeel = SynthLookAndFeel()
#lookAndFeel.load(URL('file://' + os.getcwd() + '/xbmc_code/laf.xml'))
#UIManager.setLookAndFeel(lookAndFeel)
#JFrame.setDefaultLookAndFeelDecorated(True)

win = JFrame('Search Videos...', defaultCloseOperation = WindowConstants.EXIT_ON_CLOSE)
win.size = (700, 700)
layout = GroupLayout(win.contentPane)
win.contentPane.layout = layout
layout.setAutoCreateGaps(True)
layout.setAutoCreateContainerGaps(True)

nameField = JComboBox()
nameField.preferredSize = (200, 20)
nameField.editable = True
nameField.getEditor().getEditorComponent().keyPressed = nameFieldKeyPressed

subjectField = JComboBox()
subjectField.preferredSize = (200, 20)
subjectField.editable = True
subjectField.getEditor().getEditorComponent().keyPressed = subjectFieldKeyPressed

authorField = JComboBox()
authorField.preferredSize = (200, 20)
authorField.editable = True
authorField.getEditor().getEditorComponent().keyPressed = authorFieldKeyPressed

classField = JComboBox()
classField.preferredSize = (200, 20)
classField.editable = True
classField.getEditor().getEditorComponent().keyPressed = classFieldKeyPressed

searchButton = JButton('Search')
searchButton.preferredSize = (100, 20)
searchButton.actionPerformed = buttonPressed
cancelButton = JButton('Cancel')
cancelButton.preferredSize = (100, 20)
cancelButton.actionPerformed = buttonPressed

nameLabel = JLabel('Name')
subjectLabel = JLabel('Subject')
authorLabel = JLabel('Author')
classLabel = JLabel('Class')

# Don't know why cancelButton won't show
layout.setHorizontalGroup(layout.createSequentialGroup()
        .addGroup(layout.createParallelGroup(LEADING)
		.addComponent(nameLabel)
		.addComponent(subjectLabel)
		.addComponent(authorLabel)
		.addComponent(classLabel)
		.addComponent(cancelButton))
        .addGroup(layout.createParallelGroup(LEADING)
        	.addComponent(nameField)
		.addComponent(subjectField)
		.addComponent(authorField)
		.addComponent(classField)
		.addComponent(searchButton))
)
layout.setVerticalGroup(layout.createSequentialGroup()
	.addGroup(layout.createParallelGroup(BASELINE)
                .addComponent(nameLabel)
                .addComponent(nameField))
	.addGroup(layout.createParallelGroup(BASELINE)
                .addComponent(subjectLabel)
                .addComponent(subjectField))
	.addGroup(layout.createParallelGroup(BASELINE)
                .addComponent(authorLabel)
                .addComponent(authorField))
	.addGroup(layout.createParallelGroup(BASELINE)
                .addComponent(classLabel)
                .addComponent(classField))
	.addGroup(layout.createParallelGroup(BASELINE)
	        .addComponent(cancelButton)
        	.addComponent(searchButton))
)

client = SimpleLIRCClient('xbmc_code/search.lirc')
client.addIRActionListener(MoveListener());

win.pack()
win.show()
