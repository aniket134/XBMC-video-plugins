import xbmc, xbmcgui, xbmcplugin, sys
import functions as FS
import constants_plugin as CP
import db_interaction as DB

#get actioncodes from keymap.xml
ACTION_PREVIOUS_MENU = 10
ACTION_SELECT_ITEM = 7
ACTION_PARENT_DIR = 9

class Search_class(xbmcgui.Window):
	def __init__(self):
		print(str(xbmc.getLocalizedString(10000)))
		print(str(xbmc.getSkinDir()))
		self.width = self.getWidth()
		self.height = self.getHeight()
		self.button_width = 200
		self.button_height = 30
		# Add atleast one dir to make it work correctly
		info_labels = {}
		info_labels['name'] = 'Back to Search'
		FS.ADD_DIR(0, 1, "", info_labels)
		xbmcplugin.endOfDirectory(handle = 0)
		#self.f = open('keymap.xml', 'w+')
		self.addControl(xbmcgui.ControlImage(0, 0, self.width, self.height, CP.RESOURCE_PATH + 'images/background2.jpg'))
		self.strActionInfo = xbmcgui.ControlLabel(100, 200, 200, 200, 'Push Esc to Quit', 'font13', '0xFF000000')
		self.addControl(self.strActionInfo)
		
		# Make a Text Field
		keyboard = xbmc.Keyboard('Enter Search String here')
		keyboard.doModal()
		if keyboard.isConfirmed():
			self.add_search_results(keyboard.getText())
		else:
			pass
		
	def add_search_results(self, text):
		self.buttons = []
		y_button = 40
		links = DB.search(text)
		for link in links:
			button = xbmcgui.ControlButton(10, y_button, self.button_width, self.button_height, link)
			self.addControl(button)
			self.buttons.append(button);
			y_button += self.button_height

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

	#def onControl(self, control):
		#if control == self.list:
			#item = self.list.getSelectedItem()
			#self.message('You selected: ' + item.getLabel())
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
