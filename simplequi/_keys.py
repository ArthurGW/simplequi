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
"""Key mappings for key handler functions"""


class _KeyMap(dict):
    """
    The keyboard event handlers receive the relevant key as an integer.
    Because different browsers can give different values for the same keystrokes, SimpleGUI provides a way to get the
    appropriate key integer for a given meaning. The acceptable strings for character are the letters 'a'…'z' and 'A'…'Z',
    the digits '0'…'9', 'space', 'left', 'right', 'up', and 'down'. Note that other keyboard symbols are not defined in
    simplegui.KEY_MAP.
    """

    def __missing__(self, key):
        raise KeyError('key {} is not a valid simplegui keyboard symbol'.format(key))


KEY_MAP = _KeyMap({
    'space': None,
    'left': None,
    'right': None,
    'up': None,
    'down': None,
})

# 0 - 9
for ordinal in range(48, 58):
    KEY_MAP[chr(ordinal)] = None

# A - Z
for ordinal in range(65, 91):
    KEY_MAP[chr(ordinal)] = None

# a - z
for ordinal in range(97, 123):
    KEY_MAP[chr(ordinal)] = None
