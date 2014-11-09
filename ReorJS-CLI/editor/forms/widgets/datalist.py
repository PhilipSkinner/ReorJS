import npyscreen
import curses

class DataList(npyscreen.MultiLineAction):
	def __init__(self, *args, **keywords):
		super(DataList, self).__init__(*args, **keywords)
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
