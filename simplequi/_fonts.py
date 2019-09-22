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

from PySide2.QtCore import QRect
from PySide2.QtGui import QFont, QFontMetrics, QFontDatabase
import pkg_resources

# Change the default monospace font to one a bit less wide than Courier New
font_path = pkg_resources.resource_filename(__name__, 'resources/fonts/NK57 Monospace/nk57-monospace-sc-rg.ttf')
monospace = QFontDatabase.addApplicationFont(font_path)


class FontFace(Enum):
    serif = 'serif'
    sans = 'sans-serif'
    monospace = 'monospace'


REAL_FONT_FACES = {
    FontFace.serif: 'Times New Roman',
    FontFace.sans: 'Helvetica',
    FontFace.monospace: QFontDatabase.applicationFontFamilies(monospace)[0],
}


FONT_SCALES = {
    FontFace.serif: None,
    FontFace.sans: None,
    FontFace.monospace: None,
}


FONT_CACHE = {}
METRICS_CACHE = {}
FontSpec = namedtuple('FontSpec', ['size', 'face'])


def _check_is_valid_text(text):
    # type: (str) -> None
    """Raises ValueError ifthe text can not be printed on the canvas"""
    if not text.isprintable():
        raise ValueError('text may not contain non-printing characters')


def _check_is_valid_font(font_spec):
    # type: (FontSpec) -> None
    """Raises ValueError if font spec could not be used on the canvas"""
    if font_spec.size <= 0:
        raise ValueError('invalid font size')


def get_font(font_spec):
    # type: (FontSpec) -> QFont
    """Get and if necessary cache QFont closest to the required params"""
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
    """Used internally to ensure fonts are all scaled similarly in height"""
    _check_is_valid_text(text)
    get_font(font_spec)  # Just ensure font is in cache and metrics cache
    return METRICS_CACHE[font_spec].boundingRect(text)


def get_text_width_for_font_spec(text, font_spec):
    # type: (str, FontSpec) -> int
    """Return the width in pixels of the given text for the given font spec"""
    rect = _get_text_rect_for_font_spec(text, font_spec)
    return rect.width()
