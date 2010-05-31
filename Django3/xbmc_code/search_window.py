import xbmc, xbmcgui, xbmcplugin, sys
import functions as FS

#get actioncodes from keymap.xml
ACTION_PREVIOUS_MENU = 10
ACTION_SELECT_ITEM = 7

class Search_class(xbmcgui.Window):
	def __init__(self):
		info_labels = {}
		info_labels['name'] = 'Back to Search'
		FS.ADD_DIR(0, 1, "", info_labels)
		xbmcplugin.endOfDirectory(handle = 0)

	def onAction(self, action):
		try:
			print('Action called is: ' + str(action.getId()))
			if action.getId() == ACTION_PREVIOUS_MENU:
				self.close()
			if action.getId() == ACTION_SELECT_ITEM:
				self.str_action = xbmcgui.ControlLabel(300, 200, 200, 200, '', 'font14', '0xFF00FF00')
				self.addControl(self.str_action)
				self.str_action.setLabel('Hello World!')
		except Exception,e:
			print(e)

def show():
	search_display = Search_class()
	search_display.doModal()
	del search_display
