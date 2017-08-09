import sublime
import sublime_plugin
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "ext"))

import urllib
from google import search
from bs4 import BeautifulSoup


class SourceFetchCommand(sublime_plugin.TextCommand):
	def run(self,edit):
		sels = self.view.sel()

		messages = []

		for sel in sels:
		    selection = self.view.substr(sel)
		    
		    if(len(selection) == 0):
		    	messages.append("No text selected")
		    	self.show_quick_panel(messages, self.view.window())
		    	return

		    break
		
		language = self.view.settings().get('syntax').split('/')[2].split('.')[0]

		query = '{} in {} site:stackoverflow.com'.format(selection,language)

		for url in search(query, stop = 1):
			response = urllib.request.urlopen(url).read()
			soup = BeautifulSoup(response, "html.parser")

			try:
				code = soup.find('div', attrs = {
					'class' : 'accepted-answer'
				}).find('pre').find('code').text

				self.view.replace(edit, sels[0], code)

				messages.append("{} - Completed searching".format(language))
			
			except Exception as e:
				messages.append('{} - Error in finding a good code for you'.format(language))	
			self.show_quick_panel(messages, self.view.window())
			return

		messages.append("{} - Google searching failed".format(language))
		self.show_quick_panel(messages, self.view.window())


	def show_quick_panel(self, messages, window):
		window.show_quick_panel(messages, None, sublime.MONOSPACE_FONT)