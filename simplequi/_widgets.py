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
"""Widgets used within the :class:`~simplequi._frame.Frame` UI."""

from typing import Callable, Optional

from PySide2.QtCore import Qt, Signal
from PySide2.QtGui import QCloseEvent, QTextOption, QKeyEvent
from PySide2.QtWidgets import (QLabel, QPushButton, QPlainTextEdit, QWidget,
                               QFrame, QVBoxLayout, QSizePolicy, QHBoxLayout)

from simplequi._canvas import DrawingArea
from ._canvas import DrawingAreaContainer
from ._colours import get_colour
from ._constants import DEFAULT_CONTROL_ENTRY_WIDTH, DEFAULT_FRAME_MARGIN, DEFAULT_WIDGET_HEIGHT, NO_MARGINS, Point
from ._keys import REVERSE_KEY_MAP


class Control:
    """A control that lives in the control area of a :class:`~simplequi._frame.Frame`, and allows getting and setting
    of its display text.

    :param widget: the widget that this control wraps
    """

    def __init__(self, widget):
        # type: (QWidget) -> None
        self.__widget = widget

    def get_text(self):
        # type: () -> str
        """Returns the text in a label, the text label of a button, or the text in the input field of a text input.

        For an input field, this is useful to look at the contents of the input field before the user presses Enter.

        :return: the current text of the control
        """
        return self.__widget.text()

    def set_text(self, text):
        # type: (str) -> None
        """Changes the text in a label, the text label of a button, or the text in the input field of a text input.

        For a button, it also resizes the button if the button wasn't created with a particular width.
        For an input field, this is useful to provide a default input for the input field.

        :param text: the new text to set
        """
        self.__widget.setText(text)


class EventWidget(QLabel):
    """Control for the keypress and mouse event info panels at the bottom of the :class:`~simplequi._frame.Frame`
    control area.

    :param default_string: the first part of the label to display at all times
    :param parent: the parent widget of this widget
    :param width: the width to make this control, defaults to the same as the control area
    """

    def __init__(self, default_string, parent=None, width=DEFAULT_CONTROL_ENTRY_WIDTH):
        # type: (str, Optional[QWidget], int) -> None
        super().__init__(default_string, parent)
        self.__default_string = default_string
        self.setFrameStyle(QFrame.Box | QFrame.Plain)
        self.setFixedSize(width, 17)

    def set_text(self, text):
        # type: (str) -> None
        """Sets the widget text to the object's :ivar:`default_string` + a given string

        :param text: the text to append to the default
        """
        self.setText(self.__default_string + text)


class PlainTextSingleLine(QPlainTextEdit):
    """A text edit field that prevents newlines being inserted and emits a signal when Enter is pressed.

    :param parent: the widget parent of this widget
    """

    __caught_keys = {Qt.Key_Enter, Qt.Key_Return}  # Keys to watch out for
    enter_pressed = Signal(str)  # Emitted when enter/return is pressed with this field in focus

    def __init__(self, parent):
        # type: (QWidget) -> None
        super().__init__(parent)
        self.setTabChangesFocus(True)

    def keyPressEvent(self, e):
        # type: (QKeyEvent) -> None
        """Ignores Enter/Return to prevent newlines being inserted.

        :param e: the :class:`QKeyEvent` that has occurred
        """
        if e.key() in self.__caught_keys:
            return e.accept()

        super().keyPressEvent(e)

    def keyReleaseEvent(self, e):
        # type: (QKeyEvent) -> None
        """On Enter/Return, sends signal to activate key input handler.

        :param e: the :class:`QKeyEvent` that has occurred
        """
        if e.key() in self.__caught_keys:
            self.focusNextChild()
            self.enter_pressed.emit(self.toPlainText())
            return e.accept()

        super().keyReleaseEvent(e)


class TextInputWidget(QWidget):
    """A widget that contains a labelled text input field. The label is displayed above the input.

    :param text: the label text to use
    :param parent: the widget parent of this widget
    :param width: the width to make the input widget
    """

    enter_pressed = Signal(str)  # Emitted when the input widget has keyboard focus and user presses enter/return

    def __init__(self, text, parent, width):
        # type: (str, QWidget, int) -> None
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
        # type: () -> str
        """Gets the current text in the input field

        :return: the current text
        """
        return self.__input.toPlainText()

    def setText(self, text):
        # type: (str) -> None
        """Sets the current text in the input field

        :param text: the text to set
        """
        self.__input.setPlainText(text)


class ControlPanelWidget(QWidget):
    """Layout and widget handler for the left-hand controls panel.

    :param parent: the widget parent of this widget, should be a :class:`~simplequi._frame.Frame`'s :class:`MainWidget`
    :param height: the height to make the widget, should be the same as the containing :class:`~simplequi._frame.Frame`
    :param width: the width to make the widget, if not set defaults to fit all contained widgets
    """

    def __init__(self, parent, height, width=None):
        # type: (QWidget, int, int) -> None
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
        """Updates the key widget.

        :param key: the key code for the pressed key
        """
        self.__key_widget.set_text('Down ' + REVERSE_KEY_MAP[key])

    def on_keyup(self, key):
        # type: (int) -> None
        """Updates the key widget

        :param key: the key code for the released key
        """
        self.__key_widget.set_text('Up ' + REVERSE_KEY_MAP[key])

    def on_mouseclick(self, coord):
        # type: (Point) -> None
        """Updates the mouse widget.

        :param coord: the coordinate the mouse was clicked at
        """
        self.__mouse_widget.set_text('Click {}, {}'.format(*coord))

    def on_mousedrag(self, coord):
        # type: (Point) -> None
        """Updates the mouse widget.

        :param coord: the coordinate the mouse was currently dragged to
        """
        self.__mouse_widget.set_text('Move - {}, {}'.format(*coord))

    def __add_widget(self, widget):
        # type: (QWidget) -> None
        """Actually inserts the widget to the layout, after all current widgets except the mouse and key displays.

        :param widget: the widget to insert
        """
        self.__layout.insertWidget(self.__insertion_point, widget, alignment=Qt.AlignLeft)
        self.__insertion_point += 1

    def add_label(self, text, width=None):
        # type: (str, Optional[int]) -> Control
        """Adds a text label to the control panel

        :param text: the label text
        :param width: the optional label width, defaults to fitting the text
        :return: a handle that can be used to get and set the label text
        """
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

        :param text: the button text
        :param button_handler: a function to call when the button is activated
        :param width: the optional width to make the button, defaults to fitting the text
        :return: a handle that can be used to get and set the button text
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

        :param text: the text to use for the input label
        :param input_handler: a function to call when enter/return is pressed in the input widget
        :param width: the width to make the input widget
        :return: a handle that can be used to get and set the input field text
        """
        widget = TextInputWidget(text, self, width)
        self.__add_widget(widget)
        widget.enter_pressed.connect(input_handler)
        return Control(widget)


class MainWidget(QWidget):
    """Widget that contains all other graphical widgets

    :param title: the text to use in the frame title bar
    :param canvas_width: the width of the drawing canvas part of the frame
    :param canvas_height: the height of the drawing canvas part of the frame
    :param control_width: the optional width of the controls (buttons etc.) part of the frame
    """

    closed = Signal()  #: Emitted in the closeEvent

    def __init__(self, title, canvas_width, canvas_height, control_width=None):
        # type: (str, int, int, Optional[int]) -> None
        super().__init__()

        # Basic window layout - title, colour, sizing
        self.setWindowTitle(title)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        palette = self.palette()
        palette.setColor(palette.Window, get_colour('white'))
        self.setPalette(palette)

        # Widgets layout
        self.__main_layout = QHBoxLayout()
        self.__main_layout.setSizeConstraint(QHBoxLayout.SetFixedSize)
        self.__main_layout.setSpacing(DEFAULT_FRAME_MARGIN.left())
        self.__main_layout.setContentsMargins(DEFAULT_FRAME_MARGIN)
        self.__controls = ControlPanelWidget(self, canvas_height, control_width)
        self.__drawing_area = DrawingAreaContainer(self, canvas_width, canvas_height)

        total_height = self.__drawing_area.height() + DEFAULT_FRAME_MARGIN.top() * 2
        self.setFixedHeight(total_height)

        self.__main_layout.addWidget(self.__controls, alignment=Qt.Alignment(Qt.AlignLeft | Qt.AlignTop))
        self.__main_layout.addWidget(self.__drawing_area, alignment=Qt.AlignCenter)
        self.setLayout(self.__main_layout)

        # Setup for key handling
        self.setFocusProxy(self.__drawing_area.canvas)
        self.setFocusPolicy(Qt.StrongFocus)
        self.__drawing_area.canvas.setFocus()

    def closeEvent(self, event):
        # type: (QCloseEvent) -> None
        """Tells Frame container about this event.

        :param event: the close event
        """
        self.closed.emit()
        super().closeEvent(event)

    @property
    def canvas(self):
        # type: () -> DrawingArea
        """The actual widget that does drawing"""
        return self.drawing_area.canvas

    @property
    def controls(self):
        # type: () -> ControlPanelWidget
        """The controls area on the left-hand side of the widget"""
        return self.__controls

    @property
    def drawing_area(self):
        # type: () -> DrawingAreaContainer
        """Container for the canvas drawing area on the right-hand side of the widget"""
        return self.__drawing_area
