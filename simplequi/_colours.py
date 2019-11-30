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
Colour constants and factories for use in other functions

Externally, these are most easily accessed using their colour names e.g. 'Blue'.  They can also be specified as per the
Codeskulptor documentation: "More generally, you may use any HTML color name. Furthermore, custom colors and
transparencies can be specified in a any CSS color format, including hexadecimal, RGB, RGBA, HSL, and HSLA."

Function 'get_colour' converts a colour string to a QColor and also stores it in the module dict for later use.

Note: this module is entirely generic and not specific to simplequi - it could be used anywhere to convert any valid CSS
string colour representation to a QColor.
"""

from enum import Enum
import re

from PySide2.QtGui import QColor

from ._mapping import MappingWithInitCheck

# Regexp used for parsing colour strings
NUM_RE = r'(\d+\.?\d*)'
NUM_RE = re.compile(NUM_RE)

DEFAULT_COLOURS = ['Aqua',
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
                   'Yellow']


#: Cache some default colours named in codeskulptor docs
class ColourTypes(Enum):
    """Conversion factors for various colour formats to put values in valid range, and factory functions for QColors"""
    RGB =     ([255, 255, 255, 1], QColor.fromRgbF)  # Values in range 0-255, 0 <= alpha <= 1
    RGB_PCT = ([100, 100, 100, 1], QColor.fromRgbF)  # Values in percent, 0 <= alpha <= 1
    HSL =     ([360, 100, 100, 1], QColor.fromHslF)  # Hue in range 0-360, S,L in percent, 0 <= alpha <= 1


class _ColourMap(MappingWithInitCheck):
    def _init_map(self):
        """Initialise the global colour map with the simplegui list of named default colours"""
        for colour_name in DEFAULT_COLOURS:
            if QColor.isValidColor(colour_name):
                self[colour_name] = QColor(colour_name)
            else:
                raise ValueError('invalid colour name \'{colour}\''.format(colour=colour_name))

    def __missing__(self, name):
        # type: (str) -> QColor
        """
        Attempts to translate a colour name in any valid CSS format to a QColor

        :param name: name of the colour, or a specification in RGB(A) (with 0-255 or % values) or HSL(A) format
        :raises KeyError: if the name cannot be parsed into a QColor
        :return: ``QColor`` instance to use elsewhere in the app
        """
        if QColor.isValidColor(name):
            self[name] = QColor(name)
        elif name.lower().startswith('rgb'):
            colour_type = ColourTypes.RGB_PCT if '%' in name else ColourTypes.RGB
            self[name] = self.__convert_colour_string(name, colour_type)
        elif name.lower().startswith('hsl'):
            self[name] = self.__convert_colour_string(name, ColourTypes.HSL)
        else:
            raise KeyError('unknown colour string: ' + name)

        return self[name]

    def __convert_colour_string(self, text, colour_type):
        # type: (str, ColourTypes) -> QColor
        """Converts a string in CSS RGB(A) or HSL(A) format to a QColor

        :param text: the text specifying the colour parameters
        :param colour_type: what format ``text`` should be specified in
        :return: :class:`QColor` instance to use elsewhere in the app
        """
        factors, func = colour_type.value
        numbers = self.__get_float_colour_values(text, factors)
        return func(*numbers)

    @staticmethod
    def __get_float_colour_values(text, factors):
        # type: (str, list) -> list[float]
        """Extracts float values from colour string and ensures they are all in the valid range 0.0 - 1.0.

        :param text: string to scan for colour information
        :param factors: scaling factor for each value parsed from the colour string
        :return: list of scaled values to use in ``QColor`` constructors

        :raises ValueError: not enough values are present in ``text`` to apply ``factors`` to, or values are out of range
        """
        numbers = NUM_RE.findall(text)
        numbers = [float(x) / fact for x, fact in zip(numbers, factors)]

        if len(numbers) < 3:
            raise ValueError('not enough values in colour string: ' + text)

        if not all([0.0 <= x <= 1.0 for x in numbers]):
            raise ValueError('invalid values in colour string: ' + text)

        return numbers


COLOUR_MAP = _ColourMap()  #: Colour cache used to get QColors to use elsewhere in the application


def get_colour(name):
    # type: (str) -> QColor
    """Translates a colour name in any valid CSS format to a QColor

    :param name: name of the colour, or a specification in RGB(A) (with 0-255 or % values) or HSL(A) format
    :return: ``QColor`` instance to use elsewhere in the app
    """
    if type(name) != str:
        raise TypeError('invalid colour specifier, should be a string. Got type: {}'.format(type(name)))

    return COLOUR_MAP[name]
