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
import pkg_resources

from PySide2.QtCore import QByteArray, QBuffer, QIODevice
from PySide2.QtGui import QPixmap
from PySide2.QtMultimedia import QAudio, QAudioDeviceInfo

from simplequi._image import _IMAGE_CACHE


def get_example_resource_path(filename):
    """Returns the full local path of a resource in simplequi.examples.resources"""
    return pkg_resources.resource_filename('simplequi.examples', 'resources/' + filename)


def is_sound_available():
    """Whether the system supports audio outputs"""
    info = QAudioDeviceInfo()
    supported = bool(info.availableDevices(QAudio.AudioOutput))
    if not supported:
        print('Audio output not supported, skipping sound tests.')
    return supported


def pixmap_to_bytes(pixmap):
    """Converts a pixmap to a byte array for easy comparisons"""
    array = QByteArray()
    buffer = QBuffer(array)
    buffer.open(QIODevice.WriteOnly)
    pixmap.save(buffer, "PNG")
    return array


def pixmap_data(img, x, y, dx, dy, size=None):
    """Gets a byte array for a pixmap from the given image with the given top left corner, original and target sizes"""
    pixmap = QPixmap.fromImage(_IMAGE_CACHE[img].copy(x, y, dx, dy))
    if size:
        pixmap = pixmap.scaled(*size)
    return pixmap_to_bytes(pixmap)