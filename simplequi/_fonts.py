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

"""Utilities for caching and getting fonts"""

from collections import namedtuple
from enum import Enum
import pkg_resources

from PySide2.QtCore import QRect
from PySide2.QtGui import QFont, QFontMetrics, QFontDatabase

# Changes the default monospace font to one a bit less wide than Courier New
font_path = pkg_resources.resource_filename(__name__, 'resources/fonts/NK57 Monospace/nk57-monospace-sc-rg.ttf')
monospace = QFontDatabase.addApplicationFont(font_path)


class FontFace(Enum):
    """Describes the three font faces available to users in :meth:`~simplequi._canvas.Canvas.draw_text` calls.

    Users select text by the string face name, e.g.:

    >>>def draw_handler(canvas):
    >>>    canvas.draw_text('sample', (50, 50), 14, 'red', 'sans-serif')
    >>>
    >>>frame.set_draw_handler(draw_handler)
    """

    serif = 'serif'
    sans = 'sans-serif'
    monospace = 'monospace'


REAL_FONT_FACES = {
    FontFace.serif: 'Times New Roman',
    FontFace.sans: 'Helvetica',
    FontFace.monospace: QFontDatabase.applicationFontFamilies(monospace)[0],
}  #: Converts the enumed font faces to actual font families that Qt will accept


FONT_SCALES = {
    FontFace.serif: None,
    FontFace.sans: None,
    FontFace.monospace: None,
}  #: Stores scaling factors used to make fonts all the same width for a given font point size


FONT_CACHE = {}  #: Stores previously called fonts
METRICS_CACHE = {}  #: Stores metrics used to get font widths per font size
FontSpec = namedtuple('FontSpec', ['size', 'face'])  #: Used to define a font for caching


def _check_is_valid_text(text):
    # type: (str) -> None
    """Checks if a text string will be able to be displayed

    :param text: the text to test
    :raises ValueError: if the text cannot be printed on the canvas
    """
    if not text.isprintable():
        raise ValueError('text may not contain non-printing characters')


def _check_is_valid_font(font_spec):
    # type: (FontSpec) -> None
    """Checks if a font spec defines a font that will be able to be used.

    :param font_spec: the font spec to test
    :raises ValueError: if font spec could not be used on the canvas
    """
    if font_spec.size <= 0:
        raise ValueError('invalid font size')
    FontFace(font_spec.face)


def get_font(font_spec):
    # type: (FontSpec) -> QFont
    """Gets and if necessary caches QFont closest to the required params.

    :param font_spec: defines a font in terms of face/family and size
    :return: a :class:`QFont` that can be used for example by a :class:`QPainter`
    """
    if font_spec in FONT_CACHE:
        return FONT_CACHE[font_spec]

    _check_is_valid_font(font_spec)
    font = QFont()
    font.setPixelSize(font_spec.size)
    real_face = REAL_FONT_FACES[FontFace(font_spec.face)]
    font.setFamily(real_face)
    FONT_CACHE[font_spec] = font
    METRICS_CACHE[font_spec] = QFontMetrics(font)
    return font


def _get_text_rect_for_font_spec(text, font_spec):
    # type: (str, FontSpec) -> QRect
    """Gets the bounding rectangle that encloses the given text rendered with the given font spec.

    :param text: the text to measure
    :param font_spec: the font to render with
    :return: a :class:`QRect` that encloses the text
    """
    _check_is_valid_text(text)
    get_font(font_spec)  # Just ensure font is in cache and metrics cache
    return METRICS_CACHE[font_spec].boundingRect(text)


def get_text_width_for_font_spec(text, font_spec):
    # type: (str, FontSpec) -> int
    """Gets the width in pixels of the given text for the given font spec.

    :param text: the text to measure
    :param font_spec: the font to render with
    :return: the width of the text bounding rectangle
    """
    rect = _get_text_rect_for_font_spec(text, font_spec)
    return rect.width()
