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

from typing import Callable
from typing import Optional

from PySide2.QtCore import Qt, Signal
from PySide2.QtGui import QTextOption, QKeyEvent
from PySide2.QtWidgets import (QLabel, QPushButton, QPlainTextEdit, QWidget,
                               QFrame, QVBoxLayout)

from _constants import DEFAULT_WIDGET_HEIGHT, DEFAULT_CONTROL_ENTRY_WIDTH, NO_MARGINS, Point
from _keys import REVERSE_KEY_MAP


class Control:
    """All controls have identical external API, only allowing reading and changing text"""
    def __init__(self, widget):
        # type: (QWidget) -> None
        """Store the actual widget to get and set text from/to"""
        self.__widget = widget

    def get_text(self):
        # type: () -> str
        """Returns the text in a label, the text label of a button, or the text in the input field of a text input.

        For an input field, this is useful to look at the contents of the input field before the user presses Enter."""
        return self.__widget.text()

    def set_text(self, text):
        # type: (str) -> None
        """Changes the text in a label, the text label of a button, or the text in the input field of a text input.

        For a button, it also resizes the button if the button wasn't created with a particular width.
        For an input field, this is useful to provide a default input for the input field."""
        self.__widget.setText(text)


class EventWidget(QLabel):
    """Control for the keypress and mouse event info panels"""
    def __init__(self, default_string, parent=None, width=DEFAULT_CONTROL_ENTRY_WIDTH):
        super().__init__(default_string, parent)
        self.__default_string = default_string
        self.setFrameStyle(QFrame.Box | QFrame.Plain)
        self.setFixedSize(width, 17)

    def set_text(self, text):
        self.setText(self.__default_string + text)


class PlainTextSingleLine(QPlainTextEdit):
    """Prevents newlines being inserted and emits a signal when Enter pressed"""

    __caught_keys = {Qt.Key_Enter, Qt.Key_Return}
    enter_pressed = Signal(str)

    def __init__(self, parent):
        super().__init__(parent)
        self.setTabChangesFocus(True)

    def keyPressEvent(self, e):
        # type: (QKeyEvent) -> None
        """Ignore Enter/Return to prevent newlines"""
        if e.key() in self.__caught_keys:
            return

        super().keyPressEvent(e)

    def keyReleaseEvent(self, e):
        # type: (QKeyEvent) -> None
        """On Enter/Return, send signal to activate key input handler"""
        if e.key() in self.__caught_keys:
            self.focusNextChild()
            self.enter_pressed.emit(self.toPlainText())
            return

        super().keyReleaseEvent(e)


class TextInputWidget(QWidget):
    enter_pressed = Signal(str)

    def __init__(self, text, parent, width):
        # type: (str, QWidget) -> None
        super().__init__(parent)
        self.__label = QLabel(text, self)
        self.__label.setFixedWidth(width)
        self.__input = PlainTextSingleLine(self)
        self.__input.setWordWrapMode(QTextOption.NoWrap)
        self.__input.setFixedSize(width, DEFAULT_WIDGET_HEIGHT)
        self.__input.enter_pressed.connect(self.enter_pressed)

        self.setContentsMargins(NO_MARGINS)
        layout = QVBoxLayout(self)
        layout.setSpacing(1)
        layout.setContentsMargins(NO_MARGINS)
        layout.setSizeConstraint(QVBoxLayout.SetFixedSize)
        layout.addWidget(self.__label)
        layout.addWidget(self.__input)
        self.setLayout(layout)

        self.setFocusProxy(self.__input)

    # Duplicate Qt API for buttons and labels to simplify Control class wrapper
    def text(self):
        return self.__input.toPlainText()

    def setText(self, text):
        self.__input.setPlainText(text)


class ControlPanelWidget(QWidget):
    """Layout and widget handler for the left-hand controls panel"""

    def __init__(self, parent, height, width=None):
        # type: (QWidget, int, int) -> None
        """Initialise a control panel widget of the given size"""
        super().__init__(parent)
        self.setFixedHeight(height)
        if width is not None:
            self.setFixedWidth(width)

        self.__insertion_point = 0  # Where new widgets are added
        self.setContentsMargins(NO_MARGINS)
        layout = QVBoxLayout()
        layout.setContentsMargins(NO_MARGINS)
        layout.addStretch()

        self.__key_widget = EventWidget('Key: ', self)
        self.__mouse_widget = EventWidget('Mouse: ', self)

        for cont in [self.__key_widget, self.__mouse_widget]:
            layout.addWidget(cont, alignment=Qt.AlignLeft)

        self.setLayout(layout)
        self.__layout = layout

    def on_keydown(self, key):
        # type: (int) -> None
        """Update the key widget"""
        self.__key_widget.set_text('Down ' + REVERSE_KEY_MAP[key])

    def on_keyup(self, key):
        # type: (int) -> None
        """Update the key widget"""
        self.__key_widget.set_text('Up ' + REVERSE_KEY_MAP[key])

    def on_mouseclick(self, coord):
        # type: (Point) -> None
        """Update the mouse widget"""
        self.__mouse_widget.set_text('Click {}, {}'.format(*coord))

    def on_mousedrag(self, coord):
        # type: (Point) -> None
        """Update the mouse widget"""
        self.__mouse_widget.set_text('Move - {}, {}'.format(*coord))

    def __add_widget(self, widget):
        """Actually insert the widget to the layout"""
        self.__layout.insertWidget(self.__insertion_point, widget, alignment=Qt.AlignLeft)
        self.__insertion_point += 1

    def add_label(self, text, width=None):
        # type: (str, Optional[int]) -> Control
        """Adds a text label to the control panel"""
        widget = QLabel(text, self)
        if width is not None:
            widget.setFixedWidth(width)
        self.__add_widget(widget)
        return Control(widget)

    def add_button(self, text, button_handler, width=None):
        # type: (str, Callable[[], None], Optional[int]) -> Control
        """Adds a button to the frame's control panel with the given text label.

        The width of the button defaults to fit the given text, but can be specified in pixels. If the provided width is
        less than that of the text, the text overflows the button.  The handler should be defined with no parameters.
        """
        widget = QPushButton(text, self)
        if width is not None:
            widget.setFixedWidth(width)
        self.__add_widget(widget)
        widget.clicked.connect(button_handler)
        return Control(widget)

    def add_input(self, text, input_handler, width):
        # type: (str, Callable[[str], None], int) -> Control
        """Adds a text input field to the control panel with the given text label.

        The input field has the given width in pixels. The handler should be defined with one parameter. This parameter
        will receive a string of the text input when the user presses the Enter key.
        """
        widget = TextInputWidget(text, self, width)
        self.__add_widget(widget)
        widget.enter_pressed.connect(input_handler)
        return Control(widget)
