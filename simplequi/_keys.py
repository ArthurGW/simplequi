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
"""Key mappings for key handler functions."""

from PySide2.QtCore import Qt


class _KeyMap(dict):
    """The keyboard event handlers receive the relevant key as an integer.

    Because different browsers can give different values for the same keystrokes, SimpleQui provides a way to get the
    appropriate key integer for a given meaning. The acceptable strings for character are the letters 'a'…'z' and
    A'…'Z', the digits '0'…'9', 'space', 'left', 'right', 'up', and 'down'. Note that other keyboard symbols are not
    defined in simplequi.KEY_MAP.
    """

    def __missing__(self, key_name):
        # type: (str) -> None
        """Handles users attempting to get a key integer for an undefined key.

        Note that the error message refers to simplegui, since the keys allowed are defined there. In theory, more could
        be allowed here, but for consistency the same set is kept.

        :param key_name: the key the user was attempting to look up
        :raises KeyError: always, as the keys are all defined and cached within this module
        """
        raise KeyError('key {} is not a valid simplegui keyboard symbol'.format(key_name))


class _ReverseKeyMap(dict):
    """This is used to get a string representation of a pressed key, including unicode arrows."""

    def __missing__(self, key_value):
        # type: (str) -> None
        """Handles getting a key representation for an as-yet-undefined key.

        :param key_value: the key to create a display string for
        :return: a string representation of the key for display
        """
        self[key_value] = '<{}>'.format(key_value)
        return self[key_value]


#################################################
# Now store the key values for all allowed keys:
#################################################


# Special keys
KEY_MAP = _KeyMap({
    'space': int(Qt.Key_Space),
    'left': int(Qt.Key_Left),
    'right': int(Qt.Key_Right),
    'up': int(Qt.Key_Up),
    'down': int(Qt.Key_Down),
})  #: This is the key map cache instance that is accessible to users

# 0 - 9
for ind in range(10):
    ordinal = 48 + ind
    key = Qt.Key_0 + ind
    KEY_MAP[chr(ordinal)] = key

# A - Z
for ind in range(26):
    ordinal = 65 + ind
    key = int((Qt.Key_A + ind) | Qt.ShiftModifier)
    KEY_MAP[chr(ordinal)] = key

# a - z
for ind in range(26):
    ordinal = 97 + ind
    key = Qt.Key_A + ind
    KEY_MAP[chr(ordinal)] = key

#######################################################################
# Create the reverse key lookup for displaying pressed keys in the UI:
#######################################################################

# Basic keys
REVERSE_KEY_MAP = _ReverseKeyMap({value: key for key, value in KEY_MAP.items()})

# Override display for direction keys to display nice arrow symbols instead of text like 'left'
REVERSE_KEY_MAP[KEY_MAP['up']] = '⭡'
REVERSE_KEY_MAP[KEY_MAP['right']] = '⭢'
REVERSE_KEY_MAP[KEY_MAP['down']] = '⭣'
REVERSE_KEY_MAP[KEY_MAP['left']] = '⭠'
