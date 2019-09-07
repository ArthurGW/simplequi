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

from PySide2.QtWidgets import QApplication

from simplequi._colours import get_colour, COLOUR_MAP, DEFAULT_COLOURS


class TestColours(unittest.TestCase):
    """Test cases to exercise the _colours module

    Exercises internal functions but mostly only uses external get_colour api"""

    @classmethod
    def tearDownClass(cls):
        QApplication.instance().lastWindowClosed.emit()

    def assertTupleAlmostEqual(self, t1, t2, msg='', dp=3):
        """Fuzzy comparer for tuples with floating point entries"""

        for ind, vals in enumerate(zip(t1, t2)):
            v1, v2 = vals
            v1 = round(v1, dp)
            v2 = round(v2, dp)
            if v1 != v2:
                # Mismatching entry found: use normal tuple exception for nice error formatting
                self.assertTupleEqual(t1, t2)

    def test_rgb(self):
        """Test valid and invalid rgb strings"""
        data = [
            ('rgb(0, 255, 255)', (0., 1., 1., 1.)),
            ('rgb(20%, 45%, 83.2%)', (0.2, 0.45, 0.832, 1.)),
            ('rgb(25.5, 25.5, 51.00)', (0.1, 0.1, 0.2, 1.)),
        ]

        bad_data = [
            'rgb(, , )',
            'rgb(300, 123.2, 233)',
            'rgb(120%, 99%, 30%)',
        ]

        for inp, out in data:
            self.assertTupleAlmostEqual(get_colour(inp).getRgbF(), out)

        for inp in bad_data:
            self.assertRaises(ValueError, lambda: get_colour(inp))

    def test_rgba(self):
        """Test valid and invalid rgba strings"""
        data = [
            ('rgb(12.25, 255, 255, 0.2)', (0.048, 1., 1., 0.2)),
            ('rgb(5%, 45%, 83.2%, 0.456)', (0.05, 0.45, 0.832, 0.456)),
            ('rgb(25.5, 25.5, 51.00, 0.123)', (0.1, 0.1, 0.2, 0.123)),
        ]

        bad_data = [
            'rgba(, , , )',
            'rgba(300, 123.2, 233, 1.2)',
            'rgba(120%, 99%, 30%, 0.4)',
        ]

        for inp, out in data:
            self.assertTupleAlmostEqual(get_colour(inp).getRgbF(), out)

        for inp in bad_data:
            self.assertRaises(ValueError, lambda: get_colour(inp))

    def test_hsl(self):
        """Test valid and invalid hsl strings"""
        data = [
            ('hsl(360, 5, 15)', (0., 0.05, 0.15, 1.)),
            ('hsl(120, 45%, 83.2%)', (0.333, 0.45, 0.832, 1.)),
            ('hsl(253.1, 25.5, 51.00)', (0.703, 0.255, 0.51, 1.)),
        ]

        bad_data = [
            'hsl(, , )',
            'hsl(300, 123.2, 233)',
            'hsl(454, 99%, 30%)',
        ]

        for inp, out in data:
            self.assertTupleAlmostEqual(get_colour(inp).getHslF(), out)

        for inp in bad_data:
            self.assertRaises(ValueError, lambda: get_colour(inp))

    def test_hsla(self):
        """Test valid and invalid hsla strings"""
        data = [
            ('hsla(180, 51, 15, 0.3)', (0.5, 0.51, 0.15, 0.3)),
            ('hsla(150, 45.2%, 8.97%, 0.7)', (0.417, 0.452, 0.0897, 0.7)),
            ('hsla(253.1, 25.5, 51.00, 1.0)', (0.703, 0.255, 0.51, 1.)),
        ]

        bad_data = [
            'hsla(, 34, 12, )',
            'hsla(400, 123.2, 23, 0.4)',
            'hsla(454, 99%, 30%, 5.4)',
        ]

        for inp, out in data:
            self.assertTupleAlmostEqual(get_colour(inp).getHslF(), out)

        for inp in bad_data:
            self.assertRaises(ValueError, lambda: get_colour(inp))

    def test_hex(self):
        """Test valid and invalid hex strings"""
        data = [
            ('#FFFFFF', (1., 1., 1., 1.)),
            ('#0F4D3F', (0.059, 0.302, 0.247, 1.)),
            ('#3432DD', (0.204, 0.196, 0.867, 1.)),
        ]

        bad_data = [
            '#F2345',
            '#FGFF3D',
            '#1234',
        ]

        for inp, out in data:
            self.assertTupleAlmostEqual(get_colour(inp).getRgbF(), out)

        for inp in bad_data:
            self.assertRaises(ValueError, lambda: get_colour(inp))

    def test_named_colours(self):
        """Test valid and invalid named colours"""
        # First test listed colours were all created
        for colour_name in DEFAULT_COLOURS:
            self.assertIn(colour_name, COLOUR_MAP)

        # Other legal colour names
        data = [
            ('BlanchedAlmond', (1., 0.922, 0.804, 1.)),
            ('darkseagreen', (0.561, 0.737, 0.561, 1.)),
            ('steelBlue', (0.275, 0.510, 0.706, 1.)),
        ]

        bad_data = [
            'BlancedAlmond',
            'DarkSeaBlue',
            'DarkSalmonOverlord',
        ]

        for inp, out in data:
            self.assertTupleAlmostEqual(get_colour(inp).getRgbF(), out)

        for inp in bad_data:
            self.assertRaises(ValueError, lambda: get_colour(inp))

    def test_invalid_names(self):
        """Test invalid colour strings not covered by other cases"""
        bad_data = [
            ('', ValueError),
            ([], TypeError),
            ({}, TypeError),
            ((), TypeError),
            ('#$(%@', ValueError),
        ]

        for inp, exc in bad_data:
            self.assertRaises(exc, lambda: get_colour(inp))


if __name__ == '__main__':
    unittest.main()
