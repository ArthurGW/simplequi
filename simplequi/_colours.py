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
"""
Colour constants for use in other functions

Externally, these are most easily accessed using their colour names e.g. 'Blue'.  They can also be specified as per the
Codeskulptor documentation: "More generally, you may use any HTML color name. Furthermore, custom colors and
transparencies can be specified in a any CSS color format, including hexadecimal, RGB, RGBA, HSL, and HSLA."

Function 'get_colour' converts a colour string to a QColor and also stores it in the module dict for later use.
"""

import re

from PySide2.QtGui import QColor


COLOUR_MAP = {}

NUM_RE = r'(\d+\.?\d*)'
NUM_RE = re.compile(NUM_RE)

for colour_name in ['Aqua',
                    'Black',
                    'Blue',
                    'Fuchsia',
                    'Gray',
                    'Green',
                    'Lime',
                    'Maroon',
                    'Navy',
                    'Olive',
                    'Orange',
                    'Purple',
                    'Red',
                    'Silver',
                    'Teal',
                    'White',
                    'Yellow']:
    if QColor.isValidColor(colour_name):
        COLOUR_MAP[colour_name] = QColor(colour_name)
    else:
        raise ValueError('invalid colour name {colour}'.format(colour=colour_name))


def _convert_rgb_colour(name):
    # type: (str) -> QColor
    """Convert a string in CSS RGB(A) format to a QColor"""
    numbers = NUM_RE.findall(name)
    numbers = [float(x) for x in numbers]

    if '%' in name:
        numbers[:3] = [x / 100 for x in numbers[:3]]
    else:
        numbers[:3] = [x / 255 for x in numbers[:3]]

    colour = QColor()
    colour.setRgbF(*numbers)
    return colour


def _convert_hsl_colour(name):
    # type: (str) -> QColor
    """Convert a string in CSS HSL(A) format to a QColor"""
    numbers = NUM_RE.findall(name)
    numbers = [float(x) for x in numbers]

    # Convert values to range 0-1 (except optional alpha channel which must already be in this range)
    numbers[:3] = [numbers[0] / 360, numbers[1] / 100, numbers[2] / 100]

    colour = QColor()
    colour.setHslF(*numbers)
    return colour


def get_colour(name):
    # type: (str) -> QColor
    """Translate a colour name in any valid CSS format to a QColor"""
    if name in COLOUR_MAP:
        return COLOUR_MAP[name]

    if QColor.isValidColor(name):
        COLOUR_MAP[name] = QColor(name)
    elif name.lower().startswith('rgb'):
        COLOUR_MAP[name] = _convert_rgb_colour(name)
    elif name.lower().startswith('hsl'):
        COLOUR_MAP[name] = _convert_hsl_colour(name)
    else:
        raise ValueError('unknown colour string {colour}'.format(colour=name))

    return COLOUR_MAP[name]
