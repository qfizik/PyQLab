from atom.api import (Atom, List, ContainerList, Dict, observe, Callable, Typed, Unicode)

import enaml


class DictManager(Atom):
	"""
	Control - Presenter for a dictionary of items. 
	i.e. give the ability to add/delete rename items
	"""
	itemDict = Typed(dict)
	displayFilter = Callable() # filter which items to display later
	possibleItems = List() # a list of classes that can possibly be added to this list
	displayList = ContainerList()

	def add_item(self, parent):
		"""
		Create a new item dialog window and handle the result
		"""
		with enaml.imports():
			from widgets.dialogs import AddItemDialog
		dialogBox = AddItemDialog(parent, modelNames=[i.__name__ for i in self.possibleItems], objText='')
		dialogBox.exec_()
		if dialogBox.result:
			self.itemDict[dialogBox.newLabel] = self.possibleItems[dialogBox.newModelNum](label=dialogBox.newLabel)
			self.displayList.append(dialogBox.newLabel)

	def remove_item(self, parent):
		print("Remove item called")

	def name_change():
		pass

	@observe('itemDict')
	def update_display_list(self, change):
		"""
		Eventualy itemDict will be a ContainerDict and this will fire on all events
		"""
		self.displayList = [v.label for v in self.itemDict.values() if self.displayFilter(v)]
