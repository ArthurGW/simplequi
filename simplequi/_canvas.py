# -----------------------------------------------------------------------------
# Copyright ©2019 Arthur Gordon-Wright
# <https://github.com/ArthurGW/simplequi>
# <simplequi.codeskulptor@gmail.com>
# 
# This file is part of simplequi.
# 
# simplequi is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# simplequi is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with simplequi.  If not, see <https://www.gnu.org/licenses/>.
# -----------------------------------------------------------------------------
import PySide2
from PySide2.QtCore import Qt

from PySide2.QtWidgets import QWidget, QVBoxLayout
from PySide2.QtGui import QPainter, QColor, QPaintEvent, QBrush

from _colours import get_colour
from _constants import DEFAULT_FRAME_MARGIN, NO_MARGINS


class DrawArea(QWidget):
    """The widget that actually renders the desired canvas"""

    def __init__(self, parent, width, height):
        # type: (QWidget, int, int) -> None
        """Initialise a canvas with set width and height"""
        super().__init__(parent)
        self.setFixedSize(width, height)
        self.setContentsMargins(NO_MARGINS)
        self.__background_colour = get_colour('Black')
        self.__width = width
        self.__height = height

    def set_background_colour(self, colour):
        # type: (QColor) -> None
        """Change the canvas background"""
        self.__background_colour = colour

    def paintEvent(self, event):
        # type: (QPaintEvent) -> None
        """Render all user-specified shapes on the canvas"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint(QPainter.Antialiasing | QPainter.TextAntialiasing | QPainter.SmoothPixmapTransform), True)
        painter.fillRect(0, 0, self.__width - 1, self.__height - 1, self.__background_colour)
        painter.setBrush(QBrush(get_colour('Red')))
        painter.setPen(get_colour('Red'))
        painter.drawLine(0, 0, self.__width - 1, self.__height - 1)


class CanvasContainer(QWidget):
    """Container for the canvas area"""

    def __init__(self, parent, width, height):
        super().__init__(parent)
        self.setFixedSize(width, height)
        self.setContentsMargins(NO_MARGINS)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(NO_MARGINS)
        self.__draw_area = DrawArea(self, width, height)
        layout.addWidget(self.__draw_area, alignment=Qt.AlignCenter)
        self.setLayout(layout)
