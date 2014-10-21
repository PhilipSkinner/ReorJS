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
  
  def debug_message(self, what): 
    self.insert_value("cheese")

  def insert_value(self, value):
    value = str(value)
  
    if self.editable and self.cursor_position >= 0:
      self.value = self.value[:self.cursor_position] + value + self.value[self.cursor_position:]
    
    self.cursor_position += len(value)   
  
class Editor(npyscreen.NPSApp):
  value = """function(id, data) {\n\treturn {};\n}""".replace('\t', '    ')

  def main(self):
    self.editorForm  = npyscreen.Form(name = "Editing %s" % ("myfile.js"))
    self.editor = self.editorForm.add(JSTextEditor,
                             value = self.value,
                             rely=2)
    self.editor.manager = self
    self.editorForm.edit()
  
  def displayRun(self):
    self.value = self.editor.value
    self.runForm = npyscreen.Form(name = "Running %s" % ("myfile.js"))
    
    t  = self.runForm.add(npyscreen.TitleText, name = "Text:",)
    
    self.runForm.display()
    
    
    
ed = Editor()
ed.run()
