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
from typing import Callable, Iterable, Optional, Tuple
from typing import SupportsInt
from typing import Union

from PySide2.QtCore import QTimerEvent
from PySide2.QtCore import Qt, QPoint, Signal
from PySide2.QtGui import (QBrush, QColor, QKeyEvent, QMouseEvent, QPainter, QPaintEvent,
                           QPalette, QPen, QPixmap, QPolygon, QTransform)
from PySide2.QtWidgets import QHBoxLayout, QWidget

from ._colours import get_colour
from ._constants import NO_MARGINS, Point, Size
from ._fonts import get_font, FontSpec
from ._image import Image, get_pixmap

ObjectHolder = namedtuple('ObjectHolder', ['obj_type', 'args'])


def radians_to_qpainter_angle(rads):
    # type: (float) -> int
    """Converts an angle in radians to one in 1/16ths of degrees as used by QPainter.

    :param rads: angle to covert in radians
    :return: an angle in 1/16:sup:`ths` of a degree
    """
    return int(360 * 16 * rads / (2 * pi))


def point_list_to_polygon(point_list):
    # type: (Iterable[Point]) -> QPolygon
    """Converts an iterable of (x, y) points coordinates to a QPolygon suitable for rendering.

    :param point_list: ordered iterable of points that make up the polygon
    :return: a polygon with the given points
    """
    num_points = len(point_list)
    polygon = QPolygon(num_points)
    for point in point_list:
        polygon.push_back(QPoint(*point))
    return polygon


def set_painter_line_width_and_colour(painter, line_width, line_colour):
    # type: (QPainter, int, str) -> None
    """Sets up QPainter for drawing lines.

    :param painter: the painter to be modified
    :param line_width: the new line width to set
    :param line_colour: the new line colour to set
    """
    pen = QPen(QBrush(get_colour(line_colour)), line_width)
    painter.setPen(pen)


def set_painter_fill_colour(painter, fill_colour):
    # type: (QPainter, str) -> None
    """Sets fill colour for drawing solid shapes.

    :param painter: the painter to be modified
    :param fill_colour: the new fill colour to set
    """
    painter.setBrush(QBrush(get_colour(fill_colour)))


def set_painter_lines_and_fill(painter, line_width, line_colour, fill_colour=None):
    # type: (QPainter, int, str, Optional[str]) -> None
    """Fully sets up painter for drawing.

    :param painter: the painter to be modified
    :param line_width: the new line width to set
    :param line_colour: the new line colour to set
    :param fill_colour: the new fill colour to set
    """
    set_painter_line_width_and_colour(painter, line_width, line_colour)
    if fill_colour is not None:
        set_painter_fill_colour(painter, fill_colour)


def render_line(painter, start, end, line_width, line_colour):
    # type: (QPainter, Point, Point, int, str) -> None
    """Renders a line on the canvas.

    :param painter: the painter to draw with (which knows the canvas to draw on)
    :param start: the coordinate of the start point of the line
    :param end: the coordinate of the end point of the line
    :param line_width: the width of the line to draw
    :param line_colour: the colour of the line to draw
    """
    set_painter_line_width_and_colour(painter, line_width, line_colour)
    painter.drawLine(*start, *end)


def get_circle_rect(center_point, radius):
    # type: (Point, int) -> Tuple[int, int, int, int]
    """Returns the rectangle containing a circle with given centre and radius.

    :param center_point: the center of the circle
    :param radius: the radius of the circle
    :return: tuple containing (`top_left_x`, `top_left_y`, `width`, `height`) of the rectangle.
    """
    center_x, center_y = center_point
    return center_x - radius, center_y - radius, radius * 2, radius * 2


def render_arc(painter, center_point, radius, start_angle, end_angle, line_width, line_colour, fill_colour=None):
    # type: (QPainter, Point, int, int, int, int, str, Optional[str]) -> None
    """Renders an arc (filled or not) on the canvas.

    Angles are given in radians, with 0.0 at the 3 o'clock position, and values increasing clockwise.

    :param painter: the painter to draw with (which knows the canvas to draw on)
    :param center_point: the center of the arc
    :param radius: the radius of the arc
    :param start_angle: the start angle of the arc
    :param end_angle: the end angle of the arc
    :param line_width: the line width to draw with
    :param line_colour: the line colour to draw with
    :param fill_colour: the colour to fill the arc with (optional, defaults to transparent)
    """
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
    """Renders a circle (filled or not) on the canvas.

    :param painter: the painter to draw with (which knows the canvas to draw on)
    :param center_point: the center of the circle
    :param radius: the radius of the circle
    :param line_width: the line width to draw with
    :param line_colour: the line colour to draw with
    :param fill_colour: the colour to fill the circle with, optional, defaults to transparent
    """
    rect = get_circle_rect(center_point, radius)
    set_painter_lines_and_fill(painter, line_width, line_colour, fill_colour)
    painter.drawEllipse(*rect)


def render_point(painter, point, colour):
    # type: (QPainter, Point, str) -> None
    """Renders a point on the canvas.

    :param painter: the painter to draw with (which knows the canvas to draw on)
    :param point: the coordinates of the point
    :param colour: the colour to draw the point
    """
    set_painter_line_width_and_colour(painter, 1, colour)
    painter.drawPoint(*point)


def render_polyline(painter, point_list, line_width, line_colour):
    # type: (QPainter, Iterable[Point], int, str) -> None
    """Renders a polyline on the canvas.

    :param painter: the painter to draw with (which knows the canvas to draw on)
    :param point_list: the coordinates of the line's segment start/finish points, in order
    :param line_width: the line width to draw with
    :param line_colour: the line colour to draw with
    """
    set_painter_line_width_and_colour(painter, line_width, line_colour)
    polygon = point_list_to_polygon(point_list)
    painter.drawPolyline(polygon)


def render_polygon(painter, point_list, line_width, line_colour, fill_colour=None):
    # type: (QPainter, Iterable[Point], int, str, Optional[str]) -> None
    """Renders an optionally-filled polygon on the canvas.

    :param painter: the painter to draw with (which knows the canvas to draw on)
    :param point_list: the coordinates of the polygon's vertices (the final point is always joined to the first point)
    :param line_width: the line width to draw with
    :param line_colour: the line colour to draw with
    :param fill_colour: the colour to fill the polygon with, optional, defaults to transparent
    """
    set_painter_lines_and_fill(painter, line_width, line_colour, fill_colour)
    polygon = point_list_to_polygon(point_list)
    painter.drawPolygon(polygon)


def render_text(painter, text, point, font_size, font_colour, font_face='serif'):
    # type: (QPainter, str, Point, int, str, str) -> None
    """Renders text on the canvas, positioned with its bottom-left corner at the given point.

    :param painter: the painter to draw with (which knows the canvas to draw on)
    :param text: the text to draw
    :param point: the point to draw at
    :param font_size: the font size of the text
    :param font_colour: the colour of the text
    :param font_face: the font face of the text (one of `serif`, `sans-serif` or `monospace`)
    """
    set_painter_line_width_and_colour(painter, 1, font_colour)
    font = get_font(FontSpec(font_size, font_face))
    painter.setFont(font)
    painter.drawText(*point, text)


def render_image(painter, image, source_centre, source_window, canvas_center, canvas_size, rotation=0.0):
    # type: (QPainter, Image, Point, Size, Point, Size, float) -> None
    """Renders an image or portion of it on the canvas with optional rotation and scaling.

    :param painter: the painter to draw with (which knows the canvas to draw on)
    :param image: the :class:`~simplequi._image.Image` to render
    :param source_centre: the center point of the portion of the original image to render
    :param source_window: the width and height of the portion of the original image to render
    :param canvas_center: the location to render the image on the canvas
    :param canvas_size: the size to render the image on the canvas
    :param rotation: amount in radians to rotate the image by, with 0.0 at the 3 o'clock position, increasing clockwise
    """
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
    """Used to tell the canvas which renderer to use for an object"""

    Text = 0
    Line = 1
    Polyline = 2
    Polygon = 3
    Circle = 4
    Arc = 5
    Point = 6
    Image = 7


#: Converts an object type to render to the appropriate rendering function.
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
    """Decorator that only runs enclosed the method if the object has 'started'.

    Checks whether the attribute ``started`` on the ``self`` object is `True`, then runs the method.

    :param func: function to decorate
    :return: wrapped ``func``
    """

    @wraps(func)
    def inner(inner_self, *args, **kwargs):
        if not inner_self.started:
            return
        return func(inner_self, *args, **kwargs)

    return inner


class DrawingArea(QWidget):
    """The widget that actually renders the desired canvas and handles events on it.

    :param parent: the parent QWidget of this object
    :param width: how wide to make the canvas, in pixels
    :param height: how high to make the canvas, in pixels
    """

    # Signals emitted when events handled
    mouseclick = Signal(tuple)  #: emitted when canvas is clicked, with coordinates of click
    mousedrag = Signal(tuple)  #: emitted when canvas is clicked and dragged, with coordinates of current drag end
    keydown = Signal(int)  #: emitted when canvas has focus and key is pressed, with int key value
    keyup = Signal(int)  #: emitted when canvas has focus and key is released, with int key value

    def __init__(self, parent, width, height):
        # type: (QWidget, int, int) -> None
        """Initialises a canvas with set width and height."""
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
        self.__draw_timer_id = None

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
        """Sets the draw handler and begins the rendering loop.

        :param draw_handler: function to call every 1/60:sup:`th` of a second (actually 17ms), which gets a
            :class:`Canvas` object as an argument
        """
        if self.__draw_handler is not None and self.__draw_timer_id is not None:
            self.killTimer(self.__draw_timer_id)

        self.__draw_handler = draw_handler
        if self.__started:
            self.__draw_timer_id = self.startTimer(17)  # Roughly 60FPS

    def timerEvent(self, event):
        # type: (QTimerEvent) -> None
        """Draws if the event comes from the draw timer, otherwise ignores it.

        :param event: timer event to process
        """
        if event.timerId() != self.__draw_timer_id:
            return super().timerEvent(event)
        self.__draw()

    def __reset_pixmap(self):
        """Sets new pixmap filled with the current background colour."""
        self.__pixmap = QPixmap(self.__canvas_width, self.__canvas_height)
        self.__pixmap.fill(self.__background_colour)

    @check_started
    def __draw(self):
        """Calls the draw handler and re-renders the canvas if necessary"""
        if self.__draw_handler is None:
            return

        self.__new_objects = []
        self.__draw_handler(self.__canvas)

        if self.__new_objects != self.__objects:
            self.__objects = self.__new_objects
            self.__render()

    def __render(self):
        """Actually renders the canvas"""
        self.__reset_pixmap()
        painter = QPainter(self.__pixmap)
        painter.setRenderHint(
            QPainter.RenderHint(QPainter.Antialiasing | QPainter.TextAntialiasing | QPainter.SmoothPixmapTransform))
        for obj in self.__objects:
            painter.save()
            OBJECT_RENDERERS[obj.obj_type](painter, *obj.args)
            painter.restore()
        self.update()

    def add_object(self, primitive):
        # type: (ObjectHolder) -> None
        """Adds a primitive to the draw queue.

        :param primitive: primitive described by an object holder specifying the object type and arguments
        """
        self.__new_objects.append(primitive)

    def set_background_colour(self, colour):
        # type: (QColor) -> None
        """Changes the canvas background.

        :param colour: the new background colour to use
        """
        self.__palette.setColor(QPalette.Base, colour)
        self.setPalette(self.__palette)
        self.__background_colour = colour
        self.__render()

    @check_started
    def paintEvent(self, _event):
        # type: (QPaintEvent) -> None
        """Draws cached pixmap on the canvas - :meth:`__render` takes care of creating it in the first place

        :param _event: the paint event passed in by Qt, not actually used
        """
        painter = QPainter(self)
        painter.drawPixmap(self.rect(), self.__pixmap)

    # Events
    def start(self):
        """Commences event handling and drawing"""
        self.__started = True

        # Start the draw timer if a handler exists
        if self.__draw_handler is not None:
            self.set_draw_handler(self.__draw_handler)

    @property
    def started(self):
        """Whether the frame has started drawing an event handling"""
        return self.__started

    @staticmethod
    def __connect_handlers(signal, *handlers):
        # type: (Signal, Iterable[Callable]) -> None
        """Hooks up signal to handlers.

        :param signal: the signal to connect to
        :param handlers: the functions to connect to `signal`, which should have the same argument types as the signal
        """
        try:
            signal.disconnect()
        except RuntimeError:
            # No connections
            pass
        for handler in handlers:
            signal.connect(handler)

    def set_keydown_handler(self, key_handler, controls_area_slot):
        # type: (Callable[[int], None], Callable[[int], None]) -> None
        """Adds a keyboard event handler waiting for a keydown event.

        :param key_handler: the function to call on keydown
        :param controls_area_slot: the slot to display the key pressed in the controls area
        """
        self.__connect_handlers(self.keydown, key_handler, controls_area_slot)
        self.__keydown_handler = key_handler

    def set_keyup_handler(self, key_handler, controls_area_slot):
        # type: (Callable[[int], None], Callable[[int], None]) -> None
        """Adds a keyboard event handler waiting for a keyup event.

        :param key_handler: the function to call on keyup
        :param controls_area_slot: the slot to display the key released in the controls area
        """
        self.__connect_handlers(self.keyup, key_handler, controls_area_slot)
        self.__keyup_handler = key_handler

    def set_mouseclick_handler(self, mouse_handler, controls_area_slot):
        # type: (Callable[[tuple], None], Callable[[Tuple[int, int]], None]) -> None
        """Adds a mouse event handler waiting for a mouseclick event.

        :param mouse_handler: the function to call on mouseclick
        :param controls_area_slot: the slot to display the click location in the controls area
        """
        self.__connect_handlers(self.mouseclick, mouse_handler, controls_area_slot)
        self.__mouseclick_handler = mouse_handler

    def set_mousedrag_handler(self, mouse_handler, controls_area_slot):
        # type: (Callable[[Tuple[int, int]], None], Callable[[Tuple[int, int]], None]) -> None
        """Adds a mouse event handler waiting for a mousedrag event.

        :param mouse_handler: the function to call on mousedrag
        :param controls_area_slot: the slot to display the drag location in the controls area
        """
        self.__connect_handlers(self.mousedrag, mouse_handler, controls_area_slot)
        self.__mousedrag_handler = mouse_handler

    @check_started
    def keyPressEvent(self, event):
        # type: (QKeyEvent) -> None
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
    """Creates and draws a border around the actual drawing area/canvas.

    :param parent: the parent QWidget of this object
    :param width: how wide to make the canvas, in pixels
    :param height: how high to make the canvas, in pixels
    """

    def __init__(self, parent, width, height):
        # type: (QWidget, int, int) -> None
        """Initialises a canvas and border with set width and height and calculated border width"""
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
        """The actual drawing area"""
        return self.__drawing_area

    def set_background_colour(self, colour):
        # type: (str) -> None
        """Changes the canvas background colour and triggers redraw of the canvas if required.

        Also calculates the border colour to draw. By default, the border uses the built-in colour defined for the
        ``QPalette.Shadow`` role (which is usually black), unless the requested background colour is black, in which
        case it uses ``QPalette.Dark``.

        :param colour: the new background colour to set
        """
        colour = get_colour(colour)
        if colour == self.__background_colour:
            return

        self.__background_colour = colour
        self.__drawing_area.set_background_colour(colour)
        border = QPalette.Dark if colour is get_colour('black') else QPalette.Shadow
        self.setBackgroundRole(border)


class Canvas:
    """Wrapper for the drawing area, implementing the codeskulptor canvas API.

    This class is passed to the ``draw_handler`` set by :meth:`~simplequi._frame.Frame.set_draw_handler` to allow calls
    to draw on the canvas to be made in draw events.  These events occur roughly 60 times per second. Note that users
    should not create instances of this class, creation is handled internally.

    :param drawing_area: the actual widget that will be drawn on
    """

    def __init__(self, drawing_area):
        # type: (DrawingArea) -> None
        """Initialises the wrapper"""
        self.__drawing_area = drawing_area

    @staticmethod
    def __ensure_int_coordinates(*coordinates):
        # type: (Union[Iterable[Point], Point]) -> Union[Iterable[Point], Point]
        """Casts point/rectangle coordinates to int.

        This is to ensure Py2 compatibility with scripts that have problems with floor division -> true division on Py3.
        If a single point is passed, returns a single point.  If more than one is passed, returns a list of points.

        :param coordinates: arbitrary number of coordinate pairs (x, y)
        :return: single point or list of points, depending on number of ``coordinates`` passed
        """
        res = []
        for coord in coordinates:
            new_coord = (int(coord[0]), int(coord[1]))
            res.append(new_coord)
        return res[0] if len(res) == 1 else res

    @staticmethod
    def __ensure_int_values(*values):
        # type: (Union[Iterable[SupportsInt], SupportsInt]) -> (Union[Iterable[SupportsInt], SupportsInt])
        """Casts values to int.

        This is to ensure Py2 compatibility with scripts that have problems with floor division -> true division on Py3.
        If a single value is passed, returns a single value.  If more than one is passed, returns a list of values.

        :param values: arbitrary number of values that can be cast to int
        :return: single value or list of values, depending on number of ``values`` passed
        """
        res = []
        for val in values:
            res.append(int(val))
        return res[0] if len(res) == 1 else res

    def draw_text(self, text, point, font_size, font_color, font_face='serif'):
        # type: (str, Point, int, str, str) -> None
        """Writes the given text string in the given font size, color, and font face.

        The point is a 2-element tuple or list of screen coordinates representing the lower-left-hand corner of where to
        write the text.  The supported font faces are 'serif' (the default), 'sans-serif', and 'monospace'.

        :param text: the text to draw
        :param point: the point to draw at
        :param font_size: the font size of the text
        :param font_color: the colour of the text
        :param font_face: the font face of the text (one of `serif`, `sans-serif` or `monospace`)
        """
        point = self.__ensure_int_coordinates(point)
        font_size = self.__ensure_int_values(font_size)
        self.__drawing_area.add_object(ObjectHolder(ObjectTypes.Text, (text, point, font_size, font_color, font_face)))

    def draw_line(self, point1, point2, line_width, line_color):
        # type: (Point, Point, int, str) -> None
        """Draws a line segment between the two points, each of which is a 2-element tuple or list of screen
        coordinates. The line's width is given in pixels and must be positive.

        :param point1: the coordinate of the start point of the line
        :param point2: the coordinate of the end point of the line
        :param line_width: the width of the line to draw
        :param line_color: the colour of the line to draw
        """
        point1, point2 = self.__ensure_int_coordinates(point1, point2)
        line_width = self.__ensure_int_values(line_width)
        self.__drawing_area.add_object(ObjectHolder(ObjectTypes.Line, (point1, point2, line_width, line_color)))

    def draw_polyline(self, point_list, line_width, line_color):
        # type: (Iterable[Point], int, str) -> None
        """Draws a sequence of line segments between each adjacent pair of points in the non-empty list.

        It is an error for the list of points to be empty. Each point is a 2-element tuple or list of screen
        coordinates. The line's width is given in pixels and must be positive.

        :param point_list: the coordinates of the line's segment start/finish points, in order
        :param line_width: the line width to draw with
        :param line_color: the line colour to draw with
        """
        point_list = self.__ensure_int_coordinates(*point_list)
        line_width = self.__ensure_int_values(line_width)
        self.__drawing_area.add_object(ObjectHolder(ObjectTypes.Polyline, (point_list, line_width, line_color)))

    def draw_polygon(self, point_list, line_width, line_color, fill_color=None):
        # type: (Iterable[Point], int, str, Optional[str]) -> None
        """Draws a sequence of line segments between each adjacent pair of points in the non-empty list, plus a line
        segment between the first and last points.

        It is an error for the list of points to be empty. Each point is a 2-element tuple or list of screen
        coordinates. The line's width is given in pixels, and must be positive. The fill color defaults to None. If the
        fill color is specified, then the interior of the polygon is colored.

        :param point_list: the coordinates of the polygon's vertices (the final point is always joined to the first)
        :param line_width: the line width to draw with
        :param line_color: the line colour to draw with
        :param fill_color: the colour to fill the polygon with, optional, defaults to transparent
        """
        point_list = self.__ensure_int_coordinates(*point_list)
        line_width = self.__ensure_int_values(line_width)
        self.__drawing_area.add_object(ObjectHolder(ObjectTypes.Polygon,
                                                    (point_list, line_width, line_color, fill_color)))

    def draw_circle(self, center_point, radius, line_width, line_color, fill_color=None):
        # type: (Point, int, int, str, Optional[str]) -> None
        """Draws a circle at the given center point having the given radius.

        The point is a 2-element tuple or list of screen coordinates. The line's width is given in pixels and must be
        positive. The fill color defaults to None. If the fill color is specified, then the interior of the circle is
        colored.

        :param center_point: the center of the circle
        :param radius: the radius of the circle
        :param line_width: the line width to draw with
        :param line_color: the line colour to draw with
        :param fill_color: the colour to fill the circle with, optional, defaults to transparent
        """
        center_point = self.__ensure_int_coordinates(center_point)
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

        :param center_point: the center of the arc
        :param radius: the radius of the arc
        :param start_angle: the start angle of the arc
        :param end_angle: the end angle of the arc
        :param line_width: the line width to draw with
        :param line_color: the line colour to draw with
        :param fill_color: the colour to fill the arc with (optional, defaults to transparent)
        """
        center_point = self.__ensure_int_coordinates(center_point)
        radius, line_width = self.__ensure_int_values(radius, line_width)
        self.__drawing_area.add_object(ObjectHolder(ObjectTypes.Arc,
                                                    (center_point, radius, start_angle, end_angle,
                                                     line_width, line_color, fill_color)))

    def draw_point(self, point, color):
        # type: (Point, str) -> None
        """Draws a 1×1 rectangle at the given point in the given color. The point is a 2-element tuple or list of screen
        coordinates.

        :param point: the coordinates of the point
        :param color: the colour to draw the point
        """
        point = self.__ensure_int_coordinates(point)
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

        :param image: the :class:`~simplequi._image.Image` to render
        :param center_source: the center point of the portion of the original image to render
        :param width_height_source: the width and height of the portion of the original image to render
        :param center_dest: the location to render the image on the canvas
        :param width_height_dest: the size to render the image on the canvas
        :param rotation: amount in radians to rotate the image, with 0.0 at the 3 o'clock position, increasing clockwise
        """
        # First check image is loaded - if not, stop here, to prevent caching of blank images
        if not image.get_height() or not image.get_width():
            return

        center_source, width_height_source, center_dest, width_height_dest = self.__ensure_int_coordinates(
            center_source, width_height_source, center_dest, width_height_dest
        )
        self.__drawing_area.add_object(ObjectHolder(ObjectTypes.Image,
                                                    (image, center_source, width_height_source,
                                                     center_dest, width_height_dest, rotation)))
