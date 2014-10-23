import npyscreen
import curses
import base

from widgets import *

class RunEnvironment(base.MainForm):
  MAIN_WIDGET_CLASS = DataList

  def create(self):
    self.wMain = self.add(DataList, rely=4)

    self.createInstructions([
      '^A : Add test data',
      '^M : Modify test data',
      '^D : Remove test data',
      '^E : Execute application',
    ])
    
  def beforeEditing(self):
      self.update_list()

  def addValue(self, value):
    self.wMain.values.append(value)
    self.update_list()

  def update_list(self):
      self.wMain.display()
