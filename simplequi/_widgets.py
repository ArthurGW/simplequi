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
from typing import Tuple
import sys

from PySide2.QtCore import Qt, QMargins, Signal
from PySide2.QtGui import QTextOption, QKeyEvent
from PySide2.QtWidgets import QLabel, QPushButton, QPlainTextEdit, QWidget, QFrame, QHBoxLayout, QVBoxLayout

from _colours import get_colour
from simplequi import _app


DEFAULT_WIDGET_HEIGHT = 25
DEFAULT_CONTROL_ENTRY_WIDTH = 200
DEFAULT_FRAME_MARGIN = 20


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

        self.setContentsMargins(QMargins())
        layout = QVBoxLayout(self)
        layout.setSpacing(1)
        layout.setContentsMargins(QMargins())
        layout.addWidget(self.__label)
        layout.addWidget(self.__input)
        self.setLayout(layout)

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

        layout = QVBoxLayout()
        layout.addStretch()
        self.__insertion_point = 0  # Where new widgets are added
        self.setContentsMargins(0, 0, 0, 0)
        layout.setContentsMargins(5, 5, 5, 5)

        self.__key_widget = EventWidget('Key: ', self)
        self.__mouse_widget = EventWidget('Mouse: ', self)

        for cont in [self.__key_widget, self.__mouse_widget]:
            layout.addWidget(cont, alignment=Qt.AlignLeft)

        self.setLayout(layout)
        self.__layout = layout

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


class Frame:
    """Singleton Frame containing all other widgets

    Note the singleton-ness in not strictly enforced here, but the module function 'reset_frame' is the only external
    function that should be used to get Frames, and that simply resets the fixed instance of this class
    """

    __first_init = True

    def __init__(self, title, canvas_width, canvas_height, control_width=None):
        # type: (str, int, int, Optional[int]) -> None
        """Create a frame"""
        if self.__first_init:
            # This actually gets deleted by reset but this is the easiest way to do it
            self.__main_widget = QWidget()

        # Actually setup the UI
        self.__reset(title, canvas_width, canvas_height, control_width)

        if not self.__first_init:
            # The first init is a dummy one to create the singleton, hence only show window on future inits
            self.__main_widget.show()
        else:
            self.__first_init = False

    def set_canvas_background(self, colour):
        # type: (str) -> None
        """Changes the background colour of the frame 's canvas, which defaults to black"""
        colour = get_colour(colour)
        raise NotImplementedError

    @staticmethod
    def start():
        """Commence event handling on the frame"""
        sys.exit(_app.exec_())

    def get_canvas_textwidth(self, text, size, face):
        # type: (str, int, str) -> int
        """Given a text string, a font size, and a font face, this returns the width of the text in pixels.

        It does not draw the text. This is useful in computing the position to draw text when you want it centered or
        right justified in some region. The supported font faces are the default 'serif', 'sans-serif', and 'monospace'.
        """
        raise NotImplementedError

    def add_label(self, text, width=None):
        # type: (str, Optional[int]) -> Control
        """Adds a text label to the control panel

        The width of the label defaults to fit the width of the given text, but can be specified in pixels. If the
        provided width is less than that of the text, the text overflows the label.
        """
        return self.__controls.add_label(text, width)

    def add_button(self, text, button_handler, width=None):
        # type: (str, Callable[[], None], Optional[int]) -> Control
        """Adds a button to the frame's control panel with the given text label.

        The width of the button defaults to fit the given text, but can be specified in pixels. If the provided width is
        less than that of the text, the text overflows the button.  The handler should be defined with no parameters.
        """
        return self.__controls.add_button(text, button_handler, width)

    def add_input(self, text, input_handler, width):
        # type: (str, Callable[[str], None], int) -> Control
        """Adds a text input field to the control panel with the given text label.

        The input field has the given width in pixels. The handler should be defined with one parameter. This parameter
        will receive a string of the text input when the user presses the Enter key.
        """
        return self.__controls.add_input(text, input_handler, width)

    def set_keydown_handler(self, key_handler):
        # type: (Callable[[int], None]) -> None
        """Add keyboard event handler waiting for keydown event.

        When any key is pressed, the keydown handler is called once. The handler should be defined with one parameter.
        This parameter will receive an integer representing a keyboard character."""
        raise NotImplementedError

    def set_keyup_handler(self, key_handler):
        # type: (Callable[[int], None]) -> None
        """Add keyboard event handler waiting for keyup event.

        When any key is released, the keyup handler is called once. The handler should be defined with one parameter.
        This parameter will receive an integer representing a keyboard character."""
        raise NotImplementedError

    def set_mouseclick_handler(self, mouse_handler):
        # type: (Callable[[tuple], None]) -> None
        """Add mouse event handler waiting for mouseclick event.

        When a mouse button is clicked, i.e., pressed and released, the mouseclick handler is called once. The handler
        should be defined with one parameter. This parameter will receive a pair of screen coordinates, i.e., a tuple of
        two non-negative integers.
        """
        raise NotImplementedError

    def set_mousedrag_handler(self, mouse_handler):
        # type: (Callable[[Tuple[int, int]], None]) -> None
        """Add mouse event handler waiting for mousedrag event.

        When a mouse is dragged while the mouse button is being pressed, the mousedrag handler is called for each new
        mouse position. The handler should be defined with one parameter. This parameter will receive a pair of screen
        coordinates, i.e., a tuple of two non-negative integers."""
        raise NotImplementedError

    def set_draw_handler(self, draw_handler):
        # type: (Callable[[Canvas], None]) -> None
        """Adds an event handler that is responsible for all drawing.

        The handler should be defined with one parameter. This parameter will receive a canvas object."""
        raise NotImplementedError

    # Internal API
    def __reset(self, title, canvas_width, canvas_height, control_width=None):
        # type: (str, int, int, Optional[int]) -> None
        """Destroys all widgets associated with this frame, stops handlers running, sets params to new values"""
        # Destroy old widget, which cascades down to all child widgets, and create new
        self.__main_widget.deleteLater()
        self.__main_widget = QWidget()

        # Basic window layout
        self.__main_widget.setWindowTitle(title)
        # control_width = DEFAULT_CONTROL_PANEL_WIDTH if control_width is None else control_width
        # total_width = canvas_width + control_width + DEFAULT_FRAME_MARGIN * 2
        total_height = canvas_height + DEFAULT_FRAME_MARGIN * 2
        self.__main_widget.setFixedHeight(total_height)

        # Widgets layout
        self.__main_layout = QHBoxLayout()
        self.__main_layout.setContentsMargins(*([DEFAULT_FRAME_MARGIN] * 4))
        self.__controls = ControlPanelWidget(self.__main_widget, canvas_height)
        self.__controls2 = ControlPanelWidget(self.__main_widget, canvas_height)  # Duplicate for testing
        self.__main_layout.addWidget(self.__controls, alignment=Qt.AlignLeft)
        self.__main_layout.addWidget(self.__controls2)  # Duplicate for testing.  TODO: remove
        self.__main_widget.setLayout(self.__main_layout)


# Create singleton Frame with dummy params
FRAME = Frame('', 1, 1)


def reset_frame(title, canvas_width, canvas_height, control_width=None):
    # type: (str, int, int, Optional[int]) -> Frame
    """Reset the previous frame and return singleton"""
    Frame.__init__(FRAME, title, canvas_width, canvas_height, control_width)
    return FRAME