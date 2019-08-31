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

from enum import Enum
import re

from PySide2.QtGui import QColor


# Regexps used for parsing colour strings
NUM_RE = r'(\d+\.?\d*)'
NUM_RE = re.compile(NUM_RE)


class ColourTypes(Enum):
    """Conversion factors for various colour formats to put values in valid range and factory functions for QColors"""

    RGB =     ([255, 255, 255, 1], QColor.fromRgbF)  # Values in range 0-255, 0 <= alpha <= 1
    RGB_PCT = ([100, 100, 100, 1], QColor.fromRgbF)  # Values in percent, 0 <= alpha <= 1
    HSL =     ([360, 100, 100, 1], QColor.fromHslF)  # Hue in range 0-360, S,L in percent, 0 <= alpha <= 1


# Cache colours for later retrieval
COLOUR_MAP = {}

# Cache some default colours named in codeskulptor docs
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


def _get_float_colour_values(text, factors):
    # type: (str, list) -> list[float]
    """Extract float values from colour string and ensure they are all in the valid range 0.0 - 1.0"""
    numbers = NUM_RE.findall(text)
    numbers = [float(x) / fact for x, fact in zip(numbers, factors)]

    if len(numbers) < 3:
        raise ValueError('not enough values in colour string: ' + text)

    if not all([0.0 <= x <= 1.0 for x in numbers]):
        raise ValueError('invalid values in colour string: ' + text)

    return numbers


def _convert_colour_string(name, colour_type):
    # type: (str, ColourTypes) -> QColor
    """Convert a string in CSS RGB(A) or HSL(A) format to a QColor"""
    factors, func = colour_type.value
    numbers = _get_float_colour_values(name, factors)
    return func(*numbers)


def get_colour(name):
    # type: (str) -> QColor
    """Translate a colour name in any valid CSS format to a QColor"""
    if type(name) != str:
        raise TypeError('invalid colour specifier, should be a string. Got type: {}'.format(type(name)))

    if name in COLOUR_MAP:
        return COLOUR_MAP[name]

    if QColor.isValidColor(name):
        COLOUR_MAP[name] = QColor(name)
    elif name.lower().startswith('rgb'):
        colour_type = ColourTypes.RGB_PCT if '%' in name else ColourTypes.RGB
        COLOUR_MAP[name] = _convert_colour_string(name, colour_type)
    elif name.lower().startswith('hsl'):
        COLOUR_MAP[name] = _convert_colour_string(name, ColourTypes.HSL)
    else:
        raise ValueError('unknown colour string: ' + name)

    return COLOUR_MAP[name]
