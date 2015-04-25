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

class WebElementInspector(QDockWidget):
  
  webElementChanged = pyqtSignal(name="webElementChanged")
  
  def __init__(self, title="", parent=None, flags=Qt.Widget):
    QDockWidget.__init__(self, title, parent, flags)
    self.element = None
    self.treeWidget = QTreeWidget(self)
    self.treeWidget.setColumnCount(2)
    self.treeWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
    self.treeWidget.setHeaderLabels(["Attribute", "Value"])
    self.setWidget(self.treeWidget)
    
    self.connect(self.treeWidget,
                SIGNAL("itemClicked(QTreeWidgetItem*, int)"), self.treeItemClicked)
    
    self.connect(self.treeWidget,
                SIGNAL("itemChanged(QTreeWidgetItem*, int)"), self.treeItemChanged)
    
  def setWebElement(self, element):
    if self.element == element:
      return

    self.element = element
    self.treeWidget.clear()

    if self.element:
      for name in self.element.attributeNames():
        value = self.element.attribute(name, "")
        item = QTreeWidgetItem(self.treeWidget, [name, value])
        item.setFlags(Qt.ItemIsEditable | Qt.ItemIsEnabled)
        self.treeWidget.addTopLevelItem(item)
      
  def treeItemClicked(self, item, column):
    if column == 1:
      self.treeWidget.editItem(item, column)
      
  def treeItemChanged(self, item, column):
    if self.element:
      self.element.setAttribute(item.text(0), item.text(1))
      self.webElementChanged.emit()
