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

from ._mapping import MappingWithInitCheck


class KeyMap(MappingWithInitCheck):
    """The keyboard event handlers receive the relevant key as an integer.

    Because different browsers can give different values for the same keystrokes, simplequi provides a way to get the
    appropriate key integer for a given meaning. The acceptable strings for character are the letters 'a'…'z' and
    A'…'Z', the digits '0'…'9', 'space', 'left', 'right', 'up', and 'down'. Note that other keyboard symbols are not
    defined in simplequi.KEY_MAP.
    """

    def _init_map(self):
        """Store the key map entries for all keys allowed by simplegui"""
        # Special keys
        self.update({
            'space': int(Qt.Key_Space),
            'left': int(Qt.Key_Left),
            'right': int(Qt.Key_Right),
            'up': int(Qt.Key_Up),
            'down': int(Qt.Key_Down),
        })

        # 0 - 9
        for ind in range(10):
            ordinal = 48 + ind
            key = Qt.Key_0 + ind
            self[chr(ordinal)] = key

        # A - Z
        for ind in range(26):
            ordinal = 65 + ind
            key = int((Qt.Key_A + ind) | Qt.ShiftModifier)
            self[chr(ordinal)] = key

        # a - z
        for ind in range(26):
            ordinal = 97 + ind
            key = Qt.Key_A + ind
            self[chr(ordinal)] = key

    def __getitem__(self, key):
        # type: (str) -> int
        """
        x.__getitem__('y') <==> x['y']

        Get the value that is sent to a handler for a given key press.

        This is usually called using square brackets, like ``value = simplequi.KEY_MAP['space']``

        :param key: the key press to look up
        :return: the integer value for the key
        :raises KeyError: if the key is not in the map for simplegui

        Example usage::

            def key_handler(self, key):
                if key == simplequi.KEY_MAP['left']:
                    print('Left key pressed!')
                    self.move_ship_left()
        """
        return super().__getitem__(key)

    def __missing__(self, key_name):
        # type: (str) -> None
        """
        Inform the user that they have attempted to look up an invalid key name

        Note that the error message refers to simplegui, since the keys allowed are defined there. In theory, more could
        be allowed here, but for consistency the same set is kept.

        :param key_name: the key the user is attempting to look up
        :raises KeyError: always, as the requested key is not allowed by simplegui
        """
        raise KeyError('key {} is not a valid simplegui keyboard symbol'.format(key_name))


class _ReverseKeyMap(MappingWithInitCheck):
    """This is used to get a string representation of a pressed key, including unicode arrows."""

    def __init__(self, key_map):
        # type: (KeyMap) -> None
        super().__init__()
        self.__forward_map = key_map

    def _init_map(self):
        """Set up the reverse key mapping"""
        # Ensure the forward map is initialised
        self.__forward_map.get('up')

        # Reverse map the values from the forward map
        self.update({value: key for key, value in self.__forward_map.items()})

        # Override display for direction keys to display nice arrow symbols instead of text like 'left'
        self[self.__forward_map['up']] = '⭡'
        self[self.__forward_map['right']] = '⭢'
        self[self.__forward_map['down']] = '⭣'
        self[self.__forward_map['left']] = '⭠'

    def __missing__(self, key_value):
        # type: (str) -> str
        """Handles getting a key representation for an unrecognised key value

        :param key_value: the key to create a display string for
        :return: a string representation of the key for display
        """
        self[key_value] = '<{}>'.format(key_value)
        return self[key_value]


KEY_MAP = KeyMap()  #: This is the key map cache instance that is accessible to users
REVERSE_KEY_MAP = _ReverseKeyMap(KEY_MAP)  #: This is only used for generating displayed key strings
