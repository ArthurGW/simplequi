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
from unittest.mock import Mock

from PySide2.QtCore import Qt
from PySide2.QtGui import QKeyEvent
from PySide2.QtWidgets import QLabel, QPushButton

from simplequi._widgets import Control, EventWidget, PlainTextSingleLine, TextInputWidget


class TestWidgets(unittest.TestCase):
    """Test widgets not covered by other tests"""

    def test_control(self):
        """Test text get and set"""
        widget = QLabel('label_text')
        control = Control(widget)
        self.assertEqual(control.get_text(), 'label_text')
        control.set_text('new')
        self.assertEqual(control.get_text(), 'new')
        widget = QPushButton('button')
        control = Control(widget)
        self.assertEqual(control.get_text(), 'button')
        control.set_text('new')
        self.assertEqual(control.get_text(), 'new')

    def test_event_widget(self):
        """Test default size and setting text"""
        widget = EventWidget('Data:')
        self.assertEqual(widget.width(), 200)
        self.assertEqual(widget.height(), 17)
        self.assertEqual(widget.text(), 'Data:')
        widget.set_text('text')
        self.assertEqual(widget.text(), 'Data:text')

    def test_plain_text(self):
        """Test event handling"""
        widget = PlainTextSingleLine(None)
        self.assertTrue(widget.tabChangesFocus())

        handler = Mock()
        widget.enter_pressed.connect(handler)
        event = QKeyEvent(QKeyEvent.KeyPress, Qt.Key_Enter, Qt.NoModifier)
        widget.setPlainText('text')
        widget.keyPressEvent(event)
        handler.assert_not_called()
        self.assertTrue(event.isAccepted())

        event = QKeyEvent(QKeyEvent.KeyRelease, Qt.Key_Enter, Qt.NoModifier)
        widget.keyReleaseEvent(event)
        handler.assert_called_once_with('text')
        self.assertTrue(event.isAccepted())

    def test_text_input_widget(self):
        """Test widget layout and text get and set"""
        widget = TextInputWidget('input:', None, 234)
        control = Control(widget)
        label, field, layout = widget.children()
        self.assertEqual(widget.layout(), layout)
        self.assertEqual(widget.focusProxy(), field)
        self.assertEqual(label.width(), 234)
        self.assertEqual(field.width(), 234)
        self.assertEqual(field.height(), 25)
        self.assertEqual(label.text(), 'input:')
        self.assertEqual(field.toPlainText(), '')
        self.assertEqual(widget.text(), '')
        self.assertEqual(control.get_text(), '')

        control.set_text('new_text')
        self.assertEqual(field.toPlainText(), 'new_text')
        self.assertEqual(widget.text(), 'new_text')
        self.assertEqual(control.get_text(), 'new_text')


if __name__ == '__main__':
    unittest.main()
