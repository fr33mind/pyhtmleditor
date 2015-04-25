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

from PyQt4.QtWebKit import *
from PyQt4.QtGui import QPainter
from PyQt4.QtCore import *

class WebView(QWebView):

  webElementClicked = pyqtSignal('const QWebElement&', name="webElementClicked")

  def __init__(self, parent):
    QWebView.__init__(self, parent)
    self.selectedWebElement = None
    self.connect(self,
                SIGNAL("loadStarted()"), self.clearSelection)

  def clearSelection(self):
    self.selectedWebElement = None

  def _drawSelection(self, webelement):
    if not webelement:
      return

    webframe = webelement.webFrame()
    if not webframe:
      return

    scrollPos = webframe.scrollPosition()
    rect = webelement.geometry()
    if scrollPos.x() > (rect.x() + rect.width()) or scrollPos.y() > (rect.y() + rect.height()):
      return

    rect.moveTo(rect.x() - scrollPos.x(), rect.y() - scrollPos.y())
    painter = QPainter(self)
    painter.drawRect(rect)

  def paintEvent(self, ev):
    QWebView.paintEvent(self, ev)
    self._drawSelection(self.selectedWebElement)

  def selectWebElement(self, element):
    if self.selectedWebElement == element:
      return

    self.selectedWebElement = element
    self.update()
    self.webElementClicked.emit(element)

  def mouseReleaseEvent(self, event):
    result = self.page().mainFrame().hitTestContent(event.pos())
    if not result.isNull():
      element = result.element()
      if element.isNull():
        element = result.enclosingBlockElement()
      if element != self.selectedWebElement:
        self.selectWebElement(element)

    QWebView.mousePressEvent(self, event)
