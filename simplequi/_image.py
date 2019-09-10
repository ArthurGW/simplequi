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

from typing import Optional

from PySide2.QtCore import QByteArray
from PySide2.QtGui import QImage, QPixmap, QTransform

from ._constants import Point, Size
from ._url import request

_IMAGE_CACHE = {}  # Stores the actual QImage for each Image object
_PIXMAP_CACHE = {}  # Stores pixmaps generated from each QImage for faster rendering


class Image:
    """Wrapper around a QImage to provide the codeskulptor image API"""

    def __init__(self, url):
        # type: (str) -> Image
        """
        Loads an image from the specified URL.

        The image can be in any format supported by PySide2.
        An error is raised if the file can't be loaded for any reason.
        """
        request(url, self.__load_image)
        _IMAGE_CACHE[self] = None

    def __load_image(self, data):
        # type: (QByteArray) -> None
        """Create the QImage from the data"""
        image = QImage()
        image.loadFromData(data)
        width = image.width()
        height = image.height()
        size = (width, height)
        centre_x = width / 2
        centre_y = height / 2
        centre = (centre_x, centre_y)
        _IMAGE_CACHE[self] = image
        _PIXMAP_CACHE[self] = {}

        # Cache the full-size pixmap
        get_pixmap(self, centre, size, size)

    def get_width(self):
        """Returns the width of the image in pixels. While the image is still loading, it returns zero."""
        if _IMAGE_CACHE[self] is None:
            return 0

        return _IMAGE_CACHE[self].width()

    def get_height(self):
        """Returns the height of the image in pixels. While the image is still loading, it returns zero."""
        if _IMAGE_CACHE[self] is None:
            return 0

        return _IMAGE_CACHE[self].height()


def get_pixmap(image, image_coords, image_rect, target_rect, rotation=0.0):
    # type: (Image, Point, Size, Size, float) -> Optional[QPixmap]
    """Returns a QPixmap section of the QImage associated with the image object

    The section will be taken as a rectangle centred at the image coords given with the given dimensions, optionally
    rotated, scaled to the target rectangle size and shape.
    """

    # Get the actual QImage
    orig_image = _IMAGE_CACHE[image]
    if orig_image is None:
        # Still loading or invalid result
        return None

    pixmap = _PIXMAP_CACHE[image].get((image_coords, image_rect, target_rect, rotation))
    if pixmap is not None:
        return pixmap

    x, y = image_coords
    x -= image_rect[0] / 2
    y -= image_rect[1] / 2
    coords = (x, y)
    section = orig_image.copy(*coords, *image_rect)

    if image_rect != target_rect:
        section = section.scaled(*target_rect)
    if rotation != 0.0:
        transform = QTransform()
        transform = transform.rotateRadians(rotation)
        section = section.transformed(transform)

    pixmap = QPixmap.fromImage(section)
    _PIXMAP_CACHE[image][(image_coords, image_rect, target_rect, rotation)] = pixmap
    return pixmap
