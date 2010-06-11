#!./modules/jython2.5.1/jython
from org.lirc import *
from org.lirc.util import *
from org.lirc.ui import *

from java.lang import *
from javax.swing import *
from javax.swing.plaf.metal import *
from java.awt import *
from java.io import *
class MoveListener(IRActionListener):
	def action(self, command):
		try:
			if command == 'moveUp':
				label.text = 'MoveUp'
			elif command == 'exit':
				exit()
		except Exception, e:
			print(str(e))
def keyPressed(event):
	print(str(event.keyChar))
	label.text = field.text

def buttonPressed(event):
	field.text = quotes[event.source.text]
	print(event.source.text)
	exit()
def exit():
	client.stopListening()
        System.exit(0)
lookAndFeel = UIManager.getCrossPlatformLookAndFeelClassName()
UIManager.setLookAndFeel(lookAndFeel)
MetalLookAndFeel.setCurrentTheme(OceanTheme())
UIManager.setLookAndFeel(MetalLookAndFeel())
JFrame.setDefaultLookAndFeelDecorated(True)

win = JFrame('Search Videos...', defaultCloseOperation = WindowConstants.EXIT_ON_CLOSE)
win.size = (300, 300)
win.contentPane.layout = GridLayout(0, 2)
field = JTextField('Type here', SwingConstants.RIGHT)
field.preferredSize = (200, 20)
field.size = (200, 200)
field.keyPressed = keyPressed
#field.actionPerformed = keyPressed
win.contentPane.add(field)
button = JButton('Search')
button.preferredSize = (100, 20)
quotes = {"Groucho": "Say the secret word", "Chico": "Viaduct?", "Harpo": "HONK!", "Search": "Harry Potter!"}
button.actionPerformed = buttonPressed
win.contentPane.add(button)
label = JLabel('Search', SwingConstants.LEFT)
win.contentPane.add(label)

client = SimpleLIRCClient('xbmc_code/search.lirc')
client.addIRActionListener(MoveListener());

#win.pack()
win.show()
