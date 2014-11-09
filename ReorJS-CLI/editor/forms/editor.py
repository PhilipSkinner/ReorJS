import curses
import npyscreen
from . import base

from .widgets import *

class Editor(base.MainForm):
	value = """function(id, data) {\n\treturn {};\n}""".replace('\t', '    ')

	def create(self):
		self.editor = self.add(JSTextEditor,
			value = self.value,
			rely=4,
			color="DEFAULT")

		self.createInstructions([
			'^E : Enter testing suite',
			'^O : Save to ReorJSd',
			'^X : Exit Editor',
		])

		self.editor.manager = self
