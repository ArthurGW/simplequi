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
from typing import Callable, Optional, Tuple

from PySide2.QtCore import Qt, QTimer, Signal
from PySide2.QtWidgets import QWidget, QSizePolicy, QHBoxLayout

from ._app import TheApp
from ._canvas import DrawingAreaContainer, Canvas
from ._colours import get_colour
from ._constants import DEFAULT_FRAME_MARGIN
from ._fonts import get_text_width_for_font_spec, FontSpec
from ._widgets import Control, ControlPanelWidget


class MainWidget(QWidget):
    """QWidget that notifies on close"""
    closed = Signal()

    def closeEvent(self, event):
        """Tell Frame container about this event"""
        self.closed.emit()
        super().closeEvent(event)


class Frame:
    """Singleton Frame containing all other widgets.

    Note the singleton-ness in not strictly enforced here, but the module function 'reset_frame' is the only external
    function that should be used to get Frames, and that simply resets the fixed instance of this class.
    """
    __called = False  # Whether user has created a frame
    __first_init = True
    __main_widget = None

    def __init__(self, title, canvas_width, canvas_height, control_width=None):
        # type: (str, int, int, Optional[int]) -> None
        """Create a frame"""
        self.__reset(title, canvas_width, canvas_height, control_width)

    def __init_main_widget(self):
        """Create the main widget"""
        first_init = self.__main_widget is None
        if not first_init:
            try:
                self.__main_widget.close()
            except RuntimeError:
                # Already deleted
                pass
        self.__main_widget = MainWidget()
        self.__main_widget.closed.connect(self.__on_main_widget_closed)

    # Internal
    def __on_main_widget_closed(self):
        """Remove reference to allow deletion"""
        self.__main_widget = None

    def __reset(self, title, canvas_width, canvas_height, control_width=None):
        # type: (str, int, int, Optional[int]) -> None
        """Destroys all widgets associated with this frame, stops handlers running, sets params to new values"""
        self.__init_main_widget()

        # Basic window layout
        self.__main_widget.setWindowTitle(title)
        self.__main_widget.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        palette = self.__main_widget.palette()
        palette.setColor(palette.Window, get_colour('white'))
        self.__main_widget.setPalette(palette)

        # Widgets layout
        self.__main_layout = QHBoxLayout()
        self.__main_layout.setSizeConstraint(QHBoxLayout.SetFixedSize)
        self.__main_layout.setSpacing(DEFAULT_FRAME_MARGIN.left())
        self.__main_layout.setContentsMargins(DEFAULT_FRAME_MARGIN)
        self.__controls = ControlPanelWidget(self.__main_widget, canvas_height, control_width)
        self.__drawing_area = DrawingAreaContainer(self.__main_widget, canvas_width, canvas_height)

        total_height = self.__drawing_area.height() + DEFAULT_FRAME_MARGIN.top() * 2
        self.__main_widget.setFixedHeight(total_height)

        self.__main_layout.addWidget(self.__controls, alignment=Qt.Alignment(Qt.AlignLeft | Qt.AlignTop))
        self.__main_layout.addWidget(self.__drawing_area, alignment=Qt.AlignCenter)
        self.__main_widget.setLayout(self.__main_layout)

        # Setup for key handling
        self.__main_widget.setFocusProxy(self.__drawing_area.canvas)
        self.__main_widget.setFocusPolicy(Qt.StrongFocus)
        self.__drawing_area.canvas.setFocus()

        if not self.__first_init:
            # User has initialised a frame
            self.__main_widget.show()
            self.__called = True
        else:
            self.__first_init = False
            # Ensure app closes if no frames are created, won't run until the end of the user's script
            QTimer.singleShot(0, self.__check_no_frames_created)

    def __check_no_frames_created(self):
        """If no user-created frame exists, make sure this closes to prevent it keeping the app running"""
        if not self.__called:
            self.__main_widget.close()

    def set_canvas_background(self, colour):
        # type: (str) -> None
        """Changes the background colour of the frame 's canvas, which defaults to black"""
        self.__drawing_area.set_background_colour(colour)

    def start(self):
        """Commence event handling on the frame (actually on the canvas that handles the events)"""
        self.__drawing_area.canvas.start()
        # TheApp.exec_()

    @staticmethod
    def get_canvas_textwidth(text, size, face):
        # type: (str, int, str) -> int
        """Given a text string, a font size, and a font face, this returns the width of the text in pixels.

        It does not draw the text. This is useful in computing the position to draw text when you want it centered or
        right justified in some region. The supported font faces are the default 'serif', 'sans-serif', and 'monospace'.
        """
        return get_text_width_for_font_spec(text, FontSpec(size, face))

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
        This parameter will receive an integer representing a keyboard character.
        """
        self.__drawing_area.canvas.set_keydown_handler(key_handler, self.__controls.on_keydown)

    def set_keyup_handler(self, key_handler):
        # type: (Callable[[int], None]) -> None
        """Add keyboard event handler waiting for keyup event.

        When any key is released, the keyup handler is called once. The handler should be defined with one parameter.
        This parameter will receive an integer representing a keyboard character.
        """
        self.__drawing_area.canvas.set_keyup_handler(key_handler, self.__controls.on_keyup)

    def set_mouseclick_handler(self, mouse_handler):
        # type: (Callable[[tuple], None]) -> None
        """Add mouse event handler waiting for mouseclick event.

        When a mouse button is clicked, i.e., pressed and released, the mouseclick handler is called once. The handler
        should be defined with one parameter. This parameter will receive a pair of screen coordinates, i.e., a tuple of
        two non-negative integers.
        """
        self.__drawing_area.canvas.set_mouseclick_handler(mouse_handler, self.__controls.on_mouseclick)

    def set_mousedrag_handler(self, mouse_handler):
        # type: (Callable[[Tuple[int, int]], None]) -> None
        """Add mouse event handler waiting for mousedrag event.

        When a mouse is dragged while the mouse button is being pressed, the mousedrag handler is called for each new
        mouse position. The handler should be defined with one parameter. This parameter will receive a pair of screen
        coordinates, i.e., a tuple of two non-negative integers.
        """
        self.__drawing_area.canvas.set_mousedrag_handler(mouse_handler, self.__controls.on_mousedrag)

    def set_draw_handler(self, draw_handler):
        # type: (Callable[[Canvas], None]) -> None
        """Adds an event handler that is responsible for all drawing.

        The handler should be defined with one parameter. This parameter will receive a
        :class:`~simplequi._canvas.Canvas` object.

        :param draw_handler: function to call every 1/60:sup:`th` of a second (actually 17ms), which gets a
            :class:`~simplequi._canvas.Canvas` object as an argument
        """
        self.__drawing_area.canvas.set_draw_handler(draw_handler)


# Create singleton Frame with dummy params
FRAME = Frame('', 1, 1)


def reset_frame(title, canvas_width, canvas_height, control_width=None):
    # type: (str, int, int, Optional[int]) -> Frame
    """Reset the frame singleton and return it"""
    Frame.__init__(FRAME, title, canvas_width, canvas_height, control_width)
    return FRAME
