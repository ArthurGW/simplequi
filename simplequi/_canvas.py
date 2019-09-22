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
from enum import Enum
from functools import wraps
from math import pi
from typing import Callable, Tuple
from typing import Iterable
from typing import Optional

from PySide2.QtCore import Qt, QPoint, Signal
from PySide2.QtGui import QKeyEvent, QTransform
from PySide2.QtGui import QMouseEvent
from PySide2.QtGui import QPolygon
from PySide2.QtWidgets import QWidget, QHBoxLayout
from PySide2.QtGui import QPainter, QColor, QPaintEvent, QBrush, QPen, QPalette, QPixmap

from simplequi._constants import Size
from ._colours import get_colour
from ._constants import NO_MARGINS, Point
from ._fonts import get_font, FontSpec
from ._image import Image, get_pixmap

ObjectHolder = namedtuple('ObjectHolder', ['obj_type', 'args'])


def radians_to_qpainter_angle(rads):
    # type: (float) -> int
    """Convert an angle in radians to one in 1/16ths of degrees as used by QPainter"""
    return int(360 * 16 * rads / (2 * pi))


def point_list_to_polygon(point_list):
    # type: (Iterable[Point]) -> QPolygon
    """Converts an iterable of (x, y) points coordinates to a QPolygon suitable for rendering"""
    num_points = len(point_list)
    polygon = QPolygon(num_points)
    for point in point_list:
        polygon.push_back(QPoint(*point))
    return polygon


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
    set_painter_line_width_and_colour(painter, line_width, line_colour)
    polygon = point_list_to_polygon(point_list)
    painter.drawPolyline(polygon)


def render_polygon(painter, point_list, line_width, line_colour, fill_colour=None):
    # type: (QPainter, Iterable[Point], int, str, Optional[str]) -> None
    """Render optionally-filled polygon on canvas"""
    set_painter_lines_and_fill(painter, line_width, line_colour, fill_colour)
    polygon = point_list_to_polygon(point_list)
    painter.drawPolygon(polygon)


def render_text(painter, text, point, font_size, font_colour, font_face='serif'):
    # type: (QPainter, str, Point, int, str, str) -> None
    """Render text on canvas, positioned with its bottom-left corner at given point"""
    set_painter_line_width_and_colour(painter, 1, font_colour)
    font = get_font(FontSpec(font_size, font_face))
    painter.setFont(font)
    painter.drawText(*point, text)


def render_image(painter, image, source_centre, source_window, canvas_center, canvas_size, rotation=0.0):
    # type: (QPainter, Image, Point, Size, Point, Size, float) -> None
    """Render image or portion of it on canvas with optional rotation and scaling"""
    pixmap = get_pixmap(image, source_centre, source_window, canvas_size)
    if pixmap is None:
        # Image not loaded yet, shouldn't get here but just in case...
        return

    if rotation != 0.0:
        transform = QTransform()
        transform = transform.translate(*canvas_center)
        transform = transform.rotateRadians(rotation)
        painter.save()
        painter.setTransform(transform)
        canvas_center = 0, 0
    x, y = canvas_center
    x -= canvas_size[0] / 2.
    y -= canvas_size[1] / 2.
    painter.drawPixmap(x, y, pixmap)
    if rotation != 0.0:
        painter.restore()


class ObjectTypes(Enum):
    Text = 0
    Line = 1
    Polyline = 2
    Polygon = 3
    Circle = 4
    Arc = 5
    Point = 6
    Image = 7


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


def check_started(func):
    """Decorator that will only run enclosed function if the object has 'started'"""

    @wraps(func)
    def inner(inner_self, *args, **kwargs):
        if not inner_self.started:
            return
        return func(inner_self, *args, **kwargs)

    return inner


class DrawingArea(QWidget):
    """The widget that actually renders the desired canvas and handles events on it"""

    # Signals emitted when events handled
    mouseclick = Signal(tuple)
    mousedrag = Signal(tuple)
    keydown = Signal(int)
    keyup = Signal(int)

    def __init__(self, parent, width, height):
        # type: (QWidget, int, int) -> None
        """Initialise a canvas with set width and height"""
        super().__init__(parent)

        # General layout
        self.__canvas_width = width
        self.__canvas_height = height
        self.setContentsMargins(NO_MARGINS)
        self.setFixedSize(width, height)

        # Background colour setup
        self.__palette = QPalette()
        self.__palette.setColor(QPalette.Base, get_colour('black'))
        self.setAutoFillBackground(True)
        self.setBackgroundRole(QPalette.Base)
        self.setPalette(self.__palette)
        self.__background_colour = get_colour('black')
        self.__reset_pixmap()

        # Drawing stuff
        self.__canvas = Canvas(self)
        self.__objects = []
        self.__new_objects = []
        self.__draw_handler = None
        self.__draw_timer_id = -1

        # Event stuff
        self.__started = False
        self.__keydown_handler = None
        self.__keyup_handler = None
        self.__mouseclick_handler = None
        self.__mousedrag_handler = None

        # Allow focus for event handling
        self.setFocusPolicy(Qt.StrongFocus)

    # Drawing
    def set_draw_handler(self, draw_handler):
        # type: (Callable[[Canvas], None]) -> None
        """Set draw handler and begin rendering loop"""
        if self.__draw_handler is not None:
            self.killTimer(self.__draw_timer_id)

        self.__draw_handler = draw_handler
        if self.__started:
            self.__draw_timer_id = self.startTimer(17)  # Roughly 60FPS

    def timerEvent(self, event):
        """Draw if this is the draw timer, otherwise ignore"""
        if event.timerId() != self.__draw_timer_id:
            return super().timerEvent(event)
        self.__draw()

    def __reset_pixmap(self):
        """Set new pixmap filled with background colour"""
        self.__pixmap = QPixmap(self.__canvas_width, self.__canvas_height)
        self.__pixmap.fill(self.__background_colour)

    @check_started
    def __draw(self):
        """Call draw handler and re-render widget if necessary"""
        if self.__draw_handler is None:
            return

        self.__new_objects = []
        self.__draw_handler(self.__canvas)

        if self.__new_objects != self.__objects:
            self.__objects = self.__new_objects
            self.__render()

    def __render(self):
        """Actually render the canvas"""
        self.__reset_pixmap()
        painter = QPainter(self.__pixmap)
        painter.setRenderHint(
            QPainter.RenderHint(QPainter.Antialiasing | QPainter.TextAntialiasing | QPainter.SmoothPixmapTransform))
        painter.save()
        for obj in self.__objects:
            painter.restore()
            OBJECT_RENDERERS[obj.obj_type](painter, *obj.args)
        self.update()

    def add_object(self, primitive):
        """Add a primitive to the draw queue"""
        self.__new_objects.append(primitive)

    def set_background_colour(self, colour):
        # type: (QColor) -> None
        """Change the canvas background"""
        self.__palette.setColor(QPalette.Base, colour)
        self.setPalette(self.__palette)
        self.__background_colour = colour
        self.__render()

    @check_started
    def paintEvent(self, event):
        # type: (QPaintEvent) -> None
        """Draw cached pixmap on the canvas - __render takes care of creating it"""
        painter = QPainter(self)
        painter.drawPixmap(self.rect(), self.__pixmap)

    # Events
    def start(self):
        """Commence event handling and drawing"""
        self.__started = True

        # Start the draw timer if a handler exists
        if self.__draw_handler is not None:
            self.set_draw_handler(self.__draw_handler)

    @property
    def started(self):
        return self.__started

    @staticmethod
    def __connect_handlers(signal, *handlers):
        # type: (Signal, Iterable[Callable]) -> None
        """Hook up signal to handlers"""
        try:
            signal.disconnect()
        except RuntimeError:
            # No connections
            pass
        for handler in handlers:
            signal.connect(handler)

    def set_keydown_handler(self, key_handler, controls_area_slot):
        # type: (Callable[[int], None], Callable[[int], None]) -> None
        """Add keyboard event handler waiting for keydown event"""
        self.__connect_handlers(self.keydown, key_handler, controls_area_slot)

    def set_keyup_handler(self, key_handler, controls_area_slot):
        # type: (Callable[[int], None], Callable[[int], None]) -> None
        """Add keyboard event handler waiting for keyup event"""
        self.__connect_handlers(self.keyup, key_handler, controls_area_slot)

    def set_mouseclick_handler(self, mouse_handler, controls_area_slot):
        # type: (Callable[[tuple], None], Callable[[Tuple[int, int]], None]) -> None
        """Add mouse event handler waiting for mouseclick event"""
        self.__connect_handlers(self.mouseclick, mouse_handler, controls_area_slot)

    def set_mousedrag_handler(self, mouse_handler, controls_area_slot):
        # type: (Callable[[Tuple[int, int]], None], Callable[[Tuple[int, int]], None]) -> None
        """Add mouse event handler waiting for mousedrag event"""
        self.__connect_handlers(self.mousedrag, mouse_handler, controls_area_slot)

    @check_started
    def keyPressEvent(self, event):
        # type: (QKeyEvent) -> None:
        self.keydown.emit(int(event.key()))

    @check_started
    def keyReleaseEvent(self, event):
        # type: (QKeyEvent) -> None
        self.keyup.emit(int(event.key()))

    @check_started
    def mouseReleaseEvent(self, event):
        # type: (QMouseEvent) -> None
        self.mouseclick.emit(event.pos().toTuple())

    @check_started
    def mouseMoveEvent(self, event):
        # type: (QMouseEvent) -> None
        self.mousedrag.emit(event.pos().toTuple())


class DrawingAreaContainer(QWidget):
    """Draws a border around the actual drawing area"""

    def __init__(self, parent, width, height):
        # type: (QWidget, int, int) -> None
        """Initialise a canvas and border with set width and height and calculated border width"""
        super().__init__(parent)
        # Set up colouring - default is a grey border around a black background
        self.setAutoFillBackground(True)
        palette = self.palette()
        self.__background_colour = get_colour('black')
        palette.setColor(QPalette.Dark, get_colour('darkgrey'))
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

        self.setFocusProxy(self.__drawing_area)

    @property
    def canvas(self):
        return self.__drawing_area

    def set_background_colour(self, colour):
        # type: (str) -> None
        """Change the canvas background"""
        colour = get_colour(colour)
        if colour == self.__background_colour:
            return

        self.__background_colour = colour
        self.__drawing_area.set_background_colour(colour)
        border = QPalette.Dark if colour is get_colour('black') else QPalette.Shadow
        self.setBackgroundRole(border)


class Canvas:
    """Wrapper for the drawing area. Implements the codeskulptor canvas API."""

    def __init__(self, drawing_area):
        # type: (DrawingArea) -> None
        """Initialise the wrapper"""
        self.__drawing_area = drawing_area

    def __ensure_int_coords(self, *coords):
        """Cast point/rect coords to int

        To ensure Py2 compatibility with scripts that have problems with floor division -> true division on Py3"""
        res = []
        for coord in coords:
            new_coord = (int(coord[0]), int(coord[1]))
            res.append(new_coord)
        return res[0] if len(res) == 1 else res

    def __ensure_int_values(self, *values):
        """Cast values to int

        To ensure Py2 compatibility with scripts that have problems with floor division -> true division on Py3"""
        res = []
        for val in values:
            res.append(int(val))
        return res[0] if len(res) == 1 else res

    def draw_text(self, text, point, font_size, font_color, font_face='serif'):
        # type: (str, Point, int, str, str) -> None
        """Writes the given text string in the given font size, color, and font face.

        The point is a 2-element tuple or list of screen coordinates representing the lower-left-hand corner of where to
        write the text.  The supported font faces are 'serif' (the default), 'sans-serif', and 'monospace'.
        """
        point = self.__ensure_int_coords(point)
        font_size = self.__ensure_int_values(font_size)
        self.__drawing_area.add_object(ObjectHolder(ObjectTypes.Text, (text, point, font_size, font_color, font_face)))

    def draw_line(self, point1, point2, line_width, line_color):
        # type: (Point, Point, int, str) -> None
        """Draws a line segment between the two points, each of which is a 2-element tuple or list of screen
        coordinates. The line's width is given in pixels and must be positive.
        """
        point1, point2 = self.__ensure_int_coords(point1, point2)
        line_width = self.__ensure_int_values(line_width)
        self.__drawing_area.add_object(ObjectHolder(ObjectTypes.Line, (point1, point2, line_width, line_color)))

    def draw_polyline(self, point_list, line_width, line_color):
        # type: (Iterable[Point], int, str) -> None
        """Draws a sequence of line segments between each adjacent pair of points in the non-empty list.

        It is an error for the list of points to be empty. Each point is a 2-element tuple or list of screen
        coordinates. The line's width is given in pixels and must be positive.
        """
        point_list = self.__ensure_int_coords(point_list)
        line_width = self.__ensure_int_values(line_width)
        self.__drawing_area.add_object(ObjectHolder(ObjectTypes.Polyline, (point_list, line_width, line_color)))

    def draw_polygon(self, point_list, line_width, line_color, fill_color=None):
        # type: (Iterable[Point], int, str, Optional[str]) -> None
        """Draws a sequence of line segments between each adjacent pair of points in the non-empty list, plus a line
        segment between the first and last points.

        It is an error for the list of points to be empty. Each point is a 2-element tuple or list of screen
        coordinates. The line's width is given in pixels, and must be positive. The fill color defaults to None. If the
        fill color is specified, then the interior of the polygon is colored.
        """
        point_list = self.__ensure_int_coords(point_list)
        line_width = self.__ensure_int_values(line_width)
        self.__drawing_area.add_object(ObjectHolder(ObjectTypes.Polygon,
                                                    (point_list, line_width, line_color, fill_color)))

    def draw_circle(self, center_point, radius, line_width, line_color, fill_color=None):
        # type: (Point, int, int, str, Optional[str]) -> None
        """Draws a circle at the given center point having the given radius.

        The point is a 2-element tuple or list of screen coordinates. The line's width is given in pixels and must be
        positive. The fill color defaults to None. If the fill color is specified, then the interior of the circle is
        colored.
        """
        center_point = self.__ensure_int_coords(center_point)
        radius, line_width = self.__ensure_int_values(radius, line_width)
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
        center_point = self.__ensure_int_coords(center_point)
        radius, line_width = self.__ensure_int_values(radius, line_width)
        self.__drawing_area.add_object(ObjectHolder(ObjectTypes.Arc,
                                                   (center_point, radius, start_angle, end_angle,
                                                    line_width, line_color, fill_color)))

    def draw_point(self, point, color):
        # type: (Point, str) -> None
        """Draws a 1×1 rectangle at the given point in the given color. The point is a 2-element tuple or list of screen
        coordinates."""
        point = self.__ensure_int_coords(point)
        self.__drawing_area.add_object(ObjectHolder(ObjectTypes.Point, (point, color)))

    def draw_image(self, image, center_source, width_height_source, center_dest, width_height_dest, rotation=0.0):
        # type: (Image, Point, Size, Point, Size, float) -> None
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
        # First check image is loaded - if not, stop here, to prevent caching of blank images
        if not image.get_height() or not image.get_width():
            return

        center_source, width_height_source, center_dest, width_height_dest = self.__ensure_int_coords(
            center_source, width_height_source, center_dest, width_height_dest
        )
        self.__drawing_area.add_object(ObjectHolder(ObjectTypes.Image,
                                                    (image, center_source, width_height_source,
                                                     center_dest, width_height_dest, rotation)))




