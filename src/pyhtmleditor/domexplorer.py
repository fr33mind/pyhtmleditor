# -*- coding: utf-8 -*-
# Copyright (C) 2015 Carlos Pais <freemind@live.com.pt>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from PyQt4.QtCore import *
from PyQt4.QtWebKit import *
from PyQt4.QtGui import *

class DomExplorer(QDockWidget):
  
  webElementClicked = pyqtSignal('const QWebElement&', name="webElementClicked")
  
  def __init__(self, title="", parent=None, flags=Qt.Widget):
    QDockWidget.__init__(self, title, parent, flags)
    self.document = None;
    self.webelements = []
    
    centralWidget = QWidget(self)
    centralWidget.setLayout(QVBoxLayout())
    
    self.filterEdit = QLineEdit(self)
    self.filterEdit.setPlaceholderText("CSS2 selector")
    
    self.treeWidget = QTreeWidget(self)
    self.treeWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
    self.treeWidget.setHeaderLabels(["DOM"])
    
    centralWidget.layout().addWidget(self.filterEdit)
    centralWidget.layout().addWidget(self.treeWidget)
    self.setWidget(centralWidget)
    
    self.connect(self.filterEdit,
                SIGNAL("textChanged(const QString&)"), self.filterTextChanged)
                
    self.connect(self.treeWidget,
                SIGNAL("itemSelectionChanged()"), self.onItemSelectionChanged)
    
  def setDocument(self, doc):
    self.clear()
    self.document = doc
    self._addNode(doc, self.treeWidget)
    self.treeWidget.expandAll()

  def _addNode(self, element, parent):
    item = self._addTreeItem(element, parent)
    child = element.firstChild()
    #if child:
      #item.setFlags(Qt.ItemIsEditable | Qt.ItemIsEnabled)
    while not child.isNull():
      self._addNode(child, item)
      child = child.nextSibling()
      
  def onItemSelectionChanged(self):
    items = self.treeWidget.selectedItems()
    if not items:
      return
    item = items[0]
    data = item.data(0, Qt.UserRole)
    index = data.toPyObject()
    if index >= 0 and index < len(self.webelements):
      self.webElementClicked.emit(self.webelements[index])

  def clear(self):
    self.treeWidget.clear()
    self.webelements = []
    
  def _addTreeItem(self, element, parent):
    item = QTreeWidgetItem(parent, [element.localName()])
    self.webelements.append(element)
    item.setData(0, Qt.UserRole, len(self.webelements)-1)
    return item
    
  def filterTextChanged(self, text):
    self.clear()
    
    if not text:
      self.setDocument(self.document)
      return
    
    elements = self.document.findAll(text)
    
    for element in elements:
      self._addTreeItem(element, self.treeWidget)

  def webElementAt(self, index):
    if index >= 0 and index < len(self.webelements):
      return self.webelements[index]
    return None

  def webElementFromItem(self, item):
    if item:
      index = item.data(0, Qt.UserRole).toPyObject()
      if  index >= 0 and index < len(self.webelements):
        return index
    return None

  def itemFromWebElement(self, webelement):
    try:
      index = self.webelements.index(webelement)
      items = self.treeWidget.findItems("", Qt.MatchContains | Qt.MatchRecursive)
      for item in items:
        item_index = item.data(0, Qt.UserRole).toPyObject()
        if item_index == index:
          return item
    except ValueError:
      return None
      
    return None
    
  def selectWebElement(self, webelement):
    if not webelement:
      return

    currentElement = self.webElementFromItem(self.treeWidget.currentItem())
    if currentElement == webelement:
      return

    item = self.itemFromWebElement(webelement)
    if item:
      self.treeWidget.setCurrentItem(item)
    
