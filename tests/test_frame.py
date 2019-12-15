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

import unittest
from unittest.mock import patch, Mock, call

from PySide2.QtCore import Qt, QPoint
from PySide2.QtGui import QFont, QFontMetrics, QKeyEvent, QMouseEvent
from PySide2.QtWidgets import QApplication, QLabel

import simplequi
from simplequi._fonts import FontManager


class TestFrame(unittest.TestCase):
    """Test Frame API"""

    def setUp(self):
        self.frame = simplequi.create_frame('FRAME', 100, 100)
        self.main_widget = self.frame._Frame__main_widget
        self.main_widget.hide()

    def test_frame_tracking(self):
        self.assertIn(self.frame, QApplication.instance().tracked)
        self.main_widget.close()
        self.assertNotIn(self.frame, QApplication.instance().tracked)

    def test_background(self):
        with patch('simplequi._canvas.DrawingAreaContainer.set_background_colour') as setter:
            self.frame.set_canvas_background('indigo')
            self.frame.set_canvas_background('green')
            setter.assert_has_calls([call('indigo'), call('green')])

    def test_start(self):
        self.frame.start()
        self.assertTrue(self.main_widget.canvas.started)

    @staticmethod
    def __font_width(size, family, text):
        font = QFont()
        font.setPixelSize(size)
        font.setFamily(family)
        metrics = QFontMetrics(font)
        return metrics.boundingRect(text).width()

    def test_text_width(self):
        self.assertEqual(self.frame.get_canvas_textwidth('TEXT', 12, 'sans-serif'),
                         self.__font_width(12, 'Helvetica', 'TEXT'))
        self.assertEqual(self.frame.get_canvas_textwidth(' _sfklujj', 37, 'monospace'),
                         self.__font_width(37, FontManager.monospace, ' _sfklujj'))

    @property
    def __last_control(self):
        return self.main_widget.controls.children()[-1]

    @staticmethod
    def __control_to_widget(control):
        return control._Control__widget

    def test_add_label(self):
        self.frame.add_label('LABEL')
        label = self.__last_control
        self.assertIsInstance(label, QLabel)
        self.assertEqual(label.text(), 'LABEL')

        label = self.frame.add_label('LABEL2', 123)
        label = self.__control_to_widget(label)
        self.assertIsInstance(label, QLabel)
        self.assertEqual(label.text(), 'LABEL2')
        self.assertEqual(label.width(), 123)

    def test_add_button(self):
        handler = Mock()
        self.frame.add_button('BUTTON', handler)
        button = self.__last_control
        self.assertEqual(button.text(), 'BUTTON')
        button.click()
        handler.assert_called_once_with()

        button = self.frame.add_button('BUTTON2', handler, width=59)
        button = self.__control_to_widget(button)
        self.assertEqual(button.text(), 'BUTTON2')
        self.assertEqual(button.width(), 59)
        button.click()
        self.assertEqual(handler.call_count, 2)

    def test_add_input(self):
        handler = Mock()
        inp = self.frame.add_input('INPUT', handler, 140)
        inp = self.__control_to_widget(inp)
        label, field, _ = inp.children()
        self.assertEqual(label.text(), 'INPUT')
        self.assertEqual(field.toPlainText(), '')
        inp.setText('data')
        self.assertEqual(field.toPlainText(), 'data')
        self.assertEqual(inp.text(), 'data')
        event = QKeyEvent(QKeyEvent.KeyRelease, Qt.Key_Enter, Qt.NoModifier)
        field.keyPressEvent(event)
        handler.assert_not_called()
        field.keyReleaseEvent(event)
        handler.assert_called_once_with('data')

    def test_mouse_and_key_handlers(self):
        handler = Mock()
        control_handler = Mock()

        self.main_widget.controls.on_keydown = control_handler
        self.main_widget.controls.on_keyup = control_handler
        self.main_widget.controls.on_mouseclick = control_handler
        self.main_widget.controls.on_mousedrag = control_handler

        self.frame.set_keyup_handler(handler)
        self.frame.set_keydown_handler(handler)
        self.frame.set_mouseclick_handler(handler)
        self.frame.set_mousedrag_handler(handler)
        self.frame.start()

        key_press = QKeyEvent(QKeyEvent.KeyPress, Qt.Key_L, Qt.NoModifier)
        key_release = QKeyEvent(QKeyEvent.KeyRelease, Qt.Key_L, Qt.NoModifier)
        mouse_release = QMouseEvent(QMouseEvent.MouseButtonRelease, QPoint(75, 75),
                                    Qt.MiddleButton, Qt.NoButton, Qt.NoModifier)
        mouse_move = QMouseEvent(QMouseEvent.MouseMove, QPoint(100, 75),
                                    Qt.MiddleButton, Qt.NoButton, Qt.NoModifier)
        calls = [
            call((75, 75)),
            call((100, 75)),
            call(int(Qt.Key_L)),
            call(int(Qt.Key_L))
        ]

        self.main_widget.canvas.mouseReleaseEvent(mouse_release)
        self.main_widget.canvas.mouseMoveEvent(mouse_move)
        self.main_widget.canvas.keyPressEvent(key_press)
        self.main_widget.canvas.keyReleaseEvent(key_release)

        handler.assert_has_calls(calls)
        control_handler.assert_has_calls(calls)

    def test_set_draw_handler(self):
        handler = Mock()
        self.frame.set_draw_handler(handler)
        self.frame.start()
        self.main_widget.canvas._DrawingArea__draw()
        handler.assert_called_once_with(self.main_widget.canvas._DrawingArea__canvas)

    def tearDown(self):
        try:
            self.main_widget.close()
            self.main_widget = None
        except AttributeError:
            pass


if __name__ == '__main__':
    unittest.main()
