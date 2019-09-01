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

from collections import deque, namedtuple
from enum import auto, Enum
from typing import Callable, Union, Tuple, List
from typing import Iterable
from typing import Optional

from PySide2.QtWidgets import QWidget
from PySide2.QtGui import QPainter, QColor, QPaintEvent, QBrush, QPen

from _colours import get_colour
from _constants import NO_MARGINS, SUPPORTED_FONT_FACES
from _image import Image

Point = Union[List[int], Tuple[int, int]]  # As lists are mutable typing doesn't let you specify no. of elements
Size = Point  # Same signature but different named for clarity


ObjectHolder = namedtuple('ObjectHolder', ['obj_type', 'args'])


def render_line(painter, args):
    # type: (QPainter, tuple) -> None
    """Render line on canvas"""
    painter.save()
    start, end, width, colour = args
    pen = QPen(QBrush(get_colour(colour)), width)
    painter.setPen(pen)
    painter.drawLine(*start, *end)
    painter.restore()


class ObjectTypes(Enum):
    Text = auto()
    Line = auto()
    Polyline = auto()
    Polygon = auto()
    Circle = auto()
    Arc = auto()
    Point = auto()
    Image = auto()


OBJECT_RENDERERS = {
    ObjectTypes.Line: render_line,
}


class DrawingArea(QWidget):
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

        # Drawing stuff
        self.__canvas = Canvas(self)
        self.__objects = deque()
        self.__new_objects = deque()
        self.__draw_handler = None
        self.__draw_timer_id = -1

    def set_draw_handler(self, draw_handler):
        # type: (Callable[[Canvas], None]) -> None
        """Set draw handler and begin rendering loop"""
        if self.__draw_handler is not None:
            self.killTimer(self.__draw_timer_id)

        self.__draw_handler = draw_handler
        self.__draw_timer_id = self.startTimer(17)

        self.__ang = 0

    def timerEvent(self, event):
        """Draw if this is the draw timer, otherwise ignore"""
        if event.timerId() != self.__draw_timer_id:
            return super().timerEvent(event)
        self.__draw()

    def __draw(self):
        """Call draw handler and re-render widget if necessary"""
        self.__new_objects = deque()

        self.__draw_handler(self.__canvas)

        if self.__new_objects != self.__objects:
            self.__objects = self.__new_objects
            self.update()

    def add_object(self, primitive):
        """Add a primitive to the draw queue"""
        self.__new_objects.append(primitive)

    def set_background_colour(self, colour):
        # type: (QColor) -> None
        """Change the canvas background"""
        self.__background_colour = colour

    def paintEvent(self, event):
        # type: (QPaintEvent) -> None
        """Render all user-specified shapes on the canvas"""
        painter = QPainter(self)
        painter.setRenderHint(
            QPainter.RenderHint(QPainter.Antialiasing | QPainter.TextAntialiasing | QPainter.SmoothPixmapTransform),
            True)
        painter.fillRect(0, 0, self.__width, self.__height, self.__background_colour)
        for obj in self.__objects:
            OBJECT_RENDERERS[obj.obj_type](painter, obj.args)
        painter.setPen(get_colour('Blue'))
        painter.drawArc(self.rect(), 0, self.__ang * 16)
        self.__ang += 1


class Canvas:
    """Wrapper for the drawing area.

    Implements the codeskulptor canvas API.  Used as a context manager in the canvas drawing call.
    """

    def __init__(self, drawing_area):
        # type: (DrawingArea) -> None
        """Initialise the wrapper"""
        self.__drawing_area = drawing_area

    def draw_text(self, text, point, font_size, font_color, font_face='serif'):
        # type: (str, Point, int, str, str) -> None
        """Writes the given text string in the given font size, color, and font face.

        The point is a 2-element tuple or list of screen coordinates representing the lower-left-hand corner of where to
        write the text.  The supported font faces are 'serif' (the default), 'sans-serif', and 'monospace'.
        """
        if font_face not in SUPPORTED_FONT_FACES:
            raise ValueError('invalid font face specified, valid options are {}'.format(SUPPORTED_FONT_FACES))

        raise NotImplementedError

    def draw_line(self, point1, point2, line_width, line_color):
        # type: (Point, Point, int, str) -> None
        """Draws a line segment between the two points, each of which is a 2-element tuple or list of screen
        coordinates. The line's width is given in pixels and must be positive.
        """
        self.__drawing_area.add_object(ObjectHolder(ObjectTypes.Line, (point1, point2, line_width, line_color)))

    def draw_polyline(self, point_list, line_width, line_color):
        # type: (Iterable[Point], int, str) -> None
        """Draws a sequence of line segments between each adjacent pair of points in the non-empty list.

        It is an error for the list of points to be empty. Each point is a 2-element tuple or list of screen
        coordinates. The line's width is given in pixels and must be positive.
        """
        raise NotImplementedError

    def draw_polygon(self, point_list, line_width, line_color, fill_color=None):
        # type: (Iterable[Point], int, str, Optional[str]) -> None
        """Draws a sequence of line segments between each adjacent pair of points in the non-empty list, plus a line
        segment between the first and last points.

        It is an error for the list of points to be empty. Each point is a 2-element tuple or list of screen
        coordinates. The line's width is given in pixels, and must be positive. The fill color defaults to None. If the
        fill color is specified, then the interior of the polygon is colored.
        """
        raise NotImplementedError

    def draw_circle(self, center_point, radius, line_width, line_color, fill_color=None):
        # type: (Point, int, int, str, Optional[str]) -> None
        """Draws a circle at the given center point having the given radius.

        The point is a 2-element tuple or list of screen coordinates. The line's width is given in pixels and must be
        positive. The fill color defaults to None. If the fill color is specified, then the interior of the circle is
        colored.
        """
        raise NotImplementedError

    def draw_arc(self, center_point, radius, start_angle, end_angle, line_width, line_color, fill_color=None):
        # type: (Point, int, float, float, int, str, Optional[str]) -> None
        """Draws an arc at the given center point having the given radius.

        The point is a 2-element tuple or list of screen coordinates. The starting and ending angles indicate which part
        of a circle should be drawn. Angles are given in radians, clockwise starting with a zero angle at the 3 o'clock
        position. The line's width is given in pixels and must be positive. The fill color defaults to None. If the fill
        color is specified, then the interior of the circle is colored.
        """
        raise NotImplementedError

    def draw_point(self, point, color):
        # type: (Point, str) -> None
        """Draws a 1×1 rectangle at the given point in the given color. The point is a 2-element tuple or list of screen
        coordinates."""
        raise NotImplementedError

    def draw_image(self, image, center_source, width_height_source, center_dest, width_height_dest, rotation=None):
        # type: (Image, Point, Size, Point, Size, Optional[float]) -> None
        """Draw an image that was previously loaded by simplequi.load_image.

        center_source is a pair of coordinates giving the position of the center of the image, while center_dest is a
        pair of screen coordinates specifying where the center of the image should be drawn on the canvas.
        width_height_source is a pair of integers giving the size of the original image, while width_height_dest is a
        pair of integers giving the size of how the images should be drawn. The image can be rotated clockwise by
        rotation radians.

        You can draw the whole image file or just part of it. The source information (center_source and
        width_height_source) specifies which pixels to display. If it attempts to use any pixels outside of the actual
        file size, then no image will be drawn.

        Specifying a different width or height in the destination than in the source will rescale the image.
        """
        raise NotImplementedError




