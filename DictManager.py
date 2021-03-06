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
    onChangeDelegate = Callable()
    otherActions = Dict(Unicode(), Callable())

    def __init__(self, itemDict={}, displayFilter=lambda x: True, **kwargs):
        self.displayFilter = displayFilter
        super(DictManager, self).__init__(itemDict=itemDict, displayFilter=displayFilter, **kwargs)

    def add_item(self, parent):
        """
        Create a new item dialog window and handle the result
        """
        with enaml.imports():
            from widgets.dialogs import AddItemDialog
        dialogBox = AddItemDialog(parent, modelNames=[i.__name__ for i in self.possibleItems], objText='')
        dialogBox.exec_()
        if dialogBox.result:
            if dialogBox.newLabel not in self.itemDict.keys():
                self.itemDict[dialogBox.newLabel] = self.possibleItems[dialogBox.newModelNum](label=dialogBox.newLabel)
                self.displayList.append(dialogBox.newLabel)
            else:
                print("WARNING: Can't use duplicate label %s"%dialogBox.newLabel)

    def remove_item(self, itemLabel):
        #check that the item exists before removing from the list
        if itemLabel in self.itemDict.keys():
            self.itemDict.pop(itemLabel)
            #TODO: once ContainerDicts land see if we still need this
            self.displayList.pop(self.displayList.index(itemLabel))
        elif itemLabel != '':
            self.displayList.pop(self.displayList.index(itemLabel))

    def name_changed(self, oldLabel, newLabel):
        # Add copy of changing item
        self.itemDict[newLabel] = self.itemDict[oldLabel]

        # update display list
        idx = self.displayList.index(oldLabel)
        self.displayList[idx] = newLabel

        # remove old label from itemDict list
        if oldLabel in self.itemDict.keys():
            self.itemDict.pop(oldLabel)
        else:
            print("WARNING: %s is not in the list"%oldLabel)

        # update label to new label list
        self.itemDict[newLabel].label = newLabel

        if self.onChangeDelegate:
            self.onChangeDelegate(oldLabel, newLabel)

    def update_enable(self, itemLabel, checkState):
        self.itemDict[itemLabel].enabled = checkState

    @observe('itemDict')
    def update_display_list(self, change):
        """
        Eventualy itemDict will be a ContainerDict and this will fire on all events.
        Will have to be more careful about whether it is a "create" event or "update"
        """
        self.displayList = sorted([v.label for v in self.itemDict.values() if self.displayFilter(v)])
