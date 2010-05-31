import xbmc, xbmcgui, xbmcplugin, sys
import functions as FS
import constants_plugin as CP

#get actioncodes from keymap.xml
ACTION_PREVIOUS_MENU = 10
ACTION_SELECT_ITEM = 7
ACTION_PARENT_DIR = 9
RESOURCE_PATH = CP.PLUGIN_PATH + '/' + CP.PLUGIN_NAME + '/' + 'resources/'

class Search_class(xbmcgui.Window):
	def __init__(self):
		print(str(self.getWidth()))
		print(str(self.getHeight()))
		print(str(xbmc.getLocalizedString(10000)))
		print(str(xbmc.getSkinDir()))
		# Add atleast one dir to make it work correctly
		info_labels = {}
		info_labels['name'] = 'Back to Search'
		FS.ADD_DIR(0, 1, "", info_labels)
		xbmcplugin.endOfDirectory(handle = 0)
		#self.f = open('keymap.xml', 'w+')
		self.addControl(xbmcgui.ControlImage(0, 0, 720, 480, RESOURCE_PATH + 'images/background2.jpg'))
		self.strActionInfo = xbmcgui.ControlLabel(100, 200, 200, 200, '', 'font13', '0xFFFF00FF')
		self.addControl(self.strActionInfo)
		self.strActionInfo.setLabel('Push Esc to quit.')
		
		# Make a List
		self.list = xbmcgui.ControlList(300, 250, 200, 200)
		self.addControl(self.list)
		self.list.addItem('Item 1')
		self.list.addItem('Item 2')
		self.list.addItem('Item 3')
		self.setFocus(self.list)
		

	def onAction(self, action):
		try:
			print('Action called is: ' + str(action.getId()))
			#self.f.write('\n' + str(action.getId()))
			if action.getId() == ACTION_PREVIOUS_MENU:
				self.close()
			#if action.getId() == ACTION_SELECT_ITEM:
				#self.message()
			#if action.getId() == ACTION_PARENT_DIR:
				#self.removeControl(self.str_action)
		except Exception,e:
			print(e)

	def onControl(self, control):
		if control == self.list:
			item = self.list.getSelectedItem()
			self.message('You selected: ' + item.getLabel())
	def message(self, txt):
		dialog = xbmcgui.Dialog()
		dialog.ok('My msg title', txt)
	def file_close(self):
		self.f.close()

def show():
	search_display = Search_class()
	search_display.doModal()
	#search_display.file_close()
	del search_display
