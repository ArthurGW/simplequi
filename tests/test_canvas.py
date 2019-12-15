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

import math
import unittest
from unittest.mock import call, Mock, patch

from PySide2.QtCore import QPoint, Qt
from PySide2.QtGui import QPolygon, QFont, QTransform, QPalette, QMouseEvent, QKeyEvent
from PySide2.QtWidgets import QWidget, QApplication

import simplequi
from simplequi._canvas import Canvas, DrawingAreaContainer
from simplequi._colours import get_colour
from simplequi._fonts import FontManager


class TestCanvas(unittest.TestCase):
    """Test Canvas API"""

    def setUp(self):
        self.parent = QWidget()
        self.drawing_area = DrawingAreaContainer(self.parent, 150, 150)
        self.call_count = 0
        self.polygon_list = [(0, 10), (10, 10), (10, 0), (0, 0,)]
        self.polygon = QPolygon()
        for pt in self.polygon_list:
            self.polygon.push_back(QPoint(*pt))
        self.polyline_list = [(0., 10.7), (10.9, 10.5), (5, 5)]
        rounded_list = [(0, 10), (10, 10), (5, 5)]
        self.polyline = QPolygon()
        for pt in rounded_list:
            self.polyline.push_back(QPoint(*pt))
        self.image = Mock()
        self.image.get_height.return_value = 1200
        self.image.get_width.return_value = 1000

    def draw_handler(self, _canvas):
        # type: (Canvas) -> None
        self.call_count += 1

    def test_draw_loop(self):
        """Run the draw loop for one second and check FPS"""
        self.drawing_area.canvas.set_draw_handler(self.draw_handler)
        self.drawing_area.canvas.start()
        simplequi.create_timer(1000, QApplication.instance().exit).start()
        QApplication.instance().exec_()
        self.assertAlmostEqual(60, self.call_count, delta=5)

    def draw_handler2(self, canvas):
        # type: (Canvas) -> None
        canvas.draw_point((10, 10), 'rgba(0, 10, 0, 0.5)')
        canvas.draw_polygon(self.polygon_list, 2, 'blue', 'green')
        canvas.draw_polyline(self.polyline_list, 4.6, 'rgb(10%, 50%, 12%')
        canvas.draw_arc([105, 94.2], 20, math.pi, 3 * math.pi / 2, 15., 'hsl(360, 100, 100)', 'aqua')
        canvas.draw_arc([105, 94.2], 20, math.pi, 3 * math.pi / 2, 15., 'black')
        canvas.draw_circle([25, 25], 25, 25, 'darkviolet')
        canvas.draw_line([0, 0], (150, 150), 50, 'hsla(180, 50, 0, 0.5')
        canvas.draw_text('TEXT', (10, 10), 18, 'YELLOW', 'monospace')
        canvas.draw_image(self.image, [500, 600], [1000, 1200], [75, 75], [150, 150], math.pi / 2)

    def test_drawing_calls(self):
        """Test all the drawing calls"""
        with patch('simplequi._canvas.QPainter') as painter:
            with patch('simplequi._canvas.QBrush') as brush:
                with patch('simplequi._canvas.QPen') as pen:
                    with patch('simplequi._canvas.get_pixmap') as get_pixmap:
                        self.drawing_area.canvas.set_draw_handler(self.draw_handler2)
                        self.drawing_area.canvas.start()
                        self.drawing_area.canvas._DrawingArea__draw()

        actual_brush = brush.return_value
        actual_painter = painter.return_value

        painter.assert_called_once_with(self.drawing_area.canvas._DrawingArea__pixmap)
        pen_calls = [
            call(actual_brush, 1),
            call(actual_brush, 2),
            call(actual_brush, 4),
            call(actual_brush, 15),
            call(actual_brush, 15),
            call(actual_brush, 25),
            call(actual_brush, 50),
            call(actual_brush, 1),
        ]
        pen.assert_has_calls(pen_calls)
        self.assertEqual(len(pen_calls), actual_painter.setPen.call_count)

        brush_calls = [
            call(get_colour('rgba(0, 10, 0, 0.5)')),
            call(get_colour('blue')),
            call(get_colour('green')),
            call(get_colour('rgb(10%, 50%, 12%')),
            call(get_colour('hsl(360, 100, 100)')),
            call(get_colour('aqua')),
            call(get_colour('black')),
            call(get_colour('darkviolet')),
            call(get_colour('hsla(180, 50, 0, 0.5')),
            call(get_colour('YELLOW'))
        ]
        brush.assert_has_calls(brush_calls)
        self.assertEqual(len(brush_calls) - len(pen_calls), actual_painter.setBrush.call_count)

        actual_painter.drawPoint.assert_called_once_with(10, 10)
        actual_painter.drawPolygon.assert_called_once_with(self.polygon)
        actual_painter.drawPolyline.assert_called_once_with(self.polyline)
        actual_painter.drawPie.assert_called_once_with(85, 74, 40, 40, 180 * 16, -90 * 16)
        actual_painter.drawArc.assert_called_once_with(85, 74, 40, 40, 180 * 16, -90 * 16)
        actual_painter.drawEllipse.assert_called_once_with(0, 0, 50, 50)
        actual_painter.drawLine.assert_called_once_with(0, 0, 150, 150)

        font = QFont()
        font.setPixelSize(18)
        font.setFamily(FontManager.monospace)
        actual_painter.setFont.assert_called_once_with(font)
        actual_painter.drawText.assert_called_once_with(10, 10, 'TEXT')

        transform = QTransform().translate(75, 75).rotateRadians(math.pi / 2)
        get_pixmap.assert_called_once_with(self.image, (500, 600), (1000, 1200), (150, 150))
        actual_painter.setTransform.assert_called_once_with(transform)
        actual_painter.drawPixmap.assert_called_once_with(-75, -75, get_pixmap.return_value)

    def test_background_colour(self):
        """Test setting the canvas colour through the container"""
        self.drawing_area.set_background_colour('aquamarine')
        self.assertEqual(self.drawing_area.backgroundRole(), QPalette.Shadow)
        self.assertEqual(self.drawing_area.canvas.palette().color(QPalette.Base), get_colour('aquamarine'))
        self.assertEqual(self.drawing_area.canvas._DrawingArea__background_colour, get_colour('aquamarine'))

    def test_events(self):
        handled_calls = Mock()
        control_calls = Mock()
        canvas = self.drawing_area.canvas
        canvas.set_mousedrag_handler(handled_calls, control_calls)
        canvas.set_mouseclick_handler(handled_calls, control_calls)
        canvas.set_keydown_handler(handled_calls, control_calls)
        canvas.set_keyup_handler(handled_calls, control_calls)

        key_press = QKeyEvent(QKeyEvent.KeyPress, Qt.Key_Left, Qt.NoModifier)
        key_release = QKeyEvent(QKeyEvent.KeyRelease, Qt.Key_Left, Qt.NoModifier)
        mouse_release = QMouseEvent(QMouseEvent.MouseButtonRelease, QPoint(75, 75),
                                    Qt.MiddleButton, Qt.NoButton, Qt.NoModifier)
        mouse_move = QMouseEvent(QMouseEvent.MouseMove, QPoint(100, 75),
                                    Qt.MiddleButton, Qt.NoButton, Qt.NoModifier)

        # Call handlers when canvas has not started
        canvas.keyPressEvent(key_press)
        canvas.keyReleaseEvent(key_release)
        canvas.mouseReleaseEvent(mouse_release)
        canvas.mouseMoveEvent(mouse_move)
        handled_calls.assert_not_called()
        control_calls.assert_not_called()

        # Start and call again
        canvas.start()
        canvas.keyPressEvent(key_press)
        canvas.keyReleaseEvent(key_release)
        canvas.mouseReleaseEvent(mouse_release)
        canvas.mouseMoveEvent(mouse_move)
        calls = [
            call(int(Qt.Key_Left)),
            call(int(Qt.Key_Left)),
            call((75, 75)),
            call((100, 75)),
        ]
        handled_calls.assert_has_calls(calls)
        control_calls.assert_has_calls(calls)


if __name__ == '__main__':
    unittest.main()
