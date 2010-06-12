#!./modules/jython2.5.1/jython
import constants_plugin as CP

from org.lirc.util import IRActionListener, SimpleLIRCClient

from java.lang import System
from java.net import URL
from javax.swing import *
from javax.swing.plaf.synth import *
from javax.swing.GroupLayout import Alignment

class MoveListener(IRActionListener):
	def action(self, command):
		try:
			if command == 'moveUp':
				nameLabel.text = 'MoveUp'
			elif command == 'exit':
				exit()
			elif command == 'two':
				if nameField.getEditor().getEditorComponent().hasFocus() == True:
					print('hello')
					oldText = nameField.getEditor().getEditorComponent().text
					nameField.removeAllItems()
					nameField.addItem(oldText + '2')
					nameField.addItem('Hello ' + '2')
					nameField.setPopupVisible(True)
				elif subjectField.getEditor().getEditorComponent().hasFocus() == True:
					print('yellow')
		except Exception, e:
			print(str(e))

def fieldKeyPressed(event):
	if event.getSource() == nameField.getEditor().getEditorComponent():
		oldText = nameField.getEditor().getEditorComponent().text
		nameField.removeAllItems()
		nameField.addItem(oldText)
		nameField.addItem('Hello ' + str(event.keyChar))
		nameField.setPopupVisible(True)
	elif event.getSource() == subjectField.getEditor().getEditorComponent():
		oldText = subjectField.getEditor().getEditorComponent().text
		subjectField.removeAllItems()
		subjectField.addItem(oldText)
		subjectField.addItem('Hello ' + str(event.keyChar))
		subjectField.setPopupVisible(True)
	elif event.getSource() == authorField.getEditor().getEditorComponent():
		oldText = authorField.getEditor().getEditorComponent().text
		authorField.removeAllItems()
		authorField.addItem(oldText)
		authorField.addItem('Hello ' + str(event.keyChar))
		authorField.setPopupVisible(True)
	elif event.getSource() == classField.getEditor().getEditorComponent():
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

client = SimpleLIRCClient('xbmc_code/search.lirc')
client.addIRActionListener(MoveListener());

# Uncomment the following 4 lines to enable custom look and feel.
#lookAndFeel = SynthLookAndFeel()
#lookAndFeel.load(URL('file://' + CP.PLUGIN_PATH + '/xbmc_code/laf.xml'))
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
nameField.getEditor().getEditorComponent().keyPressed = fieldKeyPressed

subjectField = JComboBox()
subjectField.preferredSize = (200, 20)
subjectField.editable = True
subjectField.getEditor().getEditorComponent().keyPressed = fieldKeyPressed

authorField = JComboBox()
authorField.preferredSize = (200, 20)
authorField.editable = True
authorField.getEditor().getEditorComponent().keyPressed = fieldKeyPressed

classField = JComboBox()
classField.preferredSize = (200, 20)
classField.editable = True
classField.getEditor().getEditorComponent().keyPressed = fieldKeyPressed

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
        .addGroup(layout.createParallelGroup(Alignment.LEADING)
		.addComponent(nameLabel)
		.addComponent(subjectLabel)
		.addComponent(authorLabel)
		.addComponent(classLabel)
		.addComponent(cancelButton))
        .addGroup(layout.createParallelGroup(Alignment.LEADING)
        	.addComponent(nameField)
		.addComponent(subjectField)
		.addComponent(authorField)
		.addComponent(classField)
		.addComponent(searchButton))
)
layout.setVerticalGroup(layout.createSequentialGroup()
	.addGroup(layout.createParallelGroup(Alignment.BASELINE)
                .addComponent(nameLabel)
                .addComponent(nameField))
	.addGroup(layout.createParallelGroup(Alignment.BASELINE)
                .addComponent(subjectLabel)
                .addComponent(subjectField))
	.addGroup(layout.createParallelGroup(Alignment.BASELINE)
                .addComponent(authorLabel)
                .addComponent(authorField))
	.addGroup(layout.createParallelGroup(Alignment.BASELINE)
                .addComponent(classLabel)
                .addComponent(classField))
	.addGroup(layout.createParallelGroup(Alignment.BASELINE)
	        .addComponent(cancelButton)
        	.addComponent(searchButton))
)

win.pack()
win.show()
