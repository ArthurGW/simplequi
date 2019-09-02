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

from collections import namedtuple
from enum import auto, Enum
from math import pi
from typing import Callable, Union, Tuple, List
from typing import Iterable
from typing import Optional

from PySide2.QtCore import Qt
from PySide2.QtWidgets import QWidget, QHBoxLayout
from PySide2.QtGui import QPainter, QColor, QPaintEvent, QBrush, QPen, QPalette

from _app import TheApp
from _colours import get_colour
from _constants import NO_MARGINS, SUPPORTED_FONT_FACES
from _image import Image

Point = Union[List[int], Tuple[int, int]]  # As lists are mutable typing doesn't let you specify no. of elements
Size = Point  # Same signature but different named for clarity


ObjectHolder = namedtuple('ObjectHolder', ['obj_type', 'args'])


def radians_to_qpainter_angle(rads):
    # type: (float) -> int
    """Convert an angle in radians to one in 1/16ths of degrees as used by QPainter"""
    return int(360 * 16 * rads / (2 * pi))


def set_painter_line_width_and_colour(painter, line_width, line_colour):
    # type: (QPainter, int, str) -> None
    """Setup QPainter for drawing"""
    pen = QPen(QBrush(get_colour(line_colour)), line_width)
    painter.setPen(pen)


def set_painter_fill_colour(painter, fill_colour):
    # type: (QPainter, str) -> None
    """Set fill"""
    painter.setBrush(QBrush(get_colour(fill_colour)))


def set_painter_lines_and_fill(painter, line_width, line_colour, fill_colour=None):
    # type: (QPainter, int, str, Optional[str]) -> None
    """Fully setup painter for drawing"""
    set_painter_line_width_and_colour(painter, line_width, line_colour)
    if fill_colour is not None:
        set_painter_fill_colour(painter, fill_colour)


def render_line(painter, start, end, line_width, line_colour):
    # type: (QPainter, Point, Point, int, str) -> None
    """Render line on canvas"""
    set_painter_line_width_and_colour(painter, line_width, line_colour)
    painter.drawLine(*start, *end)


def get_circle_rect(center_point, radius):
    # type: (Point, int) -> Tuple[int, int, int, int]
    """Returns the rectangle containing a circle with given centre and radius.

    Returns a tuple containing (top_left_x, top_left_y, width, height) of the rectangle.
    """
    center_x, center_y = center_point
    return center_x - radius, center_y - radius, radius * 2, radius * 2


def render_arc(painter, center_point, radius, start_angle, end_angle, line_width, line_colour, fill_colour=None):
    # type: (QPainter, Point, int, int, int, int, str, Optional[str]) -> None
    """Render arc (filled or not) or full circle on canvas"""
    arc_len = end_angle - start_angle
    arc_len = radians_to_qpainter_angle(arc_len)
    start_angle = radians_to_qpainter_angle(start_angle)

    rect = get_circle_rect(center_point, radius)
    set_painter_lines_and_fill(painter, line_width, line_colour, fill_colour)
    if fill_colour is None:
        painter.drawArc(*rect, start_angle, -arc_len)
    else:
        painter.drawPie(*rect, start_angle, -arc_len)


def render_circle(painter, center_point, radius, line_width, line_colour, fill_colour=None):
    # type: (QPainter, Point, int, int, str, Optional[str]) -> None
    """Render circle on canvas"""
    rect = get_circle_rect(center_point, radius)
    set_painter_lines_and_fill(painter, line_width, line_colour, fill_colour)
    painter.drawEllipse(*rect)


def render_point(painter, point, colour):
    # type: (QPainter, Point, str) -> None
    """Render point on canvas"""
    set_painter_line_width_and_colour(painter, 1, colour)
    painter.drawPoint(*point)


def render_polyline(painter, point_list, line_width, line_colour):
    # type: (QPainter, Iterable[Point], int, str) -> None
    """Render polyline on canvas"""
    pass


def render_polygon(painter, point_list, line_width, line_colour, fill_colour=None):
    # type: (QPainter, Iterable[Point], int, str, Optional[str]) -> None
    """Render optionally-filled polygon on canvas"""
    pass


def render_text(painter, text, point, font_size, font_colour, font_face='serif'):
    # type: (QPainter, str, Point, int, str, str) -> None
    """Render text on canvas, positioned with its bottom-left corner at given point"""
    pass


def render_image(painter, image, source_centre, source_window, canvas_center, canvas_size, rotation=None):
    # type: (QPainter, Image, Point, Size, Point, Size, Optional[int]) -> None
    """Render image or portion of it on canvas with optional rotation and scaling"""
    pass


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
    ObjectTypes.Arc: render_arc,
    ObjectTypes.Circle: render_circle,
    ObjectTypes.Point: render_point,
    ObjectTypes.Polyline: render_polyline,
    ObjectTypes.Polygon: render_polygon,
    ObjectTypes.Text: render_text,
    ObjectTypes.Image: render_image,
}


class DrawingArea(QWidget):
    """The widget that actually renders the desired canvas"""

    def __init__(self, parent, width, height):
        # type: (QWidget, int, int) -> None
        """Initialise a canvas with set width and height"""
        super().__init__(parent)

        # Background colour setup
        self.__palette = QPalette()
        self.__palette.setColor(QPalette.Base, get_colour('black'))
        self.setAutoFillBackground(True)
        self.setBackgroundRole(QPalette.Base)
        self.setPalette(self.__palette)

        # General layout
        self.__canvas_width = width
        self.__canvas_height = height
        self.setContentsMargins(NO_MARGINS)
        self.setFixedSize(width, height)

        # Drawing stuff
        self.__canvas = Canvas(self)
        self.__objects = []
        self.__new_objects = []
        self.__draw_handler = None
        self.__draw_timer_id = -1
        self.__painter = QPainter(self)
        self.__painter.setRenderHint(
            QPainter.RenderHint(QPainter.Antialiasing | QPainter.TextAntialiasing | QPainter.SmoothPixmapTransform))
        self.__painter.save()

    def set_draw_handler(self, draw_handler):
        # type: (Callable[[Canvas], None]) -> None
        """Set draw handler and begin rendering loop"""
        if self.__draw_handler is not None:
            self.killTimer(self.__draw_timer_id)

        self.__draw_handler = draw_handler
        self.__draw_timer_id = self.startTimer(17)

    def timerEvent(self, event):
        """Draw if this is the draw timer, otherwise ignore"""
        if event.timerId() != self.__draw_timer_id:
            return super().timerEvent(event)
        self.__draw()

    def __draw(self):
        """Call draw handler and re-render widget if necessary"""
        self.__new_objects = []

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
        self.__palette.setColor(QPalette.Base, colour)
        self.setPalette(self.__palette)

    def paintEvent(self, event):
        # type: (QPaintEvent) -> None
        """Render all user-specified shapes on the canvas"""
        self.__painter.begin(self)
        for obj in self.__objects:
            self.__painter.restore()
            OBJECT_RENDERERS[obj.obj_type](self.__painter, *obj.args)
        self.__painter.end()


class DrawingAreaContainer(QWidget):
    """Draws a border around the actual drawing area"""

    def __init__(self, parent, width, height):
        # type: (QWidget, int, int) -> None
        """Initialise a canvas and border with set width and height and calculated border width"""
        super().__init__(parent)
        # Set up colouring - default is a grey border around a black background
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.Dark, get_colour('grey'))
        palette.setColor(QPalette.Shadow, get_colour('black'))
        self.setPalette(palette)
        self.setBackgroundRole(QPalette.Dark)

        # Variable width border for widget: 1/100 * average dimension, width between 1 and 3
        border_width = min(max((width + height) // 200, 1), 3)
        self.setFixedSize(width + border_width * 2, height + border_width * 2)

        # Layout
        self.__drawing_area = DrawingArea(self, width, height)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(NO_MARGINS)
        layout.addWidget(self.__drawing_area, alignment=Qt.AlignCenter)
        self.setLayout(layout)

    def set_draw_handler(self, draw_handler):
        # type: (Callable[[Canvas], None]) -> None
        """Set draw handler for drawing area"""
        self.__drawing_area.set_draw_handler(draw_handler)

    def set_background_colour(self, colour):
        # type: (str) -> None
        """Change the canvas background"""
        colour = get_colour(colour)
        self.__drawing_area.set_background_colour(colour)
        border = QPalette.Dark if colour is get_colour('black') else QPalette.Shadow
        self.setBackgroundRole(border)


class Canvas:
    """Wrapper for the drawing area. Implements the codeskulptor canvas API."""

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

        self.__drawing_area.add_object(ObjectHolder(ObjectTypes.Text, (text, point, font_size, font_color, font_face)))

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
        self.__drawing_area.add_object(ObjectHolder(ObjectTypes.Polyline, (point_list, line_width, line_color)))

    def draw_polygon(self, point_list, line_width, line_color, fill_color=None):
        # type: (Iterable[Point], int, str, Optional[str]) -> None
        """Draws a sequence of line segments between each adjacent pair of points in the non-empty list, plus a line
        segment between the first and last points.

        It is an error for the list of points to be empty. Each point is a 2-element tuple or list of screen
        coordinates. The line's width is given in pixels, and must be positive. The fill color defaults to None. If the
        fill color is specified, then the interior of the polygon is colored.
        """
        self.__drawing_area.add_object(ObjectHolder(ObjectTypes.Polygon,
                                                    (point_list, line_width, line_color, fill_color)))

    def draw_circle(self, center_point, radius, line_width, line_color, fill_color=None):
        # type: (Point, int, int, str, Optional[str]) -> None
        """Draws a circle at the given center point having the given radius.

        The point is a 2-element tuple or list of screen coordinates. The line's width is given in pixels and must be
        positive. The fill color defaults to None. If the fill color is specified, then the interior of the circle is
        colored.
        """
        self.__drawing_area.add_object(ObjectHolder(ObjectTypes.Circle,
                                                    (center_point, radius, line_width, line_color, fill_color)))

    def draw_arc(self, center_point, radius, start_angle, end_angle, line_width, line_color, fill_color=None):
        # type: (Point, int, float, float, int, str, Optional[str]) -> None
        """Draws an arc at the given center point having the given radius.

        The point is a 2-element tuple or list of screen coordinates. The starting and ending angles indicate which part
        of a circle should be drawn. Angles are given in radians, clockwise starting with a zero angle at the 3 o'clock
        position. The line's width is given in pixels and must be positive. The fill color defaults to None. If the fill
        color is specified, then the interior of the circle is colored.
        """
        self.__drawing_area.add_object(ObjectHolder(ObjectTypes.Arc,
                                                   (center_point, radius, start_angle, end_angle,
                                                    line_width, line_color, fill_color)))

    def draw_point(self, point, color):
        # type: (Point, str) -> None
        """Draws a 1×1 rectangle at the given point in the given color. The point is a 2-element tuple or list of screen
        coordinates."""
        self.__drawing_area.add_object(ObjectHolder(ObjectTypes.Point, (point, color)))

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
        self.__drawing_area.add_object(ObjectHolder(ObjectTypes.Image,
                                                    (image, center_source, width_height_source,
                                                     center_dest, width_height_dest, rotation)))




