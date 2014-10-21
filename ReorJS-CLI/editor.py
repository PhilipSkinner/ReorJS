import npyscreen
import curses

class JSTextEditor(npyscreen.MultiLineEdit):
  #number of paging lines
  PAGING = 25

  def set_up_handlers(self):
    super(JSTextEditor, self).set_up_handlers()

    self.handlers.update({
                          ord("\t")		: self.tab,
                          curses.KEY_NPAGE	: self.page_down,
                          curses.KEY_PPAGE	: self.page_up,
                          curses.KEY_HOME	: self.home_key,
                          curses.KEY_END	: self.end_key,
                          curses.KEY_DOWN	: self.key_down,                          
                        })
    self.complex_handlers.extend((
                                  (self.is_exit, self.handle_exit),
                                  (self.is_save, self.handle_save),
                                  (self.is_run, self.handle_run),
                                ))
	
  def key_down(self, input):
    end_this_line = self.value.find("\n", self.cursor_position)
    if end_this_line == -1:
      self.cursor_position = len(self.value)
    else:
      self.cursor_position = end_this_line + 1
      for x in range(self.cursorx):
        if self.cursor_position > len(self.value)-1:
          break
        elif self.value[self.cursor_position] == "\n":
          break
        else:
          self.cursor_position += 1        

  def handle_exit(self, what):
    self.h_exit_down(what)    
    return
  
  def is_exit(self, inp):  
    if inp == 24:
      return True

    return False

  def handle_save(self, what):
    print "Will save to API"
    return

  def is_save(self, inp):
    if inp == 15:
      return True
    
    return False
  
  def is_run(self, inp):
    if inp == 5:
      return True
    
    return False
  
  def handle_run(self, what):
    self.manager.displayRun()
    return
  
  def page_up(self, what):
    numLines = 0
    while numLines <= self.PAGING and self.cursor_position >= 0:
      try:
        if self.value[self.cursor_position] == "\n":
          numLines += 1
      except:
        pass
      
      self.cursor_position -= 1
    
    self.cursor_position += 1    
    return
  
  def page_down(self, what):
    numLines = 0
    while numLines <= self.PAGING and self.cursor_position <= len(self.value):
      try:
        if self.value[self.cursor_position] == "\n":
          numLines += 1
      except:
        pass
      
      self.cursor_position += 1
    
    self.cursor_position -= 1
    return
  
  def end_key(self, what):
    while self.cursor_position <= len(self.value):
      try:
        if self.value[self.cursor_position] == "\n":
          self.cursor_position -= 1
          return
      except:
        pass
      
      self.cursor_position += 1
    return
  
  def home_key(self, what):
    while self.cursor_position >= 0:
      try:
        if self.value[self.cursor_position] == "\n":
          self.cursor_position += 1
          return
      except:
          pass
        
      self.cursor_position -= 1        
    return
  
  def tab(self, what):
    self.insert_value("  ")
  
  def insert_value(self, value):
    value = str(value)
  
    if self.editable and self.cursor_position >= 0:
      self.value = self.value[:self.cursor_position] + value + self.value[self.cursor_position:]
    
    self.cursor_position += len(value)   

class EditorApp(npyscreen.NPSAppManaged):
  _THISFORM = None
  editor = None
  runEnviron = None

  def onStart(self):
    self.editor 	= self.addForm("MAIN",		Editor, name="Editor", color="IMPORTANT")
    self.runEnviron 	= self.addForm("RUNENVIRON",	RunEnvironment, name="Run Environment", color="WARNING")
    self.testData	= self.addForm("TESTDATA",	TestDataForm, name="Test Data Form", color="WARNING")
    
  def onCleanExit(self):
    npyscreen.notify_wait("Goodbye!")
    
  def change_form(self, name):      
    self.switchForm(name)
    self.resetHistory()

class MainForm(npyscreen.ActionForm):
    def create(self):
      return

    def on_ok(self):
      # Exit the application if the OK button is pressed.
      self.parentApp.switchForm(None)

    def displayRun(self):
      self.parentApp.change_form("RUNENVIRON")
  
    def displayEditor(self):
      self.parentApp.change_form("EDITOR")    
    
    def displayTestDataForm(self):
      self.parentApp.change_form("TESTDATA")

    def change_forms(self, *args, **keywords):
        if self.name == "Editor":
            change_to = "MAIN"
        elif self.name == "Run Environment":
            change_to = "RUNENVIRON"

        # Tell the MyTestApp object to change forms.
        self.parentApp.change_form(change_to)
                                                                                                                                          
class Editor(MainForm):
  value = """function(id, data) {\n\treturn {};\n}""".replace('\t', '    ')

  def create(self):
    self.editor = self.add(JSTextEditor,
                             value = self.value,
                             rely=2,
                             color="NORMAL")
                             
    self.editor.manager = self

class TestDataForm(MainForm):
  value = """{ 'hello' : 'world' }"""
  
  def create(self):
    self.editor = self.add(JSTextEditor,
                            value = self.value,
                            rely =2,
                            color="NORMAL")
    
    self.editor.manager = self

  def on_ok(self):
    self.parentApp.runEnviron.addValue(self.editor.value)
    self.parentApp.change_form("RUNENVIRON")

class TestDataList(npyscreen.MultiLineAction):
  def __init__(self, *args, **keywords):
    super(TestDataList, self).__init__(*args, **keywords)
    self.add_handlers({
      "^A": self.add_record,
      "^D": self.delete_record
    })

  def display_value(self, vl):
    return vl

  def actionHighlighted(self, act_on_this, keypress):
    return
    
  def add_record(self, *args, **keywords):
    self.parent.parentApp.change_form("TESTDATA")

  def delete_record(self, *args, **keywords):
    return    

class RunEnvironment(MainForm):
  MAIN_WIDGET_CLASS = TestDataList

  def create(self):
    self.wMain = self.add(TestDataList)    

  def beforeEditing(self):
      self.update_list()

  def addValue(self, value):
    self.wMain.values.append(value)
    self.update_list()

  def update_list(self):
      self.wMain.display()

ed = EditorApp()
ed.run()
