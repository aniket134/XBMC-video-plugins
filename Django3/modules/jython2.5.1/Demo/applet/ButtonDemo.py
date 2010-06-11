#!/home/sh1n0b1/jython2.5.1/jython
"""A translation of an example from the Java Tutorial
http://java.sun.com/docs/books/tutorial/

This example shows how to use Buttons
"""

from java import awt, applet

class ButtonDemo(applet.Applet):
    def init(self):
	self.b1 = awt.Button('Disable middle button',
			     actionPerformed=self.disable)
	self.b2 = awt.Button('Middle button')
	self.b3 = awt.Button('Enable middle button',
			     enabled=0, actionPerformed=self.enable)

	self.add(self.b1)
	self.add(self.b2)
	self.add(self.b3)

    def enable(self, event):
	self.b1.enabled = self.b2.enabled = 1
	self.b3.enabled = 0

    def disable(self, event):
	self.b1.enabled = self.b2.enabled = 0
	self.b3.enabled = 1


if __name__ == '__main__':	
    import pawt
    print('oooooooooo00000000000000ooooooooooooo')
    pawt.test(ButtonDemo())
