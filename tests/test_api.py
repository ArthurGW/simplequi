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

import simplequi


class MyTestCase(unittest.TestCase):
    """Basic API sanity checks"""

    API = [
        ('create_frame', ('Title', 100, 100, 20)),
        ('create_timer', (500, lambda: print(5))),
        ('load_image', ('http://iana.org/_img/2015.1/iana-logo-homepage.svg',)),
        ('load_sound', ('http://iana.org/_img/2015.1/iana-logo-homepage.svg',)),
    ]

    def test_api_not_currently_implemented(self):
        for func, args in self.API:
            func = getattr(simplequi, func)
            self.assertRaises(NotImplementedError, func, *args)

    def test_key_map(self):
        """Just test by length all keys are in map and currently None"""
        self.assertEqual(67, len(simplequi.KEY_MAP))

        for key, val in simplequi.KEY_MAP.items():
            self.assertIsNone(val, 'key \'{}\' does not have value \'None\''.format(key))


if __name__ == '__main__':
    unittest.main()
