import npyscreen
import curses

from forms import *

class EditorApp(npyscreen.NPSAppManaged):
  _THISFORM = None
  editor = None
  runEnviron = None

  def onStart(self):
    self.editor 	= self.addForm("MAIN",		Editor, name="Editor", color="DEFAULT")
    self.runEnviron 	= self.addForm("RUNENVIRON",	RunEnvironment, name="Run Environment", color="DEFAULT")
    self.testData	= self.addForm("TESTDATA",	TestDataForm, name="Test Data Form", color="DEFAULT")
    
  def onCleanExit(self):
    npyscreen.notify_wait("Goodbye!")
    
  def change_form(self, name):      
    self.switchForm(name)
    self.resetHistory()
