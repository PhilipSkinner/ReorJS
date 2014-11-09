import npyscreen
import curses

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


	def createInstructions(self, instructions):
		gd = self.add(npyscreen.GridColTitles, relx = 2, rely=2, height=1, col_titles = instructions)
		gd._is_editable = False
		gd.editable = False
		gd.handlers = {
			'^P':									self.h_exit_up,
			'^N':									self.h_exit_up,
			curses.KEY_UP:				self.h_exit_up,
			curses.KEY_LEFT:			self.h_exit_up,
			curses.KEY_DOWN:			self.h_exit_up,
			curses.KEY_RIGHT:			self.h_exit_up,
		}
