import npyscreen
import curses
import base

from widgets import *

class TestDataForm(base.MainForm):
  value = """{ 'hello' : 'world' }"""
  
  def create(self):
    self.editor = self.add(JSTextEditor,
                            value = self.value,
                            rely =4,
                            color="DEFAULT")

    self.createInstructions([
      '^X : Exit Editor'
    ])
                                
    self.editor.manager = self

  def on_ok(self):
    self.parentApp.runEnviron.addValue(self.editor.value)
    self.parentApp.change_form("RUNENVIRON")
