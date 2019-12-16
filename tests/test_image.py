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
from functools import partial
from unittest.mock import patch, ANY

from PySide2.QtNetwork import QNetworkReply
from PySide2.QtWidgets import QApplication

import simplequi
from simplequi._image import _IMAGE_CACHE, _PIXMAP_CACHE, get_pixmap
from tests.helpers import get_example_resource_path, pixmap_data, pixmap_to_bytes


class TestImage(unittest.TestCase):
    """Test Image API"""

    def setUp(self):
        self.error = None
        self.passed = None

    def on_finished(self, callback, res, fail=True):
        res.deleteLater()
        self.error = res.error()
        if res.error() == QNetworkReply.NoError:
            self.passed = not fail
            data = res.readAll()
            callback(data)
        elif not fail:
            self.passed = False
        else:
            self.passed = True

    def catch_finish(self, img, fail=True, width=0, height=0):
        with patch('simplequi._url._on_finished') as finish:
            finish.side_effect = partial(self.on_finished, fail=fail)
            simplequi.create_timer(500, QApplication.instance().exit).start()
            QApplication.instance().exec_()
        finish.assert_called_with(img._Image__load_image, ANY)
        self.assertTrue(self.passed, 'failed when expected to succeed or vice versa')
        self.assertEqual(img.get_width(), width)
        self.assertEqual(img.get_height(), height)
        if not fail:
            self.assertEqual(self.error, QNetworkReply.NoError)

    def test_invalid_path(self):
        """Non-existent path fails with a network error"""
        img = simplequi.load_image('not_a_file.png')
        self.catch_finish(img)
        self.assertEqual(self.error, QNetworkReply.ProtocolUnknownError)

    def test_invalid_file(self):
        """Valid path but not an image fails to create the image or pixmaps"""
        img = simplequi.load_image(__file__)
        self.catch_finish(img, fail=False)
        self.assertIsNone(_IMAGE_CACHE[img])
        self.assertIsNone(get_pixmap(img, (10, 10), (10, 10), (10, 10)))
        self.assertNotIn(_IMAGE_CACHE[img], _PIXMAP_CACHE)

    def test_valid_image_and_pixmaps(self):
        img = simplequi.load_image(get_example_resource_path('sample_image.png'))
        self.catch_finish(img, fail=False, width=1000, height=1200)
        self.assertIsNotNone(_IMAGE_CACHE[img])
        self.assertIsNotNone(get_pixmap(img, (10, 10), (10, 10), (10, 10)))

        small_unscaled = pixmap_data(img, 0, 0, 20, 20)
        small_scaled = pixmap_data(img, 0, 0, 20, 20, size=(30, 25))
        full_scaled = pixmap_data(img, 0, 0, 1000, 1200, size=(50, 60))
        middle = pixmap_data(img, 307, 293, 250, 302)

        self.assertNotEqual(small_unscaled, small_scaled)
        self.assertEqual(pixmap_to_bytes(get_pixmap(img, (10, 10), (20, 20), (20, 20))), small_unscaled)
        self.assertEqual(pixmap_to_bytes(get_pixmap(img, (10, 10), (20, 20), (30, 25))), small_scaled)
        self.assertEqual(pixmap_to_bytes(get_pixmap(img, (500, 600), (1000, 1200), (50, 60))), full_scaled)
        self.assertEqual(pixmap_to_bytes(get_pixmap(img, (432, 444), (250, 302), (250, 302))), middle)


if __name__ == '__main__':
    unittest.main()
